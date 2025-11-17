#!/usr/bin/env python3
"""
SY19 - Meta-Model Selection Recommender

Takes a problem description and recommends a sequence of HUMMBL models
based on the relationships graph and centrality analysis.

Usage:
    python tools/sy19_recommend.py "multi-service AI feature with bottlenecks and cascades" --primaries DE07 DE06
    python tools/sy19_recommend.py "API design for distributed system" --top 10
"""

import json
import sys
import argparse
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import re


class SY19Recommender:
    """SY19 Meta-Model Selection - Recommends models based on problem description."""
    
    # Relationship type weights (from SITREP-5)
    TYPE_WEIGHTS = {
        'SCAFFOLDS': 1.0,
        'COMPOSES_WITH': 0.9,
        'REFINES': 0.8,
        'PARALLELS': 0.5,
        'CONTRASTS_WITH': 0.4,
        'CONFLICTS': 0.3,
    }
    
    # Direction weights (bidirectional edges can be traversed both ways)
    DIRECTION_WEIGHTS = {
        'unidirectional': 1.0,
        'bidirectional': 1.0,  # Can traverse both ways
    }
    
    # Hop decay factor (reduces score for models further away)
    HOP_DECAY = 0.7  # Each hop reduces score by 30%
    
    # Centrality weight coefficient
    ALPHA = 0.3
    
    # Primary model boost (ensures primaries stay in top-K)
    PRIMARY_BOOST = 0.2
    
    def __init__(self, relationships_json: str, centrality_data: Optional[Dict] = None):
        """
        Initialize recommender with relationships graph.
        
        Args:
            relationships_json: Path to relationships.json file
            centrality_data: Optional pre-computed centrality data (dict mapping model -> degree)
        """
        with open(relationships_json, 'r', encoding='utf-8') as f:
            self.relationships = json.load(f)
        
        # Build graph structures
        self.graph = defaultdict(list)  # model -> [(target, relationship_data), ...]
        self.reverse_graph = defaultdict(list)  # target -> [(source, relationship_data), ...]
        self.all_models = set()
        
        for rel in self.relationships:
            from_model = rel['from']
            to_model = rel['to']
            self.all_models.add(from_model)
            self.all_models.add(to_model)
            
            # Store relationship with metadata
            rel_data = {
                'type': rel['type'],
                'strength': rel['strength'],
                'direction': rel['direction'],
                'description': rel.get('description', '')
            }
            
            self.graph[from_model].append((to_model, rel_data))
            self.reverse_graph[to_model].append((from_model, rel_data))
            
            # Add reverse edge for bidirectional relationships
            if rel['direction'] == 'bidirectional':
                self.graph[to_model].append((from_model, rel_data))
                self.reverse_graph[from_model].append((to_model, rel_data))
        
        # Compute centrality if not provided
        if centrality_data:
            self.centrality = centrality_data
        else:
            self.centrality = self._compute_degree_centrality()
        
        # Normalize centrality for weighting
        max_degree = max(self.centrality.values()) if self.centrality.values() else 1.0
        self.normalized_centrality = {
            model: deg / max_degree if max_degree > 0 else 0.0
            for model, deg in self.centrality.items()
        }
    
    def _compute_degree_centrality(self) -> Dict[str, int]:
        """Compute degree centrality for each model."""
        centrality = {}
        for model in self.all_models:
            # Total degree (in + out)
            out_degree = len(self.graph.get(model, []))
            in_degree = len(self.reverse_graph.get(model, []))
            centrality[model] = out_degree + in_degree
        return centrality
    
    def _detect_primaries_from_text(self, problem_text: str) -> List[str]:
        """
        Detect primary models from problem text using keyword matching.
        
        This is a simple implementation. Could be enhanced with NLP in the future.
        """
        problem_lower = problem_text.lower()
        primaries = []
        
        # Keyword mappings (basic - could be expanded)
        keyword_map = {
            # Bottleneck/failure related
            'bottleneck': ['DE07'],
            'failure': ['DE06', 'IN02'],
            'error': ['DE06'],
            'breakdown': ['DE06'],
            
            # System/composition related
            'system': ['SY01'],
            'architecture': ['CO01', 'CO09'],
            'service': ['CO09'],
            'microservice': ['CO09'],
            'composition': ['CO01'],
            'integration': ['CO05'],
            
            # Pipeline/flow related
            'pipeline': ['CO03'],
            'flow': ['CO03', 'DE08'],
            'queue': ['CO12'],
            'buffer': ['CO12'],
            
            # Cascade/effect related
            'cascade': ['SY04'],
            'effect': ['SY04', 'P09'],
            'second-order': ['SY04', 'IN06'],
            
            # Feedback/recursion related
            'feedback': ['RE06'],
            'loop': ['RE06'],
            'iteration': ['RE09', 'RE03'],
            
            # Perspective related
            'perspective': ['P02'],
            'stakeholder': ['P02'],
            'viewpoint': ['P02', 'P03'],
            
            # Inversion related
            'inversion': ['IN01'],
            'invert': ['IN01'],
            'premortem': ['IN02'],
            
            # Decomposition related
            'decompose': ['DE01'],
            'break down': ['DE01'],
            'component': ['DE02'],
        }
        
        for keyword, models in keyword_map.items():
            if keyword in problem_lower:
                primaries.extend(models)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_primaries = []
        for model in primaries:
            if model not in seen:
                seen.add(model)
                unique_primaries.append(model)
        
        return unique_primaries[:3]  # Top 3 detected primaries
    
    def recommend_models(
        self,
        problem_text: str,
        primaries: Optional[List[str]] = None,
        top_k: int = 7,
        max_hops: int = 2
    ) -> List[Dict]:
        """
        Recommend models based on problem description.
        
        Args:
            problem_text: Natural language problem description
            primaries: Optional explicit list of primary models (overrides detection)
            top_k: Number of models to return
            max_hops: Maximum graph distance to traverse from primaries
            
        Returns:
            List of recommended models with scores and reasons
        """
        # Detect or use provided primaries
        if primaries is None:
            primaries = self._detect_primaries_from_text(problem_text)
        
        if not primaries:
            # Fallback: use top hub models as primaries
            sorted_centrality = sorted(
                self.centrality.items(),
                key=lambda x: x[1],
                reverse=True
            )
            primaries = [model for model, _ in sorted_centrality[:2]]
        
        # Score all models by walking from primaries
        model_scores = defaultdict(float)
        model_reasons = defaultdict(list)  # Track why each model was recommended
        
        for primary in primaries:
            if primary not in self.all_models:
                continue
            
            # Give primary a boost (ensures it stays in top-K)
            model_scores[primary] += self.PRIMARY_BOOST
            model_reasons[primary].append(f"Primary model ({primary})")
            
            # Also score primary from its own outgoing relationships (self-recommendation)
            for target, rel_data in self.graph.get(primary, []):
                # Score the primary itself from its relationships (for centrality)
                type_weight = self.TYPE_WEIGHTS.get(rel_data['type'], 0.5)
                strength = rel_data['strength']
                direction_weight = self.DIRECTION_WEIGHTS.get(rel_data['direction'], 1.0)
                centrality_weight = 1.0 + self.ALPHA * self.normalized_centrality.get(primary, 0.0)
                
                # Primary gets a base score from its relationships (reduced since it's hop 0)
                base_score = strength * type_weight * direction_weight * centrality_weight * 0.5
                model_scores[primary] += base_score
            
            # BFS from primary
            queue = [(primary, 0, [primary])]  # (current_model, hop, path)
            visited = {primary}
            
            while queue:
                current_model, hop, path = queue.pop(0)
                
                if hop >= max_hops:
                    continue
                
                # Consider outgoing relationships
                for target, rel_data in self.graph.get(current_model, []):
                    if target in visited:
                        continue
                    
                    # Calculate edge score
                    type_weight = self.TYPE_WEIGHTS.get(rel_data['type'], 0.5)
                    strength = rel_data['strength']
                    direction_weight = self.DIRECTION_WEIGHTS.get(rel_data['direction'], 1.0)
                    centrality_weight = 1.0 + self.ALPHA * self.normalized_centrality.get(target, 0.0)
                    hop_decay = self.HOP_DECAY ** hop
                    
                    edge_score = strength * type_weight * direction_weight * centrality_weight * hop_decay
                    
                    # Add to target model score
                    model_scores[target] += edge_score
                    model_reasons[target].append(
                        f"Via {current_model} → {target} ({rel_data['type']}, strength={strength:.2f})"
                    )
                    
                    # Add to queue for next hop
                    if hop + 1 < max_hops:
                        queue.append((target, hop + 1, path + [target]))
                        visited.add(target)
        
        # Ensure all primaries are included (even if score is 0)
        for primary in primaries:
            if primary in self.all_models and primary not in model_scores:
                model_scores[primary] = self.PRIMARY_BOOST
                model_reasons[primary] = [f"Primary model ({primary})"]
        
        # Sort by score and return top-K
        scored_models = [
            {
                'model': model,
                'score': score,
                'reasons': model_reasons[model][:3] if model_reasons[model] else ["Direct recommendation"],
                'centrality': self.centrality.get(model, 0),
                'is_primary': model in primaries
            }
            for model, score in model_scores.items()
        ]
        
        # Sort by score (descending), but prioritize primaries
        def sort_key(x):
            # Primaries get priority in sorting
            if x['is_primary']:
                return (1, x['score'])
            return (0, x['score'])
        
        scored_models.sort(key=sort_key, reverse=True)
        
        # Return top-K, but ensure all primaries are included
        result = scored_models[:top_k]
        primary_models = [m for m in scored_models if m['is_primary']]
        
        # Ensure primaries are in result
        for primary in primary_models:
            if primary not in result:
                result.append(primary)
                result = result[:top_k]  # Re-trim if needed
        
        # Re-sort final result
        result.sort(key=sort_key, reverse=True)
        
        return result[:top_k]
    
    def format_recommendations(self, recommendations: List[Dict], problem_text: str) -> str:
        """Format recommendations as readable text."""
        lines = [
            f"# SY19 Model Recommendations",
            f"",
            f"**Problem:** {problem_text}",
            f"",
            f"## Recommended Models (Top {len(recommendations)})",
            f"",
        ]
        
        for i, rec in enumerate(recommendations, 1):
            primary_tag = " 🔹 Primary" if rec['is_primary'] else ""
            lines.append(f"{i}. **{rec['model']}** (score: {rec['score']:.3f}){primary_tag}")
            lines.append(f"   - Centrality: {rec['centrality']} connections")
            if rec['reasons']:
                lines.append(f"   - Why: {rec['reasons'][0]}")
            lines.append("")
        
        return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SY19 Meta-Model Selection - Recommend HUMMBL models for a problem"
    )
    parser.add_argument(
        "problem",
        help="Problem description in natural language"
    )
    parser.add_argument(
        "--primaries", "-p",
        nargs="+",
        help="Explicit primary models (e.g., DE07 DE06). If not provided, detected from text."
    )
    parser.add_argument(
        "--top", "-k",
        type=int,
        default=7,
        help="Number of recommendations to return (default: 7)"
    )
    parser.add_argument(
        "--relationships", "-r",
        default="data/relationships.json",
        help="Path to relationships.json file (default: data/relationships.json)"
    )
    parser.add_argument(
        "--max-hops",
        type=int,
        default=2,
        help="Maximum graph distance from primaries (default: 2)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for formatted recommendations (default: stdout)"
    )
    
    args = parser.parse_args()
    
    try:
        # Create recommender
        recommender = SY19Recommender(args.relationships)
        
        # Get recommendations
        recommendations = recommender.recommend_models(
            problem_text=args.problem,
            primaries=args.primaries,
            top_k=args.top,
            max_hops=args.max_hops
        )
        
        # Format output
        output = recommender.format_recommendations(recommendations, args.problem)
        
        # Write or print
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✓ Recommendations written to: {args.output}")
        else:
            print(output)
        
        # Print detected primaries if auto-detected
        if args.primaries is None:
            detected = recommender._detect_primaries_from_text(args.problem)
            if detected:
                print(f"\n📌 Auto-detected primaries: {', '.join(detected)}")
        
    except FileNotFoundError:
        print(f"Error: Could not find relationships file: {args.relationships}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in relationships file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

