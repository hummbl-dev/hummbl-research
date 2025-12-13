# Case Study 1: StreamFlow AI - System Summary

**Quick reference for recording**

---

## System: StreamFlow AI

**What it is**: AI-powered content recommendation system for video streaming (Netflix/YouTube-style)

**Scale**: 
- 50M+ active users
- 10M+ content items
- Peak traffic: 8PM-11PM (3x normal load)
- Target SLA: <200ms response time

---

## 11 Services

1. **API Gateway** - Entry point, rate limiting, routing
2. **Auth Service** - User authentication, JWT validation
3. **User Profile Service** - User preferences, watch history
4. **Content Service** - Content metadata (titles, descriptions)
5. **Content Pipeline** - Ingests new content, generates embeddings
6. **Vector DB** (Pinecone) - Stores content embeddings, similarity search
7. **LLM Service** (OpenAI) - Generates descriptions, analyzes preferences
8. **Recommendation Engine** - ML model for personalized recommendations
9. **Cache** (Redis) - Caches recommendations, profiles, content
10. **Analytics Service** - Tracks engagement, A/B tests
11. **Notification Service** - Sends email/push notifications

---

## 5 Main Bottlenecks

1. **LLM Service**: Rate limited to 500 req/min, variable latency (200ms-2s)
2. **Vector DB**: Query latency growing (150ms-1s), no result caching
3. **Recommendation Engine**: CPU-bound, queue overflow (0-1000 depth)
4. **User Profile DB**: Slow queries (50ms-500ms), no read replicas
5. **Cache**: Invalidation storms, memory pressure

---

## 3 Cascade Scenarios

### Cascade 1: LLM Rate Limit
LLM (429) → Engine waits → Queue fills → CPU saturates → Timeouts → Gateway 504

### Cascade 2: Cache Invalidation Storm
New content → Cache invalidate all → Cache misses → Vector DB + Engine overload → System slowdown

### Cascade 3: Retry Storm
Service timeout → User retries → More load → More timeouts → Exponential growth

---

## Key Metrics

- **Normal latency**: 75ms (cache hit) to 835ms (cache miss)
- **Peak latency**: 800ms-2s (degraded), 3s+ (95th percentile)
- **Error rates**: 0.1% normal → 2-5% during peak
- **Cache hit rate**: 80% normal → 20% during invalidation storms
- **LLM rate limit**: 500 requests/minute

---

## Intervention Opportunities (To Discover)

- Add queues between services
- Add timeouts and fallbacks for LLM
- Implement circuit breakers
- Gradual cache invalidation
- Read replicas for databases
- Query result caching
- Request prioritization

---

**Use this summary during recording as a quick reference!**

