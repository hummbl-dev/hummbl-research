# HUMMBL Case Studies

Case studies show HUMMBL **in action** on real engineering problems.

Each case study documents:

- The **problem** and constraints  
- The **HUMMBL operator sequence** used (P, IN, DE, CO, RE, SY)  
- The **artifacts** produced (diagrams, lists, decisions)  
- The **before/after** impact (clarity, time, risk, outcomes)

Case studies are the primary way we validate HUMMBL outside synthetic tests.

---

## Standard Structure

Every case study follows this structure:

1. **Context**
   - System / project description  
   - Constraints (time, resources, risk)  
   - Success criteria

2. **Problem Statement**
   - What is hard or unclear?  
   - Why now?  
   - What happens if we do nothing?

3. **Operator Sequence**
   - Which operators/models were used, in what order  
   - For each step:
     - Question it answers  
     - Inputs (text, diagrams, logs, code)  
     - Outputs (lists, diagrams, decisions)

4. **Results**
   - Before vs after (architecture, plan, decision)  
   - Metrics (time saved, clarity gain, risk reduction)  
   - Surprises (what HUMMBL found that you would have missed)

5. **Reflection**
   - What worked well  
   - What felt heavy or awkward  
   - Which operators should be refined next

---

## Contributing a Case Study

To add a case study:

1. Copy `templates/case-study-template.md` into `case-studies/` with a new filename.  
2. Fill in all sections with concrete details.  
3. Link to any relevant code, diagrams, or videos.  
4. Open a PR or issue referencing the new case study.

See `case-study1-multi-service-ai.md` (once added) for a reference example.
