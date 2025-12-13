# Case Study 1 Recording Script

**System**: StreamFlow AI  
**Target Length**: 30-40 minutes  
**Format**: Screen recording with voiceover

---

## Pre-Recording Setup

**Have Open**:
- [ ] StreamFlow AI system summary (`case-study1-system-summary.md`)
- [ ] Architecture diagram (`case-study1-architecture-diagram.md`)
- [ ] Operator sequence quick reference (`case-study1-operator-sequence-quick-reference.md`)
- [ ] Whiteboard/drawing tool (Miro, Excalidraw, or paper)
- [ ] Brief overview document

**Screen Layout Suggestion**:
- Left: System summary / architecture diagram
- Center: Drawing tool / whiteboard
- Right: Notes / operator reference

---

## Script

### [00:00 - 02:00] Introduction

**[Show system summary on screen]**

"Welcome to Case Study 1. Today I'm going to analyze StreamFlow AI, a multi-service AI recommendation system for a video streaming platform. Think Netflix or YouTube recommendations.

**The Problem**: 
- 50 million users, 10 million content items
- During peak hours - 8PM to 11PM - we're seeing latency spikes from 200ms to over 2 seconds
- Requests are timing out, error rates are up to 5%
- When the LLM service has issues, everything seems to break
- Cache invalidation causes system-wide slowdowns
- We know there are cascades happening, but we don't have a clear map

**The Goal**: 
In this session, I'm going to use 10 HUMMBL mental models to systematically identify bottlenecks, map cascade paths, and produce a prioritized list of interventions.

Let's start."

---

### [02:00 - 05:00] Model 1: P02 – Stakeholder Mapping

**[Switch to drawing tool, create stakeholder map]**

"First, I'm applying **P02 - Stakeholder Mapping**. This helps me understand who cares about this system and what success looks like for each stakeholder.

**Who are the stakeholders?**

1. **End Users** - They want fast, relevant recommendations. Success = recommendations load quickly, are personalized, help them discover content they love.

2. **Product Team** - They want high engagement. Success = users click on recommendations, watch recommended content, stay on platform longer.

3. **Infrastructure Team** - They want system reliability. Success = low error rates, predictable latency, no outages, cost efficiency.

4. **Business** - They want revenue growth. Success = recommendations drive content consumption, increase subscription retention, reduce churn.

**What does 'good' look like?**
- Users: <200ms response time, personalized results
- Product: 30% of views from recommendations, high click-through
- Infrastructure: <0.1% error rate, predictable costs
- Business: Recommendations drive retention and revenue

**Why this matters**: Understanding these perspectives helps me prioritize what to optimize. If users care about speed, I need to focus on latency bottlenecks. If business cares about engagement, I need to ensure recommendations stay relevant even when systems are degraded.

**[Draw stakeholder map with success criteria]**

Okay, now I understand the context. Let's dive into the technical system."

---

### [05:00 - 08:00] Model 2: DE07 – Bottleneck Identification

**[Show architecture diagram]**

"Next, **DE07 - Bottleneck Identification**. I need to find where the system is constrained.

**Where do I suspect bottlenecks?**

Looking at the architecture, I can identify several candidate bottlenecks:

1. **LLM Service** - Rate limited to 500 requests per minute. During peak hours, we're hitting this limit. This is a hard constraint.

2. **Vector DB** - Query latency is growing. Started at 150ms, now up to 1 second during peak. The index has 10 million vectors and keeps growing.

3. **Recommendation Engine** - CPU-bound, single instance. Queue depth can reach 1000+ requests. This is clearly a bottleneck.

4. **User Profile Database** - Queries taking 50ms to 500ms. No read replicas. During peak, this gets slow.

5. **Cache** - Memory pressure, hit rate drops from 80% to 20% during invalidation events.

**Which components show high utilization?**
- Recommendation Engine: CPU at 100% during peak
- LLM Service: Hitting rate limits (500/min)
- Vector DB: Query latency spiking
- User Profile DB: Query latency increasing

**Initial bottleneck list:**
1. LLM Service (rate limit)
2. Recommendation Engine (CPU saturation)
3. Vector DB (query latency)
4. User Profile DB (query latency)
5. Cache (invalidation storms)

**[Draw/annotate architecture diagram with bottlenecks]**

Now I have my candidate bottlenecks. Let me analyze how each can fail."

---

### [08:00 - 11:00] Model 3: DE06 – Failure Mode Analysis

**[Create failure mode matrix]**

"**DE06 - Failure Mode Analysis**. For each bottleneck, I need to enumerate how it can fail.

**LLM Service failure modes:**
1. **Rate limit exceeded** - Returns 429, blocks all requests
2. **High latency** - Takes 2+ seconds instead of 200ms
3. **Timeout** - Request times out after 30 seconds
4. **Cost spike** - Usage exceeds budget, service disabled
5. **Model unavailability** - OpenAI service down

**Vector DB failure modes:**
1. **Query timeout** - Query takes >2s, times out
2. **Index update lag** - New content not searchable immediately
3. **Capacity limits** - Index size limits reached
4. **Network issues** - Connection failures to Pinecone

**Recommendation Engine failure modes:**
1. **CPU saturation** - 100% CPU, can't process new requests
2. **Queue overflow** - Queue depth >1000, rejects new requests
3. **Memory exhaustion** - Out of memory, crashes
4. **Model loading failure** - Can't load ML model

**User Profile DB failure modes:**
1. **Query timeout** - Complex joins timeout
2. **Connection pool exhaustion** - No available connections
3. **Lock contention** - Writes block reads
4. **Replication lag** - If we had replicas, they'd be stale

**Cache failure modes:**
1. **Memory pressure** - Evicts keys aggressively
2. **Invalidation storm** - Broadcast invalidate causes thundering herd
3. **Cache stampede** - All requests miss simultaneously
4. **Cluster split** - Redis cluster issues

**[Create failure mode matrix table]**

I can also use **IN02 - Premortem** thinking here: What would guarantee failure? If LLM is down AND cache is empty AND Vector DB is slow, the system would completely fail. That's a worst-case scenario to plan for.

Now I understand how each component can fail. Let me trace how data flows through the system."

---

### [11:00 - 15:00] Model 4: DE08 – Information Flow Tracing

**[Draw data flow diagram]**

"**DE08 - Information Flow Tracing**. I need to map how requests and data move through the system.

**Request Flow - Happy Path (Cache Hit):**
1. User request → API Gateway
2. Gateway → Auth Service (validate token, 20ms)
3. Gateway → User Profile Service (get profile, 50ms, cached)
4. Gateway → Recommendation Engine
5. Engine → Cache (check recommendations, 5ms, HIT)
6. Return to user (Total: ~75ms) ✅

**Request Flow - Cache Miss:**
1. User request → API Gateway
2. Gateway → Auth Service (20ms)
3. Gateway → User Profile Service (50ms)
4. Gateway → Recommendation Engine
5. Engine → Cache (MISS, 5ms)
6. Engine → Vector DB (similarity search, 200ms)
7. Engine → LLM Service (get descriptions, 400ms)
8. Engine → Run ML model (150ms)
9. Engine → Cache (store result, 10ms)
10. Return to user (Total: ~835ms) ⚠️

**Long Chains I See:**
- Gateway → Auth → Profile → Engine → Vector DB → LLM → Engine → Cache
- That's 7 hops! Each hop adds latency and failure points.

**Potential Circular Flows:**
- If Engine fails, Gateway retries → More load → Engine fails worse
- If Cache misses, more DB load → DB slow → More cache misses

**Information Dependencies:**
- Engine depends on: User Profile, Vector DB, LLM, Cache
- LLM depends on: Content metadata (from Content Service)
- Vector DB depends on: Content Pipeline (for embeddings)

**[Draw flow diagram showing all dependencies]**

I can see the flow now. There are long chains and potential circular dependencies. Let me turn this into explicit pipeline stages."

---

### [15:00 - 18:00] Model 5: CO03 – Pipeline / Flow Composition

**[Draw pipeline diagram]**

"**CO03 - Pipeline / Flow Composition**. I'm going to turn these flows into explicit pipeline stages.

**Recommendation Pipeline Stages:**

1. **Authentication Stage** (Serial)
   - Auth Service validates token
   - Must complete before proceeding
   - Can be cached, but still a stage

2. **Profile Retrieval Stage** (Serial)
   - Get user profile and preferences
   - Required for personalization
   - Can be parallel with content lookup if we restructure

3. **Content Discovery Stage** (Can be parallelized)
   - Vector DB similarity search
   - Content Service metadata lookup
   - These could run in parallel

4. **Enrichment Stage** (Serial, but could be optimized)
   - LLM Service generates descriptions
   - This is the slowest stage
   - Could be optional or cached

5. **Ranking Stage** (Serial)
   - Recommendation Engine runs ML model
   - Combines all inputs
   - CPU-bound, can't parallelize easily

6. **Caching Stage** (Serial)
   - Store result in cache
   - Return to user

**Serial vs Parallel:**
- **Serial**: Auth → Profile → Ranking → Cache (must be in order)
- **Parallel Opportunities**: Vector DB + Content Service could run simultaneously
- **Bottleneck**: LLM Service is serial and slow

**Pipeline Optimization Opportunities:**
- Parallelize Vector DB and Content Service lookups
- Make LLM optional (use cached descriptions)
- Pre-compute some recommendations

**[Draw pipeline with stages marked as serial/parallel]**

The pipeline is clear now. I can see where stages are serial (creating bottlenecks) and where we could parallelize. Let me think about where queues and buffers should exist."

---

### [18:00 - 21:00] Model 6: CO12 – Queues / Buffers

**[Annotate architecture with queue locations]**

"**CO12 - Queues / Buffers**. I need to identify where queues exist today and where they *should* exist.

**Current Queues:**
1. **Recommendation Engine internal queue** - 0 to 1000 depth
   - Exists but no limits, can overflow
   - No visibility into queue depth

2. **Notification Service queue** (RabbitMQ)
   - Can backup during peak
   - Not critical path, but shows queue pattern

3. **Content Pipeline queue** (Kafka)
   - Can backlog during content upload spikes
   - Background processing

**Missing Queues (Where they should exist):**

1. **Between Gateway and Recommendation Engine** ❌
   - **Why**: Decouples gateway from engine
   - **Benefit**: Gateway doesn't timeout waiting for engine
   - **Tradeoff**: Adds latency, but prevents cascades
   - **Recommendation**: Add queue with max depth limit

2. **Between Engine and LLM Service** ❌
   - **Why**: LLM is rate limited, engine shouldn't wait
   - **Benefit**: Engine can process other requests while LLM queue processes
   - **Tradeoff**: More complexity, but prevents LLM cascade
   - **Recommendation**: Add queue with timeout

3. **Between Engine and Vector DB** ❌
   - **Why**: Vector DB can be slow, shouldn't block engine
   - **Benefit**: Engine can batch queries, handle Vector DB slowness
   - **Tradeoff**: Adds complexity
   - **Recommendation**: Consider queue or connection pool

**Queue Design Considerations:**
- **Latency vs Resilience**: Queues add latency but prevent cascades
- **Queue Limits**: Need max depth to prevent unbounded growth
- **Timeouts**: Queues need timeouts to prevent indefinite waits
- **Priority**: User-facing requests should have priority

**[Draw queue locations on architecture]**

I can see where queues would help decouple services and prevent cascades. Now let me identify feedback loops."

---

### [21:00 - 24:00] Model 7: RE06 – Feedback Loops

**[Draw feedback loop diagram]**

"**RE06 - Feedback Loops**. I need to identify explicit and implicit feedback loops.

**Explicit Feedback Loops:**

1. **Retry Loop** (Destabilizing)
   - Service timeout → User retries → More load → More timeouts → More retries
   - **Amplification**: Exponential growth
   - **Stabilizing Factor**: Rate limiting at gateway (but not effective enough)
   - **Fix**: Better rate limiting, exponential backoff

2. **Cache Miss Cascade** (Destabilizing)
   - Cache miss → DB load → DB slow → More cache misses → More DB load
   - **Amplification**: Linear growth
   - **Stabilizing Factor**: None currently
   - **Fix**: Cache warming, gradual invalidation

3. **LLM Rate Limit Loop** (Destabilizing)
   - LLM rate limit → Engine waits → Queue fills → More requests → More rate limits
   - **Amplification**: Linear growth
   - **Stabilizing Factor**: None (engine has no timeout)
   - **Fix**: Timeout, fallback, queue limits

**Implicit Feedback Loops:**

4. **Scaling Policy Loop** (Could be stabilizing or destabilizing)
   - High CPU → Auto-scale up → More instances → Lower CPU
   - **Current**: Not implemented, but if it were, could help
   - **Risk**: If scaling is slow, could amplify problems

5. **Circuit Breaker Loop** (Stabilizing - Not Implemented)
   - Service failures → Circuit opens → Requests rejected → Service recovers → Circuit closes
   - **Would prevent**: Cascading failures
   - **Status**: Not implemented, should be

**Loop Classification:**
- **Stabilizing**: Circuit breaker (not implemented)
- **Destabilizing**: Retry loop, cache miss cascade, LLM rate limit loop

**[Draw feedback loops with arrows showing direction]**

The feedback loops are clear. Some are making problems worse. Now let me trace how failures cascade through the system."

---

### [24:00 - 28:00] Model 8: SY04 – Cascades & Second-Order Effects

**[Draw cascade map]**

"**SY04 - Cascades & Second-Order Effects**. I need to trace how failures propagate.

**Cascade Scenario 1: LLM Rate Limit**

1. **Trigger**: LLM service hits rate limit (500 req/min)
2. **Primary Effect**: LLM returns 429 errors
3. **First-Order Cascade**:
   - Recommendation Engine waits for LLM (no timeout!)
   - Engine queue fills up (1000+ requests)
   - Engine CPU saturates (100%)
4. **Second-Order Cascade**:
   - New requests to Engine timeout immediately
   - Gateway sees Engine timeouts
   - Gateway returns 504 errors to users
5. **Third-Order Cascade**:
   - Users see errors, retry requests
   - More load on system
   - Cascade gets worse
6. **Cascade Path**: LLM → Engine → Gateway → Users → More Load → Worse Cascade

**Cascade Scenario 2: Cache Invalidation Storm**

1. **Trigger**: Popular new content added
2. **Primary Effect**: Cache invalidation broadcast to all nodes
3. **First-Order Cascade**:
   - All cached recommendations invalidated
   - Cache hit rate drops from 80% to 20%
4. **Second-Order Cascade**:
   - Thousands of cache misses flood Vector DB
   - Vector DB query latency spikes (200ms → 1s)
   - Vector DB queries queue up
5. **Third-Order Cascade**:
   - Recommendation Engine blocked waiting for Vector DB
   - Engine queue fills
   - Engine CPU saturates
6. **Cascade Path**: New Content → Cache Invalidate → Cache Misses → Vector DB Overload → Engine Overload → System Slowdown

**Cascade Scenario 3: Retry Storm**

1. **Trigger**: Service timeout (any service)
2. **Primary Effect**: User sees error
3. **First-Order Cascade**:
   - User retries request
   - More load on already-failing service
4. **Second-Order Cascade**:
   - Service fails worse under more load
   - More users see errors
   - More retries
5. **Third-Order Cascade**:
   - Exponential growth in requests
   - System completely overwhelmed
6. **Cascade Path**: Timeout → Retry → More Load → More Timeouts → Exponential Growth

**Second-Order Effects:**
- When LLM is slow, not only are recommendations delayed, but users refresh the page, creating more load
- When cache is invalidated, not only do we have cache misses, but the timing creates a thundering herd
- When Engine is slow, not only do requests timeout, but retries create a retry storm

**[Draw cascade map showing all three scenarios]**

I can see the cascade paths clearly now. They all follow similar patterns: one service fails, downstream services get overwhelmed, and the problem amplifies. Let me create a complete system topology."

---

### [28:00 - 32:00] Model 9: SY01 – System Topology

**[Draw complete system topology graph]**

"**SY01 - System Topology**. I'm going to draw the complete system as a node-link graph.

**[Draw nodes for each service]**

**Nodes (Services):**
- API Gateway
- Auth Service
- User Profile Service
- Content Service
- Content Pipeline
- Vector DB
- LLM Service
- Recommendation Engine
- Cache
- Analytics Service
- Notification Service

**[Draw edges showing dependencies]**

**Edges (Dependencies):**
- Gateway → Auth, User Profile, Content, Engine
- Engine → Cache, Vector DB, LLM, User Profile
- Content Pipeline → Vector DB
- Engine → Analytics, Notification

**[Highlight critical paths]**

**Critical Paths:**
1. Gateway → Auth → Profile → Engine → Cache (happy path)
2. Gateway → Engine → Vector DB → LLM → Engine (cache miss path)

**[Mark bottlenecks]**
- LLM Service: RED (rate limited)
- Recommendation Engine: RED (CPU bound, queue overflow)
- Vector DB: YELLOW (growing latency)
- User Profile DB: YELLOW (slow queries)
- Cache: YELLOW (invalidation storms)

**[Mark cascade paths]**
- LLM → Engine → Gateway (red arrows)
- Cache → Vector DB → Engine (orange arrows)
- Any service → Retry storm (dashed arrows)

**[Mark missing queues]**
- Gateway → Engine: DASHED LINE (should have queue)
- Engine → LLM: DASHED LINE (should have queue)

**[Mark feedback loops]**
- Retry loop: Circular arrow
- Cache miss cascade: Circular arrow

**[Complete topology diagram]**

This topology shows me the complete picture: services, dependencies, bottlenecks, cascades, and where interventions are needed. Now let me reflect on what I've learned."

---

### [32:00 - 35:00] Model 10: SY19 – Meta-Model Selection (Reflection)

**[Review the models used]**

"**SY19 - Meta-Model Selection**. Let me reflect on which models were most useful and what the relationship graph would recommend next.

**Models I Used (In Order):**
1. P02 - Stakeholder Mapping
2. DE07 - Bottleneck Identification
3. DE06 - Failure Mode Analysis
4. DE08 - Information Flow Tracing
5. CO03 - Pipeline / Flow Composition
6. CO12 - Queues / Buffers
7. RE06 - Feedback Loops
8. SY04 - Cascades & Second-Order Effects
9. SY01 - System Topology
10. SY19 - Meta-Model Selection (this one)

**Which models were most useful?**

1. **DE07 (Bottleneck Identification)** - Immediately gave me focus. Without this, I'd be guessing.

2. **SY04 (Cascades)** - This revealed the real problems. The cascades are worse than individual bottlenecks.

3. **CO12 (Queues)** - This showed me where to intervene. Adding queues is a concrete fix.

4. **RE06 (Feedback Loops)** - Understanding the loops helped me see why problems amplify.

**What would the relationship graph recommend next?**

Looking at the relationship graph, if I wanted to go deeper:

- **SY13 (Incentive Architecture)** - Why are these services designed this way? What incentives led to these choices?

- **RE10 (Experimentation)** - How would I test these interventions? What experiments would validate the fixes?

- **DE01 (Root Cause)** - What's the root cause? Is it architecture? Is it scale? Is it design decisions?

- **IN04 (Simplification)** - Could I simplify this system? Remove some services? Combine some?

- **CO01 (Composition Planning)** - How would I redesign this system? What would a better composition look like?

**Insights from the sequence:**
- The models built on each other naturally
- Starting with stakeholders (P02) gave context
- Decomposition models (DE) helped break down the problem
- Composition models (CO) helped see the structure
- Systems models (SY) revealed the big picture

**What worked well:**
- The sequence felt natural - each model informed the next
- Drawing diagrams helped me see patterns
- The relationship graph would have suggested similar models

**What felt heavy:**
- Some models overlapped (DE08 and CO03 both looked at flows)
- Could have combined some steps

**Surprises:**
- The cascade scenarios were more complex than I expected
- The missing queues were obvious once I mapped the flows
- The feedback loops explained why problems get worse

This systematic approach was definitely faster and more thorough than ad-hoc debugging."

---

### [35:00 - 40:00] Outcomes & Summary

**[Create intervention list]**

"Let me summarize what I've discovered and create a prioritized intervention list.

**Key Findings:**

1. **5 Main Bottlenecks**: LLM Service, Recommendation Engine, Vector DB, User Profile DB, Cache
2. **3 Major Cascade Scenarios**: LLM rate limit, Cache invalidation storm, Retry storm
3. **Missing Queues**: Between Gateway-Engine and Engine-LLM
4. **Destabilizing Loops**: Retry storm, cache miss cascade, LLM rate limit loop
5. **No Circuit Breakers**: System has no protection against cascades

**Prioritized Intervention List:**

**High Impact, Low Effort:**
1. **Add timeout and fallback for LLM Service** - Engine shouldn't wait indefinitely
2. **Implement circuit breakers** - Prevent cascade propagation
3. **Add queue limits** - Prevent queue overflow

**High Impact, Medium Effort:**
4. **Add queue between Gateway and Engine** - Decouple gateway from engine
5. **Add queue between Engine and LLM** - Handle LLM rate limits gracefully
6. **Implement gradual cache invalidation** - Prevent thundering herd

**High Impact, High Effort:**
7. **Add read replicas for User Profile DB** - Reduce database contention
8. **Add query result caching for Vector DB** - Reduce Vector DB load
9. **Implement request prioritization** - Prioritize user-facing requests

**Time Saved:**
- Without this systematic approach: Probably 4-6 hours of ad-hoc debugging, trial and error
- With HUMMBL: ~40 minutes of structured analysis
- **Time saved: 3-5 hours**

**Clarity Gains:**
- Clear map of bottlenecks, cascades, and interventions
- Understanding of why problems occur
- Prioritized action plan

**Completeness:**
- Discovered cascade scenarios that weren't obvious
- Identified missing queues that weren't in the original design
- Found feedback loops that explain problem amplification

This systematic approach gave me a complete picture and a clear action plan. Much better than guessing!"

---

### [40:00 - 42:00] Closing

"**Summary:**

I've analyzed StreamFlow AI using 10 HUMMBL mental models and identified:
- 5 main bottlenecks
- 3 major cascade scenarios  
- 9 prioritized interventions
- Multiple feedback loops and failure modes

The systematic approach was faster and more thorough than ad-hoc debugging, and gave me a clear action plan.

**Next Steps:**
- Implement the high-impact, low-effort interventions first
- Test and measure improvements
- Iterate based on results

Thanks for watching! This is Case Study 1 using the HUMMBL Base120 framework."

---

## Post-Recording Checklist

- [ ] Save video file
- [ ] Export diagrams created
- [ ] Save notes and artifacts
- [ ] Review video for quality
- [ ] Extract key timestamps
- [ ] Begin written case study

---

## Tips During Recording

1. **Pause when needed** - It's okay to think out loud
2. **Draw as you go** - Diagrams are valuable artifacts
3. **Explain your thinking** - The reasoning is as important as the results
4. **Use the system summary** - Reference it when needed
5. **Be natural** - Don't read the script verbatim, use it as a guide

---

**Total Target Time: 35-42 minutes**

**Good luck with your recording!**

