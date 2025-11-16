---
title: "HUMMBL Relationships Graph Study 2025"
date: 2025-11-17
version: 1.0.0
status: Completed
researcher: Reuben Bowlby
---

# HUMMBL Relationships Graph Study (Base120, 2025)

## 1. Executive Summary

This study documents the **relationship graph** for **HUMMBL Base120**:

- **Models:** 120 mental models across 6 transformations (P, IN, CO, DE, RE, SY)  
- **Relationships:** 333 directed edges between models  
- **Goal:** Provide a **structured relationship graph** that:

  - Powers **SY19 – Meta-Model Selection** (model recommender)  
  - Guides **case study model sequences**  
  - Supports future UX (graph visualization, tooltips, suggestions)

Each relationship encodes:

- A **relation type** from a canonical taxonomy  
- A **strength** (0.0–1.0) reflecting frequency/importance  
- A **direction** (unidirectional or bidirectional)  
- A short **note** explaining the rationale

The resulting graph has an average effective strength around **0.75**, with strong coverage across transformations. It is a **v1.0 baseline** that will be refined by real-world usage and case studies.

---

## 2. Schema & Taxonomy

### 2.1 Data Schema

Relationships are stored in a tabular form (Google Sheets) and exported to JSON.

**Columns / Fields:**

- `id` – Relationship identifier (`REL-001` … `REL-333`)  
- `source_model` – Model code such as `DE01`, `IN02`, `CO05`, `P03`, `RE09`, `SY01`  
- `target_model` – Model code in the same format  
- `relation_type` – One of the canonical relationship types (see below)  
- `strength` – Float in `[0.0, 1.0]` expressing relationship strength  
- `direction` – `unidirectional` or `bidirectional`  
- `notes` – 1–2 line human-readable rationale  
- `status` – `done` (Phase 0), future: `needs_review`, `archived`  
- `validated_by` – Date string (`YYYY-MM-DD`) when relationship was last validated  
- `batch_id` – Batch marker used during Phase 0 sprint (`BATCH-01` … `BATCH-25`)

### 2.2 Canonical Relationship Types

The taxonomy contains **six primary relationship types**:

- **SCAFFOLDS**  
  - A is a **prerequisite** or foundation for B.  
  - Example: `DE02 → CO05` – Component identification scaffolds integration patterns.

- **COMPOSES_WITH**  
  - A and B are often used **in sequence or joint operation**.  
  - Example: `DE01 → CO01` – Decompose, then compose.

- **REFINES**  
  - B **improves, deepens, or clarifies** the output of A.  
  - Example: `P01 → DE01` – First principles thinking refines root cause analysis.

- **PARALLELS**  
  - A and B operate in **similar domains** with alternative or complementary methods; no strict order.  
  - Example: `P05 ↔ IN05` – Two ways of reasoning about opportunity cost.

- **CONTRASTS_WITH**  
  - A and B are **conceptual opposites or duals** that are often used together to frame tradeoffs.  
  - Example: `IN04 ↔ DE09` – Simplification vs complexity quantification.

- **CONFLICTS**  
  - A and B represent **genuine tension or tradeoff**; improving one often makes the other harder.  
  - Example: `CO01 ↔ IN04` – Composition increases complexity while simplification tries to reduce it.

### 2.3 Strength Scale

Strength is a float `0.0–1.0`, interpreted qualitatively as:

- **0.8–1.0 – HIGH:**  
  - Essential relationship, used together in the majority of relevant workflows.

- **0.5–0.7 – MEDIUM:**  
  - Often useful, but context-dependent.

- **0.2–0.4 – LOW:**  
  - Niche, rare, or only useful in specific edge cases.

- **0.0–0.1 – NEGLIGIBLE:**  
  - No meaningful relationship; mostly unused in Phase 0 (these edges are not present).

---

## 3. Construction Process

### 3.1 Sources

The graph is constructed from:

1. An original set of ~**138 manually classified relationships** (`rel_001–rel_138`) stored in JSON.  
2. A structured **Phase 0 sprint** that added the remaining relationships in a single canonical schema.

### 3.2 Phase 0 Sprint Workflow

**Workspace:** Google Sheet named `HUMMBL-Relationships-Phase0`.

**Process:**

- Defined the schema and taxonomy above.  
- Processed models in **batches** (10–20 relationships per batch).  
- Each batch focused on one or more transformations, for example:
  - `BATCH-15` – `DE01–DE05`  
  - `BATCH-16` – `DE06–DE10`  
  - `BATCH-17` – `IN01–IN05`  
  - … up to `BATCH-25` – final SY and cross-bridge relationships.
- For each source model:
  - Identified **3–5 strongest relationships** to other models (especially across transformations).  
  - Chose `relation_type`, `strength`, `direction`, and wrote a **1–2 line note**.  
  - Marked `status = done`, added `validated_by` and `batch_id`.

Total sprint time for completing the remaining 195 relationships was on the order of **~45–60 minutes** once the pattern was stable.

---

## 4. Statistics & Patterns

> Note: Numbers here are approximate descriptions; the true values can be obtained directly from the sheet.

### 4.1 Relation Type Distribution

Out of 333 relationships:

- **COMPOSES_WITH:** ~40%  
- **SCAFFOLDS:** ~19%  
- **REFINES:** ~20%  
- **PARALLELS:** ~10%  
- **CONTRASTS_WITH:** ~9%  
- **CONFLICTS:** ~7%

This reflects the design intent:

- Composition and scaffolding relationships form the **backbone** of recommended model sequences.  
- Refinements and parallels add nuance and alternative approaches.  
- Contrasts and conflicts highlight **tradeoffs** and opposing moves.

### 4.2 Strength Distribution

- **HIGH (≥0.8):** ~43% of edges  
- **MED (0.5–0.7):** ~56% of edges  
- **LOW (≤0.4):** ~1% of edges

The graph is intentionally biased toward **strong, actionable associations**, with only a small tail of weaker links for completeness.

### 4.3 Cross-Transformation Highlights

A few notable patterns:

- **DE ↔ CO (Decomposition & Composition):**  
  - Many `SCAFFOLDS` and `COMPOSES_WITH` relations.  
  - Decompose → identify components → design integration → orchestrate services.

- **DE ↔ SY (Decomposition & Meta-Systems):**  
  - Decomposition outputs (components, dependencies, constraints) **feed system-level analysis** (`SY01`, `SY03`, `SY04`).

- **IN ↔ DE/CO (Inversion & Decomposition/Composition):**  
  - Mix of `CONTRASTS_WITH` and `CONFLICTS`.  
  - Inversion often pushes against naive composition, revealing constraints and failure modes.

- **P ↔ SY/DE/CO (Perspective & Systems/Structure):**  
  - Perspective operators scaffold system mapping and decomposition.  
  - Multi-perspective analysis improves component boundaries and integration designs.

- **RE ↔ SY/DE/CO (Recursion & Systems/Structure):**  
  - Recursion models (feedback loops, compounding cycles, iterative prototyping) sit at the **dynamic layer**.  
  - They compose with system topology (`SY01`), cascades (`SY04`), and composition patterns (`CO01–CO13`).

---

## 5. Applications

### 5.1 SY19 Meta-Model Selection

The relationship graph is a key input to **SY19 – Meta-Model Selection**.

High-level algorithm:

1. **Detect primary models** from a problem description (keywords, context).  
2. **Walk the graph** from those primaries:
   - Prioritize `SCAFFOLDS`, `COMPOSES_WITH`, and `REFINES` edges.  
   - Weight by `strength`, relation type, direction, and hop distance.
3. **Aggregate scores** and return a ranked list of model recommendations:
   - 1–2 primary models  
   - 3–5 supporting models  
4. Provide **reasons** using `notes` and relation metadata.

Example:

> "API is slow and unreliable under load"  
> Primary detection: `DE07` (bottleneck identification), `DE06` (failure modes).  
> Graph lookup suggests: `CO03` (pipeline), `CO12` (queues), `SY02` (risk), `SY04` (cascades), `RE10` (experimentation).

### 5.2 Case Study Model Sequences

For each case study:

- Start from the specific use case and desired outcome.  
- Choose 1–2 primary models (usually DE/P/IN).  
- Use the relationship graph to:
  - Select **scaffolds** to run **first**.  
  - Add **composes_with** models as the main pipeline.  
  - Plug in **refines** models for depth.  
  - Use **contrasts/conflicts** to expose tradeoffs and tensions.

This ensures that each case study showcases **coherent model sequences** grounded in the same relationship graph that SY19 will later use.

### 5.3 Product & Tooling

Potential UX integrations:

- **Model detail view:**  
  - Show "Strongly Related Models" categorized by relation type (scaffolds, composition, refinements, contrasts, conflicts).

- **Interactive flows:**  
  - While a user is working through DE01, suggest:  
    - "Next: CO05 – Integration Patterns (SCAFFOLDS, 0.9)"  
    - "Alternative: IN02 – Premortem (COMPOSES_WITH, 0.8)"

- **Graph visualization:**  
  - Nodes = models, edges = relationships (color by type, thickness by strength).

---

## 6. Limitations & Future Work

This relationship graph is **v1.0** and reflects:

- The designer’s best judgment and pattern recognition during Phase 0.  
- Limited but carefully considered manual examples and mental simulations.

Limitations:

- Some relation types (especially `PARALLELS`) may be **underused** relative to their theoretical potential.  
- Strength values are **heuristic**; they will benefit from empirical calibration.  
- Certain domains (e.g., specific industry verticals) are not yet explicitly represented.

Future work:

- Use **real case studies and user feedback** to refine strengths, directionality, and relation types.  
- Add **domain-specific subgraphs** for infrastructure, AI systems, product strategy, etc.  
- Introduce **versioning** and provenance for individual relationships.  
- Build tooling to quickly **visualize and edit** the graph as HUMMBL evolves.

---

## 7. Metadata

- **Study ID:** HUMMBL-REL-001  
- **Date:** November 17, 2025  
- **Researcher:** Reuben Bowlby  
- **Framework:** HUMMBL Base120 v1.0  
- **Graph Version:** `base120-relationships-v1`  
- **Relationship Count:** 333  
- **Model Count:** 120  

The relationship graph is now ready to support both **SY19 Meta-Model Selection** and **Phase 1 case studies** as HUMMBL moves beyond Phase 0.
