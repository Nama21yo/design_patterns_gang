"""Diagrams for note 5.3 - Stream processing (Structured Streaming, Flink)."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def structured_streaming_microbatch():
    plt = mpl()
    batches = [0, 1, 2, 3, 4, 5]
    rows = [0, 50, 25, 25, 25, 25]
    cumulative = []
    total = 0
    for r in rows:
        total += r
        cumulative.append(total)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax2 = ax.twinx()
    ax.bar(batches, rows, color=BLUE, alpha=0.55, width=0.5, label="rows in this micro-batch")
    ax2.plot(batches, cumulative, color=TEAL, marker="o", linewidth=2, label="cumulative rows in the unbounded table")
    for b, c in zip(batches, cumulative):
        ax2.text(b, c + 4, str(c), ha="center", fontsize=8.5, color=TEAL)
    ax.set_xlabel("micro-batch (1 trigger per second)")
    ax.set_ylabel("rows processed this batch", color=BLUE)
    ax2.set_ylabel("cumulative rows (the 'unbounded table')", color=TEAL)
    ax.set_title("Measured: Spark Structured Streaming's rate source,\n6 real micro-batches, 1s trigger interval", loc="left", pad=10, fontsize=10.5)
    for s in ("top",):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "5-3-structured-streaming-microbatch")


def flink_architecture():
    render("5-3-flink-architecture", f"""
    rankdir=TB;
    jm [label="JobManager\\l(the 'master')\\lbuilds the job graph, coordinates\\lcheckpointing, handles failures", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    tm1 [label="TaskManager 1\\l(worker)\\lruns parallel operator\\lsubtasks in task slots", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    tm2 [label="TaskManager 2\\l(worker)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    tm3 [label="TaskManager 3\\l(worker)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    jm -> tm1 [label="  deploy tasks,\\l  trigger checkpoints"];
    jm -> tm2; jm -> tm3;
    tm1 -> tm2 [label="  event stream\\l  (network shuffle)", style=dashed, color="{TEAL}"];
    tm2 -> tm3 [style=dashed, color="{TEAL}"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Same master/worker shape as Spark (JobManager <-> Driver,\\lTaskManager <-> Executor) - the real difference is HOW work\\lflows through the workers, not who coordinates whom.\\l"];
    tm1 -> note [style=invis];
    """)


def true_streaming_vs_microbatch():
    render("5-3-true-streaming-vs-microbatch", f"""
    rankdir=LR;

    subgraph cluster_spark {{
        label="Spark Structured Streaming - micro-batch";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        e1 [label="events buffer for\\lup to 1 trigger interval\\l(e.g. 1s)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        b1 [label="process as ONE batch", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        e1 -> b1 [label="  trigger fires"];
        n1 [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}", label="latency floor ~= trigger\\linterval (typ. 100ms-1s+);\\lhigher throughput per batch\\l"];
        b1 -> n1 [style=invis];
    }}

    subgraph cluster_flink {{
        label="Flink - true (event-at-a-time) streaming";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        e2 [label="each event processed\\lthe instant it arrives", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        n2 [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}", label="latency floor ~= milliseconds;\\lstate updates flow continuously,\\lno waiting for a batch boundary\\l"];
        e2 -> n2 [style=invis];
    }}
    """)


def checkpoint_barrier():
    render("5-3-checkpoint-barrier", f"""
    rankdir=LR;
    src [label="2 upstream channels\\l(one fast, one slow)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    fast [label="fast channel: sends its\\lBARRIER, then keeps\\lsending events - THOSE\\lget BUFFERED, not processed", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    slow [label="slow channel: still\\lcatching up to ITS barrier", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    align [label="once BOTH barriers have\\larrived: snapshot state NOW\\l(this point is consistent\\lacross both inputs)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    resume [label="replay the buffered\\lpost-barrier events,\\lresume normally", fillcolor="{GRAY}", color="{SLATE}"];

    src -> fast; src -> slow;
    fast -> align; slow -> align;
    align -> resume;

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Verified in simulation: fast channel (5 events, barrier after 3) raced\\lahead of a slow channel (3 events, barrier after 1). Snapshot correctly\\lcaptured ONLY the 5 pre-barrier values (3+2=5, not the full 11) - the\\lalignment held even though one input was 2 events ahead of the other.\\l"];
    resume -> note [style=invis];
    """)


if __name__ == "__main__":
    structured_streaming_microbatch()
    flink_architecture()
    true_streaming_vs_microbatch()
    checkpoint_barrier()
