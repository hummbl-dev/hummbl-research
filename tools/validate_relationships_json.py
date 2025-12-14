#!/usr/bin/env python3
"""
Simple validation script for relationships.json
Used in CI/CD to ensure JSON structure is valid.

Usage:
    python tools/validate_relationships_json.py [path/to/relationships.json]
"""

import json
import sys
from pathlib import Path
from typing import Dict, List


def validate_relationships_json(json_path: Path) -> bool:
    """Validate relationships.json structure and schema."""
    errors = []
    
    # Check file exists
    if not json_path.exists():
        print(f"❌ ERROR: File not found: {json_path}")
        return False
    
    # Check JSON is valid
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Could not read file: {e}")
        return False
    
    # Check it's a list
    if not isinstance(data, list):
        print(f"❌ ERROR: Expected list, got {type(data).__name__}")
        return False
    
    # Check at least one relationship exists
    if len(data) == 0:
        print("❌ ERROR: No relationships found in file")
        return False
    
    print(f"✅ Found {len(data)} relationships")
    
    # Required fields
    required_fields = ['id', 'from', 'to', 'type', 'strength', 'direction', 'description']
    valid_types = ['SCAFFOLDS', 'COMPOSES_WITH', 'REFINES', 'PARALLELS', 'CONTRASTS_WITH', 'CONFLICTS']
    valid_directions = ['unidirectional', 'bidirectional']
    
    # Validate each relationship
    for i, rel in enumerate(data):
        if not isinstance(rel, dict):
            errors.append(f"Relationship {i}: Expected dict, got {type(rel).__name__}")
            continue
        
        # Check required fields
        for field in required_fields:
            if field not in rel:
                errors.append(f"Relationship {i}: Missing required field '{field}'")
        
        # Check type is valid
        if 'type' in rel and rel['type'] not in valid_types:
            errors.append(f"Relationship {i}: Invalid type '{rel['type']}'. Must be one of {valid_types}")
        
        # Check direction is valid
        if 'direction' in rel and rel['direction'] not in valid_directions:
            errors.append(f"Relationship {i}: Invalid direction '{rel['direction']}'. Must be one of {valid_directions}")
        
        # Check strength is valid (0.0-1.0)
        if 'strength' in rel:
            try:
                strength = float(rel['strength'])
                if not (0.0 <= strength <= 1.0):
                    errors.append(f"Relationship {i}: Strength {strength} out of range [0.0, 1.0]")
            except (ValueError, TypeError):
                errors.append(f"Relationship {i}: Invalid strength value '{rel['strength']}'")
    
    # Report errors
    if errors:
        print(f"\n❌ Validation failed with {len(errors)} error(s):")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more error(s)")
        return False
    
    print("✅ All relationships validated successfully")
    return True


def main():
    """Main entry point."""
    # Default path
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    default_path = repo_root / 'data' / 'relationships.json'
    
    # Allow override via command line
    if len(sys.argv) > 1:
        json_path = Path(sys.argv[1])
    else:
        json_path = default_path
    
    success = validate_relationships_json(json_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

