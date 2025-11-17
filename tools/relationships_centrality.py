import json
import sys
import networkx as nx

# Usage: python relationships_centrality.py data/relationships.json

def main(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        relationships = json.load(f)
    G = nx.DiGraph()
    for rel in relationships:
        G.add_edge(rel['from'], rel['to'], type=rel['type'], strength=rel['strength'], direction=rel['direction'], description=rel['description'])
    print("Node centrality:")
    print(nx.degree_centrality(G))
    print("Betweenness centrality:")
    print(nx.betweenness_centrality(G))
    print("PageRank:")
    print(nx.pagerank(G))
    print("Communities:")
    try:
        from networkx.algorithms.community import greedy_modularity_communities
        communities = list(greedy_modularity_communities(G.to_undirected()))
        print([list(c) for c in communities])
    except ImportError:
        print("Community detection requires networkx >=2.2")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python relationships_centrality.py <input_json>")
        sys.exit(1)
    main(sys.argv[1])
