#!/usr/bin/env python3
"""
Apply approved relationship fixes from validation results.

Usage:
    python tools/apply_relationship_fixes.py --batches 1,2,3 --apply
    python tools/apply_relationship_fixes.py --batches 1,2,3 --dry-run
"""

import json
import argparse
import re
from pathlib import Path
from typing import List, Dict

def normalize_code(code: str) -> str:
    """Normalize model code (IN8 -> IN08)"""
    match = re.match(r'([A-Z]{1,2})(\d{1,2})', code)
    if match:
        transform, number = match.groups()
        return f"{transform}{number.zfill(2)}"
    return code

def load_relationships(json_path: str = 'data/relationships.json') -> List[Dict]:
    """Load relationships from JSON"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_relationships(relationships: List[Dict], json_path: str = 'data/relationships.json'):
    """Save relationships to JSON"""
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(relationships, f, indent=2)

def extract_fixes_from_batches(batch_numbers: List[int]) -> List[Dict]:
    """Extract fixes from batch validation results"""
    validation_dir = Path('validation')
    fixes = []
    
    for batch_num in batch_numbers:
        batch_file = validation_dir / f'relationships-batch-{batch_num:02d}-results.json'
        if not batch_file.exists():
            continue
        
        with open(batch_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        for result in results:
            rel_id = result['id']
            
            # Fix direction mismatches (NEEDS_REVIEW with direction issues)
            if result['status'] == 'NEEDS_REVIEW':
                for issue in result.get('issues', []):
                    if 'Direction' in issue and 'may be incorrect' in issue:
                        # Extract expected direction
                        if 'Expected: [\'unidirectional\']' in issue or 'Expected: unidirectional' in issue:
                            fixes.append({
                                'id': rel_id,
                                'field': 'direction',
                                'new_value': 'unidirectional',
                                'reason': 'Direction mismatch fix',
                                'issue': issue
                            })
                        elif 'Expected: [\'bidirectional\']' in issue or 'Expected: bidirectional' in issue:
                            fixes.append({
                                'id': rel_id,
                                'field': 'direction',
                                'new_value': 'bidirectional',
                                'reason': 'Direction mismatch fix',
                                'issue': issue
                            })
            
            # Apply refinements (NEEDS_REFINEMENT)
            if result['status'] == 'NEEDS_REFINEMENT':
                for rec in result.get('recommendations', []):
                    # Strength refinements
                    if 'strength' in rec.lower() and '0.' in rec:
                        strength_match = re.search(r'0\.\d+', rec)
                        if strength_match:
                            new_strength = float(strength_match.group())
                            fixes.append({
                                'id': rel_id,
                                'field': 'strength',
                                'new_value': new_strength,
                                'reason': 'Strength refinement',
                                'recommendation': rec
                            })
                    
                    # Direction refinements
                    if 'direction' in rec.lower():
                        if 'unidirectional' in rec.lower():
                            fixes.append({
                                'id': rel_id,
                                'field': 'direction',
                                'new_value': 'unidirectional',
                                'reason': 'Direction refinement',
                                'recommendation': rec
                            })
                        elif 'bidirectional' in rec.lower():
                            fixes.append({
                                'id': rel_id,
                                'field': 'direction',
                                'new_value': 'bidirectional',
                                'reason': 'Direction refinement',
                                'recommendation': rec
                            })
    
    return fixes

def apply_fixes(relationships: List[Dict], fixes: List[Dict], dry_run: bool = False) -> Dict:
    """Apply fixes to relationships"""
    rel_dict = {r['id']: r for r in relationships}
    applied = []
    skipped = []
    errors = []
    
    for fix in fixes:
        rel_id = fix['id']
        if rel_id not in rel_dict:
            errors.append(f"Relationship {rel_id} not found")
            continue
        
        rel = rel_dict[rel_id]
        field = fix['field']
        new_value = fix['new_value']
        old_value = rel.get(field)
        
        if old_value == new_value:
            skipped.append(f"{rel_id}: {field} already {new_value}")
            continue
        
        if not dry_run:
            rel[field] = new_value
        
        applied.append({
            'id': rel_id,
            'field': field,
            'old': old_value,
            'new': new_value,
            'reason': fix.get('reason', '')
        })
    
    return {
        'applied': applied,
        'skipped': skipped,
        'errors': errors
    }

def main():
    parser = argparse.ArgumentParser(description='Apply relationship fixes')
    parser.add_argument('--batches', required=True, help='Comma-separated batch numbers (e.g., 1,2,3)')
    parser.add_argument('--apply', action='store_true', help='Apply fixes (default is dry-run)')
    parser.add_argument('--output', help='Output file (default: data/relationships.json)')
    
    args = parser.parse_args()
    
    batch_numbers = [int(b.strip()) for b in args.batches.split(',')]
    dry_run = not args.apply
    output_file = args.output or 'data/relationships.json'
    
    print(f"{'DRY RUN: ' if dry_run else ''}Applying fixes from batches {batch_numbers}")
    print("=" * 60)
    
    # Load relationships
    relationships = load_relationships()
    print(f"Loaded {len(relationships)} relationships")
    
    # Extract fixes
    fixes = extract_fixes_from_batches(batch_numbers)
    print(f"\nExtracted {len(fixes)} fixes")
    
    # Group by field
    by_field = {}
    for fix in fixes:
        field = fix['field']
        if field not in by_field:
            by_field[field] = []
        by_field[field].append(fix)
    
    print("\nFixes by field:")
    for field, field_fixes in by_field.items():
        print(f"  {field}: {len(field_fixes)}")
    
    # Apply fixes
    result = apply_fixes(relationships, fixes, dry_run=dry_run)
    
    print(f"\n📊 Fix Application Results:")
    print(f"   Applied: {len(result['applied'])}")
    print(f"   Skipped: {len(result['skipped'])}")
    print(f"   Errors: {len(result['errors'])}")
    
    if result['applied']:
        print(f"\n✅ Fixes to apply:")
        for fix in result['applied'][:10]:
            print(f"   {fix['id']}: {fix['field']} {fix['old']} → {fix['new']}")
        if len(result['applied']) > 10:
            print(f"   ... and {len(result['applied']) - 10} more")
    
    if result['skipped']:
        print(f"\n⏭️  Skipped (already correct):")
        for skip in result['skipped'][:5]:
            print(f"   {skip}")
    
    if result['errors']:
        print(f"\n❌ Errors:")
        for error in result['errors']:
            print(f"   {error}")
    
    # Save if not dry run
    if not dry_run and result['applied']:
        # Create backup
        backup_file = output_file.replace('.json', '.json.backup')
        import shutil
        shutil.copy(output_file, backup_file)
        print(f"\n💾 Backup created: {backup_file}")
        
        # Save updated relationships
        save_relationships(relationships, output_file)
        print(f"✅ Updated relationships saved to {output_file}")
        
        # Save fix log
        fix_log = {
            'date': __import__('datetime').datetime.now().strftime('%Y-%m-%d'),
            'batches': batch_numbers,
            'fixes_applied': result['applied'],
            'fixes_skipped': result['skipped'],
            'errors': result['errors']
        }
        log_file = Path('validation') / 'relationships-fixes-applied.json'
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(fix_log, f, indent=2)
        print(f"📝 Fix log saved to {log_file}")
    elif dry_run:
        print(f"\n💡 This was a dry run. Use --apply to actually apply fixes.")
    
    return len(result['applied']) > 0

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)

