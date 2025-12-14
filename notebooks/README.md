# HUMMBL Demo Notebooks

**Recommended first demos** to move from concept to code quickly.

## Quick Start

### 1. Workflow Demonstration (Recommended First)
```bash
python notebooks/hummbl_workflow_demo.py
```

**What it shows:**
- All 6 operators (P, IN, CO, DE, RE, SY) in action
- Operator sequencing and context passing
- Structured outputs with insights and confidence scores
- Real-world problem-solving workflow

**Best for:** Understanding how operators work together in a complete workflow.

### 2. Decomposition (DE) Operator Demo
Start with the **production-ready** DE operator (9.2/10 score):

```bash
# See validation study
cat ../validation/decomposition-study-2025.md

# Run demo
python notebooks/hummbl_workflow_demo.py
```

**Best for:** First-time users, production use cases.

### 3. SY19 Model Recommender
Get model recommendations for your specific problem:

```bash
python ../tools/sy19_recommend.py "your problem description here"
```

**Best for:** Finding which models to use for your problem.

---

## File Structure

- `hummbl_workflow_demo.py` - Complete workflow demonstration (all operators)
- `README.md` - This file

**Note:** Core development lives in the [hummbl-prototype](https://github.com/hummbl-dev/hummbl-prototype) repo. These notebooks are demonstrations only.
