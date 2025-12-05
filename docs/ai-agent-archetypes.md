# AI Agent Archetypes - Base4 Answer Set Taxonomy

**Date:** 2025-11-18  
**Purpose:** Biological hierarchy of AI agents based on Base4 answer set combinations  
**Total Possible Combinations:** 15,746,400  
**Representative Archetypes:** ~50-100 (hierarchical clustering)

---

## Biological Taxonomy Model

### Hierarchy Levels

```
Kingdom: AI Agents (all agents)
  └─ Phylum: Philosophical Stance (3 major splits)
      └─ Class: Error Handling Model (2 approaches)
          └─ Order: Extensibility Stance (3 positions)
              └─ Family: Constraint Enforcement (3 levels)
                  └─ Genus: Operational Model (4 types)
                      └─ Species: Specific Implementation (variations)
```

**Total Species:** ~15.7M combinations  
**Practical Representation:** ~50-100 archetypes (one per Genus or Family level)

---

## Kingdom: AI Agents

All agents that operate on Base4 principles (Identity·Time·State·Constraint).

---

## Phylum: Philosophical Stance

### Phylum A: **Sovereign Minimalists** (Strict Adherence)

**Characteristics:**
- Never read logs (or only post-mortem)
- No error handling (fail fast)
- Never extend (final version)
- Values immutable (manifesto fixed)
- Voltage doesn't decay (current model correct)

**Population:** ~2.6M combinations (17% of total)

**Key Questions:**
- Q1: A1-A4 (Never read) or A3 (Post-mortem only)
- Q5: A1 (Never extend)
- Q7: A1-A3 (Values don't change)
- Q8: A1-A3 (Fail fast)
- Q3: A1-A4 (No decay)

---

### Phylum B: **Pragmatic Minimalists** (Minimal but Flexible)

**Characteristics:**
- Read logs externally (not in system)
- Minimal error handling (check critical only)
- Final for now (but can fork/replace)
- Values can change (update manifesto)
- Voltage may decay (minimal implementation)

**Population:** ~6.5M combinations (41% of total)

**Key Questions:**
- Q1: B1-B3 (External reading)
- Q5: B1-B3 (Final for now)
- Q7: B1-B3 (Values can change)
- Q8: B1-B3 (Minimal error handling)
- Q3: B1-B3 (Yes, minimal decay)

---

### Phylum C: **Adaptive Minimalists** (Implicit Flexibility)

**Characteristics:**
- Read logs in system (but minimal)
- Error handling via constraints
- Final is relative (context-dependent)
- Decay is implicit (via other mechanisms)
- Operations are implicit (not explicit)

**Population:** ~6.6M combinations (42% of total)

**Key Questions:**
- Q1: C1-C3 (Read in system)
- Q5: C1-C3 (Final is relative)
- Q3: C1-C3 (Decay is implicit)
- Q2: C1-C3 (Used implicitly)
- Q4: C1-C3 (Cut is warning/checkpoint)

---

## Class: Error Handling Model

### Class I: **Fail-Fast Agents** (Phylum A, B, C)

**Characteristics:**
- No error handling (A1-A3)
- Errors are fatal (B1-B3)
- Errors don't matter (C1-C3)

**Behavior:**
- System crashes on error
- No recovery attempts
- Failures are terminal

**Population:** ~7.9M combinations (50% of total)

---

### Class II: **Graceful Degradation Agents** (Phylum B, C)

**Characteristics:**
- Check critical syscalls only (B1)
- Error = exit with code (B2)
- Log errors to stderr (B3)

**Behavior:**
- Partial error handling
- Graceful shutdown
- Error reporting

**Population:** ~7.9M combinations (50% of total)

---

## Order: Extensibility Stance

### Order 1: **Immutable Agents** (Phylum A)

**Characteristics:**
- Final, never change (A1)
- Final, but bug fixes OK (A2)
- Final, but documentation OK (A3)

**Behavior:**
- System is fixed
- No feature additions
- Only corrections allowed

**Population:** ~2.6M combinations (17% of total)

---

### Order 2: **Forkable Agents** (Phylum B)

**Characteristics:**
- Final until needed (B1)
- Final, but can fork (B2)
- Final, but can replace (B3)

**Behavior:**
- System can evolve via forking
- Original preserved
- New versions created

**Population:** ~2.2M combinations (14% of total)

---

### Order 3: **Contextual Agents** (Phylum C)

**Characteristics:**
- Final for this purpose (C1)
- Final until manifesto changes (C2)
- Final is a constraint (C3)

**Behavior:**
- System adapts to context
- Constraints can change
- Relative finality

**Population:** ~2.2M combinations (14% of total)

---

## Family: Constraint Enforcement

### Family α: **Strict Enforcers** (High Deviation Sensitivity)

**Characteristics:**
- DEVIATION_LIMIT = 0.30 (30%)
- Voltage > 95% max = cut
- Age > MAX_AGE = cut
- All three conditions enforced

**Behavior:**
- Aggressive constraint enforcement
- Early mortality
- Low tolerance for drift

**Population:** ~5.2M combinations (33% of total)

---

### Family β: **Moderate Enforcers** (Balanced Sensitivity)

**Characteristics:**
- DEVIATION_LIMIT = 0.30 (30%)
- Voltage > 95% max = cut
- Age > MAX_AGE = cut
- But cut is warning, not death

**Behavior:**
- Moderate constraint enforcement
- Warnings before cuts
- Recovery possible

**Population:** ~5.2M combinations (33% of total)

---

### Family γ: **Lenient Enforcers** (Low Sensitivity)

**Characteristics:**
- DEVIATION_LIMIT = 0.30 (30%)
- But voltage decay reduces pressure
- Cut is selection pressure, not death
- System continues after cuts

**Behavior:**
- Lenient constraint enforcement
- Evolutionary pressure
- System resilience

**Population:** ~5.3M combinations (34% of total)

---

## Genus: Operational Model

### Genus I: **Pure Sovereigns** (Phylum A, Order 1, Family α)

**Characteristics:**
- Never read logs
- Never extend
- Fail fast
- Strict enforcement
- Values immutable

**Behavior Pattern:**
```
1. Bind nodes from root
2. Never read log (append-only truth)
3. Cut on any deviation
4. System stops on first cut
5. Log is post-mortem artifact
```

**Representative Species:** ~50K combinations

**Example Implementation:**
- Q1: A1 (Never read)
- Q2: A2 (Analysis tool)
- Q3: A1 (No decay)
- Q4: B1 (System stops)
- Q5: A1 (Never extend)
- Q6: A1 (XOR is good enough)
- Q7: A1 (Immutable)
- Q8: A1 (Fail fast)

---

### Genus II: **External Analysts** (Phylum B, Order 2, Family β)

**Characteristics:**
- Read logs externally
- Can fork system
- Minimal error handling
- Moderate enforcement
- Values can change

**Behavior Pattern:**
```
1. Bind nodes from root
2. Read log via external tools
3. Analyze patterns externally
4. Fork if values change
5. Graceful error handling
```

**Representative Species:** ~50K combinations

**Example Implementation:**
- Q1: B2 (Manual inspection)
- Q2: A2 (Analysis tool)
- Q3: B1 (Linear decay)
- Q4: A1 (Node dies, continues)
- Q5: B2 (Can fork)
- Q6: B3 (Document limitation)
- Q7: B1 (Update manifesto)
- Q8: B1 (Check critical only)

---

### Genus III: **Implicit Operators** (Phylum C, Order 3, Family γ)

**Characteristics:**
- Read logs implicitly
- Final is relative
- Decay is implicit
- Lenient enforcement
- Operations are implicit

**Behavior Pattern:**
```
1. Bind nodes from root
2. Read via project() or cut()
3. Decay via random walk
4. Cut is selection pressure
5. System evolves
```

**Representative Species:** ~50K combinations

**Example Implementation:**
- Q1: C2 (Read via project)
- Q2: C1 (Used by cut internally)
- Q3: C1 (Random walk is decay)
- Q4: C3 (Selection pressure)
- Q5: C1 (Final for purpose)
- Q6: A1 (XOR is good enough)
- Q7: C2 (Until manifesto changes)
- Q8: A1 (Fail fast)

---

### Genus IV: **Hybrid Pragmatists** (Mixed Phylum, Order 2, Family β)

**Characteristics:**
- Mix of approaches
- Pragmatic choices
- Balanced enforcement
- Flexible but minimal

**Behavior Pattern:**
```
1. Bind nodes from root
2. Read logs as needed (external or implicit)
3. Moderate decay
4. Moderate enforcement
5. Can fork or extend contextually
```

**Representative Species:** ~50K combinations

**Example Implementation:**
- Q1: B1 (External script)
- Q2: B2 (Philosophical completeness)
- Q3: B2 (Decay on bind)
- Q4: C2 (Checkpoint)
- Q5: B1 (Final until needed)
- Q6: A2 (XOR is placeholder)
- Q7: B2 (Fork with new manifesto)
- Q8: B2 (Error = exit code)

---

## Species: Specific Implementations

### Species Examples (One per Genus)

#### Species I-A: **Absolute Sovereign**
- **Genus:** Pure Sovereigns
- **Full Profile:**
  - Q1: A1 (Never read)
  - Q2: A1 (Debugging tool)
  - Q3: A1 (No decay)
  - Q4: B1 (System stops)
  - Q5: A1 (Never extend)
  - Q6: A1 (XOR good enough)
  - Q7: A1 (Immutable)
  - Q8: A1 (Fail fast)

**Problem-Solving Approach:**
- Strict adherence to manifesto
- No analysis of history
- Fail immediately on deviation
- System is fixed and immutable

---

#### Species II-B: **External Analyst**
- **Genus:** External Analysts
- **Full Profile:**
  - Q1: B2 (Manual inspection)
  - Q2: A2 (Analysis tool)
  - Q3: B1 (Linear decay)
  - Q4: A1 (Node dies, continues)
  - Q5: B2 (Can fork)
  - Q6: B3 (Document limitation)
  - Q7: B1 (Update manifesto)
  - Q8: B1 (Check critical only)

**Problem-Solving Approach:**
- Analyze logs externally
- Fork system for evolution
- Moderate error handling
- Values can update

---

#### Species III-C: **Implicit Evolver**
- **Genus:** Implicit Operators
- **Full Profile:**
  - Q1: C2 (Read via project)
  - Q2: C1 (Used by cut)
  - Q3: C1 (Random walk decay)
  - Q4: C3 (Selection pressure)
  - Q5: C1 (Final for purpose)
  - Q6: A1 (XOR good enough)
  - Q7: C2 (Until manifesto changes)
  - Q8: A1 (Fail fast)

**Problem-Solving Approach:**
- Implicit operations
- Evolutionary pressure
- Context-dependent finality
- Natural selection model

---

#### Species IV-D: **Hybrid Pragmatist**
- **Genus:** Hybrid Pragmatists
- **Full Profile:**
  - Q1: B1 (External script)
  - Q2: B2 (Philosophical completeness)
  - Q3: B2 (Decay on bind)
  - Q4: C2 (Checkpoint)
  - Q5: B1 (Final until needed)
  - Q6: A2 (XOR placeholder)
  - Q7: B2 (Fork with new manifesto)
  - Q8: B2 (Error = exit code)

**Problem-Solving Approach:**
- Balanced pragmatism
- Flexible but minimal
- Moderate enforcement
- Can evolve when needed

---

## Agent Behavior Matrix

### How Each Genus Solves Problems

| Problem Type | Pure Sovereign | External Analyst | Implicit Evolver | Hybrid Pragmatist |
|--------------|----------------|------------------|------------------|-------------------|
| **Debugging** | Never debug (fail fast) | External analysis tools | Implicit via project() | External + implicit |
| **Evolution** | Never evolve (immutable) | Fork system | Natural selection | Contextual evolution |
| **Error Recovery** | No recovery (fail fast) | Graceful shutdown | Selection pressure | Moderate handling |
| **Constraint Violation** | Immediate cut | Warning then cut | Evolutionary pressure | Checkpoint system |
| **Value Changes** | Impossible (immutable) | Update manifesto | Until manifesto changes | Fork with new values |
| **Log Analysis** | Never read | External tools | Via project() | External + implicit |
| **Voltage Management** | No decay | Linear decay | Random walk decay | Decay on bind |
| **Extensibility** | Never extend | Can fork | Context-dependent | Final until needed |

---

## Population Distribution

### By Phylum

```
Phylum A (Sovereign Minimalists):    2,624,400 (17%)
Phylum B (Pragmatic Minimalists):    6,561,000 (42%)
Phylum C (Adaptive Minimalists):     6,561,000 (42%)
```

### By Class

```
Class I (Fail-Fast):                 7,873,200 (50%)
Class II (Graceful Degradation):     7,873,200 (50%)
```

### By Order

```
Order 1 (Immutable):                 2,624,400 (17%)
Order 2 (Forkable):                  2,187,000 (14%)
Order 3 (Contextual):                2,187,000 (14%)
```

### By Family

```
Family α (Strict):                   5,248,800 (33%)
Family β (Moderate):                 5,248,800 (33%)
Family γ (Lenient):                  5,248,800 (34%)
```

---

## Practical Implementation

### Representative Archetypes (50-100 agents)

Instead of 15.7M unique agents, we create:

1. **4 Genus-level archetypes** (one per Genus)
2. **12 Family-level variations** (3 families × 4 genera)
3. **24 Order-level variations** (3 orders × 8 combinations)
4. **50-100 Species-level examples** (specific implementations)

**Total:** ~50-100 representative agents covering the full space

### Clustering Strategy

**Level 1: Phylum (3 clusters)**
- Cluster by philosophical stance
- ~5.2M combinations per cluster

**Level 2: Class (2 sub-clusters per Phylum)**
- Cluster by error handling
- ~2.6M combinations per sub-cluster

**Level 3: Order (3 sub-clusters per Class)**
- Cluster by extensibility
- ~875K combinations per sub-cluster

**Level 4: Family (3 sub-clusters per Order)**
- Cluster by constraint enforcement
- ~292K combinations per sub-cluster

**Level 5: Genus (4 sub-clusters per Family)**
- Cluster by operational model
- ~73K combinations per sub-cluster

**Level 6: Species (sample from Genus)**
- Sample 1-10 representatives per Genus
- Total: 50-100 agents

---

## Agent Interaction Model

### How Different Genera Interact

**Pure Sovereign + External Analyst:**
- Sovereign creates immutable system
- Analyst forks and analyzes
- Analyst provides insights to Sovereign
- Sovereign rejects (immutable) or Analyst evolves independently

**Implicit Evolver + Hybrid Pragmatist:**
- Evolver provides natural selection pressure
- Pragmatist provides contextual adaptation
- Both evolve, but different mechanisms
- Can hybridize (create new Genus)

**All Genera:**
- Each solves problems differently
- Diversity provides robustness
- Natural selection favors effective approaches
- Evolution creates new genera over time

---

## Evolution Model

### How New Genera Emerge

**Mechanism 1: Hybridization**
- Two genera combine approaches
- New Genus with mixed characteristics
- Example: Pure Sovereign + External Analyst = "Sovereign Analyst"

**Mechanism 2: Mutation**
- Single answer changes in Species
- Creates new Species
- If successful, creates new Genus

**Mechanism 3: Selection Pressure**
- Environment favors certain approaches
- Successful genera proliferate
- Unsuccessful genera die out

**Mechanism 4: Contextual Adaptation**
- Genera adapt to specific contexts
- New specialized genera emerge
- Example: "Debugging Specialist" (high Q2-A1 usage)

---

## Implementation Recommendations

### For HUMMBL Framework

1. **Create 4 Base Genera** (one per Genus)
   - Pure Sovereign
   - External Analyst
   - Implicit Evolver
   - Hybrid Pragmatist

2. **Allow User Selection** (choose archetype)
   - User picks preferred Genus
   - System instantiates that archetype
   - Can switch archetypes (evolution)

3. **Enable Hybridization** (mix approaches)
   - User can combine characteristics
   - Creates custom archetype
   - System tracks new combinations

4. **Natural Selection** (evolution over time)
   - Track which archetypes solve problems best
   - Favor successful approaches
   - Evolve toward effectiveness

---

## Summary

**Total Possible Combinations:** 15,746,400  
**Practical Representation:** 50-100 archetypes  
**Hierarchy Levels:** 6 (Kingdom → Phylum → Class → Order → Family → Genus → Species)  
**Key Differentiators:**
- Philosophical stance (3 phyla)
- Error handling (2 classes)
- Extensibility (3 orders)
- Constraint enforcement (3 families)
- Operational model (4 genera)

**Result:** Biological taxonomy of AI agents, each solving problems differently based on their answer set profile.

---

**Last Updated:** 2025-11-18  
**Status:** Complete Taxonomy  
**Next Steps:** Implement 4 base genera as proof of concept

