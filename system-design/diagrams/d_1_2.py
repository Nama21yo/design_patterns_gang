"""Diagrams for note 1.2 - Availability, reliability, fault tolerance, resilience, durability."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def availability_vs_reliability():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis("off")
    rows = [
        ("", "availability", "reliability", "user's actual experience"),
        ("Service A\n(always up, 15% silently wrong)", "100.0%", "84.9%", "84.9% correct answers"),
        ("Service B\n(down 10%, always correct when up)", "90.0%", "100.0%", "90.0% correct answers"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.01, y, row[0], fontsize=9, fontweight=weight, color=BLUE)
        ax.text(0.42, y, row[1], fontsize=9.3, fontweight=weight, color=TEAL)
        ax.text(0.58, y, row[2], fontsize=9.3, fontweight=weight, color=AMBER)
        ax.text(0.76, y, row[3], fontsize=8.8, fontweight=weight, color=SLATE)
        ax.axhline(y - 0.45, xmin=0.01, xmax=0.99, color=(INK if i == 0 else GRAY), lw=(1.2 if i == 0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 1)
    ax.set_title("Measured: availability and reliability are ORTHOGONAL -\nneither one implies the other", loc="left", pad=10, fontsize=11)
    return save_mpl(fig, "1-2-availability-vs-reliability")


def nines_table():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    labels = ["99%", "99.9%", "99.95%", "99.99%", "99.999%"]
    downtime_minutes = [5256, 525.6, 262.8, 52.56, 5.26]
    ax.bar(labels, downtime_minutes, color=TEAL)
    ax.set_yscale("log")
    for i, v in enumerate(downtime_minutes):
        ax.text(i, v * 1.3, f"{v:,.1f} min", ha="center", fontsize=8.5)
    ax.set_ylabel("allowed downtime per year (minutes, log scale)")
    ax.set_title("Computed: each additional 9 cuts allowed downtime\nby roughly 10x", loc="left", pad=10, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "1-2-nines-table")


def series_vs_parallel():
    render("1-2-series-vs-parallel", f"""
    rankdir=LR;

    subgraph cluster_series {{
        label="SERIES (a dependency chain) - ALL must be up";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        s1 [label="LB\\l99.9%", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        s2 [label="DB\\l99.9%", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        s1 -> s2;
        sn [shape=note, fillcolor="{RED}", fontcolor=white, color="{RED}", label="combined: 99.8001%\\lWORSE than either alone -\\lmultiply the probabilities"];
        s2 -> sn [style=invis];
    }}

    subgraph cluster_parallel {{
        label="PARALLEL (redundancy) - only needs ONE up";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        p1 [label="Replica 1\\l99.9%", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        p2 [label="Replica 2\\l99.9%", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        pn [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}", label="combined: 99.9999%\\lBETTER than either alone -\\l1 minus (both down at once)"];
        p1 -> pn [style=invis]; p2 -> pn [style=invis];
    }}
    """)


def resilience_spectrum():
    render("1-2-resilience-spectrum", f"""
    rankdir=LR;
    fault [label="FAULT TOLERANCE\\la SPECIFIC mechanism:\\lredundancy lets the system\\lkeep working despite ONE\\lcomponent failing", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    resilience [label="RESILIENCE\\lthe BROADER property: detect,\\lcontain, and RECOVER from\\lfailure - fault tolerance is\\lONE tool resilience uses,\\lalong with 2.6's patterns,\\lgraceful degradation, retries", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    durability [label="DURABILITY\\la DIFFERENT axis entirely:\\lonce a write is acknowledged,\\lcan it ever be LOST? (not\\labout staying UP - about never\\lLOSING committed data)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    fault -> resilience [style=dashed, color="{SLATE}", label="  is ONE part of"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Durability is orthogonal to the other two - a system can be perfectly\\ldurable (3.1's WAL, 2.7's backups) while being down right now, and can\\lbe highly available while being completely non-durable (an in-memory\\lcache that loses everything on restart, by design - 4.1-4.3).\\l"];
    durability -> note [style=invis];
    """)


if __name__ == "__main__":
    availability_vs_reliability()
    nines_table()
    series_vs_parallel()
    resilience_spectrum()
