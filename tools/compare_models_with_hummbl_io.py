#!/usr/bin/env python3
"""
Compare repository models with hummbl.io official list.

This script:
1. Loads all models from repository via ModelLoader
2. Attempts to fetch official list from hummbl.io API
3. Compares names, codes, and identifies discrepancies
4. Reports what needs to be updated
"""

import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from validate_relationships import ModelLoader


def load_repository_models() -> Dict[str, Dict]:
    """Load all models from repository."""
    loader = ModelLoader()
    models = {}
    
    transformations = ['P', 'IN', 'CO', 'DE', 'RE', 'SY']
    for transform in transformations:
        for i in range(1, 21):
            code = f"{transform}{i:02d}"
            info = loader.load_model(code)
            if info:
                models[code] = {
                    'code': code,
                    'name': info.get('name', 'Unknown').strip(),
                    'description': info.get('description', ''),
                    'transform': transform
                }
            else:
                models[code] = {
                    'code': code,
                    'name': 'NOT FOUND',
                    'description': '',
                    'transform': transform
                }
    
    return models


def fetch_hummbl_io_models() -> Optional[Dict[str, Dict]]:
    """Attempt to fetch official model list from hummbl.io API."""
    api_endpoints = [
        'https://api.hummbl.io/models',
        'https://hummbl.io/api/models',
        'https://api.hummbl.io/v1/models',
        'https://hummbl.io/api/v1/models',
    ]
    
    for endpoint in api_endpoints:
        try:
            print(f"Trying: {endpoint}...")
            response = requests.get(endpoint, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Successfully fetched from {endpoint}")
                return data
        except Exception as e:
            print(f"  Failed: {e}")
            continue
    
    return None


def compare_models(repo_models: Dict[str, Dict], official_models: Optional[Dict[str, Dict]]) -> Dict:
    """Compare repository models with official list."""
    comparison = {
        'total_repo': len(repo_models),
        'total_official': len(official_models) if official_models else 0,
        'missing_in_repo': [],
        'missing_in_official': [],
        'name_mismatches': [],
        'duplicates_in_repo': [],
        'status': 'unknown'
    }
    
    if not official_models:
        comparison['status'] = 'no_official_data'
        return comparison
    
    # Check for missing models
    repo_codes = set(repo_models.keys())
    official_codes = set(official_models.keys())
    
    comparison['missing_in_repo'] = sorted(official_codes - repo_codes)
    comparison['missing_in_official'] = sorted(repo_codes - official_codes)
    
    # Check for name mismatches
    common_codes = repo_codes & official_codes
    for code in common_codes:
        repo_name = repo_models[code]['name']
        official_name = official_models[code].get('name', 'Unknown')
        if repo_name != official_name and repo_name != 'NOT FOUND':
            comparison['name_mismatches'].append({
                'code': code,
                'repo_name': repo_name,
                'official_name': official_name
            })
    
    # Check for duplicates in repo
    name_counts = defaultdict(list)
    for code, model in repo_models.items():
        if model['name'] != 'NOT FOUND':
            name_counts[model['name']].append(code)
    
    comparison['duplicates_in_repo'] = [
        {'name': name, 'codes': codes}
        for name, codes in name_counts.items()
        if len(codes) > 1
    ]
    
    if not comparison['missing_in_repo'] and not comparison['name_mismatches']:
        comparison['status'] = 'match'
    elif comparison['name_mismatches']:
        comparison['status'] = 'name_mismatches'
    else:
        comparison['status'] = 'missing_models'
    
    return comparison


def generate_report(comparison: Dict, repo_models: Dict[str, Dict]) -> str:
    """Generate human-readable comparison report."""
    lines = []
    lines.append("=" * 70)
    lines.append("MODEL COMPARISON REPORT: Repository vs hummbl.io")
    lines.append("=" * 70)
    lines.append("")
    
    lines.append(f"Repository models: {comparison['total_repo']}")
    if comparison['total_official'] > 0:
        lines.append(f"Official models: {comparison['total_official']}")
    lines.append("")
    
    if comparison['status'] == 'no_official_data':
        lines.append("⚠️  Could not fetch official model list from hummbl.io API")
        lines.append("   Manual comparison required")
        lines.append("")
    elif comparison['status'] == 'match':
        lines.append("✅ Repository matches official list!")
        lines.append("")
    else:
        if comparison['missing_in_repo']:
            lines.append(f"❌ Missing in repository ({len(comparison['missing_in_repo'])}):")
            for code in comparison['missing_in_repo']:
                lines.append(f"   - {code}")
            lines.append("")
        
        if comparison['missing_in_official']:
            lines.append(f"⚠️  In repository but not in official ({len(comparison['missing_in_official'])}):")
            for code in comparison['missing_in_official']:
                lines.append(f"   - {code}: {repo_models[code]['name']}")
            lines.append("")
        
        if comparison['name_mismatches']:
            lines.append(f"⚠️  Name mismatches ({len(comparison['name_mismatches'])}):")
            for mismatch in comparison['name_mismatches']:
                lines.append(f"   {mismatch['code']}:")
                lines.append(f"     Repository: '{mismatch['repo_name']}'")
                lines.append(f"     Official:   '{mismatch['official_name']}'")
            lines.append("")
    
    if comparison['duplicates_in_repo']:
        lines.append(f"⚠️  Duplicate names in repository ({len(comparison['duplicates_in_repo'])}):")
        for dup in comparison['duplicates_in_repo']:
            lines.append(f"   '{dup['name']}' appears in: {', '.join(dup['codes'])}")
        lines.append("")
    
    return "\n".join(lines)


def main():
    """Main entry point."""
    print("Loading repository models...")
    repo_models = load_repository_models()
    print(f"✅ Loaded {len(repo_models)} models from repository")
    print()
    
    print("Attempting to fetch official models from hummbl.io...")
    official_models = fetch_hummbl_io_models()
    print()
    
    if official_models:
        print("Comparing models...")
        comparison = compare_models(repo_models, official_models)
    else:
        # Still do duplicate check even without official data
        comparison = {
            'total_repo': len(repo_models),
            'total_official': 0,
            'missing_in_repo': [],
            'missing_in_official': [],
            'name_mismatches': [],
            'duplicates_in_repo': [],
            'status': 'no_official_data'
        }
        
        # Check for duplicates
        name_counts = defaultdict(list)
        for code, model in repo_models.items():
            if model['name'] != 'NOT FOUND':
                name_counts[model['name']].append(code)
        
        comparison['duplicates_in_repo'] = [
            {'name': name, 'codes': codes}
            for name, codes in name_counts.items()
            if len(codes) > 1
        ]
    
    # Generate report
    report = generate_report(comparison, repo_models)
    print(report)
    
    # Save detailed comparison to JSON
    output_file = Path(__file__).parent.parent / 'validation' / 'model-comparison-report.json'
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'comparison': comparison,
            'repo_models': repo_models,
            'official_models': official_models
        }, f, indent=2)
    
    print(f"📄 Detailed comparison saved to: {output_file}")
    
    # Return exit code based on status
    if comparison['status'] == 'match':
        return 0
    elif comparison['duplicates_in_repo'] or comparison['name_mismatches']:
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())

