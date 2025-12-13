# Case Study 1 Recording Checklist

**Case Study**: Multi-Service AI Recommendation System  
**Date**: [To be filled]  
**Target Length**: 20-40 minutes  
**Status**: Pre-Recording Preparation

---

## Pre-Recording Setup

### Materials Needed
- [ ] Problem brief printed or open on screen
- [ ] Architecture diagram (if available)
- [ ] Any relevant logs/metrics (if available)
- [ ] Screen recording software ready
- [ ] Audio/microphone tested
- [ ] HUMMBL operator reference (models list)
- [ ] Whiteboard/drawing tool for diagrams
- [ ] Note-taking app for artifacts

### Software Setup
- [ ] Screen recording software configured
  - Recommended: OBS, QuickTime (Mac), or Loom
  - Test recording for 30 seconds to verify quality
- [ ] Audio levels tested
- [ ] Screen resolution set (1920x1080 recommended)
- [ ] Browser tabs organized (brief, diagrams, notes)

### Environment
- [ ] Quiet space
- [ ] Good lighting (if using camera)
- [ ] Water/notes nearby
- [ ] Phone on silent

---

## Recording Script

### Introduction (2-3 minutes)
- [ ] Introduce the case study
- [ ] Explain the problem context
- [ ] State the goal: identify bottlenecks, cascades, and interventions
- [ ] Mention you'll be using 10 HUMMBL mental models

### Operator Sequence (20-30 minutes)

#### 1. P02 – Stakeholder Mapping (2-3 min)
- [ ] Identify stakeholders: Users, Product, Infrastructure, Business
- [ ] Define success criteria for each
- [ ] Note what "good" looks like (latency, reliability, cost)
- [ ] **Output**: Stakeholder map with criteria

#### 2. DE07 – Bottleneck Identification (2-3 min)
- [ ] List suspected bottlenecks: LLM, DB, cache, gateway
- [ ] Identify high utilization components
- [ ] Note queueing behavior
- [ ] **Output**: List of candidate bottlenecks

#### 3. DE06 – Failure Mode Analysis (2-3 min)
- [ ] For each bottleneck, enumerate failure modes:
  - Timeouts
  - Rate limits
  - Resource exhaustion
- [ ] Optionally use IN02 – Premortem for worst-case scenarios
- [ ] **Output**: Failure mode matrix

#### 4. DE08 – Information Flow Tracing (3-4 min)
- [ ] Map data/request flow between services
- [ ] Identify long chains
- [ ] Find potential circular dependencies
- [ ] **Output**: Flow diagram

#### 5. CO03 – Pipeline / Flow Composition (2-3 min)
- [ ] Turn flows into explicit pipeline stages:
  - Ingest → Embed → Recommend → Serve
- [ ] Mark parallel vs serial stages
- [ ] **Output**: Pipeline diagram

#### 6. CO12 – Queues / Buffers (2-3 min)
- [ ] Identify existing queues/buffers
- [ ] Decide where queues *should* exist
- [ ] Consider latency vs resilience tradeoffs
- [ ] **Output**: Queue placement recommendations

#### 7. RE06 – Feedback Loops (2-3 min)
- [ ] Identify feedback loops:
  - Retries
  - Backpressure
  - Scaling policies
- [ ] Label as stabilizing or destabilizing
- [ ] **Output**: Feedback loop diagram

#### 8. SY04 – Cascades & Second-Order Effects (3-4 min)
- [ ] Trace failure propagation paths
- [ ] Identify cascade chains:
  - LLM → Vector DB → Reco Engine → Gateway
- [ ] Note second-order effects
- [ ] **Output**: Cascade map

#### 9. SY01 – System Topology (3-4 min)
- [ ] Draw system as node-link graph
- [ ] Show services, dependencies, queues, loops, cascades
- [ ] Highlight bottlenecks and critical edges
- [ ] **Output**: Complete system topology diagram

#### 10. SY19 – Meta-Model Selection (Reflection) (2-3 min)
- [ ] Reflect: Which models were most useful?
- [ ] Consider: What would relationship graph recommend next?
  - SY13 (Incentives)?
  - RE10 (Experimentation)?
- [ ] **Output**: Reflection notes

### Outcomes & Metrics (5-10 minutes)
- [ ] Summarize key findings
- [ ] List top 3-7 interventions
- [ ] Estimate time saved vs unstructured approach
- [ ] Note clarity/completeness gains

### Reflection (5 minutes)
- [ ] What worked well in the operator sequence?
- [ ] What felt heavy or awkward?
- [ ] Where did relationship graph suggest non-obvious steps?
- [ ] What would you do differently?

---

## Artifacts to Capture

During or after recording, ensure you have:

- [ ] Annotated architecture diagram
- [ ] Operator log (which models used, in what order)
- [ ] Intervention list (3-7 concrete changes)
- [ ] System topology diagram
- [ ] Flow diagrams
- [ ] Reflection notes

---

## Post-Recording Tasks

### Immediate (Same Day)
- [ ] Save video file with descriptive name
- [ ] Create backup copy
- [ ] Export any diagrams created
- [ ] Save notes/artifacts

### Within 1-2 Days
- [ ] Review video for quality
- [ ] Extract key timestamps
- [ ] Begin written case study using template
- [ ] Create annotated diagrams from video

### Within 1 Week
- [ ] Complete written case study
- [ ] Publish to `docs/case-studies/case-study1-multi-service-ai.md`
- [ ] Update CaseStudiesPage component
- [ ] Create social media thread
- [ ] Update checklist status

---

## Tips for Recording

1. **Pace**: Don't rush. Take time to think through each model.
2. **Visuals**: Draw diagrams as you go - they're valuable artifacts.
3. **Pauses**: It's okay to pause and think. You can edit later if needed.
4. **Narration**: Explain your thinking out loud - that's the value.
5. **Artifacts**: Capture everything you create (diagrams, lists, notes).

---

## Success Criteria

After recording, you should have:
- ✅ Clear map of system showing bottlenecks, queues, cascades
- ✅ Ranked intervention list
- ✅ Feeling that the sequence was more structured than ad-hoc debugging
- ✅ Video ready for post-processing
- ✅ All artifacts captured

---

**Ready to record when all pre-recording items are checked!**

