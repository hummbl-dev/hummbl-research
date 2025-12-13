#!/usr/bin/env python3
"""
Extract relationship verification data for each model.

This script analyzes relationships.json and creates per-model relationship data
including:
- Incoming relationships (models that relate TO this model)
- Outgoing relationships (models this model relates TO)
- Relationship counts by type
- Relationship strength statistics
- Verification status

Usage:
    python tools/extract_relationship_data.py [--output relationships-per-model.json]
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from validate_relationships import ModelLoader


def extract_relationship_data(relationships_file: str = 'data/relationships.json') -> Dict:
    """Extract relationship data organized by model."""
    
    with open(relationships_file, 'r', encoding='utf-8') as f:
        relationships = json.load(f)
    
    loader = ModelLoader()
    
    # Organize relationships by model
    model_data: Dict[str, Dict] = defaultdict(lambda: {
        'code': '',
        'name': '',
        'incoming': [],
        'outgoing': [],
        'stats': {
            'total_incoming': 0,
            'total_outgoing': 0,
            'total_relationships': 0,
            'by_type': defaultdict(int),
            'by_direction': defaultdict(int),
            'strength_stats': {
                'min': 1.0,
                'max': 0.0,
                'avg': 0.0,
                'sum': 0.0,
                'count': 0
            }
        },
        'verification': {
            'valid': True,
            'invalid_models': [],
            'errors': []
        }
    })
    
    # Process each relationship
    for rel in relationships:
        from_code = rel['from']
        to_code = rel['to']
        
        # Verify models exist
        from_info = loader.load_model(from_code)
        to_info = loader.load_model(to_code)
        
        # Initialize model data if not already done
        if from_code not in model_data:
            model_data[from_code]['code'] = from_code
            if from_info:
                model_data[from_code]['name'] = from_info.get('name', 'Unknown')
            else:
                model_data[from_code]['verification']['valid'] = False
                model_data[from_code]['verification']['errors'].append(f"Model {from_code} not found")
        
        if to_code not in model_data:
            model_data[to_code]['code'] = to_code
            if to_info:
                model_data[to_code]['name'] = to_info.get('name', 'Unknown')
            else:
                model_data[to_code]['verification']['valid'] = False
                model_data[to_code]['verification']['errors'].append(f"Model {to_code} not found")
        
        # Add relationship to outgoing (from -> to)
        rel_data = {
            'id': rel.get('id', ''),
            'to': to_code,
            'to_name': to_info.get('name', 'Unknown') if to_info else 'Unknown',
            'type': rel.get('type', ''),
            'strength': rel.get('strength', 0.0),
            'direction': rel.get('direction', ''),
            'description': rel.get('description', '')
        }
        model_data[from_code]['outgoing'].append(rel_data)
        
        # Add relationship to incoming (to <- from)
        incoming_rel = {
            'id': rel.get('id', ''),
            'from': from_code,
            'from_name': from_info.get('name', 'Unknown') if from_info else 'Unknown',
            'type': rel.get('type', ''),
            'strength': rel.get('strength', 0.0),
            'direction': rel.get('direction', ''),
            'description': rel.get('description', '')
        }
        model_data[to_code]['incoming'].append(incoming_rel)
        
        # Update statistics
        rel_type = rel.get('type', '')
        rel_direction = rel.get('direction', '')
        rel_strength = rel.get('strength', 0.0)
        
        # From model stats
        model_data[from_code]['stats']['total_outgoing'] += 1
        model_data[from_code]['stats']['total_relationships'] += 1
        model_data[from_code]['stats']['by_type'][rel_type] += 1
        model_data[from_code]['stats']['by_direction'][rel_direction] += 1
        model_data[from_code]['stats']['strength_stats']['sum'] += rel_strength
        model_data[from_code]['stats']['strength_stats']['count'] += 1
        model_data[from_code]['stats']['strength_stats']['min'] = min(
            model_data[from_code]['stats']['strength_stats']['min'], rel_strength
        )
        model_data[from_code]['stats']['strength_stats']['max'] = max(
            model_data[from_code]['stats']['strength_stats']['max'], rel_strength
        )
        
        # To model stats
        model_data[to_code]['stats']['total_incoming'] += 1
        model_data[to_code]['stats']['total_relationships'] += 1
        model_data[to_code]['stats']['by_type'][rel_type] += 1
        model_data[to_code]['stats']['by_direction'][rel_direction] += 1
        model_data[to_code]['stats']['strength_stats']['sum'] += rel_strength
        model_data[to_code]['stats']['strength_stats']['count'] += 1
        model_data[to_code]['stats']['strength_stats']['min'] = min(
            model_data[to_code]['stats']['strength_stats']['min'], rel_strength
        )
        model_data[to_code]['stats']['strength_stats']['max'] = max(
            model_data[to_code]['stats']['strength_stats']['max'], rel_strength
        )
    
    # Calculate averages and convert defaultdicts to dicts
    for code, data in model_data.items():
        stats = data['stats']
        strength = stats['strength_stats']
        if strength['count'] > 0:
            strength['avg'] = strength['sum'] / strength['count']
        else:
            strength['min'] = 0.0
            strength['max'] = 0.0
        
        # Convert defaultdicts to regular dicts for JSON serialization
        stats['by_type'] = dict(stats['by_type'])
        stats['by_direction'] = dict(stats['by_direction'])
    
    return dict(model_data)


def main():
    parser = argparse.ArgumentParser(description='Extract relationship data per model')
    parser.add_argument('--relationships', '-r', type=str, default='data/relationships.json',
                       help='Path to relationships JSON file')
    parser.add_argument('--output', '-o', type=str, default='validation/relationships-per-model.json',
                       help='Output JSON file')
    parser.add_argument('--model', '-m', type=str, help='Extract data for a single model code')
    parser.add_argument('--summary', action='store_true', help='Show summary statistics')
    args = parser.parse_args()
    
    print("=" * 70)
    print("EXTRACTING RELATIONSHIP DATA PER MODEL")
    print("=" * 70)
    print()
    
    model_data = extract_relationship_data(args.relationships)
    
    if args.model:
        # Single model
        if args.model in model_data:
            print(json.dumps(model_data[args.model], indent=2))
        else:
            print(f"Error: Model {args.model} not found in relationships", file=sys.stderr)
            sys.exit(1)
    else:
        # All models
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to list format for easier API consumption
        models_list = []
        for code in sorted(model_data.keys()):
            model_info = model_data[code]
            # Create a compact version for API
            compact = {
                'code': model_info['code'],
                'name': model_info['name'],
                'relationships': {
                    'incoming_count': model_info['stats']['total_incoming'],
                    'outgoing_count': model_info['stats']['total_outgoing'],
                    'total_count': model_info['stats']['total_relationships'],
                    'by_type': model_info['stats']['by_type'],
                    'strength': {
                        'min': model_info['stats']['strength_stats']['min'],
                        'max': model_info['stats']['strength_stats']['max'],
                        'avg': round(model_info['stats']['strength_stats']['avg'], 2)
                    }
                },
                'verification': {
                    'valid': model_info['verification']['valid'],
                    'errors': model_info['verification']['errors']
                }
            }
            models_list.append(compact)
        
        # Save compact version
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'total': len(models_list),
                'models': models_list
            }, f, indent=2, ensure_ascii=False)
        
        # Also save full version
        full_output = output_path.parent / f"{output_path.stem}-full.json"
        with open(full_output, 'w', encoding='utf-8') as f:
            json.dump({
                'total': len(model_data),
                'models': model_data
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Extracted relationship data for {len(models_list)} models")
        print(f"   Compact version: {output_path}")
        print(f"   Full version: {full_output}")
        
        if args.summary:
            print("\n" + "=" * 70)
            print("RELATIONSHIP STATISTICS")
            print("=" * 70)
            
            total_rels = sum(m['stats']['total_relationships'] for m in model_data.values()) // 2  # Each rel counted twice
            models_with_rels = sum(1 for m in model_data.values() if m['stats']['total_relationships'] > 0)
            models_without_rels = len(model_data) - models_with_rels
            
            print(f"Total relationships: {total_rels}")
            print(f"Models with relationships: {models_with_rels}")
            print(f"Models without relationships: {models_without_rels}")
            print()
            
            # Top models by relationship count
            sorted_models = sorted(
                model_data.items(),
                key=lambda x: x[1]['stats']['total_relationships'],
                reverse=True
            )
            
            print("Top 10 models by relationship count:")
            for i, (code, data) in enumerate(sorted_models[:10], 1):
                stats = data['stats']
                print(f"  {i:2d}. {code:6s} ({data['name'][:40]:40s}): "
                      f"{stats['total_relationships']:3d} relationships "
                      f"({stats['total_incoming']:2d} in, {stats['total_outgoing']:2d} out)")
            
            # Verification status
            invalid_models = [code for code, data in model_data.items() if not data['verification']['valid']]
            if invalid_models:
                print(f"\n⚠️  {len(invalid_models)} models have verification errors:")
                for code in invalid_models:
                    print(f"   {code}: {', '.join(model_data[code]['verification']['errors'])}")
            else:
                print(f"\n✅ All {len(model_data)} models verified successfully")


if __name__ == '__main__':
    main()

