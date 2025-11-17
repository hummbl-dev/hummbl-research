# CHANGELOG

All notable changes to this project will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for research releases.

## [Unreleased]

### Added - Phase 1
- ✅ SY19 Meta-Model Selection prototype (`tools/sy19_recommend.py`)
  - Automatic primary model detection from keywords
  - Graph traversal with centrality-weighted scoring
  - Configurable recommendations (top-K, max-hops)
  - Detailed reasoning for each recommendation
  - Tested on Case Study 1 scenario

### In Progress
- Case Study 1: Multi-service AI recommendation system
- Case Study 2: Personal training program design
- Case Study 3: Ozzy (French Bulldog) health optimization

### Infrastructure
- Added case study templates and production workflow
- Added GitHub Actions markdown linting (soft enforcement)
- Created Phase 1 project tracking issues
- Added `requirements.txt` for Python dependencies (networkx, numpy, scipy)
- Added virtual environment setup for tools

## [0.1.0] - 2025-11-16

### Added
-
- Phase 0 baseline implementations for all 6 HUMMBL transformations:
  - DE (Decomposition) – validated, 9.2/10 utility.
  - RE (Recursion) – baseline, 8.0/10 utility.
  - SY (Meta-Systems) – baseline, 8.0/10 utility.
  - P (Perspective) – baseline, 7.8/10 utility.
  - CO (Composition) – baseline, 6.0/10 utility.
  - IN (Inversion) – baseline, 3.6/10 utility.
- Validation studies for each operator in `validation/`:
  - `decomposition-study-2025.md`
  - `inversion-study-2025.md`
  - `composition-study-2025.md`
  - `perspective-study-2025.md`
  - `recursion-study-2025.md`
  - `meta-systems-study-2025.md`
  - `relationships-study-2025.md`
- Complete HUMMBL Base120 relationships graph:
  - 333 typed relationships across 120 models.
  - Canonical relation types: SCAFFOLDS, COMPOSES_WITH, REFINES, PARALLELS, CONTRASTS_WITH, CONFLICTS.
  - Strength scores and directionality for each edge.
  - Normalized export as `data/relationships.json`.

- Relationships tooling:
  - `tools/relationships_to_json.py` for CSV → JSON conversion.
  - `tools/relationships_centrality.py` for weighted centrality analysis.

- Documentation and status reporting:
  - `docs/SITREP-5-phase0-operators-and-relationships.md` summarizing Phase 0.
  - `docs/case-study-plan-2025.md` outlining initial case study strategy.
  - `docs/case-study1-multi-service-ai-brief.md` as the first real-case brief (multi-service AI system).

### Notes

- This release marks completion of Phase 0 research objectives:
  - All six operators implemented, tested, and scored.
  - Relationship graph ready for SY19 Meta-Model Selection, case studies, and future UX.

- Future releases (0.2.x, 0.3.x) will focus on:
  - Case study execution and integration.
  - IN and CO operator refinements.
  - SY19 recommender tooling and basic UX prototypes.
