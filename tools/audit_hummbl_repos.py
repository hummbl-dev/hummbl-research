#!/usr/bin/env python3
"""
Comprehensive audit of all HUMMBL repositories under hummbl-dev GitHub account.

This script:
1. Lists all repositories (from web search and local)
2. Checks repository status (exists, accessible, etc.)
3. Analyzes repository structure
4. Identifies integration opportunities
5. Generates comprehensive audit report
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import requests

# Known repositories from web search
KNOWN_REPOS = [
    'hummbl-claude-skills',
    'hummbl-monorepo',
    'hummbl-io',
    'hummbl-api',
    'hummbl-docs',
    'hummbl-cli',
    'hummbl-sdk',
    'hummbl-utils',
    'hummbl-data',
    'hummbl-tests',
    'hummbl-examples',
    'hummbl-templates',
    'hummbl-configs',
    'hummbl-prototype',  # Known from local
    'hummbl-research',  # Known from local
]

LOCAL_REPO_PATH = Path('/Users/others/Documents/GitHub')


def check_repo_exists(repo_name: str) -> Dict:
    """Check if repository exists on GitHub."""
    url = f"https://api.github.com/repos/hummbl-dev/{repo_name}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'exists': True,
                'public': not data.get('private', True),
                'description': data.get('description', ''),
                'language': data.get('language', ''),
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'updated': data.get('updated_at', ''),
                'url': data.get('html_url', '')
            }
        elif response.status_code == 404:
            return {'exists': False, 'error': 'Not found'}
        else:
            return {'exists': False, 'error': f'Status {response.status_code}'}
    except Exception as e:
        return {'exists': False, 'error': str(e)}


def check_local_repo(repo_name: str) -> Dict:
    """Check if repository exists locally."""
    repo_path = LOCAL_REPO_PATH / repo_name
    if not repo_path.exists():
        return {'local': False}
    
    result = {
        'local': True,
        'path': str(repo_path),
        'is_git': (repo_path / '.git').exists(),
    }
    
    if result['is_git']:
        try:
            # Get remote URL
            remote = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if remote.returncode == 0:
                result['remote'] = remote.stdout.strip()
            
            # Get branch
            branch = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if branch.returncode == 0:
                result['branch'] = branch.stdout.strip()
            
            # Get last commit
            commit = subprocess.run(
                ['git', 'log', '-1', '--format=%H|%s|%ai', '--no-merges'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if commit.returncode == 0 and commit.stdout.strip():
                parts = commit.stdout.strip().split('|')
                if len(parts) >= 3:
                    result['last_commit'] = {
                        'hash': parts[0][:8],
                        'message': parts[1],
                        'date': parts[2]
                    }
        except Exception as e:
            result['git_error'] = str(e)
    
    # Check directory structure
    try:
        dirs = [d.name for d in repo_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        files = [f.name for f in repo_path.iterdir() if f.is_file() and not f.name.startswith('.')]
        result['structure'] = {
            'directories': sorted(dirs)[:10],  # Limit to first 10
            'files': sorted(files)[:10]
        }
    except Exception as e:
        result['structure_error'] = str(e)
    
    return result


def analyze_repo_structure(repo_name: str, local_info: Dict) -> Dict:
    """Analyze repository structure for integration opportunities."""
    if not local_info.get('local'):
        return {}
    
    repo_path = Path(local_info['path'])
    analysis = {
        'has_api': False,
        'has_workers': False,
        'has_models': False,
        'has_relationships': False,
        'has_tools': False,
        'has_docs': False,
        'integration_opportunities': []
    }
    
    # Check for API/Workers code
    if (repo_path / 'src').exists() or (repo_path / 'app').exists() or (repo_path / 'api').exists():
        analysis['has_api'] = True
        analysis['integration_opportunities'].append('API endpoint integration')
    
    if (repo_path / 'workers').exists() or (repo_path / 'wrangler.toml').exists():
        analysis['has_workers'] = True
        analysis['integration_opportunities'].append('Cloudflare Workers integration')
    
    # Check for models
    if (repo_path / 'models').exists():
        analysis['has_models'] = True
        analysis['integration_opportunities'].append('Model data integration')
    
    # Check for relationships
    if (repo_path / 'data' / 'relationships.json').exists() or (repo_path / 'relationships.json').exists():
        analysis['has_relationships'] = True
        analysis['integration_opportunities'].append('Relationship data integration')
    
    # Check for tools
    if (repo_path / 'tools').exists():
        analysis['has_tools'] = True
    
    # Check for docs
    if (repo_path / 'docs').exists() or (repo_path / 'README.md').exists():
        analysis['has_docs'] = True
    
    return analysis


def main():
    print("=" * 70)
    print("HUMMBL REPOSITORY AUDIT")
    print("=" * 70)
    print()
    
    audit_results = {
        'timestamp': datetime.now().isoformat(),
        'repositories': []
    }
    
    for repo_name in KNOWN_REPOS:
        print(f"Auditing {repo_name}...")
        
        repo_info = {
            'name': repo_name,
            'github': check_repo_exists(repo_name),
            'local': check_local_repo(repo_name)
        }
        
        # Analyze structure if local
        if repo_info['local'].get('local'):
            repo_info['analysis'] = analyze_repo_structure(repo_name, repo_info['local'])
        
        audit_results['repositories'].append(repo_info)
        
        # Print summary
        github_status = "✅" if repo_info['github'].get('exists') else "❌"
        local_status = "✅" if repo_info['local'].get('local') else "❌"
        print(f"  GitHub: {github_status} | Local: {local_status}")
    
    # Save audit results
    output_file = Path('validation/hummbl-repos-audit.json')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, indent=2, ensure_ascii=False)
    
    # Generate summary report
    print("\n" + "=" * 70)
    print("AUDIT SUMMARY")
    print("=" * 70)
    
    total = len(audit_results['repositories'])
    github_count = sum(1 for r in audit_results['repositories'] if r['github'].get('exists'))
    local_count = sum(1 for r in audit_results['repositories'] if r['local'].get('local'))
    
    print(f"Total repositories checked: {total}")
    print(f"GitHub repositories: {github_count}/{total}")
    print(f"Local repositories: {local_count}/{total}")
    print()
    
    print("Repositories with integration opportunities:")
    for repo in audit_results['repositories']:
        if repo.get('analysis', {}).get('integration_opportunities'):
            opps = repo['analysis']['integration_opportunities']
            print(f"  - {repo['name']}: {', '.join(opps)}")
    
    print(f"\n✅ Full audit saved to: {output_file}")
    
    # Generate markdown report
    md_file = Path('validation/hummbl-repos-audit-report.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# HUMMBL Repository Audit Report\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Total Repositories**: {total}\n")
        f.write(f"- **GitHub Repositories**: {github_count}\n")
        f.write(f"- **Local Repositories**: {local_count}\n\n")
        f.write("## Repository Details\n\n")
        
        for repo in audit_results['repositories']:
            f.write(f"### {repo['name']}\n\n")
            
            github = repo['github']
            local = repo['local']
            
            if github.get('exists'):
                f.write(f"- **GitHub**: ✅ [View]({github.get('url', '#')})\n")
                f.write(f"  - Description: {github.get('description', 'N/A')}\n")
                f.write(f"  - Language: {github.get('language', 'N/A')}\n")
                f.write(f"  - Stars: {github.get('stars', 0)}\n")
            else:
                f.write(f"- **GitHub**: ❌ {github.get('error', 'Not found')}\n")
            
            if local.get('local'):
                f.write(f"- **Local**: ✅ {local.get('path', 'N/A')}\n")
                if local.get('branch'):
                    f.write(f"  - Branch: {local.get('branch')}\n")
                if local.get('last_commit'):
                    commit = local['last_commit']
                    f.write(f"  - Last commit: {commit.get('hash')} - {commit.get('message', '')[:50]}\n")
            else:
                f.write(f"- **Local**: ❌ Not cloned\n")
            
            if repo.get('analysis', {}).get('integration_opportunities'):
                f.write(f"- **Integration Opportunities**:\n")
                for opp in repo['analysis']['integration_opportunities']:
                    f.write(f"  - {opp}\n")
            
            f.write("\n")
    
    print(f"✅ Markdown report saved to: {md_file}")


if __name__ == '__main__':
    main()

