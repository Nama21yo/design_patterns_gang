"""Diagrams for note 5.5 - Pub/Sub and fan-out patterns."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def fanout_write_vs_read():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8, 4))
    labels = ["normal user\n(200 followers)\nwrite", "celebrity\n(2,000,000 followers)\nwrite"]
    times = [0.10, 2910.55]
    colors = [TEAL, RED]
    ax.bar(labels, times, color=colors, width=0.5)
    ax.set_yscale("log")
    ax.set_ylabel("write latency (ms, log scale)")
    for i, v in enumerate(times):
        ax.text(i, v * 1.3, f"{v:,.2f}ms", ha="center", fontsize=9.5)
    ax.set_title("Measured: fan-out-on-write's cost is proportional to follower\ncount - a celebrity's single post did 2M synchronous feed writes",
                loc="left", pad=10, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "5-5-fanout-write-vs-read")


def fanout_pattern_diagram():
    render("5-5-fanout-patterns", f"""
    rankdir=TB;

    subgraph cluster_write {{
        label="Fan-out on WRITE (push)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        p1 [label="user posts", fillcolor="{INK}", fontcolor=white, color="{INK}"];
        f1 [label="push into EVERY\\lfollower's feed cache\\lNOW", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        r1 [label="read: O(1),\\lalready precomputed", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        p1 -> f1 -> r1;
        n1 [shape=note, fillcolor="{RED}", fontcolor=white, color="{RED}", label="breaks for celebrities:\\lmillions of writes per post"];
        f1 -> n1 [style=invis];
    }}

    subgraph cluster_read {{
        label="Fan-out on READ (pull)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        p2 [label="user posts", fillcolor="{INK}", fontcolor=white, color="{INK}"];
        f2 [label="just append to the\\lauthor's own post list\\l- O(1), always", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        r2 [label="read: MERGE every\\lfollowed author's posts\\lat request time", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        p2 -> f2 -> r2;
        n2 [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}", label="every read does real work,\\leven for inactive users"];
        r2 -> n2 [style=invis];
    }}

    hybrid [label="Production answer: HYBRID - fan-out-on-write for normal users,\\lfan-out-on-read for celebrities specifically", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    r1 -> hybrid [style=invis]; n2 -> hybrid [style=invis];
    """)


def multi_consumer_group_fanout():
    render("5-5-multi-consumer-group", f"""
    rankdir=LR;
    topic [label="ONE topic:\\lblog_1 published\\lblog_2 published\\lblog_3 published", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    g1 [label="search-index-group\\l(own offset, own retries)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    g2 [label="counter-group\\l(own offset, own retries,\\lcan join LATE and still\\lreplay from the start)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    topic -> g1; topic -> g2;

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Verified: a group that joined AFTER 2 of 3 events still received ALL 3 from\\lthe start of the log. This is what actually fixes 5.2's dual-write problem -\\leach consumer group commits its own work independently, not two side-\\leffecting calls made inline in one request.\\l"];
    g2 -> note [style=invis];
    """)


def kafka_vs_redis_pubsub():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(9.5, 3.4))
    ax.axis("off")
    rows = [
        ("", "Kafka (a log)", "Redis Pub/Sub (real-time pub/sub)"),
        ("durability", "retained for a retention period", "NONE - published while nobody is\nsubscribed = message is just gone"),
        ("late subscriber", "replays from any offset", "gets nothing before it subscribed"),
        ("latency", "low, but not the floor", "lowest possible - no log/disk at all"),
        ("typical use", "durable event pipelines,\nfan-out, audit trail", "config push, live cursors,\nchat presence, ephemeral broadcast"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.02, y, row[0], fontsize=9.3, fontweight=weight, color=SLATE)
        ax.text(0.20, y, row[1], fontsize=9.0, fontweight=weight, color=BLUE)
        ax.text(0.58, y, row[2], fontsize=9.0, fontweight=weight, color=TEAL)
        ax.axhline(y - 0.4, xmin=0.02, xmax=0.98, color=(INK if i == 0 else GRAY), lw=(1.2 if i == 0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 0.8)
    ax.set_title("Kafka vs. Redis Pub/Sub - verified: publish() with no subscriber\nreturned 0 receivers on Redis; Kafka's late group still got everything",
                loc="left", pad=10, fontsize=10)
    return save_mpl(fig, "5-5-kafka-vs-redis-pubsub")


if __name__ == "__main__":
    fanout_write_vs_read()
    fanout_pattern_diagram()
    multi_consumer_group_fanout()
    kafka_vs_redis_pubsub()
