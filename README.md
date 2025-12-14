# HUMMBL Framework
### Executable Mental Models for Engineers

**By Reuben Bowlby** | [@ReubenBowlby](https://twitter.com/ReubenBowlby)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Fully Developed](https://img.shields.io/badge/Status-Fully_Developed-green.svg)](https://github.com/hummbl-dev/hummbl-research)

**License:** Code (MIT) | Content (CC BY 4.0) - See [License](#license) section for details

---

## What This Is

HUMMBL (Base120) is a comprehensive framework of **120 mental models** organized across **6 transformations** that make engineering reasoning:

- **Explicit** (not implicit)
- **Traceable** (not black-box)
- **Improvable** (not fixed)
- **Executable** (not just descriptions)

**Not just ideas about thinking. Actual algorithms that run.**

### Understanding Operator Maturity

Operators are scored on a **5-dimension utility rubric (1-10 scale)**:
- **≥7.0/10 = VALIDATED** ✅ Production-ready, safe to use
- **<7.0/10 = BASELINE** ⚠️ Functional but experimental, use with caution

**What scores mean:**
- **9.2/10 (DE)**: Production-ready, exemplar quality
- **8.0/10 (RE, SY)**: Strong baseline, minor refinements needed
- **7.8/10 (P)**: Good baseline, close to validated
- **6.0/10 (CO)**: Functional but needs refinement
- **3.6/10 (IN)**: Experimental, significant work needed

Each operator is evaluated on: insight quality, usefulness, catch rate, speed, and recommendation likelihood.

---

## Quick Example

**Traditional approach:**
> "Just break it down and think through it..."

**HUMMBL Decomposition:**
```python
from hummbl import decompose

result = decompose("""
  Build distributed system with authentication,
  caching, monitoring, and horizontal scaling
""")

# Returns:
# • 8 components identified
# • 12 dependencies mapped
# • Critical path: 4 sequential steps
# • 3 parallel work streams
# • Coupling analysis
# • Traceable reasoning

Try it live →

---

## Getting Started

**Quick start for engineers:** Get HUMMBL running in 5 minutes.

### 1. Install Dependencies

```bash
# Clone the repository
git clone https://github.com/hummbl-dev/hummbl-research.git
cd hummbl-research

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up API Key (Optional)

For Vertex AI features (enhanced SY19 recommender):
```bash
# Follow the setup guide
cat docs/create-api-key.md

# Or use the setup script
./setup-vertex-ai.sh
```

### 3. Run Your First Demo

**Recommended:** Start with the Decomposition (DE) operator demo:

```bash
# Run the workflow demonstration
python notebooks/hummbl_workflow_demo.py

# Or explore the notebook
jupyter notebook notebooks/hummbl_workflow_demo.py
```

**What you'll see:**
- DE operator breaking down a problem into components
- Dependency mapping and critical path analysis
- Structured output with insights and confidence scores

### 4. Try SY19 Model Recommender

Get model recommendations for your problem:

```bash
python tools/sy19_recommend.py "I need to debug a distributed system with latency spikes"
```

**Next Steps:**
- Read [validation studies](validation/) to understand operator quality
- Explore [case studies](case-studies/) for real-world examples
- Check [docs/for-engineers.md](docs/for-engineers.md) for daily workflow integration

---

## Recommended First Demos

**Start here to move from concept to code quickly:**

1. **`notebooks/hummbl_workflow_demo.py`** - Complete workflow demonstration
   - Shows all 6 operators in action
   - Demonstrates operator sequencing
   - Includes example outputs and insights

2. **Decomposition (DE) Operator** - Production-ready, best starting point
   - See it in action: `validation/decomposition-study-2025.md`
   - Try it: Use DE for any problem breakdown task
   - Score: 9.2/10 (validated, production-ready)

3. **SY19 Model Recommender** - Get recommendations for your problem
   - Run: `python tools/sy19_recommend.py "your problem description"`
   - Uses validated 367-relationship graph
   - Optional: Enhanced with Vertex AI for better detection

**Want more?** See [Tools & Code](#tools--code) section below.

---

## Framework Overview
HUMMBL Base120 consists of 6 transformations with 20 models each:
TransformPurposeModelsStatus
P - Perspective
Change analytical frame
20
✅ Fully Developed (20 models fleshed)
IN - Inversion
Find failure modes
20
✅ Fully Developed (20 models fleshed)
CO - Composition
Combine components
20
✅ Fully Developed (20 models fleshed)
DE - Decomposition
Break into parts
20
✅ Validated + Fully Developed (20 models fleshed)
RE - Recursion
Iterative refinement
20
✅ Fully Developed (20 models fleshed)
SY - Synthesis
Meta-analysis
20
✅ Fully Developed (20 models fleshed)
Explore all 120 models →

## Transformation Operator Status

| Operator | Code | Status | Utility Score | When to Use | Implementation | Validation |
|----------|------|--------|---------------|-------------|----------------|------------|
| **Decomposition** | DE | ✅ VALIDATED | 9.2/10 | **Production-ready:** Use for any problem breakdown, architecture planning, or component identification. Safe for production use. | [hummbl-prototype](https://github.com/hummbl-dev/hummbl-prototype) | [`validation/decomposition-study-2025.md`](validation/decomposition-study-2025.md) |
| **Inversion** | IN | ⚠️ BASELINE | 3.6/10 | **Experimental:** Use for failure mode analysis, but expect limited extraction quality. Not recommended for production. | [hummbl-prototype](https://github.com/hummbl-dev/hummbl-prototype) | [`validation/inversion-study-2025.md`](validation/inversion-study-2025.md) |
| **Composition** | CO | ⚠️ BASELINE | 6.0/10 | **Functional:** Use for integration planning, but results may need manual refinement. Good for exploration, not final decisions. | [hummbl-prototype](https://github.com/hummbl-dev/hummbl-prototype) | [`validation/composition-study-2025.md`](validation/composition-study-2025.md) |
| **Perspective** | P | ⚠️ BASELINE | 7.8/10 | **Strong baseline:** Use for multi-stakeholder analysis and perspective shifts. Close to validated, minor refinements needed. | [hummbl-prototype](https://github.com/hummbl-dev/hummbl-prototype) | [`validation/perspective-study-2025.md`](validation/perspective-study-2025.md) |
| **Recursion** | RE | ⚠️ BASELINE | 8.0/10 | **Strong baseline:** Use for iterative refinement and feedback loop analysis. Very close to validated, safe for most use cases. | [hummbl-prototype](https://github.com/hummbl-dev/hummbl-prototype) | [`validation/recursion-study-2025.md`](validation/recursion-study-2025.md) |
| **Meta-Systems** | SY | ⚠️ BASELINE | 8.0/10 | **Strong baseline:** Use for system-level analysis and meta-patterns. Very close to validated, safe for most use cases. | [hummbl-prototype](https://github.com/hummbl-dev/hummbl-prototype) | [`validation/meta-systems-study-2025.md`](validation/meta-systems-study-2025.md) |

**Status Guide:**
- ✅ **VALIDATED (≥7.0)**: Production-ready, safe to use in production
- ⚠️ **BASELINE (<7.0)**: Functional but experimental, use with caution

### Validation Criteria

Operators must score ≥7.0/10 on a 5-dimension utility rubric to achieve **VALIDATED** status:
1. Finds meaningful insights/components/failure modes  
2. Useful for analysis/debugging  
3. Catches things you'd miss mentally  
4. Faster than manual analysis  
5. Would recommend to others

### Recent Updates

**November 16, 2025 (Continued):**
- 🎉 **HUMMBL Base120 COMPLETE!** All 120 mental models fully developed
- ✅ Final 30 models implemented (P16-P20, IN16-IN20, CO16-CO20, DE16-DE20, RE16-RE20, SY16-SY20)
- ✅ Framework status: FULLY DEVELOPED (120/120 models)
- 📈 Total framework coverage: 100% - ready for Phase 1 implementation and case studies

**November 16, 2025:**
- ✅ Meta-Systems (SY) operator baseline implemented (v0.1)  
- ✅ Validation study completed: 8.0/10 utility score  
- ⚠️ Status: BASELINE – strong meta-systems baseline, minor refinements required  
- 📋 Refinement priorities documented in `validation/meta-systems-study-2025.md` Section 6  
- ✅ Recursion (RE) operator baseline implemented (v0.1)  
- ✅ Validation study completed: 8.0/10 utility score  
- ⚠️ Status: BASELINE – strong iterative refinement baseline, minor refinements required  
- 📋 Refinement priorities documented in `validation/recursion-study-2025.md` Section 6  
- ✅ Perspective (P) operator baseline implemented (v0.1)  
- ✅ Validation study completed: 7.8/10 utility score  
- ⚠️ Status: BASELINE – strong functional baseline, minor refinements required  
- 📋 Refinement priorities documented in `validation/perspective-study-2025.md` Section 6  
- ✅ Composition (CO) operator baseline implemented (v0.1)  
- ✅ Validation study completed: 6.0/10 utility score  
- ⚠️ Status: BASELINE – iteration required post-Phase 0  
- 📋 Refinement priorities documented in `validation/composition-study-2025.md` Section 6  

**November 15, 2025:**
- ✅ Inversion (IN) operator baseline implemented (v0.1)  
- ✅ Validation study completed: 3.6/10 score  
- ⚠️ Status: BASELINE – iteration required post-Phase 0  
- 📋 Refinement plan documented in `validation/inversion-study-2025.md` Section 6  

**Earlier:**
- ✅ Decomposition (DE) operator validated at 9.2/10 (production-ready)  
- ✅ Full test coverage (≈98% across hummbl-prototype)  
- ✅ CI/CD pipeline operational

### Phase 0 Strategy ✅ COMPLETE

**Goal:** Baseline implementation of all 6 core operators by **November 25, 2025**. **ACHIEVED November 16, 2025**

**Approach:**
- Prioritize breadth (6 baseline operators) over depth (perfect implementation).  
- Use DE's 9.2/10 score as architectural template.  
- Mark operators below 7.0 threshold for post-Phase 0 refinement.  
- Enable case studies with a functional (if imperfect) operator portfolio.

**Results:**
- All 120 mental models fully developed and documented
- Framework status: FULLY DEVELOPED
- Ready for Phase 1 implementation and case studies

**Refinement Pipeline:**
- IN operator improvements documented in `validation/inversion-study-2025.md` Section 6.  
- Post-Phase 0 re-validation targets ≥7.0/10 scores for all operators.  
- User feedback will guide refinement priorities.

---

## Roadmap

### Phase 0 – Operator Baselines & Relationship Graph ✅ COMPLETE

- [x] 6 transformation operators validated (baseline or better)
- [x] **367 relationship classifications complete** (validated December 5, 2025)
- [x] Comprehensive validation studies across all operators
- [x] Production infrastructure deployed
- [x] **120/120 mental models fully developed** (November 16, 2025)
- [x] **Relationship graph 100% validated** (December 5, 2025)
- **Status:** `v0.1.0` released November 2025 – **FULLY DEVELOPED**

---

### Phase 1 – Case Studies & Intelligence (In Progress)

- [x] SY19 `recommend_models()` prototype ✅
- [ ] Case Study 1: Multi-service AI system (Target: Jan 2026)
- [ ] Case Study 2: Fitness transformation (Target: Dec 2025)
- [ ] Case Study 3: Ozzy health protocol (Target: Dec 2025)
- **Target:** January 2026 completion

---

### Phase 2 – Refinement & Production

- [ ] Operator refinements (IN, CO improvements)
- [ ] Enhanced UX development
- [ ] Commercial deployment preparation
- **Target:** Q1 2026

---

### Phase 3 – Community & Scale

- [ ] Public beta launch
- [ ] Community contributions
- [ ] Partnership development
- **Target:** Q2 2026

---

## Validation Studies

Detailed operator validation documentation:

| Study | Date | Operator | Score | Status | Location |
|-------|------|----------|-------|--------|----------|
| Decomposition Validation 2025 | Oct 2025 | DE | 9.2/10 | ✅ VALIDATED | `validation/decomposition-study-2025.md` |
| Inversion Validation 2025 | Nov 15, 2025 | IN | 3.6/10 | ⚠️ BASELINE | `validation/inversion-study-2025.md` |
| Composition Validation 2025 | Nov 16, 2025 | CO | 6.0/10 | ⚠️ BASELINE | `validation/composition-study-2025.md` |
| Perspective Validation 2025 | Nov 16, 2025 | P | 7.8/10 | ⚠️ BASELINE | `validation/perspective-study-2025.md` |
| Recursion Validation 2025 | Nov 16, 2025 | RE | 8.0/10 | ⚠️ BASELINE | `validation/recursion-study-2025.md` |
| Meta-Systems Validation 2025 | Nov 16, 2025 | SY | 8.0/10 | ⚠️ BASELINE | `validation/meta-systems-study-2025.md` |

### Validation Methodology

Each operator undergoes:
1. Implementation following proven architectural patterns  
2. Comprehensive test coverage (unit + integration)  
3. Real-world test case validation  
4. 5-dimension utility scoring (1–10 scale)  
5. Gap analysis and refinement planning  
6. Production readiness assessment

Operators scoring ≥7.0/10 are marked **VALIDATED** for production use.  
Operators scoring <7.0/10 are marked **BASELINE** with documented refinement plans.

Case Studies
Real-World Applications
HUMMBL Prototype Project Planning
Context: Planning a multi-week research project with validation gates
Challenge: Complex dependencies, unclear sequencing, risk of premature infrastructure
HUMMBL Application: Decomposition operator (DE)
Results:
Time saved: ~25-55 minutes vs manual decomposition
Completeness: +20% improvement (95% vs 75%)
Quality score: 9.2/10
Outcome: Successfully identified critical path, parallelizable work, and constraint implications
Read full case study →

Use Cases
Debugging
Systematic root cause analysis using Inversion and Decomposition
Architecture Design
Explicit tradeoff analysis using Composition and Synthesis
Project Planning
Component breakdown using Decomposition and dependency mapping
Technical Decisions
Traceable reasoning using the full transformation suite
Learning
Build systematic thinking vocabulary

Tools & Code
Research Implementation
hummbl-prototype - Python research implementation (active development)
Current operators:
✅ Decomposition (DE) – VALIDATED (9.2/10)
⚠️ Inversion (IN) – BASELINE (3.6/10, extraction refinements pending)
⚠️ Composition (CO) – BASELINE (6.0/10, integration refinements pending)
⚠️ Perspective (P) – BASELINE (7.8/10, perspective/gap refinements pending)
⚠️ Recursion (RE) – BASELINE (8.0/10, refinement/constraint handling pending)
⚠️ Meta-Systems (SY) – BASELINE (8.0/10, extraction/summarization refinements pending)
Production Deployment
Only after research validation confirms utility
Interactive Demos
Decomposition Demo
Framework Overview

For Different Audiences
Engineers - How to apply HUMMBL in your daily work
Teams - Adopting HUMMBL organizationally
Researchers - Academic foundations and methodology
Business Case - The opportunity and market

About
HUMMBL, LLC
Founded to commercialize executable mental models for engineering.
Mission: Make engineering reasoning explicit, traceable, and improvable.
Approach: Research → Validate → Build → Deploy
Status: Phase 0 - Research & validation
Reuben Bowlby
Chief Engineer, HUMMBL LLC
18 months developing the HUMMBL Base120 framework. Background in systematic thinking, cognitive frameworks, and AI system coordination.
Currently:
Dynamic Personal Trainer, Life Time Fitness
Preparing for law school, Georgia State University
Building HUMMBL commercialization infrastructure
Connect:
Twitter: @ReubenBowlby
Email: reuben@hummbl.io
Website: hummbl.io
Location: Brookhaven, GA

Contributing
HUMBBL is in research phase. Contributions welcome for:
✅ Case studies from real engineering work
✅ Validation study participation
✅ Model refinements and clarifications
✅ Documentation improvements
✅ Academic citations and research

**Case Study Contribution Workflow:**
1. **Open an issue** describing your case study idea
2. **Share context** - problem domain, constraints, goals
3. **Create PR** into `case-studies/` following the [case study template](case-studies/templates/case-study-template.md)
4. **Include artifacts** - diagrams, operator outputs, before/after comparisons

See [contributing guidelines](CONTRIBUTING.md) for details →

Citation
If you use HUMMBL in research or writing:
@software{hummbl2025,
  author = {Bowlby, Reuben},
  title = {HUMMBL: Executable Mental Models for Engineers},
  year = {2025},
  url = {https://github.com/hummbl-dev/hummbl-research},
  version = {0.1.0}
}

CITATION.cff

License
Content (documentation, models, studies): CC BY 4.0
Code (algorithms, implementations): MIT License

Repository Structure
hummbl-research/
├─ models/              # 120 mental models (P, IN, CO, DE, RE, SY)
├─ validation/          # Empirical validation studies
├─ case-studies/        # Real-world applications
├─ docs/                # Documentation for different audiences
├─ essays/              # Thought leadership and writing
├─ notebooks/           # Interactive demonstrations
├─ CITATION.cff         # Academic citation format
├─ LICENSE              # Dual license (MIT + CC BY 4.0)
├─ CONTRIBUTING.md      # Contribution guidelines
└─ README.md            # This file


Last Updated: November 16, 2025
Version: 0.1.0 (Research Phase)
Next Milestone: Relationship classification & case studies
Latest Success: Meta-Systems operator baseline validated at 8.0/10 utility score ⚠️

---
