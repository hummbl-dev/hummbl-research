# StreamFlow AI - Architecture Diagram (Text Format)

**For use during Case Study 1 recording**

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Users / Clients                         │
│                    (Mobile Apps, Web Browser)                    │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              │ HTTPS
                              │
┌─────────────────────────────▼────────────────────────────────────┐
│                      API Gateway (Kong)                        │
│  • Rate Limiting (1000 req/min/user)                           │
│  • Request Routing                                             │
│  • SSL Termination                                             │
│  • No Circuit Breakers ❌                                      │
└─────────────┬───────────────────────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼───┐ ┌───▼────┐
│ Auth  │ │User  │ │Content │
│Service│ │Profile│ │Service │
│       │ │Service│ │        │
│20-30ms│ │50-500ms│ │50-500ms│
└───┬───┘ └───┬──┘ └───┬────┘
    │         │         │
    └─────────┼─────────┘
              │
              │ All services call:
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼────┐ ┌───▼────┐
│Content│ │Vector │ │  LLM   │
│Pipeline│ │  DB   │ │Service │
│       │ │(Pinecone)│ │(OpenAI)│
│Kafka  │ │150-1000ms│ │200-2000ms│
│       │ │        │ │Rate:500/min│
└───┬───┘ └───┬────┘ └───┬────┘
    │         │         │
    └─────────┼─────────┘
              │
              │
    ┌─────────▼─────────┐
    │ Recommendation   │
    │     Engine        │
    │  (ML Model)       │
    │  100-150ms        │
    │  CPU-bound        │
    │  Queue: 0-1000    │
    └─────────┬─────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼────┐ ┌──▼────┐
│ Cache │ │Analytics│ │Notify│
│(Redis)│ │Service │ │Service│
│       │ │        │ │       │
│5-10ms │ │ClickHouse│ │RabbitMQ│
│80% hit│ │        │ │       │
└───────┘ └────────┘ └───────┘
```

---

## Data Flow: Recommendation Request

### Normal Flow (Cache Hit)
```
User → Gateway → Auth (20ms) → User Profile (50ms, cached)
  → Recommendation Engine → Cache (5ms, HIT) → Return (75ms total) ✅
```

### Degraded Flow (Cache Miss, Normal Load)
```
User → Gateway → Auth (20ms) → User Profile (50ms)
  → Recommendation Engine → Cache (5ms, MISS)
  → Vector DB (200ms) → LLM (400ms) → Engine (150ms)
  → Cache Store (10ms) → Return (835ms total) ⚠️
```

### Failure Flow (Cascade)
```
User → Gateway → Auth (TIMEOUT 1s)
  → Recommendation Engine → LLM (429 Rate Limit)
  → Engine waits 30s (no timeout) → Queue fills (1000+)
  → New requests timeout → Gateway 504 → User retries
  → More load → Worse cascade ❌
```

---

## Service Dependencies

```
API Gateway
  ├── Auth Service
  ├── User Profile Service
  │     └── PostgreSQL DB
  ├── Content Service
  │     └── PostgreSQL DB
  └── Recommendation Engine
        ├── Cache (Redis)
        ├── Vector DB (Pinecone)
        ├── LLM Service (OpenAI)
        └── User Profile Service
              └── PostgreSQL DB
```

---

## Critical Paths

### Path 1: User Request → Recommendation
```
Gateway → Auth → User Profile → Engine → Cache → Return
Time: 20ms + 50ms + 5ms = 75ms (cache hit)
```

### Path 2: Cache Miss → Full Pipeline
```
Gateway → Auth → User Profile → Engine → Vector DB → LLM → Engine → Cache → Return
Time: 20ms + 50ms + 200ms + 400ms + 150ms + 10ms = 835ms
```

### Path 3: LLM Failure → Cascade
```
Gateway → Engine → LLM (429) → Engine waits → Queue fills → Timeouts → 504
Time: TIMEOUT / ERROR
```

---

## Bottleneck Locations

1. **LLM Service**: Rate limit (500/min), variable latency (200ms-2s)
2. **Vector DB**: Growing latency (150ms-1s), no caching
3. **Recommendation Engine**: CPU-bound, queue overflow
4. **User Profile DB**: Slow queries (50ms-500ms), no read replicas
5. **Cache**: Invalidation storms, memory pressure

---

## Queue Locations

### Current Queues
- **Recommendation Engine**: Internal queue (0-1000 depth)
- **Notification Service**: RabbitMQ queue (can backup)
- **Content Pipeline**: Kafka topics (can backlog)

### Missing Queues (To Discover)
- Between Gateway and Recommendation Engine
- Between Engine and LLM Service
- Between Engine and Vector DB

---

## Feedback Loops

### Destabilizing
1. **Retry Storm**: Timeout → Retry → More load → More timeouts
2. **Cache Miss Cascade**: Miss → DB load → DB slow → More misses

### Stabilizing (Not Implemented)
1. **Circuit Breaker**: Failures → Circuit opens → Service recovers
2. **Backpressure**: Queue full → Reject new requests → Prevent overload

---

**Use this diagram during recording to visualize the system and identify bottlenecks, cascades, and interventions!**

