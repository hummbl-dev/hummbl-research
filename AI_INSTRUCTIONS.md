# AI Assistant Instructions for HUMMBL Research Repository

**Version:** 1.0.0  
**Last Updated:** 2025-11-17  
**Purpose:** Comprehensive guide for AI assistants working with the HUMMBL research codebase

---

## Repository Overview

The HUMMBL Research repository is a **content and research portfolio** for the HUMMBL Base120 framework—a system of 120 executable mental models organized across 6 transformations that make engineering reasoning explicit, traceable, and improvable.

### Key Facts

- **120 mental models** across 6 transformations: P (Perspective), IN (Inversion), CO (Composition), DE (Decomposition), RE (Recursion), SY (Synthesis)
- **333 relationships** mapped between models
- **Status:** Phase 0 complete (all 120 models fully developed), Phase 1 in progress (case studies)
- **Repository Type:** Research/content repository (not production code)
- **Implementation:** Python code lives in separate `hummbl-prototype` repository

---

## Core Architecture

### The Four Core Concepts

All HUMMBL operators extract, manipulate, and reason about these first-class abstractions:

1. **Identity** - What makes something uniquely identifiable
   - Intrinsic properties (name, type, structure, purpose)
   - Relational properties (connections to other entities)
   - Contextual properties (role, scope, abstraction level)

2. **Time** - Temporal ordering, sequences, and evolution
   - Sequential ordering (before/after)
   - Durations, deadlines, milestones
   - Evolution patterns, temporal dependencies

3. **State** - Current condition or configuration
   - Configuration (settings, parameters, values)
   - Status (healthy, degraded, failed)
   - Data state, behavioral state, relational state

4. **Constraints** - Limitations, requirements, and boundaries
   - Hard constraints (must satisfy)
   - Soft constraints (should satisfy)
   - Resource, technical, organizational, temporal constraints

**Reference:** `docs/core-concepts.md`

### The Six Transformations

| Code | Name | Purpose | Status | Utility Score |
|------|------|---------|--------|---------------|
| **DE** | Decomposition | Break into parts | ✅ VALIDATED | 9.2/10 |
| **IN** | Inversion | Find failure modes | ⚠️ BASELINE | 3.6/10 |
| **CO** | Composition | Combine components | ⚠️ BASELINE | 6.0/10 |
| **P** | Perspective | Change analytical frame | ⚠️ BASELINE | 7.8/10 |
| **RE** | Recursion | Iterative refinement | ⚠️ BASELINE | 8.0/10 |
| **SY** | Synthesis | Meta-analysis | ⚠️ BASELINE | 8.0/10 |

**Validation Threshold:** Operators scoring ≥7.0/10 are marked **VALIDATED** for production use.

---

## Directory Structure

```
hummbl-research/
├── models/              # 120 mental models (P, IN, CO, DE, RE, SY)
│   ├── P/              # Perspective models (P01-P20)
│   ├── IN/             # Inversion models (IN01-IN20)
│   ├── CO/             # Composition models (CO01-CO20)
│   ├── DE/             # Decomposition models (DE01-DE20)
│   ├── RE/             # Recursion models (RE01-RE20)
│   └── SY/             # Synthesis models (SY01-SY20)
├── validation/         # Empirical validation studies
├── case-studies/       # Real-world applications
├── docs/               # Documentation for different audiences
├── essays/             # Thought leadership and writing
├── notebooks/          # Interactive demonstrations (Jupyter)
├── tools/              # Analysis tools (Python scripts)
├── data/               # Relationship graph data (CSV, JSON)
└── venv/               # Python virtual environment
```

---

## File Formats & Conventions

### Model Files (`models/{TRANSFORM}/{CODE}.md`)

**Format:**
```markdown
---
code: DE01
name: Root Cause Analysis
transformation: DE
status: validated
version: 0.1.0
---

# DE01 - Root Cause Analysis

> Tagline/quote

## Description
[Detailed description of the model]

## Example
[Concrete example]

## Related Models
- [Model codes and brief descriptions]
```

**Key Fields:**
- `code`: Unique identifier (e.g., DE01, SY19)
- `name`: Human-readable name
- `transformation`: One of P, IN, CO, DE, RE, SY
- `status`: `validated`, `baseline`, `prototype`, `draft`
- `version`: Semantic version (e.g., 0.1.0)

**Naming Convention:**
- Files: `{CODE}.md` (e.g., `DE01.md`, `SY19.md`)
- Directories: `{TRANSFORM}/` (e.g., `DE/`, `SY/`)

### Validation Studies (`validation/{study-name}-{year}.md`)

**Template:** `validation/validation-template.md`

**Required Sections:**
1. Objective
2. Hypotheses
3. Methods (Design, Participants, Measures)
4. Procedure
5. Analysis Plan
6. Results
7. Threats to Validity
8. Conclusions

**Naming:** `{operator-name}-study-{year}.md` (e.g., `decomposition-study-2025.md`)

### Case Studies (`case-studies/{name}.md`)

**Template:** `case-studies/templates/case-study-template.md`

**Required Sections:**
1. Context
2. Challenge
3. HUMMBL Application
4. Results (time saved, completeness, quality score)
5. Outcome

### Documentation (`docs/{topic}.md`)

**Key Documents:**
- `core-concepts.md` - The four core concepts (Identity, Time, State, Constraints)
- `engineering-workflows.md` - How to use HUMMBL in practice
- `for-engineers.md` - Engineer-focused guide
- `for-teams.md` - Team adoption guide
- `production-readiness-roadmap.md` - Production deployment plan

---

## Working with Models

### Reading Models

1. **By Transformation:** Navigate to `models/{TRANSFORM}/`
2. **By Code:** Use `models/{TRANSFORM}/{CODE}.md`
3. **All Models:** Each transformation has 20 models (01-20)

### Understanding Relationships

- **Data Source:** `data/relationships.json` (333 relationships)
- **Analysis Tool:** `tools/relationships_centrality.py`
- **Relationship Types:**
  - `SCAFFOLDS` - One model builds on another
  - `COMPOSES_WITH` - Models work together
  - `REFINES` - One model refines another
  - `PARALLELS` - Similar approaches
  - `CONTRASTS_WITH` - Different perspectives
  - `CONFLICTS` - Conflicting approaches

### Model Status Values

- **validated** - Production-ready, utility score ≥7.0/10
- **baseline** - Functional but needs refinement, utility score <7.0/10
- **prototype** - Experimental implementation
- **draft** - Incomplete or preliminary

---

## Tools & Scripts

### Available Tools (`tools/`)

1. **`relationships_to_json.py`**
   - Converts CSV relationships to JSON
   - Usage: `python tools/relationships_to_json.py data/relationships.csv data/relationships.json`

2. **`relationships_centrality.py`**
   - Analyzes relationship network (NetworkX)
   - Computes: degree centrality, betweenness, PageRank, communities
   - Usage: `python tools/relationships_centrality.py data/relationships.json`

3. **`sy19_recommend.py`**
   - Meta-model selection tool
   - Recommends models based on problem description
   - Usage: `python tools/sy19_recommend.py "problem description" [--primaries CODE CODE]`

### Setup

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Common Tasks

### Task 1: Add a New Model

1. **Create file:** `models/{TRANSFORM}/{CODE}.md`
2. **Add frontmatter:**
   ```yaml
   ---
   code: {CODE}
   name: {Name}
   transformation: {TRANSFORM}
   status: draft
   version: 0.1.0
   ---
   ```
3. **Fill sections:** Description, Example, Related Models
4. **Update relationships:** Add to `data/relationships.csv` if needed

### Task 2: Update Model Status

1. **Edit frontmatter:** Change `status` field
2. **Update README.md:** Update operator status table if validated
3. **Create validation study:** If moving to validated, create study in `validation/`

### Task 3: Create Validation Study

1. **Copy template:** `validation/validation-template.md`
2. **Rename:** `{operator-name}-study-{year}.md`
3. **Fill sections:** Follow template structure
4. **Update README.md:** Add to validation studies table

### Task 4: Write Case Study

1. **Copy template:** `case-studies/templates/case-study-template.md`
2. **Fill sections:** Context, Challenge, Application, Results, Outcome
3. **Include metrics:** Time saved, completeness improvement, quality score
4. **Link from README.md:** Add to case studies section

### Task 5: Analyze Relationships

```bash
# Convert CSV to JSON (if needed)
python tools/relationships_to_json.py data/relationships.csv data/relationships.json

# Analyze centrality
python tools/relationships_centrality.py data/relationships.json

# Get model recommendations
python tools/sy19_recommend.py "your problem description"
```

---

## Codebase Rules & Constraints

### DO

✅ **Use Markdown** for all content (models, docs, case studies, essays)  
✅ **Follow naming conventions** (e.g., `DE01.md`, `decomposition-study-2025.md`)  
✅ **Include frontmatter** in model files  
✅ **Reference core concepts** (Identity, Time, State, Constraints) when relevant  
✅ **Link related models** in model files  
✅ **Update README.md** when adding validated operators or case studies  
✅ **Use semantic versioning** (0.1.0, 0.2.0, etc.) for models  
✅ **Keep Python tools simple** - this is a research repo, not production code  

### DON'T

❌ **Don't add production code** - Python implementation lives in `hummbl-prototype` repo  
❌ **Don't modify relationships.json directly** - Edit CSV, then convert  
❌ **Don't skip validation studies** - Required for validated status  
❌ **Don't create models without frontmatter**  
❌ **Don't use inconsistent naming** - Follow existing patterns  
❌ **Don't break existing relationships** - Check impact before removing models  

---

## Understanding Context

### Current Phase: Phase 1 (Case Studies & Intelligence)

**Completed:**
- ✅ Phase 0: All 120 models fully developed (November 16, 2025)
- ✅ 333 relationships classified
- ✅ DE operator validated (9.2/10)
- ✅ SY19 prototype implemented

**In Progress:**
- 🔄 Case Study 1: Multi-service AI system (Target: Jan 2026)
- 🔄 Case Study 2: Fitness transformation (Target: Dec 2025)
- 🔄 Case Study 3: Ozzy health protocol (Target: Dec 2025)

**Next Steps:**
- Operator refinements (IN, CO improvements)
- Enhanced UX development
- Commercial deployment preparation (Q1 2026)

### Key Documents to Reference

- **README.md** - Project overview, status, roadmap
- **docs/core-concepts.md** - The four core concepts
- **docs/engineering-workflows.md** - Practical usage patterns
- **CONTRIBUTING.md** - Contribution guidelines
- **validation/** - Validation methodology and results

---

## AI Assistant Guidelines

### When Editing Models

1. **Preserve frontmatter structure** - Don't change YAML format
2. **Maintain consistency** - Follow existing model patterns
3. **Update related models** - If adding relationships, update both models
4. **Check relationships** - Verify relationship data if model changes significantly

### When Creating Documentation

1. **Reference core concepts** - Always connect to Identity, Time, State, Constraints
2. **Include examples** - Concrete examples are essential
3. **Link to models** - Use model codes (e.g., DE01, SY19)
4. **Follow existing style** - Match tone and structure of existing docs

### When Analyzing Code

1. **Remember this is research** - Code is for analysis, not production
2. **Check tools/README.md** - Tool documentation exists
3. **Python code is separate** - Production code in `hummbl-prototype` repo
4. **Focus on content** - This repo is primarily Markdown content

### When Answering Questions

1. **Reference specific models** - Use codes (DE01, SY19, etc.)
2. **Cite core concepts** - Connect to Identity, Time, State, Constraints
3. **Link to documentation** - Point to relevant docs/ files
4. **Check validation status** - Note if operator is validated or baseline

---

## Quick Reference

### Model Codes by Transformation

- **P (Perspective):** P01-P20
- **IN (Inversion):** IN01-IN20
- **CO (Composition):** CO01-CO20
- **DE (Decomposition):** DE01-DE20
- **RE (Recursion):** RE01-RE20
- **SY (Synthesis):** SY01-SY20

### Key Model Examples

- **DE01** - Root Cause Analysis (validated)
- **SY19** - Meta-Model Selection (prototype)
- **DE07** - Bottleneck Identification
- **DE06** - Failure Mode Analysis
- **SY01** - System Topology (highest centrality: 0.237)

### File Paths

- Models: `models/{TRANSFORM}/{CODE}.md`
- Validation: `validation/{operator}-study-{year}.md`
- Case Studies: `case-studies/{name}.md`
- Relationships: `data/relationships.json` or `data/relationships.csv`
- Tools: `tools/{script}.py`

---

## Troubleshooting

### Issue: Model not found
- **Check:** File exists at `models/{TRANSFORM}/{CODE}.md`
- **Verify:** Code format is correct (e.g., DE01, not DE1)

### Issue: Relationship analysis fails
- **Check:** `data/relationships.json` exists and is valid JSON
- **Convert:** Run `relationships_to_json.py` if only CSV exists

### Issue: Tool import errors
- **Check:** Virtual environment is activated
- **Install:** Run `pip install -r requirements.txt`
- **Verify:** Dependencies in `requirements.txt` are installed

### Issue: Inconsistent model format
- **Check:** Frontmatter matches template
- **Reference:** Existing validated models (e.g., DE01.md)
- **Verify:** All required fields present

---

## Additional Resources

- **GitHub:** https://github.com/hummbl-dev/hummbl-research
- **Website:** hummbl.io
- **Author:** Reuben Bowlby (@ReubenBowlby)
- **License:** Content (CC BY 4.0), Code (MIT)

---

**Last Updated:** 2025-11-17  
**Version:** 1.0.0  
**Status:** Active Development

