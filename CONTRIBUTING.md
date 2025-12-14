# Contributing to HUMMBL Research

This repository is a content and research portfolio for HUMMBL Systems.

## Quick Start

- Use Markdown for models, validation studies, case studies, and essays.
- Use Jupyter notebooks in `notebooks/` for demonstrations only, not core development.
- Keep Python implementation code in the `hummbl-prototype` repository.

## Code Quality & CI/CD

This repository uses automated CI/CD to maintain code quality:

### Pre-Commit Checks

Before committing, ensure your code passes:

1. **Markdown Linting:** All `.md` files are linted with `markdownlint`
   - Configuration: `.markdownlint.json`
   - Workflow: `.github/workflows/markdown-lint.yml`

2. **Python Linting:** All `.py` files are checked with `ruff` and `black`
   - Configuration: `pyproject.toml`
   - Workflow: `.github/workflows/python-lint.yml`
   - Format code: `black .`
   - Check linting: `ruff check .`

3. **Relationships Validation:** `data/relationships.json` is validated on changes
   - Script: `tools/validate_relationships_json.py`
   - Workflow: `.github/workflows/validate-relationships.yml`

### Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run markdown linting locally (requires Node.js)
npm install -g markdownlint-cli
markdownlint "**/*.md"

# Run Python linting
ruff check .
black --check .

# Validate relationships.json
python tools/validate_relationships_json.py data/relationships.json
```

## Contributing Case Studies

See the [README Case Study Contribution Workflow](README.md#contributing) for details.

## Development Guidelines

- Follow existing code style
- Add tests for new tools
- Update documentation when adding features
- Ensure all CI checks pass before submitting PRs
