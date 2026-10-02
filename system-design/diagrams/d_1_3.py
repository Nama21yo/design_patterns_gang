"""Diagrams for note 1.3 - Scalability, performance, latency vs throughput, maintainability, cost."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def latency_vs_throughput_highway():
    render("1-3-latency-vs-throughput", f"""
    rankdir=LR;
    car [label="ONE car's trip:\\l30 minutes door to door\\l= LATENCY", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    highway [label="The highway", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    cars [label="10,000 cars pass a\\lpoint per hour\\l= THROUGHPUT", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    car -> highway -> cars;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Adding more LANES raises throughput (more cars/hour) WITHOUT changing any\\lone car's travel time. The two numbers are independent - a system can have\\llow latency and low throughput (a sports car, empty road) or high latency\\land high throughput (a loaded cargo ship, but one leaves every hour).\\l"];
    cars -> note [style=invis];
    """)


def batching_tradeoff_verified():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8.5, 4))
    ax2 = ax.twinx()
    labels = ["no batching", "batch=10", "batch=100", "batch=1000"]
    latency = [5.10, 11.00, 25.00, 130.00]
    throughput = [196, 1667, 6667, 9524]
    x = range(len(labels))
    ax.bar([i - 0.2 for i in x], latency, width=0.35, color=RED, label="per-item latency (ms)")
    ax2.bar([i + 0.2 for i in x], throughput, width=0.35, color=TEAL, label="throughput (items/sec)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("per-item latency (ms)", color=RED)
    ax2.set_ylabel("throughput (items/sec)", color=TEAL)
    ax.set_title("Measured: bigger batches make EVERY item's latency worse,\nwhile throughput climbs up to 48.6x", loc="left", pad=10, fontsize=10.5)
    for s in ("top",):
        ax.spines[s].set_visible(False)
        ax2.spines[s].set_visible(False)
    return save_mpl(fig, "1-3-batching-tradeoff-verified")


def maintainability_cost():
    render("1-3-maintainability-cost", f"""
    rankdir=LR;

    subgraph cluster_maint {{
        label="Maintainability";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        m1 [label="can a NEW engineer\\lunderstand this system\\lwithout tribal knowledge?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        m2 [label="can a change be made\\lSAFELY (tests, clear\\lboundaries, no spooky\\laction at a distance)?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        m3 [label="can it be OPERATED day\\lto day (observability,\\lPart 6; clear runbooks)?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    }}

    subgraph cluster_cost {{
        label="Cost";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        c1 [label="infra spend per\\luser / per request", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        c2 [label="does the design fit a\\lSTATED budget, or is\\lit a blank check?", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        c3 [label="full cost modeling\\land trade-off analysis\\l- Part 8.3", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    }}
    """)


if __name__ == "__main__":
    latency_vs_throughput_highway()
    batching_tradeoff_verified()
    maintainability_cost()
