#!/usr/bin/env python3
"""
Fix duplicate model names based on pattern analysis and official sources.

This script:
1. Identifies duplicate model names
2. Applies fixes based on pattern (developed > draft) or official list
3. Updates model markdown files
4. Creates backup before changes
"""

import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Duplicate fixes based on analysis
# Pattern: developed versions are more complete, so they likely have correct names
# Draft versions may need renaming or may be placeholders

DUPLICATE_FIXES = {
    # Format: (code_to_fix, new_name, reason)
    # If new_name is None, we'll need to determine from official source
    
    # Systems Thinking: P04 (draft) vs P18 (developed)
    # P18 is developed and more detailed - likely correct
    # P04 might need a different name or is a duplicate
    'P04': {
        'action': 'verify',  # Need to check official name
        'current_name': 'Systems Thinking',
        'conflict_with': 'P18',
        'suggested_fix': None  # Will be determined
    },
    
    # Stakeholder Mapping: P12 (draft) vs P17 (developed)
    'P12': {
        'action': 'verify',
        'current_name': 'Stakeholder Mapping',
        'conflict_with': 'P17',
        'suggested_fix': None
    },
    
    # Assumption Inversion: IN14 (draft) vs IN17 (developed)
    'IN14': {
        'action': 'verify',
        'current_name': 'Assumption Inversion',
        'conflict_with': 'IN17',
        'suggested_fix': None
    },
    
    # Functional Decomposition: DE02 (draft) vs DE16 (developed)
    'DE02': {
        'action': 'verify',
        'current_name': 'Functional Decomposition',
        'conflict_with': 'DE16',
        'suggested_fix': None
    },
    
    # Recursive Optimization: RE14 (draft) vs RE16 (developed)
    'RE14': {
        'action': 'verify',
        'current_name': 'Recursive Optimization',
        'conflict_with': 'RE16',
        'suggested_fix': None
    },
    
    # Holistic Integration: SY03 (draft) vs SY18 (developed)
    'SY03': {
        'action': 'verify',
        'current_name': 'Holistic Integration',
        'conflict_with': 'SY18',
        'suggested_fix': None
    },
}


def load_model_file(model_path: Path) -> Dict:
    """Load and parse a model markdown file."""
    if not model_path.exists():
        return None
    
    with open(model_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = {}
            for line in parts[1].strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
            return {
                'frontmatter': frontmatter,
                'content': parts[2] if len(parts) > 2 else '',
                'full_content': content
            }
    
    return None


def update_model_name(model_path: Path, new_name: str, backup_dir: Path) -> bool:
    """Update model name in markdown file."""
    model_data = load_model_file(model_path)
    if not model_data:
        return False
    
    # Create backup
    backup_path = backup_dir / model_path.name
    shutil.copy2(model_path, backup_path)
    
    # Update frontmatter
    frontmatter = model_data['frontmatter']
    old_name = frontmatter.get('name', '')
    frontmatter['name'] = new_name
    
    # Reconstruct file
    frontmatter_lines = ['---']
    for key, value in frontmatter.items():
        frontmatter_lines.append(f"{key}: {value}")
    frontmatter_lines.append('---')
    
    new_content = '\n'.join(frontmatter_lines) + '\n' + model_data['content']
    
    # Write updated file
    with open(model_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ Updated {model_path.name}: '{old_name}' → '{new_name}'")
    return True


def create_fix_plan() -> Dict:
    """Create a plan for fixing duplicates."""
    repo_root = Path(__file__).parent.parent
    models_dir = repo_root / 'models'
    
    fixes = []
    for code, fix_info in DUPLICATE_FIXES.items():
        transform = code[:2] if len(code) > 2 and code[1].isalpha() else code[0]
        model_file = models_dir / transform / f"{code}.md"
        
        if model_file.exists():
            fixes.append({
                'code': code,
                'file': model_file,
                'current_name': fix_info['current_name'],
                'conflict_with': fix_info['conflict_with'],
                'action': fix_info['action']
            })
    
    return fixes


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    models_dir = repo_root / 'models'
    backup_dir = repo_root / 'validation' / 'model-backups' / datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("DUPLICATE MODEL NAME FIXER")
    print("=" * 70)
    print()
    
    # Load official fixes if available
    official_fixes_file = repo_root / 'validation' / 'official-model-names.json'
    official_fixes = {}
    
    if official_fixes_file.exists():
        with open(official_fixes_file, 'r') as f:
            official_fixes = json.load(f)
        print(f"✅ Loaded official names from: {official_fixes_file}")
        print()
    
    # Create fix plan
    fixes = create_fix_plan()
    
    print(f"Found {len(fixes)} models with duplicate names")
    print()
    
    if not official_fixes:
        print("⚠️  No official model names file found.")
        print("   Creating verification report instead of applying fixes.")
        print()
        
        # Create verification report
        report = {
            'timestamp': datetime.now().isoformat(),
            'duplicates_found': len(fixes),
            'fixes_needed': [
                {
                    'code': f['code'],
                    'file': str(f['file']),
                    'current_name': f['current_name'],
                    'conflict_with': f['conflict_with'],
                    'action': f['action']
                }
                for f in fixes
            ],
            'status': 'verification_required',
            'next_steps': [
                '1. Get official model names from hummbl.io',
                '2. Save to validation/official-model-names.json',
                '3. Re-run this script to apply fixes'
            ]
        }
        
        report_file = repo_root / 'validation' / 'fix-verification-report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Verification report saved to: {report_file}")
        print()
        print("To apply fixes:")
        print("  1. Get official names from hummbl.io")
        print("  2. Create validation/official-model-names.json with format:")
        print('     {"P04": "New Name", "P12": "New Name", ...}')
        print("  3. Re-run this script")
        return 0
    
    # Apply fixes
    print("Applying fixes...")
    print()
    
    applied = 0
    for fix in fixes:
        code = fix['code']
        if code in official_fixes:
            new_name = official_fixes[code]
            if update_model_name(fix['file'], new_name, backup_dir):
                applied += 1
    
    print()
    print(f"✅ Applied {applied} fixes")
    print(f"📦 Backups saved to: {backup_dir}")
    print()
    
    if applied > 0:
        print("⚠️  Please verify the changes and test ModelLoader")
        print("   Run: python tools/compare_models_with_hummbl_io.py")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

