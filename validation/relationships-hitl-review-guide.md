# HITL Review Guide - Relationships Validation

**Date:** 2025-12-05  
**Purpose:** Streamlined guide for reviewing and approving validation results

---

## Quick Summary

- **Total Items for Review:** 206
  - 52 relationships (NEEDS_REVIEW)
  - 9 relationships (NEEDS_REFINEMENT)
  - 115 symmetry issues
  - 39 missing relationship candidates

---

## HITL Gate 2: Batch Approvals (2.1-2.7)

### Batch 1: ✅ Ready for Approval
- **Status:** 98% validated (49/50)
- **Issues:** 1 NEEDS_REVIEW, 2 NEEDS_REFINEMENT
- **Action:** Quick review, approve

### Batch 2: ✅ Ready for Approval
- **Status:** 100% validated (50/50)
- **Issues:** None
- **Action:** Approve immediately

### Batch 3: ✅ Ready for Approval
- **Status:** 94% validated (47/50)
- **Issues:** 3 NEEDS_REVIEW
- **Action:** Quick review, approve

### Batch 4: ⚠️ Review Required
- **Status:** 80% validated (40/50)
- **Issues:** 10 NEEDS_REVIEW, 2 NEEDS_REFINEMENT
- **Action:** Review NEEDS_REVIEW relationships

### Batch 5: ⚠️ Review Required
- **Status:** 66% validated (33/50)
- **Issues:** 17 NEEDS_REVIEW, 3 NEEDS_REFINEMENT
- **Action:** Review NEEDS_REVIEW relationships

### Batch 6: ⚠️ Review Required
- **Status:** 68% validated (34/50)
- **Issues:** 16 NEEDS_REVIEW, 2 NEEDS_REFINEMENT
- **Action:** Review NEEDS_REVIEW relationships

### Batch 7: ⚠️ Review Required
- **Status:** 84.8% validated (28/33)
- **Issues:** 5 NEEDS_REVIEW
- **Action:** Review NEEDS_REVIEW relationships

---

## Common Issue Patterns

### Issue Type 1: Direction Mismatches (52 relationships)

**Pattern:** Relationship type suggests one direction, but marked as different

**Most Common:**
- **REFINES marked bidirectional (47 cases)**
  - REFINES should typically be unidirectional (A → B improves A)
  - **Decision:** Change to unidirectional OR verify if bidirectional is intentional
  
- **SCAFFOLDS marked bidirectional (4 cases)**
  - SCAFFOLDS should typically be unidirectional (A → B, A is prerequisite)
  - **Decision:** Change to unidirectional OR verify if bidirectional is intentional

- **PARALLELS marked unidirectional (1 case)**
  - PARALLELS should typically be bidirectional
  - **Decision:** Change to bidirectional

**Review Process:**
1. Check relationship description - does it imply direction?
2. If description is symmetric → bidirectional is correct
3. If description is asymmetric → unidirectional is correct
4. Approve or request direction change

### Issue Type 2: Symmetry Issues (115 relationships)

**Pattern:** Bidirectional relationships don't have explicit reverse entries

**Analysis:**
- This may be **by design** - relationships stored once, interpreted bidirectionally
- OR may need explicit reverse relationships added

**Review Process:**
1. Check if relationship description works both ways
2. If yes → Current design is fine (no action needed)
3. If no → Add reverse relationship OR change to unidirectional
4. Approve symmetry as-is OR request fixes

**Recommendation:** Review sample of 10-15 symmetry issues to determine pattern, then batch-approve similar cases

### Issue Type 3: Missing Relationships (39 candidates)

**Pattern:** Model files mention relationships not in relationship graph

**Breakdown:**
- 34 from model files (MEDIUM priority)
- 5 pattern completion opportunities (LOW priority)

**Review Process:**
1. Check if mentioned relationship makes sense
2. Verify relationship doesn't already exist (check both directions)
3. If valid → Add relationship
4. If invalid → Mark as false positive

**Priority:**
- Review model file mentions first (MEDIUM priority)
- Pattern completions are optional (LOW priority)

---

## Prioritized Review Checklist

### High Priority (Review First)

1. **Direction Mismatches - REFINES (47 relationships)**
   - File: Check batch results for REL-141, REL-146, REL-148, REL-158, etc.
   - Decision: Unidirectional or bidirectional?
   - Impact: High - affects relationship interpretation

2. **Symmetry Issues - Sample Review (10-15 relationships)**
   - File: `validation/relationships-consistency-report.json`
   - Decision: By design or need fixes?
   - Impact: Medium - affects data structure

### Medium Priority

3. **Missing Relationships from Model Files (34 candidates)**
   - File: `validation/relationships-missing-report.json`
   - Decision: Add or reject?
   - Impact: Medium - improves completeness

4. **NEEDS_REFINEMENT (9 relationships)**
   - File: Batch results
   - Decision: Approve refinements or keep as-is?
   - Impact: Low - mostly strength/description tweaks

### Low Priority

5. **Pattern Completion (5 candidates)**
   - File: `validation/relationships-missing-report.json`
   - Decision: Add or skip?
   - Impact: Low - nice-to-have

---

## Quick Approval Paths

### Path 1: Conservative (Recommended)
1. ✅ Approve Batches 1-3 immediately (≥90% validated)
2. ⚠️ Review Batches 4-7 NEEDS_REVIEW (52 relationships)
3. ⚠️ Review symmetry sample (10-15) to determine pattern
4. ⚠️ Review missing relationships (34 from model files)
5. ✅ Final approval after fixes

### Path 2: Aggressive (Fast Track)
1. ✅ Approve all batches (84.4% validated is acceptable)
2. ✅ Approve symmetry as-is (by design interpretation)
3. ⚠️ Review only HIGH priority missing relationships
4. ✅ Final approval

### Path 3: Comprehensive (Thorough)
1. ⚠️ Review all 52 NEEDS_REVIEW relationships individually
2. ⚠️ Review all 115 symmetry issues
3. ⚠️ Review all 39 missing relationship candidates
4. ✅ Final approval after all fixes

---

## Review Tools

### View Batch Results
```bash
# View specific batch
cat validation/relationships-batch-01-results.json | jq '.[] | select(.status == "NEEDS_REVIEW")'

# Count by status
cat validation/relationships-batch-01-results.json | jq '[.[] | .status] | group_by(.) | map({status: .[0], count: length})'
```

### View Consistency Issues
```bash
# View symmetry issues
cat validation/relationships-consistency-report.json | jq '.issues[:10]'
```

### View Missing Relationships
```bash
# View missing relationships
cat validation/relationships-missing-report.json | jq '.missing_relationships[:10]'
```

---

## Decision Templates

### For Direction Mismatches
```
Relationship: REL-XXX
Type: REFINES
Current Direction: bidirectional
Expected: unidirectional

Decision: [ ] Keep bidirectional (relationship is symmetric)
          [ ] Change to unidirectional (relationship is asymmetric)
          [ ] Needs more context
```

### For Symmetry Issues
```
Relationship: REL-XXX
Direction: bidirectional
Reverse exists: No

Decision: [ ] By design - no action needed
          [ ] Add reverse relationship
          [ ] Change to unidirectional
```

### For Missing Relationships
```
Candidate: CO01 → DE08
Source: Model file CO01.md mentions DE08
Priority: MEDIUM

Decision: [ ] Add relationship
          [ ] Reject (false positive)
          [ ] Defer (low priority)
```

---

## Estimated Review Time

- **Batches 1-3:** 5 minutes (quick approval)
- **Batches 4-7:** 30-45 minutes (review 52 NEEDS_REVIEW)
- **Symmetry Issues:** 15-20 minutes (sample review + pattern decision)
- **Missing Relationships:** 20-30 minutes (review 39 candidates)
- **Total:** 70-100 minutes

---

## Approval Criteria

### Batch Approval
- ✅ ≥90% validated OR
- ✅ All critical issues resolved OR
- ✅ Acceptable quality for production use

### Final Approval
- ✅ All batches approved
- ✅ Consistency issues resolved or accepted
- ✅ Missing relationships prioritized
- ✅ Overall quality ≥80%

---

**Next Action:** Start with Batch 1-3 approvals, then proceed through remaining gates.

