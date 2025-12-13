# Case Study 1: Quick Operator Sequence Reference

**For use during recording**

---

## The 10 Models (In Order)

### 1. P02 – Stakeholder Mapping
**Question**: Who cares about this system and what do they value?

**Actions**:
- List stakeholders: Users, Product, Infrastructure, Business
- Define success criteria for each
- Note priorities (latency, reliability, cost)

**Output**: Stakeholder map

---

### 2. DE07 – Bottleneck Identification
**Question**: Where are the system constraints?

**Actions**:
- Identify suspected bottlenecks (LLM, DB, cache, gateway)
- Check for high utilization
- Look for queueing behavior

**Output**: List of candidate bottlenecks

---

### 3. DE06 – Failure Mode Analysis
**Question**: How can each bottleneck fail?

**Actions**:
- Enumerate failure modes per bottleneck:
  - Timeouts
  - Rate limits
  - Resource exhaustion
- Use IN02 – Premortem for worst cases

**Output**: Failure mode matrix

---

### 4. DE08 – Information Flow Tracing
**Question**: How does data/requests flow through the system?

**Actions**:
- Map request paths between services
- Identify long chains
- Find circular dependencies

**Output**: Flow diagram

---

### 5. CO03 – Pipeline / Flow Composition
**Question**: What are the explicit pipeline stages?

**Actions**:
- Define stages: Ingest → Embed → Recommend → Serve
- Mark parallel vs serial stages
- Identify dependencies

**Output**: Pipeline diagram

---

### 6. CO12 – Queues / Buffers
**Question**: Where should queues/buffers exist?

**Actions**:
- Identify existing queues
- Decide where queues *should* be
- Consider latency vs resilience

**Output**: Queue placement recommendations

---

### 7. RE06 – Feedback Loops
**Question**: What feedback loops exist?

**Actions**:
- Identify loops: retries, backpressure, scaling
- Label as stabilizing or destabilizing
- Note loop behavior

**Output**: Feedback loop diagram

---

### 8. SY04 – Cascades & Second-Order Effects
**Question**: How do failures propagate?

**Actions**:
- Trace failure propagation paths
- Identify cascade chains (LLM → Vector DB → Reco Engine → Gateway)
- Note second-order effects

**Output**: Cascade map

---

### 9. SY01 – System Topology
**Question**: What does the complete system look like?

**Actions**:
- Draw node-link graph
- Show services, dependencies, queues, loops, cascades
- Highlight bottlenecks and critical edges

**Output**: Complete system topology diagram

---

### 10. SY19 – Meta-Model Selection (Reflection)
**Question**: What worked and what's next?

**Actions**:
- Reflect on most useful models
- Consider what relationship graph would recommend next
- Note insights

**Output**: Reflection notes

---

## Quick Tips

- **Time per model**: 2-4 minutes each
- **Total sequence**: ~20-30 minutes
- **Draw as you go**: Diagrams are valuable
- **Think out loud**: Explain your reasoning
- **It's okay to pause**: Take time to think

---

**Print this or keep it open during recording!**

