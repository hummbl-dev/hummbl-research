# Relationships Validation Results

This directory contains all validation results and reports for the HUMMBL Base120 relationship graph (333 relationships).

## Quick Start

**Status:** ✅ All automated validation phases complete  
**Next Step:** HITL review and approval

**Start Here:**
1. Read `relationships-validation-next-steps.md` for prioritized review guide
2. Review `relationships-hitl-review-guide.md` for detailed review process
3. Use `relationships-hitl-quick-review.json` for quick review of first 20 issues

## Files Overview

### Validation Results
- `relationships-validation-results.json` - Complete validation results (333 relationships)
- `relationships-validation-summary-final.md` - Human-readable final summary
- `relationships-batch-01-results.json` through `-07-results.json` - Individual batch results

### Analysis Reports
- `relationships-consistency-report.json` - Consistency analysis (symmetry, strength, patterns)
- `relationships-missing-report.json` - Missing relationship candidates (39)

### Review Guides
- `relationships-hitl-review-guide.md` - Comprehensive HITL review guide
- `relationships-hitl-quick-review.json` - Quick review file (first 20 NEEDS_REVIEW)
- `relationships-validation-next-steps.md` - Prioritized next steps

### Status Documents
- `relationships-validation-plan.md` - Original validation plan
- `relationships-validation-status.md` - Progress tracking
- `relationships-validation-summary.md` - Batch-by-batch summary
- `relationships-validation-complete.md` - Completion report

## Validation Summary

- **Total Relationships:** 333
- **Validated:** 281 (84.4%)
- **Needs Review:** 52 (15.6%)
- **Needs Refinement:** 9 (2.7%)
- **Invalid:** 0 (0%)

## Quality Scores

- **Accuracy:** 84.4%
- **Consistency:** 65.5%
- **Completeness:** 88.3%
- **Overall:** 79.5%

## HITL Gates Status

- **Gate 1:** ✅ Approved (Data availability)
- **Gates 2.1-2.7:** ⚠️ Pending (Batch approvals)
- **Gate 3:** ⚠️ Pending (Consistency review)
- **Gate 4:** ⚠️ Pending (Missing relationships review)
- **Gate 5:** ⚠️ Pending (Final approval)

## Next Actions

See `relationships-validation-next-steps.md` for prioritized review sequence.

---

**Last Updated:** 2025-12-05  
**Validation Tool:** `tools/validate_relationships.py`

