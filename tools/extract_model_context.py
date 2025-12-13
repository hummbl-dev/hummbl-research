#!/usr/bin/env python3
"""
Extract enhanced context from HUMMBL model files for API enhancement.

This script extracts rich context from repository model files that can be
added to the API response, including:
- Full description (vs. current 80-char definition)
- Examples
- Related models
- Status and version
- Additional metadata

Usage:
    python tools/extract_model_context.py [--output enhanced-models.json]
"""

import sys
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from validate_relationships import ModelLoader

# Import relationship data extractor
try:
    from extract_relationship_data import extract_relationship_data
    HAS_RELATIONSHIP_EXTRACTOR = True
except ImportError:
    HAS_RELATIONSHIP_EXTRACTOR = False
    extract_relationship_data = None  # type: ignore


def extract_example(content: str) -> Optional[str]:
    """Extract example section from markdown content."""
    # Look for ## Example section
    example_match = re.search(r'##\s+Example\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if example_match:
        example_text = example_match.group(1).strip()
        # Clean up markdown formatting
        example_text = re.sub(r'\*\*(.*?)\*\*', r'\1', example_text)  # Remove bold
        example_text = re.sub(r'`(.*?)`', r'\1', example_text)  # Remove code ticks
        example_text = re.sub(r'\n+', ' ', example_text)  # Collapse newlines
        example_text = re.sub(r'\s+', ' ', example_text)  # Collapse spaces
        # Limit to reasonable length for API
        if len(example_text) > 500:
            example_text = example_text[:497] + "..."
        return example_text
    return None


def extract_enhanced_context(model_code: str, loader: ModelLoader, relationship_data: Optional[Dict] = None) -> Optional[Dict]:
    """Extract all available context for a model."""
    info = loader.load_model(model_code)
    if not info:
        return None
    
    # Load raw content for example extraction
    match = re.match(r'([A-Z]{1,2})(\d{1,2})', model_code)
    if not match:
        return None
    
    transform, number = match.groups()
    normalized_code = f"{transform}{number.zfill(2)}"
    model_file = Path(loader.models_dir) / transform / f"{normalized_code}.md"
    
    raw_content = ""
    if model_file.exists():
        with open(model_file, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    
    enhanced = {
        'code': normalized_code,
        'name': info.get('name', '').strip(),
        'transformation': info.get('transformation', transform),
        'definition': info.get('description', '')[:80] if info.get('description') else '',  # Keep short for backward compat
        'description': info.get('description', '').strip(),  # Full description
        'status': info.get('status', 'draft'),
        'version': info.get('version', '0.1.0'),
    }
    
    # Add example if available
    example = extract_example(raw_content)
    if example:
        enhanced['example'] = example
    
    # Add related models
    related = info.get('related_models', [])
    if related:
        enhanced['related_models'] = related
    
    # Add priority if available (could be derived from transformation + number)
    # For now, we'll use transformation order: P=1, IN=2, CO=3, DE=4, RE=5, SY=6
    transform_priority = {'P': 1, 'IN': 2, 'CO': 3, 'DE': 4, 'RE': 5, 'SY': 6}
    enhanced['priority'] = transform_priority.get(transform, 0)
    
    # Add relationship verification data if available
    if relationship_data and normalized_code in relationship_data:
        rel_info = relationship_data[normalized_code]
        enhanced['relationships'] = {
            'incoming_count': rel_info['stats']['total_incoming'],
            'outgoing_count': rel_info['stats']['total_outgoing'],
            'total_count': rel_info['stats']['total_relationships'],
            'by_type': rel_info['stats']['by_type'],
            'strength': {
                'min': round(rel_info['stats']['strength_stats']['min'], 2),
                'max': round(rel_info['stats']['strength_stats']['max'], 2),
                'avg': round(rel_info['stats']['strength_stats']['avg'], 2)
            },
            'verification': {
                'valid': rel_info['verification']['valid'],
                'errors': rel_info['verification']['errors']
            }
        }
    
    return enhanced


def main():
    parser = argparse.ArgumentParser(description='Extract enhanced context from HUMMBL models for API')
    parser.add_argument('--output', '-o', type=str, default='validation/enhanced-models-context.json',
                       help='Output JSON file for enhanced context')
    parser.add_argument('--model', '-m', type=str, help='Extract context for a single model code')
    parser.add_argument('--format', choices=['api', 'full'], default='api',
                       help='Output format: api (for API response) or full (all fields)')
    args = parser.parse_args()
    
    loader = ModelLoader()
    
    # Load relationship data if available
    relationship_data = None
    if HAS_RELATIONSHIP_EXTRACTOR:
        try:
            relationship_data = extract_relationship_data('data/relationships.json')  # type: ignore
            print("✅ Loaded relationship data", file=sys.stderr)
        except Exception as e:
            print(f"⚠️  Could not load relationship data: {e}", file=sys.stderr)
            print("   Continuing without relationship data...", file=sys.stderr)
    
    if args.model:
        # Single model
        enhanced = extract_enhanced_context(args.model, loader, relationship_data)
        if enhanced:
            print(json.dumps(enhanced, indent=2))
        else:
            print(f"Error: Could not load model {args.model}", file=sys.stderr)
            sys.exit(1)
    else:
        # All models
        all_enhanced = []
        transformations = ['P', 'IN', 'CO', 'DE', 'RE', 'SY']
        
        for transform in transformations:
            for i in range(1, 21):
                code = f"{transform}{i:02d}"
                enhanced = extract_enhanced_context(code, loader, relationship_data)
                if enhanced:
                    all_enhanced.append(enhanced)
        
        # Save to file
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'total': len(all_enhanced),
                'models': all_enhanced
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Extracted enhanced context for {len(all_enhanced)} models")
        print(f"   Saved to: {output_path}")
        
        # Show statistics
        print("\n" + "=" * 70)
        print("CONTEXT STATISTICS")
        print("=" * 70)
        
        desc_lengths = [len(m.get('description', '')) for m in all_enhanced]
        examples_count = sum(1 for m in all_enhanced if 'example' in m)
        related_count = sum(1 for m in all_enhanced if 'related_models' in m)
        
        print(f"Description lengths:")
        print(f"  Min: {min(desc_lengths)} chars")
        print(f"  Max: {max(desc_lengths)} chars")
        print(f"  Avg: {sum(desc_lengths) // len(desc_lengths)} chars")
        print()
        print(f"Models with examples: {examples_count}/{len(all_enhanced)}")
        print(f"Models with related_models: {related_count}/{len(all_enhanced)}")
        print()
        print("=" * 70)
        print("API ENHANCEMENT RECOMMENDATION")
        print("=" * 70)
        print()
        print("Current API fields:")
        print("  - code, name, definition (~80 chars), priority, transformation")
        print()
        print("Proposed additional fields:")
        print("  - description: Full description (200-700 chars)")
        print("  - example: Usage example (optional, 100-500 chars)")
        print("  - related_models: Array of model codes (optional)")
        print("  - status: draft/prototype/developed")
        print("  - version: Semantic version")
        print()
        print("NOTE: Cloudflare Workers typically support:")
        print("  - Response size: Up to 100MB (plenty of room)")
        print("  - Individual field: No hard limit, but keep reasonable")
        print("  - Recommended: description < 1000 chars, example < 500 chars")


if __name__ == '__main__':
    import re
    main()

