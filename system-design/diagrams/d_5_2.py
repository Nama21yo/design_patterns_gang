"""Diagrams for note 5.2 - Delivery semantics."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def dual_write_problem():
    render("5-2-dual-write-problem", f"""
    rankdir=LR;
    publish [label="publish(blog_2)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    write1 [label="write 1: index in\\lsearch service - SUCCEEDS", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    write2 [label="write 2: increment\\lblog counter - FAILS", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    result [label="blog_2 is now searchable\\lbut PERMANENTLY missing\\lfrom the count - no record\\lthat this even happened", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    publish -> write1 -> write2 -> result;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Verified: 3 blogs published, one counter write failed mid-sequence ->\\l3 indexed but counter only shows 2, with no signal the mismatch occurred.\\l"];
    result -> note [style=invis];
    """)


def delivery_semantics_taxonomy():
    render("5-2-delivery-semantics", f"""
    rankdir=TB;
    q [label="How does the system handle a failure\\lduring delivery or processing?", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    amo [label="AT-MOST-ONCE\\lsend and forget - a failure\\lmeans the message is just LOST", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    alo [label="AT-LEAST-ONCE\\lretry until ACKed - a failure\\lmeans the message may be\\lDELIVERED TWICE", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    eo [label="'EXACTLY-ONCE'\\lat-least-once delivery +\\lan idempotency/dedup key\\l= EFFECTIVELY-once processing", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    q -> amo; q -> alo; alo -> eo [label="  + dedup (3.7)"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="True exactly-once DELIVERY isn't achievable over an unreliable network\\l(you can't tell 'the ack was lost' from 'the message was lost' - FLP's\\lpractical shadow, 3.6). What real systems build instead: at-least-once\\ldelivery + idempotent processing = the OUTCOME of exactly-once, without\\lthe network guarantee. See 3.7's outbox + idempotent-consumer pattern.\\l"];
    eo -> note [style=invis];
    """)


def dlq_flow():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.axis("off")
    rounds = ["round 1", "round 2", "round 3"]
    main_q = [1, 1, 0]
    dlq = [0, 0, 1]
    x = range(len(rounds))
    ax.bar(x, main_q, color=BLUE, width=0.4, label="poison message still in main queue")
    ax.bar([i + 0.42 for i in x], dlq, color=RED, width=0.4, label="poison message in DLQ")
    ax.set_xticks([i + 0.21 for i in x])
    ax.set_xticklabels(rounds)
    ax.set_ylim(0, 1.4)
    ax.set_yticks([0, 1])
    ax.axis("on")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("Verified: a malformed message retried 3x, then routed to the\nDLQ instead of looping forever (the good message processed on round 1)",
                loc="left", pad=10, fontsize=10)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    return save_mpl(fig, "5-2-dlq-flow")


if __name__ == "__main__":
    dual_write_problem()
    delivery_semantics_taxonomy()
    dlq_flow()
