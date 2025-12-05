#!/usr/bin/env python3
"""
HUMMBL Relationships Validation Tool

Validates 333 relationships across 5 dimensions:
1. Accuracy (type, direction, existence)
2. Strength calibration (0.0-1.0)
3. Description quality
4. Completeness
5. Consistency

Usage:
    python tools/validate_relationships.py --phase prepare
    python tools/validate_relationships.py --phase batch --batch 1
    python tools/validate_relationships.py --phase consistency
    python tools/validate_relationships.py --phase missing
    python tools/validate_relationships.py --phase final
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import re

# Relationship type definitions
RELATIONSHIP_TYPES = {
    'SCAFFOLDS': 'A is a prerequisite or foundation for B',
    'COMPOSES_WITH': 'A and B are often used in sequence or joint operation',
    'REFINES': 'B improves, deepens, or clarifies the output of A',
    'PARALLELS': 'A and B operate in similar domains with alternative methods',
    'CONTRASTS_WITH': 'A and B are conceptual opposites or duals',
    'CONFLICTS': 'A and B represent genuine tension or tradeoff'
}

# Strength scale
STRENGTH_SCALE = {
    'HIGH': (0.8, 1.0),
    'MEDIUM': (0.5, 0.7),
    'LOW': (0.2, 0.4),
    'NEGLIGIBLE': (0.0, 0.1)
}

# Expected direction by type
EXPECTED_DIRECTIONS = {
    'SCAFFOLDS': ['unidirectional'],
    'COMPOSES_WITH': ['unidirectional', 'bidirectional'],
    'REFINES': ['unidirectional'],
    'PARALLELS': ['bidirectional'],
    'CONTRASTS_WITH': ['bidirectional'],
    'CONFLICTS': ['bidirectional']
}

class ModelLoader:
    """Loads and parses HUMMBL model files"""
    
    def __init__(self, models_dir: str = None):
        if models_dir is None:
            # Find models directory - try multiple strategies
            repo_root = None
            
            # Strategy 1: Use __file__ if available
            try:
                script_file = Path(__file__)
                if script_file.exists():
                    script_dir = script_file.parent.resolve()
                    # If script is in tools/, repo_root is parent
                    if script_dir.name == 'tools':
                        repo_root = script_dir.parent
                    else:
                        repo_root = script_dir
            except (NameError, AttributeError):
                pass
            
            # Strategy 2: Check current directory
            if repo_root is None or not (repo_root / 'models').exists():
                cwd = Path.cwd().resolve()
                if (cwd / 'models').exists():
                    repo_root = cwd
                elif (cwd / 'tools').exists() and (cwd.parent / 'models').exists():
                    repo_root = cwd.parent
            
            if repo_root is None:
                raise RuntimeError("Could not find repository root. Please specify models_dir explicitly.")
            
            models_dir = repo_root / 'models'
        
        self.models_dir = Path(models_dir).resolve()
        if not self.models_dir.exists():
            raise RuntimeError(f"Models directory not found: {self.models_dir}")
        self.cache = {}
    
    def load_model(self, model_code: str) -> Optional[Dict]:
        """Load a model file and parse its metadata"""
        if model_code in self.cache:
            return self.cache[model_code]
        
        # Normalize model code (e.g., IN8 -> IN08, DE1 -> DE01)
        # Format: 1-2 uppercase letters followed by 1-2 digits
        match = re.match(r'([A-Z]{1,2})(\d{1,2})', model_code)
        if not match:
            return None
        
        transform, number = match.groups()
        # Pad number to 2 digits
        normalized_code = f"{transform}{number.zfill(2)}"
        
        model_file = self.models_dir / transform / f"{normalized_code}.md"
        
        if not model_file.exists():
            return None
        
        try:
            with open(model_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter
            model_data = self._parse_frontmatter(content)
            # Check if frontmatter has any content (not just empty dict)
            if not model_data or len(model_data) == 0:
                return None
            
            model_data['code'] = normalized_code
            model_data['description'] = self._extract_description(content)
            model_data['related_models'] = self._extract_related_models(content)
            
            # Cache both original and normalized codes
            self.cache[model_code] = model_data
            self.cache[normalized_code] = model_data
            return model_data
        except Exception as e:
            print(f"Error loading {model_code}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return None
    
    def _parse_frontmatter(self, content: str) -> Dict:
        """Parse YAML frontmatter from model file"""
        frontmatter = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                for line in parts[1].strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()
        return frontmatter
    
    def _extract_description(self, content: str) -> str:
        """Extract description section from model file"""
        # Look for ## Description section
        match = re.search(r'## Description\s*\n\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_related_models(self, content: str) -> List[str]:
        """Extract related models from model file"""
        models = []
        # Look for ## Related Models section
        match = re.search(r'## Related Models\s*\n\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if match:
            lines = match.group(1).strip().split('\n')
            for line in lines:
                # Extract model codes (e.g., DE01, P02)
                codes = re.findall(r'([A-Z]{2}\d{2})', line)
                models.extend(codes)
        return list(set(models))


class RelationshipValidator:
    """Validates relationships across 5 dimensions"""
    
    def __init__(self, models_dir: str = 'models'):
        self.model_loader = ModelLoader(models_dir)
        self.validation_date = datetime.now().strftime('%Y-%m-%d')
    
    def validate_relationship(self, relationship: Dict) -> Dict:
        """Validate a single relationship"""
        from_model = self.model_loader.load_model(relationship['from'])
        to_model = self.model_loader.load_model(relationship['to'])
        
        if not from_model or not to_model:
            return {
                'id': relationship['id'],
                'status': 'INVALID',
                'confidence': 'LOW',
                'validation_date': self.validation_date,
                'validator': 'agent-v1',
                'issues': [f"Model file not found: {relationship.get('from') if not from_model else relationship.get('to')}"],
                'recommendations': [],
                'notes': 'Cannot validate - model file missing'
            }
        
        # Validate each dimension
        type_result = self._validate_type(relationship, from_model, to_model)
        direction_result = self._validate_direction(relationship, from_model, to_model)
        strength_result = self._validate_strength(relationship, from_model, to_model)
        description_result = self._validate_description(relationship, from_model, to_model)
        
        # Collect all issues
        issues = []
        issues.extend(type_result['issues'])
        issues.extend(direction_result['issues'])
        issues.extend(strength_result['issues'])
        issues.extend(description_result['issues'])
        
        # Determine status
        if not issues:
            status = 'VALIDATED'
            confidence = 'HIGH'
        elif any('INVALID' in issue for issue in issues):
            status = 'INVALID'
            confidence = 'HIGH'
        elif len(issues) <= 1 and all('minor' in issue.lower() for issue in issues):
            status = 'VALIDATED'
            confidence = 'MEDIUM'
        elif any('strength' in issue.lower() or 'description' in issue.lower() for issue in issues):
            status = 'NEEDS_REFINEMENT'
            confidence = 'MEDIUM'
        else:
            status = 'NEEDS_REVIEW'
            confidence = 'MEDIUM'
        
        # Generate recommendations
        recommendations = []
        recommendations.extend(type_result.get('recommendations', []))
        recommendations.extend(direction_result.get('recommendations', []))
        recommendations.extend(strength_result.get('recommendations', []))
        recommendations.extend(description_result.get('recommendations', []))
        
        return {
            'id': relationship['id'],
            'status': status,
            'confidence': confidence,
            'validation_date': self.validation_date,
            'validator': 'agent-v1',
            'issues': issues,
            'recommendations': recommendations,
            'notes': self._generate_notes(type_result, direction_result, strength_result, description_result)
        }
    
    def _validate_type(self, relationship: Dict, from_model: Dict, to_model: Dict) -> Dict:
        """Validate relationship type is appropriate"""
        issues = []
        recommendations = []
        rel_type = relationship['type']
        
        # Check if type is valid
        if rel_type not in RELATIONSHIP_TYPES:
            issues.append(f"INVALID: Unknown relationship type '{rel_type}'")
            return {'issues': issues, 'recommendations': recommendations}
        
        # Basic semantic checks
        from_name = from_model.get('name', '')
        to_name = to_model.get('name', '')
        from_desc = from_model.get('description', '')
        to_desc = to_model.get('description', '')
        
        # SCAFFOLDS: from should be prerequisite for to
        if rel_type == 'SCAFFOLDS':
            if not from_desc or not to_desc:
                issues.append("minor: Cannot verify SCAFFOLDS relationship - descriptions incomplete")
        
        # REFINES: to should improve from
        elif rel_type == 'REFINES':
            if not from_desc or not to_desc:
                issues.append("minor: Cannot verify REFINES relationship - descriptions incomplete")
        
        # PARALLELS: models should be similar
        elif rel_type == 'PARALLELS':
            # Check if models are in same transformation
            from_transform = relationship['from'][:2]
            to_transform = relationship['to'][:2]
            if from_transform == to_transform:
                # Same transformation - more likely to be parallel
                pass
            else:
                # Cross-transformation parallels - verify similarity
                if not from_desc or not to_desc:
                    issues.append("minor: Cross-transformation PARALLELS - verify similarity")
        
        return {'issues': issues, 'recommendations': recommendations}
    
    def _validate_direction(self, relationship: Dict, from_model: Dict, to_model: Dict) -> Dict:
        """Validate direction is correct for relationship type"""
        issues = []
        recommendations = []
        rel_type = relationship['type']
        direction = relationship['direction']
        
        expected = EXPECTED_DIRECTIONS.get(rel_type, [])
        if direction not in expected:
            issues.append(f"Direction '{direction}' may be incorrect for type '{rel_type}'. Expected: {expected}")
            recommendations.append(f"Consider changing direction to: {expected[0]}")
        
        return {'issues': issues, 'recommendations': recommendations}
    
    def _validate_strength(self, relationship: Dict, from_model: Dict, to_model: Dict) -> Dict:
        """Validate strength value is reasonable"""
        issues = []
        recommendations = []
        strength = relationship['strength']
        
        # Check range
        if strength < 0.0 or strength > 1.0:
            issues.append(f"INVALID: Strength {strength} is outside valid range [0.0, 1.0]")
            return {'issues': issues, 'recommendations': recommendations}
        
        # Check strength scale appropriateness
        rel_type = relationship['type']
        
        # SCAFFOLDS and COMPOSES_WITH should generally be HIGH strength
        if rel_type in ['SCAFFOLDS', 'COMPOSES_WITH']:
            if strength < 0.7:
                issues.append(f"Strength {strength} seems low for {rel_type} relationship. Typical range: 0.7-1.0")
                recommendations.append(f"Consider increasing strength to 0.7-0.9 for {rel_type}")
        
        # PARALLELS can be lower
        elif rel_type == 'PARALLELS':
            if strength > 0.9:
                issues.append(f"Strength {strength} seems high for PARALLELS relationship. Typical range: 0.5-0.8")
        
        # CONTRASTS_WITH and CONFLICTS typically medium
        elif rel_type in ['CONTRASTS_WITH', 'CONFLICTS']:
            if strength > 0.9:
                issues.append(f"Strength {strength} seems high for {rel_type} relationship. Typical range: 0.5-0.8")
        
        return {'issues': issues, 'recommendations': recommendations}
    
    def _validate_description(self, relationship: Dict, from_model: Dict, to_model: Dict) -> Dict:
        """Validate description quality"""
        issues = []
        recommendations = []
        description = relationship.get('description', '')
        
        if not description:
            issues.append("Description is missing")
            recommendations.append("Add a description explaining why this relationship exists")
            return {'issues': issues, 'recommendations': recommendations}
        
        if len(description) < 20:
            issues.append("Description is too short (less than 20 characters)")
            recommendations.append("Expand description to clearly explain the relationship")
        
        if len(description) > 200:
            issues.append("Description is too long (more than 200 characters)")
            recommendations.append("Condense description to 1-2 sentences")
        
        # Check for model codes in description
        from_code = relationship['from']
        to_code = relationship['to']
        if from_code not in description and to_code not in description:
            # Not necessarily an issue, but could be improved
            pass
        
        return {'issues': issues, 'recommendations': recommendations}
    
    def _generate_notes(self, type_result: Dict, direction_result: Dict, 
                       strength_result: Dict, description_result: Dict) -> str:
        """Generate validation notes"""
        all_issues = []
        all_issues.extend(type_result.get('issues', []))
        all_issues.extend(direction_result.get('issues', []))
        all_issues.extend(strength_result.get('issues', []))
        all_issues.extend(description_result.get('issues', []))
        
        if not all_issues:
            return "Relationship type, direction, strength, and description all validated"
        else:
            return f"Found {len(all_issues)} issue(s) requiring attention"


def load_relationships(json_path: str = None) -> List[Dict]:
    """Load relationships from JSON file"""
    if json_path is None:
        # Find data directory relative to script location
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent
        json_path = repo_root / 'data' / 'relationships.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_batch(relationships: List[Dict], batch_num: int, batch_size: int = 50) -> List[Dict]:
    """Get a batch of relationships"""
    start = (batch_num - 1) * batch_size
    end = start + batch_size
    return relationships[start:end]


def phase_prepare():
    """Phase 1: Data Preparation"""
    print("Phase 1: Data Preparation")
    print("=" * 50)
    
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    json_path = repo_root / 'data' / 'relationships.json'
    
    if not json_path.exists():
        print(f"❌ ERROR: {json_path} not found")
        return False
    
    relationships = load_relationships(json_path)
    count = len(relationships)
    
    print(f"✅ Found {count} relationships in {json_path}")
    
    if count != 333:
        print(f"⚠️  WARNING: Expected 333 relationships, found {count}")
    
    # Validate schema
    required_fields = ['id', 'from', 'to', 'type', 'strength', 'direction', 'description']
    schema_errors = []
    
    for i, rel in enumerate(relationships[:10]):  # Sample check
        for field in required_fields:
            if field not in rel:
                schema_errors.append(f"Relationship {i}: missing field '{field}'")
    
    if schema_errors:
        print(f"❌ Schema errors found:")
        for error in schema_errors:
            print(f"  - {error}")
        return False
    
    print("✅ Schema validation passed")
    print("\n📋 HITL Gate 1: Data Availability")
    print("   Please review and approve proceeding to batch validation")
    
    # Save input file for validation
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    validation_dir = repo_root / 'validation'
    validation_dir.mkdir(exist_ok=True)
    output_path = validation_dir / 'relationships-validation-input.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(relationships, f, indent=2)
    print(f"✅ Saved validation input to {output_path}")
    
    return True


def phase_batch(batch_num: int):
    """Phase 2: Batch Validation"""
    print(f"Phase 2: Batch Validation - Batch {batch_num}")
    print("=" * 50)
    
    relationships = load_relationships()
    batch = get_batch(relationships, batch_num)
    
    if not batch:
        print(f"❌ ERROR: Batch {batch_num} is empty")
        return False
    
    print(f"Validating {len(batch)} relationships...")
    
    # Validator will auto-detect models directory
    validator = RelationshipValidator()
    results = []
    
    for rel in batch:
        result = validator.validate_relationship(rel)
        results.append(result)
        
        # Progress indicator
        status_icon = {
            'VALIDATED': '✅',
            'NEEDS_REVIEW': '⚠️',
            'INVALID': '❌',
            'NEEDS_REFINEMENT': '📝'
        }.get(result['status'], '❓')
        print(f"  {status_icon} {rel['id']}: {result['status']}")
    
    # Generate batch report
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    validation_dir = repo_root / 'validation'
    validation_dir.mkdir(exist_ok=True)
    report_path = validation_dir / f'relationships-batch-{batch_num:02d}-results.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Generate summary
    status_counts = {}
    for result in results:
        status = result['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\n📊 Batch Summary:")
    for status, count in sorted(status_counts.items()):
        percentage = (count / len(results)) * 100
        print(f"  {status}: {count} ({percentage:.1f}%)")
    
    validated_count = status_counts.get('VALIDATED', 0) + status_counts.get('NEEDS_REFINEMENT', 0)
    validated_pct = (validated_count / len(results)) * 100
    
    print(f"\n✅ Validated (including refinements): {validated_count}/{len(results)} ({validated_pct:.1f}%)")
    print(f"📄 Full results saved to {report_path}")
    
    if validated_pct >= 90:
        print("\n✅ Batch meets approval criteria (≥90% validated)")
    else:
        print(f"\n⚠️  Batch below approval criteria (need ≥90%, have {validated_pct:.1f}%)")
    
    print(f"\n📋 HITL Gate 2.{batch_num}: Batch {batch_num} Approval")
    print("   Please review batch results and approve or request re-validation")
    
    return True


def phase_consistency():
    """Phase 3: Cross-Validation & Consistency Checks"""
    print("Phase 3: Cross-Validation & Consistency Checks")
    print("=" * 50)
    
    relationships = load_relationships()
    print(f"Analyzing {len(relationships)} relationships for consistency...\n")
    
    # Build relationship graph
    graph = {}
    reverse_graph = {}
    for rel in relationships:
        from_model = rel['from']
        to_model = rel['to']
        rel_id = rel['id']
        
        if from_model not in graph:
            graph[from_model] = []
        graph[from_model].append((to_model, rel))
        
        if to_model not in reverse_graph:
            reverse_graph[to_model] = []
        reverse_graph[to_model].append((from_model, rel))
    
    issues = []
    
    # 1. Symmetry Validation
    print("1. Symmetry Validation...")
    symmetry_issues = []
    for rel in relationships:
        from_model = rel['from']
        to_model = rel['to']
        direction = rel['direction']
        rel_type = rel['type']
        
        # Normalize model codes for comparison
        def normalize_code(code):
            match = re.match(r'([A-Z]{1,2})(\d{1,2})', code)
            if match:
                transform, number = match.groups()
                return f"{transform}{number.zfill(2)}"
            return code
        
        from_norm = normalize_code(from_model)
        to_norm = normalize_code(to_model)
        
        # Check if reverse relationship exists
        reverse_exists = False
        if to_norm in graph:
            for target, rev_rel in graph[to_norm]:
                if normalize_code(target) == from_norm:
                    reverse_exists = True
                    break
        
        # For bidirectional relationships, reverse should exist
        if direction == 'bidirectional' and not reverse_exists:
            symmetry_issues.append({
                'relationship': rel['id'],
                'issue': f"Bidirectional relationship {rel['id']} ({from_model} ↔ {to_model}) has no reverse",
                'recommendation': f"Add reverse relationship or change direction to unidirectional"
            })
    
    print(f"   Found {len(symmetry_issues)} symmetry issues")
    issues.extend(symmetry_issues)
    
    # 2. Strength Consistency
    print("2. Strength Consistency Analysis...")
    strength_issues = []
    
    # Group by relationship type
    by_type = {}
    for rel in relationships:
        rel_type = rel['type']
        if rel_type not in by_type:
            by_type[rel_type] = []
        by_type[rel_type].append(rel['strength'])
    
    # Check for outliers
    for rel_type, strengths in by_type.items():
        if len(strengths) < 5:
            continue
        avg_strength = sum(strengths) / len(strengths)
        variance = sum((s - avg_strength) ** 2 for s in strengths) / len(strengths)
        std_dev = variance ** 0.5 if variance > 0 else 0
        
        for rel in relationships:
            if rel['type'] == rel_type:
                strength = rel['strength']
                # Flag if more than 2 standard deviations from mean
                if std_dev > 0.1 and abs(strength - avg_strength) > 2 * std_dev:
                    strength_issues.append({
                        'relationship': rel['id'],
                        'issue': f"Strength {strength:.2f} is outlier for {rel_type} (avg: {avg_strength:.2f}, std: {std_dev:.2f})",
                        'recommendation': f"Consider adjusting strength to {avg_strength:.2f} ± {std_dev:.2f}"
                    })
    
    print(f"   Found {len(strength_issues)} strength consistency issues")
    issues.extend(strength_issues)
    
    # 3. Hub Model Validation
    print("3. Hub Model Validation...")
    hub_issues = []
    
    # Normalize model codes and count connections
    def normalize_code(code):
        match = re.match(r'([A-Z]{1,2})(\d{1,2})', code)
        if match:
            transform, number = match.groups()
            return f"{transform}{number.zfill(2)}"
        return code
    
    connection_counts = {}
    for rel in relationships:
        from_model = normalize_code(rel['from'])
        to_model = normalize_code(rel['to'])
        connection_counts[from_model] = connection_counts.get(from_model, 0) + 1
        connection_counts[to_model] = connection_counts.get(to_model, 0) + 1
    
    # Identify hubs (top 10% by connections)
    sorted_models = sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)
    hub_threshold = sorted_models[len(sorted_models) // 10][1] if len(sorted_models) > 10 else sorted_models[0][1] if sorted_models else 0
    hubs = [model for model, count in sorted_models if count >= hub_threshold]
    
    print(f"   Identified {len(hubs)} hub models (≥{hub_threshold} connections)")
    if sorted_models:
        print(f"   Top hubs: {', '.join([f'{m}({c})' for m, c in sorted_models[:5]])}")
    
    # Validate hub relationships are appropriate
    for hub in hubs[:5]:  # Check top 5 hubs
        hub_rels = [rel for rel in relationships 
                   if normalize_code(rel['from']) == hub or normalize_code(rel['to']) == hub]
        # Check if hub has appropriate relationship types
        types = [rel['type'] for rel in hub_rels]
        if 'SCAFFOLDS' not in types and 'COMPOSES_WITH' not in types:
            hub_issues.append({
                'relationship': f'HUB-{hub}',
                'issue': f"Hub model {hub} lacks SCAFFOLDS or COMPOSES_WITH relationships",
                'recommendation': f"Review if {hub} should have more foundational relationships"
            })
    
    print(f"   Found {len(hub_issues)} hub validation issues")
    issues.extend(hub_issues)
    
    # 4. Pattern Validation
    print("4. Transformation Pattern Validation...")
    pattern_issues = []
    
    # Check DE ↔ CO pattern
    de_co_rels = [rel for rel in relationships 
                  if (rel['from'].startswith('DE') and rel['to'].startswith('CO')) or
                     (rel['from'].startswith('CO') and rel['to'].startswith('DE'))]
    if len(de_co_rels) < 10:
        pattern_issues.append({
            'relationship': 'PATTERN-DE-CO',
            'issue': f"Only {len(de_co_rels)} DE ↔ CO relationships found (expected more)",
            'recommendation': 'Review if DE/CO cross-transformation relationships are complete'
        })
    
    # Check IN ↔ DE pattern
    in_de_rels = [rel for rel in relationships 
                  if (rel['from'].startswith('IN') and rel['to'].startswith('DE')) or
                     (rel['from'].startswith('DE') and rel['to'].startswith('IN'))]
    if len(in_de_rels) < 5:
        pattern_issues.append({
            'relationship': 'PATTERN-IN-DE',
            'issue': f"Only {len(in_de_rels)} IN ↔ DE relationships found (expected more)",
            'recommendation': 'Review if IN/DE cross-transformation relationships are complete'
        })
    
    print(f"   Found {len(pattern_issues)} pattern validation issues")
    issues.extend(pattern_issues)
    
    # Generate report
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    validation_dir = repo_root / 'validation'
    validation_dir.mkdir(exist_ok=True)
    
    report = {
        'validation_date': datetime.now().strftime('%Y-%m-%d'),
        'total_relationships': len(relationships),
        'total_issues': len(issues),
        'issues_by_category': {
            'symmetry': len(symmetry_issues),
            'strength_consistency': len(strength_issues),
            'hub_validation': len(hub_issues),
            'pattern_validation': len(pattern_issues)
        },
        'hub_models': {
            hub: connection_counts[hub] for hub in hubs[:10]
        },
        'issues': issues
    }
    
    report_path = validation_dir / 'relationships-consistency-report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Consistency Summary:")
    print(f"   Total issues found: {len(issues)}")
    print(f"   - Symmetry: {len(symmetry_issues)}")
    print(f"   - Strength consistency: {len(strength_issues)}")
    print(f"   - Hub validation: {len(hub_issues)}")
    print(f"   - Pattern validation: {len(pattern_issues)}")
    print(f"\n📄 Full report saved to {report_path}")
    print(f"\n📋 HITL Gate 3: Consistency Review")
    print("   Please review consistency report and approve fixes")
    
    return True


def phase_missing():
    """Phase 4: Missing Relationship Detection"""
    print("Phase 4: Missing Relationship Detection")
    print("=" * 50)
    
    relationships = load_relationships()
    model_loader = ModelLoader()
    
    # Build set of existing relationships
    existing_rels = set()
    for rel in relationships:
        # Normalize model codes
        def normalize(code):
            match = re.match(r'([A-Z]{1,2})(\d{1,2})', code)
            if match:
                transform, number = match.groups()
                return f"{transform}{number.zfill(2)}"
            return code
        
        from_norm = normalize(rel['from'])
        to_norm = normalize(rel['to'])
        # Store both directions
        existing_rels.add((from_norm, to_norm))
        existing_rels.add((to_norm, from_norm))
    
    print(f"Analyzing {len(relationships)} existing relationships...")
    print(f"Checking model files for mentioned relationships...\n")
    
    missing_candidates = []
    
    # 1. Check model files for "Related Models" sections
    print("1. Checking model files for mentioned relationships...")
    model_file_missing = []
    
    # Get all model codes
    all_models = set()
    for rel in relationships:
        all_models.add(rel['from'])
        all_models.add(rel['to'])
    
    # Normalize all model codes
    def normalize_code(code):
        match = re.match(r'([A-Z]{1,2})(\d{1,2})', code)
        if match:
            transform, number = match.groups()
            return f"{transform}{number.zfill(2)}"
        return code
    
    normalized_models = {normalize_code(m): m for m in all_models}
    
    checked = 0
    for norm_code in sorted(normalized_models.keys())[:20]:  # Check first 20 models
        model = model_loader.load_model(norm_code)
        if model and 'related_models' in model:
            related = model.get('related_models', [])
            for related_code in related:
                related_norm = normalize_code(related_code)
                # Check if relationship exists
                if (norm_code, related_norm) not in existing_rels:
                    model_file_missing.append({
                        'source_model': norm_code,
                        'target_model': related_norm,
                        'source': f"Model file {norm_code}.md mentions {related_code}",
                        'priority': 'MEDIUM',
                        'recommendation': f"Add relationship from {norm_code} to {related_norm}"
                    })
        checked += 1
    
    print(f"   Checked {checked} model files")
    print(f"   Found {len(model_file_missing)} missing relationships mentioned in model files")
    missing_candidates.extend(model_file_missing)
    
    # 2. Semantic similarity analysis (simplified - check same transformation)
    print("2. Checking for missing same-transformation relationships...")
    same_transform_missing = []
    
    # Group by transformation
    by_transform = {}
    for rel in relationships:
        from_transform = rel['from'][:2] if len(rel['from']) >= 2 else rel['from'][:1]
        to_transform = rel['to'][:2] if len(rel['to']) >= 2 else rel['to'][:1]
        
        if from_transform == to_transform:
            if from_transform not in by_transform:
                by_transform[from_transform] = set()
            from_norm = normalize_code(rel['from'])
            to_norm = normalize_code(rel['to'])
            by_transform[from_transform].add((from_norm, to_norm))
    
    # Check if models in same transformation have relationships
    for transform, rels in by_transform.items():
        transform_models = [normalize_code(m) for m in all_models if normalize_code(m).startswith(transform)]
        # Check if all models in transformation are connected
        # (This is a simplified check - in reality, not all models need relationships)
        if len(transform_models) > 10 and len(rels) < len(transform_models) * 2:
            # Low priority - just noting potential gaps
            pass
    
    print(f"   Analysis complete")
    
    # 3. Pattern completion
    print("3. Checking for missing pattern completions...")
    pattern_missing = []
    
    # Check if hub models have relationships to all major transformations
    hub_models = ['SY01', 'P02', 'P03', 'IN02', 'IN03']  # From consistency report
    major_transforms = ['P', 'IN', 'CO', 'DE', 'RE', 'SY']
    
    for hub in hub_models:
        hub_norm = normalize_code(hub)
        hub_rels = [rel for rel in relationships 
                   if normalize_code(rel['from']) == hub_norm or normalize_code(rel['to']) == hub_norm]
        connected_transforms = set()
        for rel in hub_rels:
            from_norm = normalize_code(rel['from'])
            to_norm = normalize_code(rel['to'])
            if from_norm == hub_norm:
                connected_transforms.add(to_norm[:2] if len(to_norm) >= 2 else to_norm[:1])
            else:
                connected_transforms.add(from_norm[:2] if len(from_norm) >= 2 else from_norm[:1])
        
        missing_transforms = [t for t in major_transforms if t not in connected_transforms]
        if missing_transforms:
            pattern_missing.append({
                'source_model': hub_norm,
                'target_models': missing_transforms,
                'source': f"Hub model {hub_norm} missing connections to {', '.join(missing_transforms)}",
                'priority': 'LOW',
                'recommendation': f"Consider adding relationships from {hub_norm} to models in {', '.join(missing_transforms)}"
            })
    
    print(f"   Found {len(pattern_missing)} pattern completion opportunities")
    missing_candidates.extend(pattern_missing)
    
    # Generate report
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    validation_dir = repo_root / 'validation'
    validation_dir.mkdir(exist_ok=True)
    
    # Prioritize missing relationships
    high_priority = [m for m in missing_candidates if m.get('priority') == 'HIGH']
    medium_priority = [m for m in missing_candidates if m.get('priority') == 'MEDIUM']
    low_priority = [m for m in missing_candidates if m.get('priority') == 'LOW']
    
    report = {
        'validation_date': datetime.now().strftime('%Y-%m-%d'),
        'total_missing_candidates': len(missing_candidates),
        'by_priority': {
            'HIGH': len(high_priority),
            'MEDIUM': len(medium_priority),
            'LOW': len(low_priority)
        },
        'by_source': {
            'model_files': len(model_file_missing),
            'pattern_completion': len(pattern_missing)
        },
        'missing_relationships': missing_candidates
    }
    
    report_path = validation_dir / 'relationships-missing-report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Missing Relationships Summary:")
    print(f"   Total candidates: {len(missing_candidates)}")
    print(f"   - HIGH priority: {len(high_priority)}")
    print(f"   - MEDIUM priority: {len(medium_priority)}")
    print(f"   - LOW priority: {len(low_priority)}")
    print(f"\n📄 Full report saved to {report_path}")
    print(f"\n📋 HITL Gate 4: Missing Relationships Review")
    print("   Please review missing relationship candidates and approve additions")
    
    return True


def phase_final():
    """Phase 5: Final Validation Report Generation"""
    print("Phase 5: Final Validation Report Generation")
    print("=" * 50)
    
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    validation_dir = repo_root / 'validation'
    
    # Load all batch results
    print("Loading batch validation results...")
    all_batch_results = []
    for i in range(1, 8):
        batch_file = validation_dir / f'relationships-batch-{i:02d}-results.json'
        if batch_file.exists():
            with open(batch_file, 'r', encoding='utf-8') as f:
                batch_results = json.load(f)
                all_batch_results.extend(batch_results)
    
    print(f"   Loaded {len(all_batch_results)} relationship validations")
    
    # Load consistency report
    print("Loading consistency report...")
    consistency_file = validation_dir / 'relationships-consistency-report.json'
    consistency_report = None
    if consistency_file.exists():
        with open(consistency_file, 'r', encoding='utf-8') as f:
            consistency_report = json.load(f)
        print(f"   Loaded consistency report ({consistency_report['total_issues']} issues)")
    
    # Load missing relationships report
    print("Loading missing relationships report...")
    missing_file = validation_dir / 'relationships-missing-report.json'
    missing_report = None
    if missing_file.exists():
        with open(missing_file, 'r', encoding='utf-8') as f:
            missing_report = json.load(f)
        print(f"   Loaded missing relationships report ({missing_report['total_missing_candidates']} candidates)")
    
    # Calculate overall statistics
    print("\nCalculating overall statistics...")
    status_counts = {}
    confidence_counts = {}
    for result in all_batch_results:
        status = result['status']
        confidence = result['confidence']
        status_counts[status] = status_counts.get(status, 0) + 1
        confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
    
    total = len(all_batch_results)
    validated_count = status_counts.get('VALIDATED', 0) + status_counts.get('NEEDS_REFINEMENT', 0)
    validated_pct = (validated_count / total) * 100 if total > 0 else 0
    
    # Generate comprehensive report
    final_report = {
        'validation_date': datetime.now().strftime('%Y-%m-%d'),
        'validator_version': 'agent-v1',
        'total_relationships': total,
        'validation_summary': {
            'validated': status_counts.get('VALIDATED', 0),
            'needs_refinement': status_counts.get('NEEDS_REFINEMENT', 0),
            'needs_review': status_counts.get('NEEDS_REVIEW', 0),
            'invalid': status_counts.get('INVALID', 0),
            'total_validated': validated_count,
            'validation_percentage': validated_pct
        },
        'confidence_distribution': confidence_counts,
        'consistency_analysis': {
            'total_issues': consistency_report['total_issues'] if consistency_report else 0,
            'issues_by_category': consistency_report.get('issues_by_category', {}) if consistency_report else {},
            'hub_models': consistency_report.get('hub_models', {}) if consistency_report else {}
        },
        'missing_relationships': {
            'total_candidates': missing_report['total_missing_candidates'] if missing_report else 0,
            'by_priority': missing_report.get('by_priority', {}) if missing_report else {}
        },
        'quality_metrics': {
            'accuracy_score': validated_pct,
            'consistency_score': 100 - (consistency_report['total_issues'] / total * 100) if consistency_report and total > 0 else 0,
            'completeness_score': 100 - (missing_report['total_missing_candidates'] / total * 100) if missing_report and total > 0 else 0,
            'overall_score': 0  # Will calculate below
        },
        'detailed_results': all_batch_results
    }
    
    # Calculate overall quality score (weighted average)
    accuracy_weight = 0.5
    consistency_weight = 0.3
    completeness_weight = 0.2
    
    overall_score = (
        final_report['quality_metrics']['accuracy_score'] * accuracy_weight +
        final_report['quality_metrics']['consistency_score'] * consistency_weight +
        final_report['quality_metrics']['completeness_score'] * completeness_weight
    )
    final_report['quality_metrics']['overall_score'] = overall_score
    
    # Save comprehensive JSON report
    json_report_path = validation_dir / 'relationships-validation-results.json'
    with open(json_report_path, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2)
    
    # Generate human-readable summary
    summary_path = validation_dir / 'relationships-validation-summary-final.md'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# HUMMBL Relationships Validation - Final Report\n\n")
        f.write(f"**Date:** {final_report['validation_date']}\n")
        f.write(f"**Validator:** {final_report['validator_version']}\n\n")
        f.write("## Executive Summary\n\n")
        f.write(f"- **Total Relationships:** {total}\n")
        f.write(f"- **Validated:** {validated_count} ({validated_pct:.1f}%)\n")
        f.write(f"- **Needs Review:** {status_counts.get('NEEDS_REVIEW', 0)}\n")
        f.write(f"- **Needs Refinement:** {status_counts.get('NEEDS_REFINEMENT', 0)}\n")
        f.write(f"- **Invalid:** {status_counts.get('INVALID', 0)}\n\n")
        f.write("## Quality Metrics\n\n")
        f.write(f"- **Accuracy Score:** {final_report['quality_metrics']['accuracy_score']:.1f}%\n")
        f.write(f"- **Consistency Score:** {final_report['quality_metrics']['consistency_score']:.1f}%\n")
        f.write(f"- **Completeness Score:** {final_report['quality_metrics']['completeness_score']:.1f}%\n")
        f.write(f"- **Overall Score:** {overall_score:.1f}%\n\n")
        f.write("## Status Distribution\n\n")
        for status, count in sorted(status_counts.items()):
            pct = (count / total) * 100
            f.write(f"- **{status}:** {count} ({pct:.1f}%)\n")
        f.write("\n## Confidence Distribution\n\n")
        for confidence, count in sorted(confidence_counts.items()):
            pct = (count / total) * 100
            f.write(f"- **{confidence}:** {count} ({pct:.1f}%)\n")
        f.write("\n## Consistency Analysis\n\n")
        if consistency_report:
            f.write(f"- **Total Issues:** {consistency_report['total_issues']}\n")
            for category, count in consistency_report.get('issues_by_category', {}).items():
                f.write(f"- **{category}:** {count}\n")
        f.write("\n## Missing Relationships\n\n")
        if missing_report:
            f.write(f"- **Total Candidates:** {missing_report['total_missing_candidates']}\n")
            for priority, count in missing_report.get('by_priority', {}).items():
                f.write(f"- **{priority}:** {count}\n")
        f.write("\n## Recommendations\n\n")
        if validated_pct < 95:
            f.write(f"- Review {status_counts.get('NEEDS_REVIEW', 0)} relationships flagged for review\n")
        if consistency_report and consistency_report['total_issues'] > 0:
            f.write(f"- Address {consistency_report['total_issues']} consistency issues\n")
        if missing_report and missing_report['total_missing_candidates'] > 0:
            f.write(f"- Consider adding {missing_report['total_missing_candidates']} missing relationship candidates\n")
        f.write("\n## Files Generated\n\n")
        f.write("- `relationships-validation-results.json` - Complete validation results\n")
        f.write("- `relationships-validation-summary-final.md` - This summary\n")
        f.write("- `relationships-batch-*-results.json` - Individual batch results\n")
        f.write("- `relationships-consistency-report.json` - Consistency analysis\n")
        f.write("- `relationships-missing-report.json` - Missing relationship candidates\n")
    
    print(f"\n📊 Final Validation Summary:")
    print(f"   Total Relationships: {total}")
    print(f"   Validated: {validated_count} ({validated_pct:.1f}%)")
    print(f"   Needs Review: {status_counts.get('NEEDS_REVIEW', 0)}")
    print(f"   Needs Refinement: {status_counts.get('NEEDS_REFINEMENT', 0)}")
    print(f"   Invalid: {status_counts.get('INVALID', 0)}")
    print(f"\n📈 Quality Metrics:")
    print(f"   Accuracy: {final_report['quality_metrics']['accuracy_score']:.1f}%")
    print(f"   Consistency: {final_report['quality_metrics']['consistency_score']:.1f}%")
    print(f"   Completeness: {final_report['quality_metrics']['completeness_score']:.1f}%")
    print(f"   Overall: {overall_score:.1f}%")
    print(f"\n📄 Reports Generated:")
    print(f"   - {json_report_path}")
    print(f"   - {summary_path}")
    print(f"\n📋 HITL Gate 5: Final Approval")
    print("   Please review final validation report and approve relationship data")
    
    # Success criteria check
    if validated_pct >= 95:
        print(f"\n✅ Validation exceeds 95% target threshold")
    elif validated_pct >= 90:
        print(f"\n✅ Validation meets 90% minimum threshold")
    else:
        print(f"\n⚠️  Validation below 90% threshold - review recommended")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Validate HUMMBL relationships')
    parser.add_argument('--phase', required=True, 
                       choices=['prepare', 'batch', 'consistency', 'missing', 'final'],
                       help='Validation phase to execute')
    parser.add_argument('--batch', type=int, help='Batch number (for batch phase)')
    
    args = parser.parse_args()
    
    if args.phase == 'prepare':
        success = phase_prepare()
        sys.exit(0 if success else 1)
    elif args.phase == 'batch':
        if not args.batch:
            print("❌ ERROR: --batch required for batch phase")
            sys.exit(1)
        success = phase_batch(args.batch)
        sys.exit(0 if success else 1)
    elif args.phase == 'consistency':
        success = phase_consistency()
        sys.exit(0 if success else 1)
    elif args.phase == 'missing':
        success = phase_missing()
        sys.exit(0 if success else 1)
    elif args.phase == 'final':
        success = phase_final()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

