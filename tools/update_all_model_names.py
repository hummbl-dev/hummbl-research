#!/usr/bin/env python3
"""
Update all model names in repository to match hummbl.io official API.

This script:
1. Loads official model names from hummbl.io API
2. Updates all model markdown files with correct names
3. Creates backups before changes
4. Reports what was changed
"""

import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime

def normalize_code(code: str) -> str:
    """Normalize P1 -> P01, P10 -> P10, etc."""
    if len(code) == 2 and code[1].isdigit():
        transform = code[0]
        num = int(code[1:])
        return f"{transform}{num:02d}"
    return code


def load_official_models() -> Dict[str, Dict]:
    """Load official model names from API data."""
    repo_root = Path(__file__).parent.parent
    official_file = repo_root / 'validation' / 'hummbl-io-official-models.json'
    
    if not official_file.exists():
        print(f"❌ Official models file not found: {official_file}")
        print("   Run: curl -s 'https://hummbl-api.hummbl.workers.dev/v1/models' > validation/hummbl-io-official-models.json")
        return {}
    
    with open(official_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    official_mapping = {}
    for model in data.get('models', []):
        normalized = normalize_code(model['code'])
        official_mapping[normalized] = {
            'name': model['name'],
            'definition': model.get('definition', ''),
            'transformation': model.get('transformation', '')
        }
    
    return official_mapping


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


def update_model_name(model_path: Path, new_name: str, backup_dir: Path) -> tuple[bool, str]:
    """Update model name in markdown file. Returns (success, old_name)."""
    model_data = load_model_file(model_path)
    if not model_data:
        return False, ''
    
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
    
    return True, old_name


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    models_dir = repo_root / 'models'
    backup_dir = repo_root / 'validation' / 'model-backups' / datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("UPDATE ALL MODEL NAMES TO MATCH HUMMBL.IO")
    print("=" * 70)
    print()
    
    # Load official models
    print("Loading official model names from hummbl.io API...")
    official_models = load_official_models()
    
    if not official_models:
        print("❌ Could not load official models. Exiting.")
        return 1
    
    print(f"✅ Loaded {len(official_models)} official models")
    print()
    
    # Load repository models
    print("Scanning repository model files...")
    transformations = ['P', 'IN', 'CO', 'DE', 'RE', 'SY']
    updates = []
    not_found = []
    
    for transform in transformations:
        for i in range(1, 21):
            code = f"{transform}{i:02d}"
            model_file = models_dir / transform / f"{code}.md"
            
            if not model_file.exists():
                not_found.append(code)
                continue
            
            # Check if official name exists
            if code not in official_models:
                not_found.append(code)
                continue
            
            official_name = official_models[code]['name']
            
            # Load current name
            model_data = load_model_file(model_file)
            if not model_data:
                continue
            
            current_name = model_data['frontmatter'].get('name', '').strip()
            
            # Update if different
            if current_name != official_name:
                success, old_name = update_model_name(model_file, official_name, backup_dir)
                if success:
                    updates.append({
                        'code': code,
                        'old_name': old_name,
                        'new_name': official_name
                    })
    
    # Report
    print()
    print("=" * 70)
    print("UPDATE SUMMARY")
    print("=" * 70)
    print()
    
    if updates:
        print(f"✅ Updated {len(updates)} model names:")
        print()
        for update in updates:
            print(f"  {update['code']}: '{update['old_name']}' → '{update['new_name']}'")
        print()
    else:
        print("✅ No updates needed - all names match!")
        print()
    
    if not_found:
        print(f"⚠️  {len(not_found)} models not found in official list:")
        for code in not_found[:10]:
            print(f"  - {code}")
        if len(not_found) > 10:
            print(f"  ... and {len(not_found) - 10} more")
        print()
    
    print(f"📦 Backups saved to: {backup_dir}")
    print()
    
    # Save update log
    log_file = repo_root / 'validation' / 'model-name-updates.json'
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_updates': len(updates),
            'updates': updates,
            'not_found_in_official': not_found
        }, f, indent=2)
    
    print(f"📄 Update log saved to: {log_file}")
    print()
    
    if updates:
        print("⚠️  Please verify the changes and test ModelLoader:")
        print("   python tools/compare_models_with_hummbl_io.py")
        print()
        return 1  # Indicate changes were made
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

