#!/usr/bin/env python3
"""Create the Notion 'System Design' page tree via the ntn CLI.

Idempotent-ish: reads system-design/notion_pages.json and skips anything already
created (keyed by stable slug). Safe to re-run after partial failures.
"""
import json
import os
import subprocess
import sys
import time

ROOT_ID = "3ccddfa5-e685-81bd-ae5f-ff6eaac21fb9"
HERE = os.path.dirname(os.path.abspath(__file__))
MAP_PATH = os.path.join(HERE, "notion_pages.json")
WORKDIR = "/tmp/claude-1000/-home-matania-Desktop-design-patterns-gang/a9d83e5a-c4b0-41d4-80f0-fc3e572de418/scratchpad/ntnwork"

os.makedirs(WORKDIR, exist_ok=True)

if os.path.exists(MAP_PATH):
    with open(MAP_PATH) as f:
        PAGES = json.load(f)
else:
    PAGES = {}


def save():
    with open(MAP_PATH, "w") as f:
        json.dump(PAGES, f, indent=2)


def create(slug, title, parent_id, body):
    if slug in PAGES and PAGES[slug].get("id"):
        print(f"skip  {slug}")
        return PAGES[slug]["id"]
    # Quote the title: an unquoted ':' in YAML frontmatter makes ntn drop the title.
    safe = title.replace('"', "'")
    content = f'---\ntitle: "{safe}"\n---\n\n{body}\n'
    p = subprocess.run(
        ["ntn", "pages", "create", "--parent", f"page:{parent_id}", "--json"],
        input=content, capture_output=True, text=True, cwd=WORKDIR,
    )
    if p.returncode != 0:
        print(f"FAIL  {slug}\n{p.stderr}", file=sys.stderr)
        save()
        sys.exit(1)
    data = json.loads(p.stdout)
    PAGES[slug] = {"id": data["id"], "title": title, "url": data["url"], "parent": parent_id}
    save()
    print(f"made  {slug}  {data['url']}")
    time.sleep(0.5)
    return data["id"]


def stub(topics):
    lines = ["> Status: not yet written.", "", "**To cover:**", ""]
    for t in topics:
        lines.append(f"- [ ] {t}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Structure: list of (part_slug, part_title, part_intro, [ (leaf_slug, leaf_title, leaf_body) ])
# ---------------------------------------------------------------------------

TREE = []

TREE.append(("p0", "Part 0 - Orientation",
    "How to run the system design interview and size systems quickly.", [
    ("0.1-study-plan", "0.1 How to use this syllabus + study plan",
     stub(["Week-by-week schedule", "How to use each note", "Spaced review of case studies", "Mock interview cadence"])),
    ("0.2-interview-framework", "0.2 The system design interview framework",
     stub(["Clarify functional + non-functional requirements", "Back-of-envelope estimation",
           "API design", "Data model", "High-level design", "Deep dives on 2-3 components",
           "Identify bottlenecks and justify trade-offs", "How to drive the conversation and handle curveballs"])),
    ("0.3-estimation", "0.3 Back-of-the-envelope estimation + latency numbers",
     stub(["Powers of two and unit cheat sheet", "Latency numbers every engineer should know",
           "QPS, storage, bandwidth estimation method", "Worked examples"])),
]))

TREE.append(("p1", "Part 1 - Fundamentals",
    "The vocabulary and theorems every design rests on.", [
    ("1.1-func-nonfunc", "1.1 Functional vs non-functional requirements", stub(["Definitions", "How to elicit them", "Turning them into design constraints"])),
    ("1.2-availability-reliability", "1.2 Availability, reliability, fault tolerance, resilience, durability",
     stub(["Nines and downtime budgets", "Reliability vs availability", "Fault vs failure",
           "Redundancy, failover, graceful degradation", "Durability guarantees"])),
    ("1.3-scalability-performance", "1.3 Scalability, performance, latency vs throughput, maintainability, cost",
     stub(["Vertical vs horizontal scaling", "Latency vs throughput vs goodput", "Tail latency (p99)",
           "Little's Law", "Operability, evolvability, cost"])),
    ("1.4-cap-pacelc", "1.4 CAP theorem and PACELC", stub(["CAP precise statement and common misreadings", "CP vs AP systems", "PACELC extension", "Examples mapped to real databases"])),
    ("1.5-consistency-models", "1.5 Consistency models",
     stub(["Strong / linearizable", "Sequential", "Causal", "Eventual", "Read-your-writes, monotonic reads/writes",
           "Client-centric vs data-centric"])),
    ("1.6-acid-base", "1.6 ACID vs BASE", stub(["ACID properties in depth", "Isolation levels and anomalies", "BASE", "When each is appropriate"])),
    ("1.7-distributed-models", "1.7 Distributed system models and the fallacies",
     stub(["Synchronous / partially synchronous / asynchronous", "Crash-stop, crash-recovery, Byzantine",
           "The 8 fallacies of distributed computing", "Network partitions in practice"])),
]))

TREE.append(("p2", "Part 2 - Communication",
    "How services talk, fail, and recover.", [
    ("2.1-network-stack", "2.1 Network stack for backend: TCP/UDP, HTTP/1.1/2/3, TLS",
     stub(["TCP vs UDP", "Head-of-line blocking", "HTTP/1.1 keep-alive, HTTP/2 multiplexing, HTTP/3 QUIC",
           "TLS handshake and session resumption", "Connection pooling"])),
    ("2.2-rest-rpc-grpc-graphql", "2.2 REST, RPC, gRPC, GraphQL",
     stub(["REST constraints and resource modeling", "RPC and gRPC / protobuf / streaming",
           "GraphQL and the N+1 problem", "Choosing between them"])),
    ("2.3-realtime", "2.3 Real-time delivery: polling, SSE, WebSockets, pub/sub",
     stub(["Short vs long polling", "Server-Sent Events", "WebSockets and connection management at scale",
           "Presence and fan-out", "Choosing a push transport"])),
    ("2.4-failure-retries-idempotency", "2.4 Failure detection, timeouts, retries, backoff, idempotency",
     stub(["Timeout budgets and deadlines", "Retry storms", "Exponential backoff with jitter",
           "Idempotency keys", "Exactly-once as idempotency + dedup"])),
    ("2.5-load-balancing", "2.5 Load balancing, reverse proxy, API gateway",
     stub(["L4 vs L7", "Algorithms: round robin, least connections, consistent hashing", "Health checks",
           "Reverse proxy responsibilities", "API gateway: auth, rate limit, routing, aggregation"])),
    ("2.6-fault-tolerance-patterns", "2.6 Fault tolerance patterns",
     stub(["Circuit breaker", "Bulkhead", "Backpressure", "Load shedding", "Hedged / tied requests", "Graceful degradation"])),
]))

TREE.append(("p3", "Part 3 - Storage",
    "Storage engines, data models, partitioning, replication, consensus.", [
    ("3.1-storage-engines", "3.1 Storage engine internals: B-Tree vs LSM-tree",
     stub(["B-Tree structure and write amplification", "LSM-tree, memtable, SSTables, compaction",
           "Write-ahead log", "Page cache and fsync", "Read/write/space amplification trade-offs"])),
    ("3.2-sql-nosql-models", "3.2 SQL vs NoSQL and data models",
     stub(["Relational model and normalization", "Key-value", "Document", "Wide-column", "Graph", "Time-series",
           "Picking a store from access patterns"])),
    ("3.3-indexing", "3.3 Indexing", stub(["Primary vs secondary", "Clustered vs non-clustered", "Composite and covering indexes", "Inverted index", "Index maintenance cost"])),
    ("3.4-partitioning", "3.4 Partitioning / sharding",
     stub(["Hash vs range partitioning", "Consistent hashing and virtual nodes", "Hot partitions and skew",
           "Rebalancing strategies", "Routing requests to partitions", "Secondary indexes on partitioned data"])),
    ("3.5-replication", "3.5 Replication",
     stub(["Leader-follower (sync/async)", "Multi-leader and conflict resolution", "Leaderless (Dynamo-style)",
           "Quorums R + W > N", "Read repair and anti-entropy", "Replication lag anomalies"])),
    ("3.6-consensus", "3.6 Consensus and coordination",
     stub(["Why consensus is hard (FLP)", "Leader election", "Raft in detail", "Paxos / Multi-Paxos overview",
           "ZooKeeper / etcd and their use cases"])),
    ("3.7-distributed-transactions", "3.7 Distributed transactions",
     stub(["Two-phase commit and its blocking problem", "Three-phase commit", "Sagas and compensation",
           "Transactional outbox", "Idempotent consumers"])),
    ("3.8-cdc-event-sourcing-cqrs", "3.8 CDC, event sourcing, CQRS",
     stub(["Change data capture", "Event sourcing: log as source of truth", "CQRS read/write separation",
           "Materialized views", "Trade-offs and pitfalls"])),
    ("3.9-object-file-storage", "3.9 Object/blob storage and distributed file systems",
     stub(["Object storage model (S3)", "GFS/HDFS architecture", "Erasure coding vs replication",
           "Metadata service scaling", "When to use blob storage vs a database"])),
]))

TREE.append(("p4", "Part 4 - Memory and Caching",
    "Serving hot data fast and the failure modes that come with it.", [
    ("4.1-caching-strategies", "4.1 Caching strategies and eviction",
     stub(["Cache-aside, read-through, write-through, write-behind", "TTL design",
           "Eviction: LRU, LFU, ARC, W-TinyLFU", "Where caches live (client, CDN, app, DB)"])),
    ("4.2-cache-invalidation", "4.2 Cache invalidation and stampede protection",
     stub(["Invalidation strategies", "Thundering herd / cache stampede", "Request coalescing / singleflight",
           "Negative caching", "Stale-while-revalidate", "Consistency between cache and store"])),
    ("4.3-redis-memcached", "4.3 Redis and Memcached deep dive",
     stub(["Memcached model and slab allocation", "Redis data structures", "Persistence: RDB and AOF",
           "Redis Cluster and sharding", "Eviction policies", "Redis as more than a cache (locks, streams, rate limiting)"])),
    ("4.4-cdn", "4.4 CDN and edge caching",
     stub(["How a CDN routes (anycast, DNS)", "Cache keys and cache control headers", "Origin shielding",
           "Purge / invalidation", "Dynamic content at the edge"])),
    ("4.5-probabilistic-structures", "4.5 Probabilistic data structures",
     stub(["Bloom filter and false-positive math", "Counting Bloom filter", "Count-Min Sketch",
           "HyperLogLog", "t-digest / quantile sketches", "Where each shows up in system design"])),
]))

TREE.append(("p5", "Part 5 - Data Processing and Messaging",
    "Moving and transforming data reliably at volume.", [
    ("5.1-queues-brokers", "5.1 Message queues and brokers",
     stub(["Queue vs log", "Kafka architecture (partitions, offsets, consumer groups)", "RabbitMQ / AMQP",
           "SQS / cloud queues", "Choosing a broker"])),
    ("5.2-delivery-semantics", "5.2 Delivery semantics and ordering",
     stub(["At-most-once, at-least-once, exactly-once", "Ordering guarantees and partitioning",
           "Deduplication", "Dead-letter queues", "Poison messages and retry policy"])),
    ("5.3-stream-processing", "5.3 Stream processing",
     stub(["Event time vs processing time", "Windowing (tumbling, sliding, session)", "Watermarks and late data",
           "State management and checkpoints", "Exactly-once in Flink / Kafka Streams"])),
    ("5.4-batch-lambda-kappa", "5.4 Batch processing; Lambda vs Kappa",
     stub(["MapReduce model", "Spark model", "Lambda architecture", "Kappa architecture", "Reprocessing and backfills"])),
    ("5.5-pubsub-fanout", "5.5 Pub/Sub and fan-out patterns",
     stub(["Fan-out on write vs fan-out on read", "Hybrid fan-out", "Push vs pull to subscribers",
           "Subscription management and backpressure"])),
]))

TREE.append(("p6", "Part 6 - Infrastructure and Operations",
    "Running systems across machines and regions, and seeing inside them.", [
    ("6.1-containers-orchestration", "6.1 Containers, orchestration, service discovery, service mesh",
     stub(["Containers vs VMs", "Kubernetes scheduling model", "Service discovery", "Service mesh (sidecar, mTLS, retries)"])),
    ("6.2-multi-region", "6.2 Multi-region and geo-distribution",
     stub(["Active-passive vs active-active", "Geo-routing (GeoDNS, anycast)", "Data residency and replication across regions",
           "Cell-based architecture and blast radius", "Disaster recovery: RTO and RPO"])),
    ("6.3-observability", "6.3 Observability and SLOs",
     stub(["Metrics, logs, traces (the three pillars)", "RED and USE methods", "Cardinality and sampling",
           "SLI / SLO / SLA and error budgets", "Alerting on symptoms not causes"])),
    ("6.4-rate-limiting", "6.4 Rate limiting and throttling algorithms",
     stub(["Token bucket", "Leaky bucket", "Fixed and sliding window counters", "Sliding window log",
           "Distributed rate limiting (Redis, cell counters)", "Client behavior: 429, Retry-After"])),
    ("6.5-deployment", "6.5 Deployment strategies, config, feature flags",
     stub(["Blue-green, canary, rolling", "Config management and hot reload", "Feature flags and kill switches",
           "Schema/config migrations without downtime"])),
]))

TREE.append(("p7", "Part 7 - Security and Time",
    "Trust boundaries, and reasoning about order without a global clock.", [
    ("7.1-authn-authz", "7.1 AuthN / AuthZ: OAuth2, OIDC, JWT, sessions, mTLS",
     stub(["Authentication vs authorization", "Sessions vs tokens", "OAuth2 flows", "OIDC", "JWT structure and pitfalls",
           "RBAC / ABAC", "mTLS and service identity"])),
    ("7.2-encryption-secrets", "7.2 Encryption at rest and in transit, key management, secrets",
     stub(["TLS in practice", "Envelope encryption and KMS", "Key rotation", "Secret storage", "Tokenization"])),
    ("7.3-threats-mitigations", "7.3 Threats and mitigations",
     stub(["DDoS and mitigation layers", "Replay attacks", "Injection and SSRF", "WAF", "Least privilege and defense in depth",
           "Rate limits as a security control"])),
    ("7.4-physical-clocks", "7.4 Time: physical clocks, NTP, clock skew",
     stub(["Wall clock vs monotonic clock", "NTP and how far off clocks drift", "Why timestamps are unsafe for ordering",
           "Leap seconds"])),
    ("7.5-logical-clocks", "7.5 Logical clocks: Lamport, vector, hybrid logical clocks, TrueTime",
     stub(["Lamport timestamps and total order", "Vector clocks and causality detection", "Version vectors",
           "Hybrid logical clocks", "Spanner TrueTime and commit wait"])),
    ("7.6-ordering-snapshots", "7.6 Ordering, causality, distributed snapshots",
     stub(["Happens-before", "Causal broadcast", "Chandy-Lamport snapshot algorithm", "Consistent cuts",
           "Use in checkpointing and stream processing"])),
]))

TREE.append(("p8", "Part 8 - Product Thinking for Backend Engineers",
    "Translating fuzzy product asks into systems, and evolving them.", [
    ("8.1-scoping", "8.1 Scoping a product and eliciting requirements",
     stub(["Questions to ask", "Identifying the core use case vs nice-to-haves", "Non-functional constraints from product context",
           "Defining success metrics"])),
    ("8.2-api-data-model-evolution", "8.2 API and data model design and evolution",
     stub(["API as a contract", "Versioning strategies", "Backward/forward compatibility", "Schema evolution",
           "Deprecation"])),
    ("8.3-tradeoffs-capacity-cost-migration", "8.3 Trade-off analysis, capacity planning, cost, migrations",
     stub(["Structured trade-off analysis", "Capacity planning method", "Cost modeling", "Migration patterns (dual write, backfill, shadow read)"])),
]))

TREE.append(("p9", "Part 9 - Design Case Studies",
    "Reusable blueprints. Each is a full design you can adapt in an interview.", [
    ("9.1-url-shortener", "9.1 URL shortener / Pastebin", stub(["Requirements", "Key generation (counter, hash, base62)", "Storage and cache", "Redirect path", "Analytics", "Scale numbers"])),
    ("9.2-rate-limiter", "9.2 Distributed rate limiter", stub(["Requirements", "Algorithm choice", "Where it runs (gateway vs library)", "Distributed counter design", "Failure modes"])),
    ("9.3-notification-service", "9.3 Notification / fan-out service", stub(["Requirements", "Channels (push, email, SMS, in-app)", "Templating", "Rate limiting and user preferences", "Retries and idempotency", "Provider abstraction"])),
    ("9.4-news-feed", "9.4 News feed / timeline", stub(["Requirements", "Fan-out on write vs read", "Ranking", "Pagination", "Celebrity problem", "Caching"])),
    ("9.5-top-k", "9.5 Top-K / trending (heavy hitters)", stub(["Requirements", "Exact vs approximate", "Count-Min Sketch + heap", "Time windows and decay", "Sharding and merge", "Snapshots"])),
    ("9.6-chat", "9.6 Real-time chat and presence", stub(["Requirements", "Connection layer (WebSocket gateway)", "Message storage and ordering", "Delivery and read receipts", "Group chat fan-out", "Presence"])),
    ("9.7-autocomplete", "9.7 Search autocomplete / typeahead", stub(["Requirements", "Trie construction and storage", "Ranking by frequency", "Sharding the trie", "Updates", "Client debounce and caching"])),
    ("9.8-distributed-cache", "9.8 Distributed cache", stub(["Requirements", "Consistent hashing", "Replication and failover", "Eviction", "Client vs proxy topology", "Hot key handling"])),
    ("9.9-object-store", "9.9 Object storage service (S3-like)", stub(["Requirements", "Data path and metadata service", "Partitioning and placement", "Durability (replication / erasure coding)", "Consistency model", "Multipart upload"])),
    ("9.10-web-crawler", "9.10 Web crawler", stub(["Requirements", "URL frontier and prioritization", "Politeness and robots.txt", "Dedup (content and URL)", "DNS and fetch", "Storage and scale"])),
    ("9.11-metrics-system", "9.11 Metrics / time-series monitoring system", stub(["Requirements", "Ingestion pipeline", "Time-series storage and downsampling", "Query layer", "Alerting", "Cardinality control"])),
    ("9.12-job-scheduler", "9.12 Distributed job scheduler", stub(["Requirements", "Job store and state machine", "Leader election / work distribution", "Exactly-once execution", "Retries and dead jobs", "Cron semantics and clock skew"])),
]))

# ---- Part 10: Bloomberg ----
BL = []
BL.append(("10.0-bloomberg-overview", "10.0 Bloomberg system design interview: process and what they test",
    stub(["Interview loop structure", "Themes: real-time, low-latency, reliability, no data loss, financial data",
          "How the round is run (whiteboard/paper, rapid follow-ups, curveballs)",
          "Common failure modes from candidate write-ups (event listener terminology, snapshot/retention questions, server-failure recovery)",
          "How to stand on fundamentals when pushed"])))

def bl(slug, title, prompt_md, topics):
    body = "## Interview prompt(s)\n\n" + prompt_md.strip() + "\n\n## Notes\n\n" + stub(topics)
    BL.append((slug, title, body))

bl("10.1-custom-index", "10.1 [bl] Custom Index - core system",
   """
Design a system to manage custom indexes for our users. A custom index is an arithmetic
expression which calculates a value based on the current prices of one or more securities
(financial instruments). For example, "IBM equity + BP equity" is a custom index composed
of the sum of the prices of IBM and BP stocks.

The system should:
- Allow a user to create / modify / delete custom indexes.
- Return the current value of a user's custom index.

The design should include: the major components of the system, the APIs the system presents,
and what data the system would store.

Variant wording: an index/query a customer can create, e.g. "MSFT * AAPL / GOOG + AMZN";
any arithmetic operation, any number of securities.
   """,
   ["Requirements and scope", "Expression parsing / AST / validation", "Security price source (market data feed)",
    "Evaluation engine and caching of sub-expressions", "API design (CRUD + get value)", "Data model (index def, user, securities)",
    "Scaling reads", "Consistency of price snapshots used in a computation"])

bl("10.2-custom-index-pubsub", "10.2 [bl] Custom Index - pub/sub extension",
   """
Extend the custom index system so that it acts as a pub/sub system: allow a user to subscribe
to their custom index(es) and receive notifications whenever the value of their index changes.
   """,
   ["Dependency graph: security -> indexes that reference it", "Incremental re-evaluation on price tick",
    "Change detection and thresholds (avoid notification storms)", "Subscription store", "Delivery (WebSocket / push / webhook)",
    "Fan-out and backpressure", "Ordering and dedup of notifications", "Handling subscriber disconnect and catch-up"])

bl("10.3-stock-alert", "10.3 [bl] Stock price alert / notification system",
   """
Stock alert notification system. Users can create alerts on stock options and the system raises
an alert when a stock transaction happens for more than a specific amount (threshold crossing).
Assume ~100,000 stock options. Discuss databases, scaling, keeping the service running 24/7,
and handling service crashes.

References:
- leetcode.com/discuss/interview-question/system-design/1555003 (New Grad 2022 rejection write-up)
- leetcode.com/discuss/interview-question/968803 (Onsite - Stock Change Notification System)
   """,
   ["Requirements and scale estimation", "Alert rule storage and indexing by symbol", "Matching engine: price tick -> matching rules",
    "Interval / windowing of price changes", "Notification delivery pipeline", "24/7 availability, leader election, failover",
    "Crash recovery and no missed alerts (checkpointing, replay)", "Idempotent notifications"])

bl("10.4-top-k-news", "10.4 [bl] Top-K most popular news on the Terminal",
   """
On the Bloomberg terminal, the most popular news appears, with a selectable time interval.
Design a system that displays the most popular news and discuss components, storage, and data model.

Follow-ups reported by candidates:
- How do you aggregate news view counts when the services aren't directly available? (answer: an
  event-listener/telemetry service that records news items viewed by clients)
- How does that event handler operate? Is a message queue the right tool?
- Ensure aggregation is not limited to a single time window.
- Snapshots: how are they stored in a key-value store? Rows grow unboundedly - how do you handle
  retention? (naive "delete after 30 days" breaks references to old news)
- If servers fail, how do you recover?
   """,
   ["Requirements: top-K over selectable windows", "Event ingestion (client view events -> queue)",
    "Aggregation: Count-Min Sketch + heap, per-time-bucket counters", "Sliding windows and merging buckets",
    "Snapshot storage in KV and retention / archival", "Serving layer and caching", "Server failure recovery and replay",
    "Exact vs approximate trade-off"])

bl("10.5-news-notification", "10.5 [bl] News notification system",
   """
Design a News Notification System.
   """,
   ["Requirements: who gets notified of what", "News ingestion and classification / tagging",
    "Subscription model (topics, tickers, watchlists)", "Matching news -> interested users", "Fan-out and delivery channels",
    "Deduplication and rate control", "Delivery guarantees"])

bl("10.6-news-feed", "10.6 [bl] News feed design",
   """
Design a News Feed (Bloomberg Terminal news). A publisher to UI news pipeline with search and
scaling considerations: low-latency reads for the UI, indexing strategy, what to shard/replicate,
query patterns, caching.
   """,
   ["Requirements", "Ingestion from publishers", "Storage and indexing (inverted index for search)",
    "Ranking and personalization", "Low-latency read path and caching", "Sharding / replication of the index", "Search queries"])

bl("10.7-notes-collab", "10.7 [bl] Collaborative note-taking app with sharing and permissions",
   """
Design a note-taking app. A user should be able to:
- Create and save a note
- View their notes as well as notes shared with them
- Share notes with other users to collaborate
- Edit notes

Also: a user shares a file (gives permissions) to either just view or edit, and the shared
document should appear as the most recent when that user fetches their notes.
   """,
   ["Requirements", "Data model: notes, users, permissions (ACL), share links", "Permission checks on every access",
    "'Recently modified / shared with me' ordering and indexing", "Concurrent edit strategy (last-write-wins vs OT vs CRDT)",
    "API design", "Storage and sync", "Scaling reads and the shared-with-me query"])

bl("10.8-notes-offline", "10.8 [bl] Note-taking app with offline support (mobile)",
   """
Design a note-taking app. The user should be able to retrieve notes offline as well; it is a
mobile application. The user should be able to use the app under network issues or bad network
(offline functionality), including creating/editing notes offline and syncing later.
   """,
   ["Requirements", "Local-first storage on device (SQLite)", "Sync protocol (change log, deltas, tombstones)",
    "Conflict resolution (CRDT / OT / version vectors)", "Handling partial connectivity and retries",
    "Server-side model", "Security of offline data"])

bl("10.9-terminal-memo", "10.9 [bl] 'Memo' for the Bloomberg Terminal",
   """
Building a Memo for the Bloomberg terminal: a note app on the terminal that can be shared with
other terminal users with varying permissions like edit, view, and share.
   """,
   ["Requirements and constraints of the terminal environment", "Entitlements / permission model (view, edit, share)",
    "Real-time collaboration between terminal users", "Data model and storage", "Sync and presence",
    "Audit of who changed what", "Relationship to 10.7 (same core, terminal-specific)"])

bl("10.10-twitter-sentiment", "10.10 [bl] Twitter sentiment analysis for a company over time",
   """
Design a system that gets tweets from the Twitter API and analyzes whether they are positive or
negative comments on a given company, then displays this to the user as a graph over a given
time period. Prioritize accuracy of the system.

Variant: fetch data from Twitter on a periodic interval (e.g. every 5 days), separate tweets by
company, classify positive/negative, and display as a graph over time.
   """,
   ["Requirements; accuracy as the priority", "Ingestion: polling the API, rate limits, dedup, backfill",
    "Entity resolution: mapping tweets to a company / ticker", "Classification pipeline (model serving, batching, versioning)",
    "Accuracy: human-in-the-loop, confidence thresholds, re-labeling, model eval", "Aggregation into time buckets",
    "Storage (time-series) and the graph query API", "Reprocessing when the model improves"])

bl("10.11-offline-video", "10.11 [bl] Offline video mobile app",
   """
Design a mobile application where users can watch videos with or without an internet connection:
download videos, save videos to watch later, and save the timestamp of videos they previously
didn't finish so they can resume later.
   """,
   ["Requirements", "Video storage, encoding ladder, CDN", "Download manager: DRM, encryption at rest, storage limits, eviction",
    "Adaptive streaming (HLS/DASH) vs full download", "Watch-later list and resume-timestamp sync across devices",
    "Offline playback and later telemetry sync", "API design"])

bl("10.12-distributed-tracing", "10.12 [bl] Distributed tracing system that scales",
   """
Build a distributed tracing system that scales.
   """,
   ["Requirements", "Trace/span data model, context propagation (trace id, span id, baggage)",
    "Instrumentation and sampling (head vs tail sampling)", "Ingestion pipeline and collectors",
    "Storage (columnar / trace store) and indexing by trace id, service, tags", "Query and visualization (waterfall)",
    "Cardinality and cost control", "Reference: Dapper"])

bl("10.13-log-pipeline-warehouse", "10.13 [bl] Log processing pipeline to a warehouse",
   """
Given a defined input of data (logs) and a defined output (logs stored in a warehouse after being
processed), design a processing system that has reliability and low latency. Processing must also
be accurate: if a log has reached the warehouse, it must have been processed, to satisfy SLAs.
   """,
   ["Requirements: reliability, low latency, accuracy/SLA", "Ingestion and durable buffering (Kafka)",
    "Processing with exactly-once / effectively-once semantics", "Idempotent writes to the warehouse, dedup keys",
    "Ordering and late data", "Backpressure and autoscaling", "Monitoring, lag metrics, SLA alerting",
    "Replay and dead-letter handling"])

bl("10.14-audit-logging", "10.14 [bl] Audit logging service for stock logs",
   """
Design a logging service for an audit system that receives data and writes it to a database.
Ensure it is safe to write to the database, since the input is a stream of stock logs which
may or may not be legal (valid).
   """,
   ["Requirements: audit-grade durability and integrity", "Validation / sanitization stage; quarantine invalid records",
    "Safe write path: schema validation, size limits, injection protection", "Append-only / immutable store, hash chaining for tamper evidence",
    "Ordering and idempotency", "Backpressure on the input stream", "Retention and compliance (WORM)", "Access control and read audit"])

bl("10.15-distributed-logging", "10.15 [bl] Distributed logging system",
   """
Design a distributed logging system (collect logs from many services/hosts, transport, store,
and make them searchable).
   """,
   ["Requirements and scale", "Agent on host, local buffering", "Transport (Kafka) and partitioning",
    "Indexing and storage (ELK-style, or columnar)", "Retention tiers (hot/warm/cold) and archival",
    "Search and query performance", "Backpressure and loss policy", "Multitenancy and cost"])

bl("10.16-market-data-ipc", "10.16 [bl] Market-data fan-out to local processes",
   """
Create a program that streams data from an external data provider to several applications running
on the same machine. The external provider sends info about trades on a stock exchange. Other
applications run as separate processes on the same machine and can ask your program to send them
data about a certain stock. Design questions: how to transfer data between your process and other
processes; how to support streaming data for multiple stocks; what to do when consumer processes
that queried data die; how to manage application state. (Discussion / on-paper, no coding.)
   """,
   ["Requirements and constraints (single machine, low latency)", "IPC choice: shared memory ring buffer, Unix domain sockets, mmap",
    "Subscription registry: process -> set of symbols", "Per-symbol fan-out and zero-copy considerations",
    "Slow / dead consumer detection and cleanup (heartbeats, drop policy)", "Backpressure: overwrite vs block vs disconnect",
    "State management and recovery on restart", "Snapshot + incremental updates for late joiners"])

bl("10.17-rate-limiting-service", "10.17 [bl] Rate limiting service",
   """
Design a rate limiting service.
   """,
   ["Requirements: per-user / per-API / global limits", "Algorithm (token bucket / sliding window)",
    "Centralized vs distributed counters (Redis, local + sync)", "Latency budget: must not slow the request path",
    "Failure mode: fail-open vs fail-closed", "Configuration and rule distribution", "Response semantics (429, Retry-After, headers)"])

bl("10.18-notification-service", "10.18 [bl] Generic notification service",
   """
Design a notification service.
   """,
   ["Requirements", "Channels: push (APNs/FCM), email, SMS, in-app", "Template and localization service",
    "User preferences, quiet hours, opt-out", "Rate limiting and batching / digest", "Provider abstraction and failover",
    "Retries, idempotency, delivery tracking", "Priority lanes"])

TREE.append(("p10", "Part 10 - Bloomberg Interview Prep", "Real Bloomberg system design questions, one page each. Prompts captured verbatim; notes to be written.", BL))

TREE.append(("p11", "Part 11 - Resources: Blogs and Papers", "Read these alongside the notes.", [
    ("11.1-papers", "11.1 Papers list (annotated)",
     stub(["Lamport - Time, Clocks, and the Ordering of Events (1978)", "Chandy-Lamport - Distributed Snapshots (1985)",
           "FLP - Impossibility of Consensus with One Faulty Process (1985)", "Google - GFS (2003), MapReduce (2004), Bigtable (2006)",
           "Amazon - Dynamo (2007)", "Google - Chubby (2006), Spanner (2012), Percolator (2010)",
           "Kafka - a Distributed Messaging System (2011)", "Raft - In Search of an Understandable Consensus Algorithm (2014)",
           "Google - Dapper (2010), Borg (2015), Monarch (2020)", "Cassandra (2010)"])),
    ("11.2-books-courses", "11.2 Books and courses",
     stub(["Designing Data-Intensive Applications (Kleppmann) + chapter index", "Kleppmann distributed systems lecture series (Cambridge)",
           "Database Internals (Petrov)", "Understanding Distributed Systems (Vitillo)"])),
    ("11.3-blogs", "11.3 Engineering blogs and curated lists",
     stub(["awesome-distributed-systems (GitHub)", "Murat Buffalo's blog", "Marc Brooker's blog", "Aphyr / Jepsen analyses",
           "High Scalability", "Company eng blogs: Netflix, Uber, Discord, Cloudflare, Stripe, Figma"])),
]))

if __name__ == "__main__":
    part_filter = sys.argv[1] if len(sys.argv) > 1 else None
    for part_slug, part_title, part_intro, leaves in TREE:
        if part_filter and part_slug != part_filter:
            continue
        pid = create(part_slug, part_title, ROOT_ID, f"# {part_title}\n\n{part_intro}")
        for leaf in leaves:
            lslug, ltitle, lbody = leaf
            create(lslug, ltitle, pid, f"# {ltitle}\n\n{lbody}")
    print("\nDONE. Map at", MAP_PATH)
