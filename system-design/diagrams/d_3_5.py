"""Diagrams for note 3.5 - Replication."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def leader_follower():
    render("3-5-leader-follower", f"""
    rankdir=LR;
    client [label="Clients", fillcolor="{GRAY}", color="{SLATE}"];
    leader [label="Leader\\l(accepts ALL writes)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    f1 [label="Follower 1\\l(replays the leader's\\lWAL / oplog)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    f2 [label="Follower 2", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    f3 [label="Follower 3", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    client -> leader [label="  writes"];
    client -> f1 [label="  reads", style=dashed, color="{BLUE}"];
    client -> f2 [style=dashed, color="{BLUE}"];
    client -> f3 [style=dashed, color="{BLUE}"];
    leader -> f1 [label="  replicate"];
    leader -> f2 [label="  replicate"];
    leader -> f3 [label="  replicate"];
    {{ rank=same; f1; f2; f3 }}
    """)


def sync_vs_async_timeline():
    plt = mpl()
    fig, axes = plt.subplots(2, 1, figsize=(10, 4.4), sharex=True)

    ax = axes[0]
    ax.set_title("Asynchronous replication - measured", loc="left", fontsize=10.5)
    ax.barh(0, 0.001, left=0, height=0.5, color=TEAL)
    ax.text(0.0015, 0, "primary COMMIT returns\nafter ~0.8 ms (doesn't wait)", fontsize=8.5, va="center")
    ax.barh(-1, 1.24, left=0, height=0.3, color=LIGHTBLUE, edgecolor=BLUE)
    ax.text(1.3, -1, "replica catches up ~1.24 ms later\n(measured; a read just before this\ncan return the OLD value)", fontsize=8.5, va="center")
    ax.set_xlim(-0.3, 6)
    ax.set_ylim(-2, 1)
    ax.axis("off")

    ax = axes[1]
    ax.set_title("Synchronous replication - measured (standby unreachable)", loc="left", fontsize=10.5)
    ax.barh(0, 4.06, left=0, height=0.5, color=RED)
    ax.text(4.2, 0, "primary COMMIT BLOCKS for 4.06s\nuntil the standby reconnects and acks", fontsize=8.5, va="center")
    ax.set_xlim(-0.3, 6)
    ax.set_ylim(-1, 1)
    ax.set_xlabel("seconds since the write was issued")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_yticks([])
    return save_mpl(fig, "3-5-sync-vs-async-timeline")


def multi_leader():
    render("3-5-multi-leader", f"""
    rankdir=LR;
    c1 [label="Clients\\l(region A)", fillcolor="{GRAY}", color="{SLATE}"];
    c2 [label="Clients\\l(region B)", fillcolor="{GRAY}", color="{SLATE}"];
    l1 [label="Leader A", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    l2 [label="Leader B", fillcolor="{INK}", fontcolor=white, color="{INK}"];

    c1 -> l1 [label="  writes"];
    c2 -> l2 [label="  writes"];
    l1 -> l2 [label="  replicate\\l  (both directions)", dir=both, color="{AMBER}", penwidth=2];

    conflict [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
             label="Same row written on BOTH leaders before either\\lreplicates to the other -> CONFLICT. Someone has\\lto resolve it: last-write-wins (simple, can silently\\ldrop a write), app-level merge, or a CRDT\\l(convergent data type - the merge is defined so\\lit's always resolvable without coordination).\\l"];
    l1 -> conflict [style=invis];
    """)


def leaderless_quorum():
    render("3-5-leaderless-quorum", f"""
    rankdir=TB;
    client [label="Client: write(key, v)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    n1 [label="Node 1\\lACK", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    n2 [label="Node 2\\lACK", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    n3 [label="Node 3\\l(slow / down)", fillcolor="{GRAY}", color="{SLATE}"];
    ok [label="W=2 acks received\\l-> write succeeds\\l(didn't wait for node 3)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    client -> n1; client -> n2; client -> n3;
    n1 -> ok; n2 -> ok;

    read [label="Client: read(key)\\lqueries R=2 nodes,\\ltakes the newest\\l(highest version)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    ok -> read [style=dashed, color="{SLATE}", label="  later"];

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="N=3 replicas.  R + W > N  (e.g. R=2, W=2, N=3: 2+2=4 > 3)\\lguarantees every read overlaps at least one node that\\lhas the latest write - no leader required, any node can\\lcoordinate a request, tolerates N-W nodes being down\\lfor writes and N-R nodes being down for reads.\\l"];
    read -> note [style=invis];
    """)


def read_repair():
    render("3-5-read-repair", f"""
    rankdir=LR;
    client [label="Client: read(key)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    n1 [label="Node 1: v=5\\l(stale)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    n2 [label="Node 2: v=7\\l(latest)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    n3 [label="Node 3: v=7\\l(latest)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    client -> n1; client -> n2; client -> n3;
    fix [label="Coordinator notices node 1\\lis behind -> writes v=7 back\\lto node 1 in the background\\l('read repair')", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    n1 -> fix [style=dashed, color="{RED}"];
    n2 -> fix [style=dashed];

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Anti-entropy: separately, a background process continuously\\lcompares replicas (e.g. via Merkle trees) and repairs drift\\leven for keys nobody has read recently.\\l"];
    fix -> note [style=invis];
    """)


if __name__ == "__main__":
    leader_follower()
    sync_vs_async_timeline()
    multi_leader()
    leaderless_quorum()
    read_repair()
