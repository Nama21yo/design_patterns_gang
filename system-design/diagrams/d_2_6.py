"""Diagrams for note 2.6 - Fault tolerance patterns."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def cascading_failure_motivation():
    render("2-6-cascading-failure", f"""
    rankdir=LR;
    profile [label="Profile service\\loverwhelmed, every call\\lslow or times out", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    feed [label="Feed service\\lkeeps calling it anyway,\\lthreads pile up waiting", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    gateway [label="API gateway\\lfeed service now slow too\\l-> gateway threads pile up", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    everything [label="the ENTIRE product\\lis now slow, because of\\lONE overwhelmed dependency", fillcolor="{RED}", fontcolor=white, color="{RED}"];

    profile -> feed -> gateway -> everything [color="{RED}", penwidth=2];

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="This is CASCADING FAILURE - one slow dependency propagates its slowness\\lupstream through every caller, because nothing stops the calls from being\\lmade. A circuit breaker exists specifically to cut this chain.\\l"];
    everything -> note [style=invis];
    """)


def circuit_breaker_states():
    render("2-6-circuit-breaker-states", f"""
    rankdir=LR;
    closed [label="CLOSED\\lcalls pass through normally,\\lfailures are counted", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    open [label="OPEN\\lcalls fail FAST, downstream\\lis never even contacted", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    half [label="HALF-OPEN\\lafter a recovery timeout,\\lallow ONE trial request", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    closed -> open [label="  failure count\\l  >= threshold"];
    open -> half [label="  recovery\\l  timeout elapses"];
    half -> closed [label="  trial succeeds"];
    half -> open [label="  trial fails"];

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Verified: 3 real timeouts opened the breaker; the next 3 requests failed\\lfast with ZERO calls reaching the already-overwhelmed service; after the\\lrecovery timeout and the service recovering, a half-open trial succeeded\\land the breaker closed again automatically.\\l"];
    closed -> note [style=invis];
    """)


def reliability_patterns_grid():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.axis("off")
    rows = [
        ("pattern", "what it does", "protects against"),
        ("Circuit breaker", "stop calling a failing dependency, fail fast", "cascading failure (verified above)"),
        ("Bulkhead", "separate resource pools (threads/connections)\nper dependency, like a ship's watertight compartments", "one slow dependency starving\nresources that OTHER calls need"),
        ("Backpressure", "a producer signals 'slow down' when a\nconsumer can't keep up, instead of silently queuing forever", "unbounded memory growth,\nlatency spiraling under overload"),
        ("Load shedding", "deliberately REJECT some requests when\noverloaded, to keep serving the rest well", "an overloaded system serving\nEVERYONE badly instead of most well"),
        ("Hedged requests", "send a duplicate request to a 2nd replica if\nthe 1st hasn't answered within a latency budget", "one slow REPLICA (not a full outage)\ndragging down your p99 latency"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.01, y, row[0], fontsize=9.3, fontweight=weight, color=BLUE)
        ax.text(0.20, y, row[1], fontsize=8.6, fontweight=weight, color=INK)
        ax.text(0.62, y, row[2], fontsize=8.4, fontweight=weight, color=SLATE)
        ax.axhline(y - 0.42, xmin=0.01, xmax=0.99, color=(INK if i == 0 else GRAY), lw=(1.2 if i == 0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 0.8)
    ax.set_title("Fault tolerance patterns at a glance", loc="left", pad=10)
    return save_mpl(fig, "2-6-reliability-patterns-grid")


if __name__ == "__main__":
    cascading_failure_motivation()
    circuit_breaker_states()
    reliability_patterns_grid()
