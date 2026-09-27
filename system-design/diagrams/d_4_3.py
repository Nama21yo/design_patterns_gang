"""Diagrams for note 4.3 - Redis and Memcached deep dive."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def redis_data_structures():
    render("4-3-redis-data-structures", f"""
    rankdir=LR;
    root [label="Redis value types", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    str_ [label="String\\l'user:42:name' -> 'Abebe'\\lblobs, counters (INCR)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    hash_ [label="Hash\\l'user:42' -> {{name, age, city}}\\la row without a DB", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    set_ [label="Set\\l'post:9:likes' -> {{user1,user2}}\\lmembership + set algebra", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    zset [label="Sorted set (ZSET)\\l'leaderboard' -> member:score\\lTHE leaderboard structure", fillcolor="{GRAY}", color="{SLATE}"];
    list_ [label="List\\l'notifications:42' -> [...]\\lqueue / recent-activity feed", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    root -> str_; root -> hash_; root -> set_; root -> zset; root -> list_;
    """)


def persistence():
    render("4-3-persistence", f"""
    rankdir=LR;

    subgraph cluster_rdb {{
        label="RDB (snapshotting)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        r1 [label="Periodic point-in-time\\lsnapshot of the whole\\ldataset to disk", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        r2 [label="Fast restart (load one\\lfile), compact, but can\\llose everything since the\\lLAST snapshot on a crash", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        r1 -> r2;
    }}

    subgraph cluster_aof {{
        label="AOF (append-only file)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        a1 [label="Log EVERY write\\loperation, like a WAL (3.1)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        a2 [label="Much less data loss on\\lcrash (configurable fsync),\\lbut a bigger file, slower\\lto replay on restart", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        a1 -> a2;
    }}

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Most production Redis uses BOTH: RDB for fast full backups/restarts,\\lAOF for minimizing the loss window - the same durability-vs-speed\\ltrade 3.5 covers for database replication, one layer over.\\l"];
    r2 -> note [style=invis]; a2 -> note [style=invis];
    """)


def memcached_slabs():
    render("4-3-memcached-slabs", f"""
    rankdir=LR;
    item [label="SET a 100-byte item", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    classes [label="Slab CLASSES\\l(e.g. 96B, 120B, 152B...\\lgrowth factor ~1.25x)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    chosen [label="Rounds UP to the\\lnearest class (120B)\\l-> that class's slab\\l(4.7's slab allocator,\\lexactly)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    item -> classes -> chosen;

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="Simpler than Redis on purpose: key -> byte blob only, no rich\\ltypes, multi-threaded (Redis is famously single-threaded per\\lcore), no persistence, no replication built in. The slab\\lallocator is WHY Memcached doesn't fragment under constant\\lsame-ish-sized churn - same trade-off 4.7 covered generally.\\l"];
    chosen -> note [style=invis];
    """)


def scaling_cache():
    render("4-3-scaling-cache", f"""
    rankdir=LR;

    subgraph cluster_v {{
        label="Vertical scaling";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        v1 [label="one bigger Redis\\linstance - more RAM,\\lmore CPU", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    }}

    subgraph cluster_h {{
        label="Horizontal scaling (Redis Cluster / client-side sharding)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        h1 [label="shard A\\l(hash slot range)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        h2 [label="shard B", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        h3 [label="shard C", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        {{ rank=same; h1; h2; h3 }}
    }}

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="Exactly 3.4's sharding/partitioning ideas, applied to a cache instead\\lof a database: consistent hashing across shards, each shard usually\\lALSO replicated (3.5) for its own availability. The cost of scaling\\lout: cross-shard operations (multi-key transactions, some ZSET/SET\\lalgebra spanning keys on different shards) get much harder or\\limpossible - the same cross-shard trade-off 3.4 already named.\\l"];
    h1 -> note [style=invis];
    """)


if __name__ == "__main__":
    redis_data_structures()
    persistence()
    memcached_slabs()
    scaling_cache()
