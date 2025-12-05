#!/usr/bin/env python3
"""
Visualize HUMMBL relationship graph.

Creates interactive HTML visualization of the relationship network.

Usage:
    python tools/visualize_relationships.py
    python tools/visualize_relationships.py --output graph.html --layout spring
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set

try:
    import networkx as nx
    from pyvis.network import Network
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip install networkx pyvis")
    sys.exit(1)


def load_relationships(json_path: str) -> List[Dict]:
    """Load relationships from JSON."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def normalize_code(code: str) -> str:
    """Normalize model code (IN8 -> IN08)."""
    import re
    match = re.match(r'([A-Z]{1,2})(\d{1,2})', code)
    if match:
        transform, number = match.groups()
        return f"{transform}{number.zfill(2)}"
    return code


def build_graph(relationships: List[Dict]) -> nx.DiGraph:
    """Build NetworkX graph from relationships."""
    G = nx.DiGraph()
    
    for rel in relationships:
        from_model = normalize_code(rel['from'])
        to_model = normalize_code(rel['to'])
        
        G.add_edge(
            from_model,
            to_model,
            type=rel['type'],
            strength=rel['strength'],
            direction=rel['direction'],
            description=rel.get('description', '')
        )
        
        # Add reverse edge for bidirectional
        if rel['direction'] == 'bidirectional':
            G.add_edge(
                to_model,
                from_model,
                type=rel['type'],
                strength=rel['strength'],
                direction=rel['direction'],
                description=rel.get('description', '')
            )
    
    return G


def get_transformation(model_code: str) -> str:
    """Extract transformation from model code."""
    if len(model_code) >= 2:
        return model_code[:2] if model_code[1].isdigit() else model_code[0]
    return model_code[0] if model_code else '?'


def get_transformation_color(transform: str) -> str:
    """Get color for transformation."""
    colors = {
        'P': '#FF6B6B',   # Red - Perspective
        'IN': '#4ECDC4',   # Teal - Inversion
        'CO': '#45B7D1',   # Blue - Composition
        'DE': '#FFA07A',   # Light Salmon - Decomposition
        'RE': '#98D8C8',   # Mint - Recursion
        'SY': '#F7DC6F',   # Yellow - Synthesis
    }
    return colors.get(transform, '#CCCCCC')


def compute_centrality(G: nx.DiGraph) -> Dict[str, float]:
    """Compute degree centrality."""
    centrality = {}
    for node in G.nodes():
        centrality[node] = G.degree(node)
    return centrality


def create_visualization(
    relationships: List[Dict],
    output_file: str = 'validation/relationships-graph.html',
    layout: str = 'spring',
    height: str = '800px',
    width: str = '100%'
):
    """Create interactive HTML visualization."""
    # Build graph
    G = build_graph(relationships)
    centrality = compute_centrality(G)
    
    # Create pyvis network
    net = Network(
        height=height,
        width=width,
        directed=True,
        bgcolor='#222222',
        font_color='white'
    )
    
    # Set physics options
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -2000,
          "centralGravity": 0.1,
          "springLength": 200,
          "springConstant": 0.04,
          "damping": 0.09
        }
      },
      "nodes": {
        "font": {
          "size": 14,
          "color": "white"
        },
        "borderWidth": 2
      },
      "edges": {
        "arrows": {
          "to": {
            "enabled": true,
            "scaleFactor": 0.5
          }
        },
        "color": {
          "inherit": true
        },
        "smooth": {
          "type": "continuous"
        }
      }
    }
    """)
    
    # Add nodes
    max_centrality = max(centrality.values()) if centrality.values() else 1.0
    
    for node in G.nodes():
        transform = get_transformation(node)
        color = get_transformation_color(transform)
        size = 10 + (centrality[node] / max_centrality) * 30  # Scale by centrality
        
        # Node title (tooltip)
        title = f"{node}\nTransformation: {transform}\nConnections: {centrality[node]}"
        
        net.add_node(
            node,
            label=node,
            color=color,
            size=size,
            title=title,
            font={'size': 12, 'color': 'white'}
        )
    
    # Add edges
    edge_types = {
        'SCAFFOLDS': {'color': '#FFD700', 'width': 3},
        'COMPOSES_WITH': {'color': '#00CED1', 'width': 2},
        'REFINES': {'color': '#FF69B4', 'width': 2},
        'PARALLELS': {'color': '#90EE90', 'width': 1.5},
        'CONTRASTS_WITH': {'color': '#FFA500', 'width': 1.5},
        'CONFLICTS': {'color': '#FF6347', 'width': 1.5},
    }
    
    for edge in G.edges(data=True):
        from_node, to_node, data = edge
        rel_type = data['type']
        strength = data['strength']
        
        edge_config = edge_types.get(rel_type, {'color': '#CCCCCC', 'width': 1})
        
        # Width based on strength
        width = edge_config['width'] * strength
        
        net.add_edge(
            from_node,
            to_node,
            title=f"{rel_type} (strength: {strength:.2f})",
            color=edge_config['color'],
            width=width,
            arrows={'to': {'enabled': True}}
        )
    
    # Save
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    net.save_graph(str(output_path))
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Visualize HUMMBL relationship graph"
    )
    parser.add_argument(
        '--relationships', '-r',
        default='data/relationships.json',
        help='Path to relationships.json (default: data/relationships.json)'
    )
    parser.add_argument(
        '--output', '-o',
        default='validation/relationships-graph.html',
        help='Output HTML file (default: validation/relationships-graph.html)'
    )
    parser.add_argument(
        '--layout',
        choices=['spring', 'hierarchical'],
        default='spring',
        help='Layout algorithm (default: spring)'
    )
    parser.add_argument(
        '--height',
        default='800px',
        help='Canvas height (default: 800px)'
    )
    parser.add_argument(
        '--width',
        default='100%',
        help='Canvas width (default: 100%)'
    )
    
    args = parser.parse_args()
    
    try:
        print(f"Loading relationships from {args.relationships}...")
        relationships = load_relationships(args.relationships)
        print(f"✅ Loaded {len(relationships)} relationships")
        
        print(f"Creating visualization...")
        output_path = create_visualization(
            relationships,
            output_file=args.output,
            layout=args.layout,
            height=args.height,
            width=args.width
        )
        
        print(f"✅ Visualization saved to: {output_path}")
        print(f"   Open in browser to explore the graph interactively")
        
    except FileNotFoundError:
        print(f"Error: Could not find {args.relationships}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

