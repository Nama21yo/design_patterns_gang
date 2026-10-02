"""Diagrams for note 1.6 - ACID vs BASE."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def acid_vs_base_philosophy():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.axis("off")
    rows = [
        ("", "ACID", "BASE"),
        ("priority", "correctness, always", "availability, always"),
        ("under a partition (1.4)", "CP - refuse rather than risk wrong", "AP - serve, accept divergence"),
        ("consistency (1.5)", "strong - every read is current", "eventual - converges over time"),
        ("typical home", "relational DBs (3.2, deep dive there)", "Dynamo-style NoSQL (3.5's quorums)"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.01, y, row[0], fontsize=9.2, fontweight=weight, color=SLATE)
        ax.text(0.30, y, row[1], fontsize=8.8, fontweight=weight, color=BLUE)
        ax.text(0.65, y, row[2], fontsize=8.8, fontweight=weight, color=TEAL)
        ax.axhline(y - 0.45, xmin=0.01, xmax=0.99, color=(INK if i == 0 else GRAY), lw=(1.2 if i == 0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 0.9)
    ax.set_title("ACID and BASE are two different ANSWERS to 1.4's CAP trade-off,\nnot two unrelated acronyms", loc="left", pad=10, fontsize=10.5)
    return save_mpl(fig, "1-6-acid-vs-base-philosophy")


def base_three_words():
    render("1-6-base-three-words", f"""
    rankdir=LR;
    ba [label="BASICALLY AVAILABLE\\lthe system always responds -\\lthis IS 1.4's 'A' in AP", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    ss [label="SOFT STATE\\la replica's local view can\\lCHANGE on its own over time,\\leven with NO new writes -\\lpurely from background\\lconvergence (3.5's anti-entropy)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    ec [label="EVENTUALLY CONSISTENT\\lgiven no new writes, replicas\\lconverge - this IS 1.5's\\leventual consistency model", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    ba -> ss -> ec;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Two of BASE's three words are just renamed concepts already covered in\\lthis Part (1.4's Availability, 1.5's eventual consistency). SOFT STATE is\\lthe genuinely new idea: state that drifts toward convergence passively,\\lnot just 'eventually correct after a write' but ACTIVELY CHANGING without\\lone, purely as background replicas merge with each other.\\l"];
    ec -> note [style=invis];
    """)


def soft_state_verified():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    stages = ["before\nmerge", "after\nmerge", "after 2nd\nmerge"]
    replica_a = [3, 5, 5]
    replica_b = [2, 5, 5]
    x = range(len(stages))
    width = 0.35
    ax.bar([i - width/2 for i in x], replica_a, width, label="replica A's local total", color=BLUE)
    ax.bar([i + width/2 for i in x], replica_b, width, label="replica B's local total", color=TEAL)
    for i, (a, b) in enumerate(zip(replica_a, replica_b)):
        ax.text(i - width/2, a + 0.1, str(a), ha="center", fontsize=9)
        ax.text(i + width/2, b + 0.1, str(b), ha="center", fontsize=9)
    ax.set_xticks(list(x))
    ax.set_xticklabels(stages)
    ax.set_ylabel("counter total")
    ax.set_ylim(0, 6)
    ax.set_title("Verified (G-Counter CRDT): each replica's state changed with\nZERO new writes, purely from a background merge - then stayed stable",
                loc="left", pad=10, fontsize=10)
    ax.legend(frameon=False, fontsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "1-6-soft-state-verified")


if __name__ == "__main__":
    acid_vs_base_philosophy()
    base_three_words()
    soft_state_verified()
