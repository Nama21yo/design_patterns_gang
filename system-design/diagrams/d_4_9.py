"""Diagrams for note 4.9 - CPU caches: associativity and cache-friendly code."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def associativity_spectrum():
    plt = mpl()
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4))

    def draw_cache(ax, n_lines, n_sets, title):
        cell_w = 1.0
        for s in range(n_sets):
            ways = n_lines // n_sets
            for w in range(ways):
                x = s * (ways + 0.6) + w
                ax.add_patch(plt.Rectangle((x, 0), 0.9, 1, facecolor=LIGHTTEAL, edgecolor=TEAL))
            if n_sets > 1:
                ax.text(s * (ways + 0.6) + ways/2 - 0.3, -0.35, f"set {s}", fontsize=8, color=SLATE, ha="center")
        ax.set_xlim(-0.5, n_sets * ((n_lines // n_sets) + 0.6))
        ax.set_ylim(-0.7, 1.3)
        ax.axis("off")
        ax.set_title(title, fontsize=10.5)

    draw_cache(axes[0], 8, 8, "Direct-mapped\n(1 way/set - block -> exactly ONE line)")
    draw_cache(axes[1], 8, 2, "4-way set-associative\n(block -> one of 4 lines in ITS set)")
    draw_cache(axes[2], 8, 1, "Fully associative\n(block -> ANY of the 8 lines)")
    fig.suptitle("The associativity spectrum: how many lines a block is allowed to go in",
                 fontsize=11.5, y=1.04)
    return save_mpl(fig, "4-9-associativity-spectrum")


def associativity_results():
    plt = mpl()
    labels = ["direct-mapped\n(1-way)", "2-way", "4-way", "8-way", "fully\nassociative"]
    hits = [0, 0, 95, 95, 95]
    colors = [RED, RED, TEAL, TEAL, TEAL]
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.bar(labels, hits, color=colors, width=0.55)
    for i, v in enumerate(hits):
        ax.text(i, v + 2, f"{v}%", ha="center", fontsize=10)
    ax.set_ylim(0, 105)
    ax.set_ylabel("hit rate")
    ax.set_title("Measured: 3-block working set cycled through a same-aliased\n"
                 "line/set - associativity determines whether it even fits",
                 loc="left", pad=10, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "4-9-associativity-results")


def skewed_pseudo():
    render("4-9-skewed-pseudo-associative", f"""
    rankdir=LR;

    subgraph cluster_skew {{
        label="Two-way skewed associative";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        blk [label="block address", fillcolor="{GRAY}", color="{SLATE}"];
        h1 [label="hash fn 1 -> way 0\\l(DIFFERENT function\\lthan way 1's)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        h2 [label="hash fn 2 -> way 1", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        blk -> h1; blk -> h2;
        snote [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
              label="two blocks that collide in way 0 usually DON'T also\\lcollide in way 1 (different hash) - fewer pathological\\lcollision patterns than plain 2-way, near fully-\\lassociative hit rates, at 2-way hardware cost\\l"];
        h1 -> snote [style=invis];
    }}

    subgraph cluster_pseudo {{
        label="Pseudo-associative (column-associative)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        p1 [label="check the PRIMARY line\\l(direct-mapped speed)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        p2 [label="miss -> check ONE\\lalternate line before\\lgiving up", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        p1 -> p2 [label="  miss"];
        pnote [shape=note, fillcolor="{GRAY}", color="{SLATE}",
              label="fast path = direct-mapped latency; a second chance on\\lmiss recovers some of associativity's hit-rate benefit\\lwithout paying its cost on every single access\\l"];
        p2 -> pnote [style=invis];
    }}
    """)


def cache_friendly_timing():
    plt = mpl()
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.6))

    ax = axes[0]
    labels = ["row-major\n(contiguous)", "column-major\n(strided)"]
    vals = [0.0293, 0.0757]
    ax.bar(labels, vals, color=[TEAL, RED], width=0.5)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.002, f"{v*1000:.1f} ms", ha="center", fontsize=9)
    ax.set_ylabel("seconds (summing a 4000x4000 array)")
    ax.set_title("2.6x - same data, same operation,\ndifferent memory access pattern", fontsize=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    ax = axes[1]
    labels2 = ["naive\n(list-of-lists)", "blocked\n(list-of-lists)"]
    vals2 = [0.009, 0.010]
    ax.bar(labels2, vals2, color=[SLATE, SLATE], width=0.5)
    for i, v in enumerate(vals2):
        ax.text(i, v + 0.0003, f"{v*1000:.0f} ms", ha="center", fontsize=9)
    ax.set_title("Blocked transpose: NO reliable gain on\nPython lists (not contiguous memory)", fontsize=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    fig.suptitle("Cache-friendly code, measured", fontsize=12, y=1.04)
    return save_mpl(fig, "4-9-cache-friendly-timing")


if __name__ == "__main__":
    associativity_spectrum()
    associativity_results()
    skewed_pseudo()
    cache_friendly_timing()
