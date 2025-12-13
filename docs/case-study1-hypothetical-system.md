# Case Study 1: Hypothetical System - "StreamFlow AI"

**System Name**: StreamFlow AI  
**Type**: AI-Powered Content Streaming Recommendation Platform  
**Purpose**: Personalized content recommendations for a video streaming service (Netflix/YouTube-style)

---

## System Overview

StreamFlow AI is a content recommendation system that helps users discover videos, shows, and content based on their viewing history, preferences, and real-time behavior. The system processes millions of content items and user interactions to generate personalized recommendations in real-time.

**Business Context**: 
- 50M+ active users
- 10M+ content items (videos, shows, movies)
- Peak traffic: 8PM-11PM daily (3x normal load)
- Critical SLA: <200ms recommendation response time
- Revenue impact: 30% of content views come from recommendations

---

## Architecture

### Services Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        API Gateway                           │
│              (Rate limiting, routing, SSL termination)       │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
│  Auth        │ │  Content    │ │  User      │
│  Service     │ │  Service    │ │  Profile   │
│              │ │             │ │  Service   │
└───────┬──────┘ └──────┬──────┘ └─────┬──────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
│  Content     │ │  Vector     │ │  LLM        │
│  Pipeline    │ │  DB         │ │  Service    │
│              │ │  (Pinecone) │ │  (OpenAI)   │
└───────┬──────┘ └──────┬──────┘ └─────┬──────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
                ┌───────▼───────┐
                │ Recommendation│
                │    Engine     │
                │   (ML Model)  │
                └───────┬───────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
│  Cache       │ │  Analytics │ │  Notification│
│  (Redis)     │ │  Service   │ │  Service    │
└──────────────┘ └────────────┘ └─────────────┘
```

---

## Service Details

### 1. API Gateway
- **Technology**: Kong / AWS API Gateway
- **Responsibilities**:
  - Request routing to backend services
  - Rate limiting (1000 req/min per user)
  - SSL termination
  - Request/response logging
- **Current Issues**:
  - Rate limiting logic causes some legitimate requests to be throttled
  - No circuit breakers - passes through all requests even when downstream is failing

### 2. Auth Service
- **Technology**: Node.js / JWT tokens
- **Responsibilities**:
  - User authentication
  - Token generation and validation
  - Session management
- **Current Issues**:
  - Token validation adds 20-30ms latency per request
  - No caching of valid tokens

### 3. Content Service
- **Technology**: Python / FastAPI
- **Responsibilities**:
  - Serves content metadata (titles, descriptions, thumbnails)
  - Content search and filtering
  - Content availability checks
- **Current Issues**:
  - Database queries slow during peak hours (500ms+)
  - No read replicas

### 4. User Profile Service
- **Technology**: Go / PostgreSQL
- **Responsibilities**:
  - Stores user preferences, watch history
  - Tracks viewing behavior
  - Manages user settings
- **Current Issues**:
  - Watch history queries are expensive (joins across multiple tables)
  - No caching of frequently accessed profiles

### 5. Content Pipeline
- **Technology**: Python / Kafka
- **Responsibilities**:
  - Ingests new content from content creators
  - Processes video metadata
  - Generates content embeddings
  - Updates content index
- **Current Issues**:
  - Processing backlog during content upload spikes
  - Embedding generation is slow (5-10 seconds per video)
  - No prioritization of popular content

### 6. Vector DB (Pinecone)
- **Technology**: Pinecone / Managed vector database
- **Responsibilities**:
  - Stores content embeddings (10M+ vectors)
  - Semantic similarity search
  - Nearest neighbor queries
- **Current Issues**:
  - Query latency increases with index size (currently 150-200ms)
  - No query result caching
  - Index updates cause temporary slowdowns

### 7. LLM Service
- **Technology**: OpenAI API / Anthropic Claude
- **Responsibilities**:
  - Generates content descriptions and summaries
  - Analyzes user preferences from text (reviews, comments)
  - Creates personalized recommendation explanations
  - Classifies content by genre/topic
- **Current Issues**:
  - **CRITICAL**: Rate limited to 500 requests/minute
  - Latency varies (200ms - 2s depending on model)
  - Costs increase significantly during peak hours
  - No fallback when rate limited

### 8. Recommendation Engine
- **Technology**: Python / TensorFlow / Custom ML model
- **Responsibilities**:
  - Combines user profile + content embeddings + LLM insights
  - Runs collaborative filtering algorithm
  - Generates ranked recommendation list
  - Personalizes based on viewing history
- **Current Issues**:
  - Model inference takes 100-150ms
  - CPU-bound, doesn't scale horizontally well
  - Depends on LLM service for "explainability" features
  - No graceful degradation when dependencies fail

### 9. Cache (Redis)
- **Technology**: Redis Cluster
- **Responsibilities**:
  - Caches recommendation results (TTL: 5 minutes)
  - Caches user profiles (TTL: 10 minutes)
  - Caches content metadata (TTL: 1 hour)
  - Session storage
- **Current Issues**:
  - Cache invalidation is broadcast to all nodes (causes thundering herd)
  - No cache warming strategy
  - Memory pressure during peak hours

### 10. Analytics Service
- **Technology**: Python / ClickHouse
- **Responsibilities**:
  - Tracks recommendation clicks, views, engagement
  - A/B testing data collection
  - Real-time metrics dashboard
- **Current Issues**:
  - High write volume during peak hours
  - Batch processing causes delays

### 11. Notification Service
- **Technology**: Node.js / RabbitMQ
- **Responsibilities**:
  - Sends email notifications for new recommendations
  - Push notifications for mobile apps
  - In-app notification delivery
- **Current Issues**:
  - Queue backup during peak hours
  - No rate limiting on notifications

---

## Current Symptoms (Matching Brief)

### 1. Latency Spikes During Peak Traffic
- **When**: 8PM-11PM daily
- **Symptoms**:
  - Recommendation API response time: 200ms → 800ms-2s
  - 95th percentile latency: 500ms → 3s
  - Timeout errors increase from 0.1% to 5%

### 2. Intermittent Failures and Timeouts
- **Symptoms**:
  - Gateway timeouts (504 errors) during peak: 2-3% of requests
  - Recommendation engine timeouts: 1-2% of requests
  - LLM service timeouts: 0.5-1% of requests
  - User sees "Unable to load recommendations" error

### 3. LLM Service Degradation Cascades
- **Scenario**: LLM service hits rate limit (500 req/min)
- **Cascade Path**:
  1. LLM service returns 429 (rate limit) errors
  2. Recommendation engine waits for LLM response (no timeout)
  3. Recommendation engine requests queue up
  4. Engine CPU saturates (100% utilization)
  5. New requests to engine timeout
  6. Gateway sees engine timeouts
  7. Gateway returns 504 to users
  8. Users retry → more load → worse cascade

### 4. Cache Invalidation Thundering Herd
- **Scenario**: Popular new content is added
- **Cascade Path**:
  1. Content Pipeline processes new viral video
  2. Cache invalidation broadcast sent to all Redis nodes
  3. All cached recommendations for similar content invalidated
  4. Thousands of users request recommendations simultaneously
  5. Cache misses flood Vector DB and Recommendation Engine
  6. Vector DB query latency spikes (200ms → 1s)
  7. Recommendation Engine overloaded
  8. System-wide slowdown

### 5. Vague Sense of Cascades
- **Operators know**:
  - "When LLM is slow, everything is slow"
  - "Cache invalidation causes problems"
  - "Peak hours are bad"
- **Operators don't know**:
  - Exact cascade paths
  - Which services are most critical
  - Where to add queues/buffers
  - What failure modes exist

---

## Metrics & Observability

### Current Metrics Available
- **API Gateway**: Request rate, latency, error rate, timeout rate
- **LLM Service**: Request rate, latency, rate limit hits, cost
- **Vector DB**: Query latency, index size, query rate
- **Recommendation Engine**: Inference latency, CPU usage, queue depth
- **Cache**: Hit rate, memory usage, eviction rate
- **All Services**: Error logs, request logs (structured JSON)

### Metrics Gaps
- No service dependency graph visualization
- No cascade detection/alerting
- Limited visibility into queue depths
- No circuit breaker metrics

---

## Data Flow Example: Recommendation Request

### Happy Path (Normal Load)
1. User opens app → API Gateway receives request
2. Gateway → Auth Service: Validate token (20ms)
3. Gateway → User Profile Service: Get user profile (50ms, cached)
4. Gateway → Recommendation Engine: Request recommendations
5. Engine → Cache: Check for cached recommendations (cache hit: 5ms)
6. **Return cached recommendations** (Total: ~75ms) ✅

### Degraded Path (Peak Load, Cache Miss)
1. User opens app → API Gateway receives request
2. Gateway → Auth Service: Validate token (30ms, slow)
3. Gateway → User Profile Service: Get user profile (200ms, DB slow)
4. Gateway → Recommendation Engine: Request recommendations
5. Engine → Cache: Check cache (miss: 5ms)
6. Engine → Vector DB: Get similar content (300ms, slow)
7. Engine → LLM Service: Get content descriptions (800ms, rate limited)
8. Engine → Recommendation Engine: Run ML model (150ms)
9. Engine → Cache: Store result (10ms)
10. **Return recommendations** (Total: ~1.5s) ⚠️

### Failure Path (Cascade)
1. User opens app → API Gateway receives request
2. Gateway → Auth Service: Validate token (timeout after 1s)
3. Gateway retries → Auth Service: Still timing out
4. Gateway → Recommendation Engine: Request (bypasses auth due to retry logic bug)
5. Engine → LLM Service: Request (429 rate limit)
6. Engine waits for LLM (no timeout) → 30s wait
7. Engine CPU at 100%, queue depth: 1000+ requests
8. New requests to Engine timeout immediately
9. Gateway sees Engine timeouts → Returns 504 to user
10. User sees error, retries → More load → Worse cascade
11. **System partially down** (Total: timeout/error) ❌

---

## Specific Bottleneck Scenarios

### Bottleneck 1: LLM Service Rate Limiting
- **When**: During peak hours (8PM-11PM)
- **Symptom**: 429 errors, 10-20% of LLM requests fail
- **Impact**: Recommendation Engine waits indefinitely, queues fill up
- **Root Cause**: No rate limit handling, no fallback, no timeout

### Bottleneck 2: Vector DB Query Latency
- **When**: During cache invalidation events or peak load
- **Symptom**: Query latency: 200ms → 800ms-1s
- **Impact**: Recommendation Engine blocked waiting for vector queries
- **Root Cause**: No query result caching, index size growing, no query prioritization

### Bottleneck 3: Recommendation Engine CPU Saturation
- **When**: During peak hours or when LLM is slow
- **Symptom**: CPU at 100%, queue depth: 500-1000 requests
- **Impact**: New requests timeout immediately
- **Root Cause**: CPU-bound model, no horizontal scaling, no queue limits

### Bottleneck 4: Cache Invalidation Storms
- **When**: New popular content added
- **Symptom**: Cache hit rate drops from 80% to 20%
- **Impact**: Massive load on Vector DB and Recommendation Engine
- **Root Cause**: Broadcast invalidation, no gradual invalidation, no cache warming

### Bottleneck 5: Database Contention (User Profile Service)
- **When**: During peak hours
- **Symptom**: Query latency: 50ms → 500ms+
- **Impact**: User profile lookups slow, affecting all recommendations
- **Root Cause**: No read replicas, expensive joins, no query optimization

---

## Failure Modes

### Failure Mode 1: LLM Service Rate Limit
- **Trigger**: >500 requests/minute to LLM service
- **Failure**: LLM returns 429 (rate limit exceeded)
- **Propagation**: 
  - Recommendation Engine waits (no timeout)
  - Engine queue fills up
  - Engine CPU saturates
  - New requests timeout
  - Gateway returns 504 errors
- **User Impact**: "Unable to load recommendations" error

### Failure Mode 2: Vector DB Timeout
- **Trigger**: Vector DB query takes >2s (timeout)
- **Failure**: Query fails, no results returned
- **Propagation**:
  - Recommendation Engine gets empty results
  - Engine falls back to simple popularity-based recommendations
  - Fallback is slow (not optimized)
  - Overall latency increases
- **User Impact**: Slower recommendations, less personalized

### Failure Mode 3: Cache Cluster Memory Pressure
- **Trigger**: Cache memory usage >90%
- **Failure**: Redis evicts keys aggressively
- **Propagation**:
  - Cache hit rate drops
  - More requests to Vector DB and DB
  - Those services slow down
  - More cache misses (vicious cycle)
- **User Impact**: Slower recommendations, higher latency

### Failure Mode 4: Recommendation Engine Queue Overflow
- **Trigger**: Queue depth >1000 requests
- **Failure**: New requests rejected immediately
- **Propagation**:
  - Gateway sees rejections
  - Returns 503 (service unavailable)
  - Users retry → more load
  - System can't recover
- **User Impact**: Complete recommendation failure

---

## Feedback Loops

### Destabilizing Loop 1: Retry Storm
- **Pattern**: Service timeout → User retries → More load → More timeouts → More retries
- **Amplification**: Exponential growth in requests
- **Stabilizing Factor**: Rate limiting at gateway (but not effective enough)

### Destabilizing Loop 2: Cache Miss Cascade
- **Pattern**: Cache miss → DB load → DB slow → More cache misses → More DB load
- **Amplification**: Linear growth in DB load
- **Stabilizing Factor**: None currently

### Stabilizing Loop 1: Circuit Breaker (Not Implemented)
- **Pattern**: Service failures → Circuit opens → Requests rejected → Service recovers → Circuit closes
- **Would prevent**: Cascading failures
- **Status**: Not implemented

---

## Intervention Opportunities

### High-Impact Interventions (To Discover During Case Study)

1. **Add Queue Between Gateway and Recommendation Engine**
   - Decouple gateway from engine
   - Allow engine to process at its own rate
   - Prevent gateway timeouts

2. **Add Timeout and Fallback for LLM Service**
   - Don't wait indefinitely for LLM
   - Fallback to cached descriptions or simple rules
   - Prevent LLM cascade

3. **Add Circuit Breakers**
   - Open circuit when service fails
   - Prevent cascade propagation
   - Allow services to recover

4. **Implement Gradual Cache Invalidation**
   - Don't broadcast invalidate all at once
   - Invalidate gradually or on-demand
   - Prevent thundering herd

5. **Add Read Replicas for User Profile Service**
   - Distribute read load
   - Reduce database contention
   - Improve query latency

6. **Add Query Result Caching for Vector DB**
   - Cache common vector queries
   - Reduce Vector DB load
   - Improve latency

7. **Implement Request Prioritization**
   - Prioritize user-facing requests
   - Defer background processing
   - Improve user experience during peak

---

## Success Criteria for Case Study

After applying HUMMBL operators, you should identify:

1. **Bottlenecks**: LLM service, Vector DB, Recommendation Engine, Cache
2. **Cascade Paths**: LLM → Engine → Gateway, Cache → Vector DB → Engine
3. **Interventions**: At least 5-7 concrete changes
4. **Time Saved**: Should be faster than ad-hoc debugging (estimate: 2-3 hours saved)

---

## Ready for Analysis

This system is now ready for Case Study 1 analysis. You have:

- ✅ Clear architecture with 11 services
- ✅ Specific bottleneck scenarios
- ✅ Documented cascade failure patterns
- ✅ Failure modes identified
- ✅ Feedback loops described
- ✅ Intervention opportunities (to discover)

**You can now use this system during your recording to apply the 10 HUMMBL models and demonstrate the operator sequence!**

