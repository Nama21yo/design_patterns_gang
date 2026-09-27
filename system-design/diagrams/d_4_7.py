"""Diagrams for note 4.7 - Memory allocation."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def fit_algorithms():
    plt = mpl()
    fig, axes = plt.subplots(4, 1, figsize=(9, 5.6), sharex=True)
    holes = [100, 500, 200, 300, 600]
    starts = [0]
    for h in holes[:-1]:
        starts.append(starts[-1] + h + 15)
    request = 180

    picks = {"First-fit\n(first hole >= 180)": 1,
            "Best-fit\n(smallest hole that fits)": 2,
            "Worst-fit\n(largest hole)": 4,
            "Next-fit\n(from last position, wrapping)": 1}

    for ax, (label, idx) in zip(axes, picks.items()):
        for i, (s, h) in enumerate(zip(starts, holes)):
            color = AMBER if i == idx else LIGHTTEAL
            edge = AMBER if i == idx else TEAL
            ax.barh(0, h, left=s, height=0.6, color=color, edgecolor=edge)
            ax.text(s + h/2, 0, f"{h}", ha="center", va="center", fontsize=8)
        ax.set_xlim(-10, starts[-1] + holes[-1] + 10)
        ax.set_yticks([])
        ax.set_ylabel(label, rotation=0, ha="right", va="center", fontsize=9)
        for s_ in ("top", "right", "left"):
            ax.spines[s_].set_visible(False)
    axes[0].set_title(f"Same free-hole layout, same request (180 bytes) - which hole gets picked",
                     loc="left", pad=10)
    axes[-1].set_xlabel("memory address ->  (hole sizes labeled)")
    return save_mpl(fig, "4-7-fit-algorithms")


def fragmentation_result():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    labels = ["allocated\nblocks", "free\nholes"]
    values = [52, 30]
    colors = [BLUE, AMBER]
    ax.bar(labels, values, color=colors, width=0.5)
    for i, v in enumerate(values):
        ax.text(i, v + 1, str(v), ha="center", fontsize=11)
    ax.set_title("Measured after 4,000 random alloc/free ops (WITH coalescing):\n"
                 "holes / allocated = 0.577 - Knuth's fifty-percent rule predicts ~0.5",
                 loc="left", pad=10, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "4-7-fragmentation-result")


def slab_allocation():
    render("4-7-slab-allocation", f"""
    rankdir=TB;
    req [label="alloc() for a fixed-size\\lobject (e.g. a 64B struct)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    cache [label="Slab cache for size 64B", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    slab1 [label="Slab 1 (1 page)\\l[used][free][used][used]\\lpre-carved into 64B slots", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    slab2 [label="Slab 2 (1 page)\\l[free][free][used][used]", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    req -> cache;
    cache -> slab1 [label="  pop a free slot\\l  O(1), no search"];
    cache -> slab2 [style=dashed, color="{SLATE}"];

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="Every slot is EXACTLY the requested size - no splitting, no\\lsearching for a hole, no external fragmentation at all for\\lthis object type. New slabs are added only when every existing\\lone is full. This is what Memcached's memory allocator (4.3)\\luses internally to avoid fragmenting under constant small,\\lsame-sized alloc/free churn.\\l"];
    slab1 -> note [style=invis];
    """)


def buddy_allocation():
    render("4-7-buddy-allocation", f"""
    rankdir=TB;
    root [label="1024B (order 10) - free", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l1a [label="512B - free", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l1b [label="512B (order 9) - SPLIT again", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    l2a [label="256B - ALLOCATED\\l(alloc(200) rounds up)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    l2b [label="256B (order 8) - split again", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    l3a [label="128B - ALLOCATED\\l(alloc(100) rounds up)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    l3b [label="128B - free", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    root -> l1a; root -> l1b;
    l1b -> l2a; l1b -> l2b;
    l2b -> l3a; l2b -> l3b;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Only ever split in HALF. Freeing a block checks its 'buddy' (XOR\\lthe address with the block size) - if the buddy is ALSO free,\\lmerge them back into the parent size, and check ITS buddy too,\\lrecursively. Verified: alloc(100)+alloc(200)+alloc(50), then\\lfree all three, fully re-coalesces back into one 1024B block.\\lFast (O(log n) split/merge), some internal waste (100 rounds up\\lto 128 - up to ~50% worst case), no external fragmentation.\\l"];
    l3a -> note [style=invis];
    """)


if __name__ == "__main__":
    fit_algorithms()
    fragmentation_result()
    slab_allocation()
    buddy_allocation()
