# HUMMBL Research Tools

Tools for analyzing and processing the HUMMBL Base120 relationship graph.

## Setup

1. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

## Tools

### `relationships_to_json.py`

Converts relationships CSV to JSON format.

**Usage:**
```bash
python tools/relationships_to_json.py data/relationships.csv data/relationships.json
```

**Input:** CSV file with relationship data (header: `relation_id,from_model,to_model,relation_type,strength,direction,description`)

**Output:** JSON array of relationship objects

---

### `relationships_centrality.py`

Analyzes the relationship network using NetworkX to compute centrality metrics.

**Usage:**
```bash
python tools/relationships_centrality.py data/relationships.json
```

**Output:**
- **Node centrality**: Degree centrality for each model
- **Betweenness centrality**: Bridge/connector scores
- **PageRank**: Importance/influence scores
- **Communities**: Detected model clusters

**Top Hubs** (highest degree centrality):
- `SY01` - System Topology (0.237)
- `P02` - Multiple Perspectives (0.167)
- `P03` - Timeframe Shifting (0.132)
- `CO01` - Composition (0.132)
- `P01` - First Principles (0.114)

**Key Metrics:**
- 333 relationships across 120 models
- Average relationships per model: ~5.55
- Network density: ~0.023 (sparse, well-structured)

---

## Dependencies

- `networkx>=3.0` - Network analysis
- `numpy>=1.20.0` - Numerical operations
- `scipy>=1.7.0` - Scientific computing (for PageRank)

All dependencies listed in `../requirements.txt`.

---

### `sy19_recommend.py`

Meta-model selection tool - Recommends HUMMBL models based on problem description.

**Usage:**
```bash
# Auto-detect primaries from keywords
python tools/sy19_recommend.py "multi-service system with bottlenecks and cascades"

# Specify explicit primaries
python tools/sy19_recommend.py "problem description" --primaries DE07 DE06

# Customize output
python tools/sy19_recommend.py "problem" --top 10 --max-hops 3 --output recommendations.md
```

**Features:**
- Automatic primary model detection (keyword-based)
- Graph traversal from primaries (configurable depth)
- Centrality-weighted scoring
- Detailed reasoning for each recommendation
- Primary model boost (ensures primaries stay in top-K)

**Example Output:**
```
# SY19 Model Recommendations

**Problem:** multi-service AI feature with bottlenecks and cascades

## Recommended Models (Top 7)

1. **DE07** (score: 3.182) 🔹 Primary
   - Centrality: 17 connections
   - Why: Primary model (DE07)

2. **DE06** (score: 5.450) 🔹 Primary
   - Centrality: 16 connections
   - Why: Via P04 → DE06 (REFINES, strength=0.70)
...
```

**Algorithm:**
- Detects primary models from keywords or uses provided primaries
- Walks relationships graph from primaries (BFS with max_hops)
- Scores models using: `strength × type_weight × direction_weight × centrality_weight × hop_decay`
- Returns top-K ranked recommendations with reasons

---

## Notes

- The CSV format expects a title row that will be skipped automatically
- JSON format uses keys: `id`, `from`, `to`, `type`, `strength`, `direction`, `description`
- Relationship types: `SCAFFOLDS`, `COMPOSES_WITH`, `REFINES`, `PARALLELS`, `CONTRASTS_WITH`, `CONFLICTS`
- Strength values range from 0.0 to 1.0

