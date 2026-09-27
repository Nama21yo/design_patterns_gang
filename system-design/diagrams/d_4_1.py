"""Diagrams for note 4.1 - Caching strategies and eviction."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def caching_patterns():
    render("4-1-caching-patterns", f"""
    rankdir=TB;

    subgraph cluster_aside {{
        label="Cache-aside (lazy loading)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        a1 [label="App checks cache", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        a2 [label="miss -> app reads DB,\\lapp writes cache itself", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        a1 -> a2;
    }}
    subgraph cluster_rt {{
        label="Read-through";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        b1 [label="App only ever\\ltalks to the cache", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        b2 [label="miss -> the CACHE ITSELF\\lloads from the DB\\l(app never sees a miss)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        b1 -> b2;
    }}
    subgraph cluster_wt {{
        label="Write-through";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        c1 [label="App writes to cache", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        c2 [label="cache synchronously\\lwrites through to the DB\\lbefore acking", fillcolor="{GRAY}", color="{SLATE}"];
        c1 -> c2;
    }}
    subgraph cluster_wb {{
        label="Write-behind (write-back)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        d1 [label="App writes to cache,\\lacked IMMEDIATELY", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        d2 [label="cache flushes to the DB\\lLATER, asynchronously,\\lbatched", fillcolor="{RED}", fontcolor=white, color="{RED}"];
        d1 -> d2;
    }}
    """)


def population_lazy_eager():
    render("4-1-population-lazy-eager", f"""
    rankdir=LR;

    subgraph cluster_lazy {{
        label="Lazy population - populate ON a cache miss";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        l1 [label="request arrives", fillcolor="{GRAY}", color="{SLATE}"];
        l2 [label="cache miss", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        l3 [label="fetch from source,\\lcache it with a TTL", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        l1 -> l2 -> l3;
        lnote [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}", label="e.g. caching a blog post -\\lonly cache what's actually\\lrequested; simple; first\\lrequest after expiry pays\\lthe full cost\\l"];
        l3 -> lnote [style=invis];
    }}

    subgraph cluster_eager {{
        label="Eager population - populate PROACTIVELY, before it's asked for";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        e1 [label="a write happens\\l(or a predicted-hot\\levent occurs)", fillcolor="{GRAY}", color="{SLATE}"];
        e2 [label="update the DB AND\\lpush the new value into\\lthe cache immediately", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        e1 -> e2;
        enote [shape=note, fillcolor="{LIGHTBLUE}", color="{BLUE}", label="e.g. a celebrity's tweet -\\ldon't wait for the stampede\\lof readers to each trigger\\la miss; push it in ahead of\\ltime so every reader hits\\l"];
        e2 -> enote [style=invis];
    }}
    """)


def caching_levels():
    render("4-1-caching-levels", f"""
    rankdir=LR;
    client [label="Client-side\\l(browser/app cache -\\lnear-constant data,\\ltime-based invalidation)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    cdn [label="CDN\\l(static assets, images,\\lvideo - geographically\\lnearest edge, 4.4)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    lb [label="Load balancer\\l(can cache full HTTP\\lresponses for identical\\lrequests)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    remote [label="Remote cache\\l(Redis/Memcached -\\lcentralized, shared,\\l4.3)", fillcolor="{GRAY}", color="{SLATE}"];
    db [label="Database-level\\l(a denormalized column,\\lmaterialized view -\\lavoid recomputation)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    never [label="NEVER cache\\l(account balance,\\lanything where staleness\\lis a correctness bug)", fillcolor="{RED}", fontcolor=white, color="{RED}"];

    client -> cdn -> lb -> remote -> db -> never [style=invis];
    {{ rank=same; client; cdn; lb; remote; db; never }}
    """)


def eviction_comparison():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8.5, 4))
    results = {"LFU": 60.0, "LRU": 46.9, "FIFO": 41.1, "Random": 41.0, "MRU": 14.3}
    items = sorted(results.items(), key=lambda kv: -kv[1])
    labels = [k for k, v in items]
    vals = [v for k, v in items]
    colors = [TEAL, BLUE, AMBER, SLATE, RED]
    ax.bar(labels, vals, color=colors, width=0.55)
    for i, v in enumerate(vals):
        ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontsize=10)
    ax.set_ylabel("hit rate")
    ax.set_ylim(0, 70)
    ax.set_title("Measured on a stationary Zipf-skewed access trace,\nsame capacity, 5 eviction policies",
                 loc="left", pad=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "4-1-eviction-comparison")


def lru_structure():
    render("4-1-lru-structure", f"""
    rankdir=LR;
    map [label="hashmap\\lkey -> node pointer\\l(O(1) lookup)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    head [label="HEAD\\l(dummy)", fillcolor="{GRAY}", color="{SLATE}"];
    n1 [label="node: key=c\\l(most recently used)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    n2 [label="node: key=a", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    n3 [label="node: key=b\\l(least recently used)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    tail [label="TAIL\\l(dummy)", fillcolor="{GRAY}", color="{SLATE}"];

    head -> n1 -> n2 -> n3 -> tail [dir=both];
    map -> n1 [style=dashed, color="{AMBER}", label="  O(1) find"];
    map -> n2 [style=dashed, color="{AMBER}"];
    map -> n3 [style=dashed, color="{AMBER}"];

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="get(key): hashmap finds the node in O(1), unlink it, relink it\\lright after HEAD (now most-recent) - O(1).\\lput() over capacity: evict TAIL.prev (the LRU node) - O(1).\\lNeither structure alone gives O(1) for both 'find by key' AND\\l'reorder by recency' - together, they do.\\l"];
    tail -> note [style=invis];
    """)


def lruk_scan_resistance():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    labels = ["plain LRU", "LRU-2"]
    vals = [0.0, 95.0]
    colors = [RED, TEAL]
    ax.bar(labels, vals, color=colors, width=0.45)
    for i, v in enumerate(vals):
        ax.text(i, v + 2, f"{v:.0f}%", ha="center", fontsize=12)
    ax.set_ylabel("hit rate on the HOT SET\n(after a one-time scan pollutes the cache)")
    ax.set_ylim(0, 105)
    ax.set_title("Verified: a one-time index/table scan interleaved with hot\ntraffic - LRU-2 refuses to let single-touch pages evict the hot set",
                 loc="left", pad=10, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "4-1-lruk-scan-resistance")


if __name__ == "__main__":
    caching_patterns()
    population_lazy_eager()
    caching_levels()
    eviction_comparison()
    lru_structure()
    lruk_scan_resistance()
