"""Diagrams for note 3.1 - Storage engines."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)
import math


def hdd_structure():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(6.8, 6.8))
    import numpy as np
    theta = np.linspace(0, 2 * math.pi, 300)
    # concentric tracks
    radii = np.linspace(1.2, 4.6, 7)
    for i, r in enumerate(radii):
        ax.plot(r * np.cos(theta), r * np.sin(theta), color=SLATE, lw=1, alpha=0.6)
    ax.text(radii[2] * math.cos(0.15), radii[2] * math.sin(0.15), "track 2",
           fontsize=8, color=SLATE, ha="left")
    ax.text(radii[5] * math.cos(0.15), radii[5] * math.sin(0.15), "track 5",
           fontsize=8, color=SLATE, ha="left")
    # sector spokes
    n_sectors = 12
    for k in range(n_sectors):
        a = 2 * math.pi * k / n_sectors
        ax.plot([1.2 * math.cos(a), 4.6 * math.cos(a)], [1.2 * math.sin(a), 4.6 * math.sin(a)],
               color=GRAY, lw=0.8)
    # highlight one block = intersection of track 5 and one sector
    a0, a1 = 2 * math.pi * 1 / n_sectors, 2 * math.pi * 2 / n_sectors
    r0, r1 = radii[4], radii[5]
    wedge_theta = np.linspace(a0, a1, 20)
    xs = list(r0 * np.cos(wedge_theta)) + list(r1 * np.cos(wedge_theta[::-1]))
    ys = list(r0 * np.sin(wedge_theta)) + list(r1 * np.sin(wedge_theta[::-1]))
    ax.fill(xs, ys, color=AMBER, alpha=0.85, zorder=5)
    ax.annotate("this wedge on this track = one BLOCK\n(track 5, sector 1)",
               xy=(r0 * math.cos((a0+a1)/2)*1.05, r0 * math.sin((a0+a1)/2)*1.05),
               xytext=(0.3, -5.6), fontsize=9.5, color=INK,
               arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.4))
    # spindle
    ax.scatter([0], [0], s=60, color=INK, zorder=6)
    ax.text(0, -0.5, "spindle", fontsize=8, ha="center", color=SLATE)
    ax.set_xlim(-5.5, 5.5); ax.set_ylim(-6.4, 5.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("One platter surface: concentric tracks, radial sectors,\n"
                 "a (track, sector) pair identifies one block", fontsize=11)
    return save_mpl(fig, "3-1-hdd-structure")


def address_translation():
    render("3-1-address-translation", f"""
    rankdir=LR;
    byte [label="Give me byte offset\\l4,398,221 of this file", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    fs [label="File system\\lfile offset -> (device, block number)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    addr [label="Disk controller\\lblock number -> (track, sector)\\l+ byte offset within the sector", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    seek [label="Seek: move the head\\lto that track", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    rot [label="Rotate: wait for that\\lsector to pass under the head", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    read [label="Read the block,\\lreturn the requested\\lbytes from the offset", fillcolor="{GRAY}", color="{SLATE}"];

    byte -> fs -> addr -> seek -> rot -> read;
    """)


def multilevel_index():
    render("3-1-multilevel-index", f"""
    rankdir=TB;
    data [label="100 data records\\l(sorted on disk by key)", fillcolor="{GRAY}", color="{SLATE}"];
    idx1 [label="Level-1 index: 100 entries\\l(key -> block pointer)\\lone entry per record - still\\lbig enough to scan slowly", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    data2 [label="1,000 data records", fillcolor="{GRAY}", color="{SLATE}"];
    idxA [label="Level-1 index: 1,000 entries\\l(key -> block pointer)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    idxB [label="Level-2 index: ~32 entries\\l(key range -> level-1 block)\\l'an index about the index'", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    data -> idx1 [label="  index built over"];
    data2 -> idxA [label="  index built over"];
    idxA -> idxB [label="  index built over\\l  THE INDEX ITSELF"];

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="Keep doing this - indexing the index, then indexing\\lTHAT index - and the natural, self-balancing limit\\lof 'how many levels' is exactly what a B-tree formalizes.\\l"];
    idxB -> note [style=invis];
    """)


def mway_insertion_problem():
    render("3-1-mway-insertion-problem", f"""
    rankdir=LR;
    a [label="Balanced m-way tree\\l(like a wide BST)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    b [label="Insert one key in\\lthe wrong spot", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    c [label="Subtree below it can\\lbecome unbalanced -\\lheight grows unevenly", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    d [label="Unbalanced = some lookups\\lnow cost more disk reads\\lthan others - unacceptable\\lfor an on-disk index", fillcolor="{GRAY}", color="{SLATE}"];
    a -> b -> c -> d;
    """)


def btree_rules():
    render("3-1-btree-rules", f"""
    rankdir=TB;
    root [label="root: 2 to m children\\l(at least 2, even though\\linterior nodes need ceil(m/2))", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    n1 [label="interior node\\lceil(m/2) to m children\\l(never less than half full)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    n2 [label="interior node\\lceil(m/2) to m children", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    l1 [label="leaf", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l2 [label="leaf", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l3 [label="leaf", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l4 [label="leaf", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    root -> n1; root -> n2;
    n1 -> l1; n1 -> l2;
    n2 -> l3; n2 -> l4;
    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="ALL leaves at the same depth, always -\\lgrowth happens by splitting and pushing\\la key UP, never by adding depth at the\\lbottom. This is the 'bottom-up' construction:\\lthe tree grows from repeated leaf splits,\\lroot included, not from inserting under a\\lfixed root like a plain BST.\\l"];
    l2 -> note [style=invis];
    """)


def btree_insertion_split():
    render("3-1-btree-insertion-split", f"""
    rankdir=LR;
    node [shape=box];

    before [label="Leaf (max 3 keys): [10|20|30]\\linsert 25 -> would be [10|20|25|30]\\l-> OVERFULL", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    split [label="Split at the median (25):\\lleft=[10|20]  right=[30]\\lpush 25 UP to the parent", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    after [label="Parent gains a key + a\\lchild pointer. If the PARENT\\lis now overfull, it splits too -\\lsplits can cascade to the root.", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    root [label="If the ROOT splits, a brand\\lnew root is created above it -\\lthis is the ONLY way a B-tree\\lgrows taller.", fillcolor="{INK}", fontcolor=white, color="{INK}"];

    before -> split -> after -> root;
    """)


def bplustree_structure():
    render("3-1-bplustree-structure", f"""
    rankdir=TB;
    root [label="root (routing only,\\lno record pointers)\\l[ 30 | 60 ]", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    n1 [label="[ 10 | 20 ]", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    n2 [label="[ 40 | 50 ]", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    n3 [label="[ 70 | 80 ]", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    l1 [label="leaf: 10,20\\l-> record ptrs", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l2 [label="leaf: 30,40,50\\l-> record ptrs", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l3 [label="leaf: 60,70\\l-> record ptrs", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l4 [label="leaf: 80,90\\l-> record ptrs", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    root -> n1; root -> n2; root -> n3;
    n1 -> l1; n1 -> l2;
    n2 -> l2; n2 -> l3;
    n3 -> l3; n3 -> l4;

    l1 -> l2 -> l3 -> l4 [constraint=false, color="{AMBER}", penwidth=2,
                         label="  leaves linked - a range scan never\\l  revisits the interior nodes at all"];
    """)


def lsm_tree():
    render("3-1-lsm-tree", f"""
    rankdir=TB;
    write [label="Write(key, value)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    wal [label="1. Append to WAL\\l(crash safety)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    mem [label="2. Insert into MemTable\\l(in-memory sorted structure,\\le.g. a skip list / balanced tree)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    flush [label="3. MemTable full\\l-> flush as an immutable,\\lsorted SSTable file on disk", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    l0 [label="Level 0 SSTables\\l(newest, many small files)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l1 [label="Level 1 SSTables\\l(compacted, fewer/bigger)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l2 [label="Level 2 SSTables\\l(oldest, biggest, fewest)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    write -> wal -> mem -> flush -> l0;
    l0 -> l1 [label="  compaction: merge +\\l  drop overwritten/deleted keys"];
    l1 -> l2 [label="  compaction"];

    read [label="Read(key)", fillcolor="{GRAY}", color="{SLATE}"];
    read -> mem [label="  check newest first...", style=dashed];
    read -> l0 [style=dashed];
    read -> l1 [style=dashed];
    read -> l2 [label="  ...oldest last", style=dashed];
    """)


def base_pillars():
    render("3-1-base-pillars", f"""
    rankdir=LR;
    a [label="Basically Available\\lthe system responds,\\leven under failure\\l(maybe with stale data)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    s [label="Soft state\\lstate can change over\\ltime even with no new\\linput, while it converges", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    e [label="Eventual consistency\\lgiven enough time with\\lno new writes, all replicas\\lconverge to the same value", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    a -> s -> e [style=invis];
    """)


def gfs_architecture():
    render("3-1-gfs-architecture", f"""
    rankdir=LR;
    client [label="Client", fillcolor="{GRAY}", color="{SLATE}"];
    master [label="Master\\l(metadata only: which\\lchunks belong to which\\lfile, which servers hold\\lthem - never the data itself)", fillcolor="{INK}", fontcolor=white, color="{INK}"];

    cs1 [label="Chunkserver 1\\l64MB chunks", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    cs2 [label="Chunkserver 2\\l64MB chunks", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    cs3 [label="Chunkserver 3\\l64MB chunks", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    client -> master [label="  1. where are the\\l  chunks for file X?", dir=both];
    client -> cs1 [label="  2. read/write chunk\\l  data directly", color="{BLUE}"];
    client -> cs2 [style=invis];

    cs1 -> cs2 [label="  each chunk replicated\\l  (usually 3x) across\\l  chunkservers", style=dashed, color="{SLATE}"];
    cs2 -> cs3 [style=dashed, color="{SLATE}"];

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="The master is consulted for METADATA only, once per\\lfile/chunk lookup - actual data never flows through it,\\lso it never becomes the throughput bottleneck.\\l"];
    master -> note [style=invis];
    """)


if __name__ == "__main__":
    hdd_structure()
    address_translation()
    multilevel_index()
    mway_insertion_problem()
    btree_rules()
    btree_insertion_split()
    bplustree_structure()
    lsm_tree()
    base_pillars()
    gfs_architecture()
