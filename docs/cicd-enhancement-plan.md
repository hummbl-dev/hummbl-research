# CI/CD Enhancement Plan

**Issue:** #4 - Repo Hygiene (CI/CD)  
**Status:** Enhancement Plan  
**Date:** December 2025

## Current State Assessment

### Existing Infrastructure
- ✅ **Markdown Linting:** `.github/workflows/markdown-lint.yml`
  - Runs on push/PR for `.md` files
  - Uses `markdownlint-cli`
  - **Issue:** Soft enforcement (`|| true` doesn't block PRs)

### Gaps Identified
- ❌ No Python code linting/formatting
- ❌ No automated testing for Python tools
- ❌ No validation of `data/relationships.json` structure
- ❌ No operator status consistency checks
- ❌ No pre-commit hooks
- ❌ No dependency update automation
- ❌ No documentation build validation

---

## Enhancement Plan

### Phase 1: Immediate Improvements (High Priority)

#### 1.1 Enforce Markdown Linting
**Goal:** Block PRs with markdown linting errors

**Action:**
- Remove `|| true` from markdown-lint workflow
- Add `.markdownlint.json` configuration file
- Document linting rules

**Files to Create/Modify:**
- `.github/workflows/markdown-lint.yml` - Remove soft fail
- `.markdownlint.json` - Configuration file

**Estimated Effort:** 30 minutes

---

#### 1.2 Python Code Quality Checks
**Goal:** Ensure Python code follows standards

**Action:**
- Add workflow for Python linting (flake8 or ruff)
- Add workflow for Python formatting check (black)
- Optionally: Add type checking (mypy)

**Files to Create:**
- `.github/workflows/python-lint.yml`
- `pyproject.toml` or `.flake8` for configuration

**Estimated Effort:** 1-2 hours

---

#### 1.3 Relationships JSON Validation
**Goal:** Validate `data/relationships.json` structure on changes

**Action:**
- Create validation script (can reuse `tools/validate_relationships.py`)
- Add workflow that runs validation on changes to `data/relationships.json`
- Ensure schema compliance

**Files to Create:**
- `.github/workflows/validate-relationships.yml`

**Estimated Effort:** 1 hour

---

### Phase 2: Testing Automation (Medium Priority)

#### 2.1 Python Tool Testing
**Goal:** Automatically test Python tools

**Action:**
- Add pytest workflow
- Run unit tests for `tools/` directory
- Ensure test coverage for critical paths

**Files to Create:**
- `.github/workflows/python-tests.yml`
- Ensure `tests/` directory exists or create test files

**Estimated Effort:** 2-3 hours

---

#### 2.2 SY19 Recommender Testing
**Goal:** Ensure SY19 recommender works with relationship graph

**Action:**
- Add integration test for SY19
- Test against known scenarios
- Validate recommendation quality

**Estimated Effort:** 2 hours

---

### Phase 3: Advanced Checks (Low Priority)

#### 3.1 Operator Status Consistency
**Goal:** Verify operator scores match across README and validation studies

**Action:**
- Create script to extract scores from:
  - `README.md` operator table
  - Validation study frontmatter
  - Case study documentation
- Report inconsistencies in PR comments

**Estimated Effort:** 3-4 hours

---

#### 3.2 Documentation Build Validation
**Goal:** Ensure all markdown files are properly formatted and linked

**Action:**
- Add dead link checking
- Validate frontmatter in markdown files
- Check for broken internal links

**Estimated Effort:** 2-3 hours

---

#### 3.3 Pre-commit Hooks
**Goal:** Catch issues before commits

**Action:**
- Add `.pre-commit-config.yaml`
- Install pre-commit hooks locally
- Run basic checks before commit

**Files to Create:**
- `.pre-commit-config.yaml`
- Update `CONTRIBUTING.md` with setup instructions

**Estimated Effort:** 1-2 hours

---

## Implementation Priority

### Immediate (This Week)
1. ✅ Enforce markdown linting (remove soft fail)
2. ✅ Add Python linting workflow
3. ✅ Add relationships JSON validation

### Short-term (Next 2 Weeks)
4. Add Python testing workflow
5. Add SY19 integration tests

### Long-term (Next Month)
6. Operator status consistency checks
7. Documentation validation
8. Pre-commit hooks

---

## Workflow Files Structure

```
.github/
├── workflows/
│   ├── markdown-lint.yml          # ✅ Exists (needs update)
│   ├── python-lint.yml            # ⏳ To create
│   ├── python-tests.yml           # ⏳ To create
│   ├── validate-relationships.yml # ⏳ To create
│   └── consistency-checks.yml     # ⏳ To create (future)
├── CODEOWNERS                     # ⏳ Optional
└── dependabot.yml                 # ⏳ Optional
```

---

## Configuration Files Needed

### `.markdownlint.json`
```json
{
  "default": true,
  "MD013": {
    "line_length": 120,
    "code_blocks": false
  },
  "MD033": false,
  "MD041": false
}
```

### `pyproject.toml` (for ruff/flake8/black)
```toml
[tool.black]
line-length = 100
target-version = ['py39']

[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I"]
```

---

## Success Metrics

- **Code Quality:** All PRs must pass linting checks
- **Validation:** Relationships JSON validated on every change
- **Testing:** Critical tools have automated test coverage
- **Consistency:** Operator scores consistent across documentation
- **Developer Experience:** Fast feedback (< 5 minutes for most checks)

---

## Dependencies

### Required
- GitHub Actions (already available)
- Python 3.9+ (already in use)
- Node.js 22 (already configured for markdown linting)

### Optional
- Dependabot for dependency updates
- Code scanning (if desired)
- Release automation (future)

---

## Notes

- Start with Phase 1 items for immediate value
- Can implement incrementally
- Focus on blocking obvious errors first
- Soft checks can be added later for warnings
- Consider cost implications for GitHub Actions minutes (free tier: 2,000/month)

---

**Next Steps:**
1. Review and prioritize items
2. Start with Phase 1.1 (enforce markdown linting)
3. Create workflow files incrementally
4. Test workflows with sample PRs
5. Document in CONTRIBUTING.md

