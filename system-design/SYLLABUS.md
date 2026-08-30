# System Design - Study Syllabus (Bloomberg-focused)

Local source of truth for the Notion "System Design" page tree. Each leaf below becomes
one Notion subpage. We write the notes one at a time.

Reference courses used only to shape this syllabus (NOT to be named in Notion):
- Arpit Bhayani - System Design for Beginners
- LeetCode - System Design for Interviews and Beyond
- Arpit Bhayani - System Design Masterclass
- Epic Institute - Real-time Backend (lecture list provided by user)

Legend: `[bl]` = Bloomberg-specific interview question page.

---

## 0. Orientation
- 0.1 How to use this syllabus + study plan / schedule
- 0.2 The system design interview framework (requirements -> estimation -> API -> data model -> HLD -> deep dives -> bottlenecks)
- 0.3 Back-of-the-envelope estimation + latency numbers every engineer should know

## 1. Fundamentals
- 1.1 Functional vs non-functional requirements
- 1.2 Availability, reliability, fault tolerance, resilience, durability
- 1.3 Scalability, performance, latency vs throughput, maintainability, cost
- 1.4 CAP theorem, PACELC
- 1.5 Consistency models (strong, eventual, causal, read-your-writes, monotonic)
- 1.6 ACID vs BASE
- 1.7 Distributed system models: synchrony, failure modes, the 8 fallacies

## 2. Communication
- 2.1 Network stack for backend: TCP vs UDP, HTTP/1.1 vs HTTP/2 vs HTTP/3, TLS
- 2.2 REST, RPC, gRPC, GraphQL - trade-offs
- 2.3 Real-time: short/long polling, SSE, WebSockets, pub/sub over the wire
- 2.4 Failure detection, timeouts, retries, backoff, jitter, idempotency keys
- 2.5 Load balancing (L4 vs L7), reverse proxy, API gateway
- 2.6 Fault tolerance patterns: circuit breaker, bulkhead, backpressure, load shedding, hedged requests

## 3. Storage
- 3.1 Storage engine internals: B-Tree vs LSM-tree, WAL, page cache, compaction
- 3.2 SQL vs NoSQL; data models: key-value, document, wide-column, graph, time-series
- 3.3 Indexing: primary/secondary, covering, composite, inverted
- 3.4 Partitioning / sharding: hash, range, consistent hashing, hot partitions, rebalancing
- 3.5 Replication: leader-follower, multi-leader, leaderless, quorums (R+W>N)
- 3.6 Consensus: leader election, Raft, Paxos overview, ZooKeeper/etcd
- 3.7 Distributed transactions: 2PC, 3PC, sagas, outbox, idempotent consumers
- 3.8 Change Data Capture, event sourcing, CQRS
- 3.9 Object/blob storage, distributed file systems, data lakes

## 4. Memory and Caching
- 4.1 Caching strategies: cache-aside, read/write-through, write-behind; TTL and eviction (LRU/LFU/ARC)
- 4.2 Cache invalidation, stampede/thundering herd, negative caching, request coalescing
- 4.3 Redis and Memcached deep dive: data structures, persistence, clustering, eviction
- 4.4 CDN and edge caching
- 4.5 Probabilistic structures: Bloom filter, Counting Bloom, Count-Min Sketch, HyperLogLog, t-digest

## 5. Data Processing and Messaging
- 5.1 Message queues and brokers: Kafka, RabbitMQ, SQS, NATS; log vs queue
- 5.2 Delivery semantics: at-most / at-least / exactly-once, ordering, dedup, DLQ
- 5.3 Stream processing: windowing, watermarks, state, exactly-once (Flink / Kafka Streams)
- 5.4 Batch processing: MapReduce, Spark; Lambda vs Kappa architecture
- 5.5 Pub/Sub and fan-out patterns (fan-out on write vs read)

## 6. Infrastructure and Operations
- 6.1 Containers, orchestration, service discovery, service mesh
- 6.2 Multi-region and geo-distribution, cell-based architecture, failover and DR
- 6.3 Observability: metrics, logging, distributed tracing, SLI/SLO/SLA, error budgets
- 6.4 Rate limiting and throttling algorithms (token bucket, leaky bucket, sliding window, distributed)
- 6.5 Deployment strategies, config management, feature flags

## 7. Security and Time
- 7.1 AuthN/AuthZ: OAuth2, OIDC, JWT, sessions, API keys, mTLS
- 7.2 Encryption at rest and in transit, key management, secrets
- 7.3 Threats and mitigations: DDoS, replay, injection, SSRF; WAF; least privilege
- 7.4 Time in distributed systems: physical clocks, NTP, clock skew
- 7.5 Logical clocks: Lamport timestamps, vector clocks, hybrid logical clocks, TrueTime
- 7.6 Ordering, causality, distributed snapshots

## 8. Product Thinking for Backend Engineers
- 8.1 Scoping a product; turning vague asks into requirements and constraints
- 8.2 API and data model design as a product surface; versioning and evolution
- 8.3 Trade-off analysis, capacity planning, cost modeling, migration strategy

## 9. Design Case Studies (generic patterns)
- 9.1 URL shortener / Pastebin
- 9.2 Distributed rate limiter
- 9.3 Notification / fan-out service (email, push, SMS, in-app)
- 9.4 News feed / timeline
- 9.5 Top-K / trending (heavy hitters)
- 9.6 Real-time chat / presence
- 9.7 Search autocomplete / typeahead
- 9.8 Distributed cache
- 9.9 Object storage service (S3-like)
- 9.10 Web crawler
- 9.11 Metrics / time-series monitoring system
- 9.12 Distributed job scheduler

## 10. Bloomberg Interview Prep  [bl]
- 10.0 Bloomberg system design interview: process, what they test, how to drive the round
- 10.1 [bl] Custom index / custom indexes - arithmetic expression over security prices, create/modify/delete, current value, APIs, data model
- 10.2 [bl] Custom index - extend to pub/sub: subscribe and get notified when index value changes
- 10.3 [bl] Stock price alert / notification system (alerts on threshold crossings, ~100k options, 24/7, crash recovery)
- 10.4 [bl] Top-K most popular news on the Terminal (time-window aggregation, event listener, snapshots, retention)
- 10.5 [bl] News notification system
- 10.6 [bl] News feed design
- 10.7 [bl] Collaborative note-taking app: create/edit/share notes, permissions (view/edit/share), "recently modified" ordering
- 10.8 [bl] Note-taking app with offline support (mobile, retrieve notes offline, sync/merge)
- 10.9 [bl] "Memo" for the Bloomberg Terminal - shared terminal notes with view/edit/share permissions
- 10.10 [bl] Twitter sentiment analysis for a company over time (fetch on interval, classify +/-, graph; prioritize accuracy)
- 10.11 [bl] Offline video mobile app: watch offline, download, watch-later, resume-from-timestamp
- 10.12 [bl] Distributed tracing system that scales
- 10.13 [bl] Log processing pipeline to a warehouse (reliable, low-latency, accurate/no-loss to meet SLA)
- 10.14 [bl] Audit logging service - safe writes for a stream of (possibly invalid) stock logs
- 10.15 [bl] Distributed logging system
- 10.16 [bl] Market-data fan-out to local processes (IPC/streaming to other processes on the same machine, multi-stock, consumer death, state management)
- 10.17 [bl] Rate limiting service
- 10.18 [bl] Generic notification service

## 11. Resources - Blogs and Papers
- 11.1 Papers list (annotated) - Lamport clocks, Chandy-Lamport, FLP, Dynamo, Bigtable, GFS/MapReduce, Kafka, Raft, Spanner, Chubby, Cassandra, Percolator, Borg, Monarch, Dapper
- 11.2 Books and courses - DDIA and index, Kleppmann lectures
- 11.3 Engineering blogs to follow + curated lists
