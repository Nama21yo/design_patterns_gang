"""Diagrams for note 3.4 - Partitioning / sharding."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def vertical_vs_horizontal_scaling():
    render("3-4-vertical-vs-horizontal-scaling", f"""
    rankdir=LR;

    subgraph cluster_v {{
        label="Vertical scaling - one bigger box";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        v1 [label="small\\linstance", fillcolor="{LIGHTBLUE}", color="{BLUE}", width=0.9];
        v2 [label="bigger\\linstance", fillcolor="{LIGHTBLUE}", color="{BLUE}", width=1.3];
        v3 [label="biggest\\linstance you\\lcan buy", fillcolor="{LIGHTBLUE}", color="{BLUE}", width=1.7];
        v1 -> v2 -> v3 [label="  upgrade"];
    }}

    subgraph cluster_h {{
        label="Horizontal scaling - more boxes";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        h1 [label="instance", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        h2 [label="instance", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        h3 [label="instance", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        h4 [label="instance", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        {{ rank=same; h1; h2; h3; h4 }}
    }}
    """)


def sharding_vs_partition_vs_replica():
    render("3-4-sharding-partition-replica", f"""
    rankdir=TB;

    subgraph cluster_a {{
        label="Replication (read replicas) - no partitioning";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        p1 [label="Primary\\lALL data (rows 1-1000)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
        r1 [label="Replica\\lALL data (rows 1-1000)\\l(a full copy)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        r2 [label="Replica\\lALL data (rows 1-1000)\\l(a full copy)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        p1 -> r1 [label="  replicate"]; p1 -> r2 [label="  replicate"];
    }}

    subgraph cluster_b {{
        label="Sharding - each shard holds a different PARTITION";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        s1 [label="Shard A\\lpartition: rows 1-333", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        s2 [label="Shard B\\lpartition: rows 334-666", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        s3 [label="Shard C\\lpartition: rows 667-1000", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        {{ rank=same; s1; s2; s3 }}
    }}

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="Each shard is usually ALSO replicated for durability -\\lsharding and replication are independent axes you combine,\\lnot alternatives to each other.\\l"];
    r1 -> note [style=invis];
    """)


def horizontal_vs_vertical_partitioning():
    render("3-4-horizontal-vs-vertical-partitioning", f"""
    rankdir=TB;

    orig [label="users table\\lid | name | email | bio | last_login", fillcolor="{GRAY}", color="{SLATE}"];

    subgraph cluster_h {{
        label="Horizontal partitioning - split by ROW";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        h1 [label="partition 1\\lrows: id 1-1000\\l(same columns)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        h2 [label="partition 2\\lrows: id 1001-2000\\l(same columns)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    }}

    subgraph cluster_v {{
        label="Vertical partitioning - split by COLUMN";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        v1 [label="partition 1\\lid | name | email\\l(hot, small columns)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        v2 [label="partition 2\\lid | bio | last_login\\l(cold / large columns)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    }}

    orig -> h1 [style=invis]; orig -> v1 [style=invis];
    """)


def hash_vs_range():
    render("3-4-hash-vs-range-partitioning", f"""
    rankdir=LR;

    subgraph cluster_hash {{
        label="Hash partitioning";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        hk [label="key -> hash(key) % N\\l-> uniform spread,\\lno range queries", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        hn1 [label="node 0", fillcolor="white"]; hn2 [label="node 1", fillcolor="white"]; hn3 [label="node 2", fillcolor="white"];
        hk -> hn1; hk -> hn2; hk -> hn3;
    }}

    subgraph cluster_range {{
        label="Range partitioning";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        rk [label="key -> which range\\lit falls in\\l-> easy range scans,\\lrisk of hot ranges", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        rn1 [label="node 0\\lA - I", fillcolor="white"]; rn2 [label="node 1\\lJ - R", fillcolor="white"]; rn3 [label="node 2\\lS - Z", fillcolor="white"];
        rk -> rn1; rk -> rn2; rk -> rn3;
    }}
    """)


def consistent_hash_ring():
    plt = mpl()
    import numpy as np
    fig, ax = plt.subplots(figsize=(6.4, 6.4), subplot_kw={"projection": "polar"})
    node_colors = {0: BLUE, 1: TEAL, 2: AMBER}
    import random
    random.seed(11)
    vnodes = {0: [], 1: [], 2: []}
    for node in range(3):
        for v in range(8):
            vnodes[node].append(random.uniform(0, 2 * 3.14159))
    for node, angles in vnodes.items():
        ax.scatter(angles, [1] * len(angles), s=140, color=node_colors[node], zorder=3,
                  label=f"node {node} (virtual nodes)", edgecolor="white")
    key_angle = 1.1
    ax.scatter([key_angle], [1], marker="*", s=400, color=RED, zorder=4, label="key K")
    # find clockwise-next vnode
    all_pts = [(a, node) for node, angs in vnodes.items() for a in angs]
    nxt = min((a for a, n in all_pts if a > key_angle), default=min(a for a, n in all_pts))
    ax.annotate("", xy=(nxt, 1), xytext=(key_angle, 1),
               arrowprops=dict(arrowstyle="->", color=RED, lw=1.6, connectionstyle="arc3,rad=0.15"))
    ax.set_ylim(0, 1.3)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title("Consistent hashing ring: K is owned by the\nnext virtual node clockwise",
                 pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=8, frameon=False)
    return save_mpl(fig, "3-4-consistent-hash-ring")


def rebalancing_cost():
    plt = mpl()
    ns = [4, 8, 16]
    naive = [0.801, 0.890, 0.941]
    consistent = [0.178, 0.102, 0.053]
    x = range(len(ns))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.bar([i - width/2 for i in x], naive, width, label="naive hash(key) % N", color=RED)
    ax.bar([i + width/2 for i in x], consistent, width, label="consistent hashing (100 vnodes/node)", color=TEAL)
    for i, (a, b) in enumerate(zip(naive, consistent)):
        ax.text(i - width/2, a + 0.02, f"{a:.0%}", ha="center", fontsize=9)
        ax.text(i + width/2, b + 0.02, f"{b:.0%}", ha="center", fontsize=9)
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{n} -> {n+1} nodes" for n in ns])
    ax.set_ylabel("fraction of keys that must move")
    ax.set_ylim(0, 1.05)
    ax.set_title("Measured: keys remapped when adding one node", loc="left", pad=12)
    ax.legend(frameon=False, fontsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "3-4-rebalancing-cost")


def secondary_index_strategies():
    render("3-4-secondary-index-strategies", f"""
    rankdir=TB;

    q [label="Query: find items WHERE color = 'red'\\l(sharded by item_id, not by color)", fillcolor="{INK}", fontcolor=white, color="{INK}"];

    subgraph cluster_local {{
        label="Local secondary index - index lives with the data shard";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        l1 [label="Shard A\\l+ local index on color", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        l2 [label="Shard B\\l+ local index on color", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        l3 [label="Shard C\\l+ local index on color", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        lnote [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}", label="must fan out to ALL\\lshards, scatter-gather\\l(cheap write, expensive read)"];
    }}

    subgraph cluster_global {{
        label="Global secondary index - a separate index, itself partitioned by color";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        g1 [label="Index shard: red\\l-> [item ids...]", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        g2 [label="Index shard: blue\\l-> [item ids...]", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        gnote [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}", label="query hits ONE index shard\\l(cheap read, but the write\\lnow needs a second, cross-\\lshard update - often async)"];
    }}

    q -> l1; q -> l2; q -> l3;
    q -> g1;
    """)


if __name__ == "__main__":
    vertical_vs_horizontal_scaling()
    sharding_vs_partition_vs_replica()
    horizontal_vs_vertical_partitioning()
    hash_vs_range()
    consistent_hash_ring()
    rebalancing_cost()
    secondary_index_strategies()
