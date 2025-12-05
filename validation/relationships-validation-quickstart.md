# Relationships Validation - Quick Start Guide

**Full Plan:** See `relationships-validation-plan.md`

## Overview

Validate all 333 HUMMBL relationships through autonomous AI agent workflows with HITL approvals at gate checks.

## 5 Validation Dimensions

1. **Accuracy** - Correct type, direction, existence
2. **Strength Calibration** - Reasonable 0.0-1.0 value
3. **Description Quality** - Clear, accurate explanation
4. **Completeness** - All important relationships captured
5. **Consistency** - Similar relationships handled consistently

## 5 Phases

### Phase 1: Data Preparation
- Ensure 333 relationships available
- **HITL Gate:** Approve data availability

### Phase 2: Batch Validation (20 batches)
- Validate 50 relationships per batch
- Autonomous execution
- **HITL Gates:** Approve each batch (≥90% validated)

### Phase 3: Cross-Validation
- Consistency checks (symmetry, transitivity, patterns)
- **HITL Gate:** Approve consistency fixes

### Phase 4: Missing Detection
- Identify relationships that should exist
- **HITL Gate:** Approve missing relationship additions

### Phase 5: Final Report
- Generate comprehensive validation report
- **HITL Gate:** Final approval (≥95% validated)

## Validation Status Values

- ✅ **VALIDATED** - Passes all criteria
- ⚠️ **NEEDS_REVIEW** - Flagged for human review
- 🔴 **INVALID** - Fails validation
- 📝 **NEEDS_REFINEMENT** - Exists but needs adjustment
- ➕ **MISSING** - Should exist but doesn't

## Success Criteria

- **Accuracy:** ≥95% validated (not invalid)
- **Confidence:** ≥80% HIGH confidence validations
- **Completeness:** ≤5% missing relationships
- **Consistency:** ≤10% consistency issues

## Timeline

**2-3 days total** (mostly autonomous)
- Day 1: Phases 1-2 (batches 1-10)
- Day 2: Phase 2 (batches 11-20) + Phase 3
- Day 3: Phases 4-5 + Final approval

## HITL Gate Checks

You only need to approve at:
1. **Gate 1:** Data availability (after Phase 1)
2. **Gates 2:** Batch approvals (20 gates, after each batch)
3. **Gate 3:** Consistency review (after Phase 3)
4. **Gate 4:** Missing relationships review (after Phase 4)
5. **Gate 5:** Final approval (after Phase 5)

**Total HITL interactions:** ~24 gate checks

## Output Files

- `validation/relationships-validation-results.json` - Full results
- `validation/relationships-validation-summary.md` - Human-readable summary
- `data/relationships-validated.json` - Updated production data

## Next Steps

1. Implement validation tool
2. Execute Phase 1
3. Approve Gate 1
4. Continue through all phases

