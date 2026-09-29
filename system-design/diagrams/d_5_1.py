"""Diagrams for note 5.1 - Message queues and brokers."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def async_decoupling_motivation():
    render("5-1-async-decoupling", f"""
    rankdir=LR;
    upload [label="User uploads a video", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    sync [label="Synchronous: API request\\lblocks until 480p+720p+1080p\\ltranscoding all finish", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    queue [label="Broker (buffer):\\lenqueue 3 transcode jobs,\\lrespond to the user NOW", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    workers [label="Pool of transcode workers\\lpull jobs whenever THEY\\lhave capacity", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    upload -> sync [style=dashed, color="{RED}", label="  times out / ties up\\l  a request thread for minutes"];
    upload -> queue -> workers;

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="The broker is the buffer: it decouples 'a job exists' from 'a worker is\\lfree right now' - producer and consumer rates no longer have to match.\\l"];
    workers -> note [style=invis];
    """)


def broker_requeue_mechanics():
    render("5-1-broker-requeue", f"""
    rankdir=LR;
    producer [label="Producer", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    q [label="Queue\\l(message stays until ACKed)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    worker [label="Worker receives it\\l(now INVISIBLE to others\\lfor the visibility timeout)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    crash [label="Worker crashes before\\lACKing (e.g. never finishes\\lgenerating subtitles)", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    requeue [label="Visibility timeout expires\\l-> message becomes visible\\lagain, another worker gets it", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    producer -> q -> worker;
    worker -> crash [style=dashed, color="{RED}"];
    crash -> requeue;
    requeue -> q [style=dashed, color="{SLATE}", label="  redelivered"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Verified with real moto-mocked SQS calls: a crashed worker's message was\\lhidden immediately, then automatically became visible again once its\\lvisibility timeout expired, and was picked up by the next receive_message().\\l"];
    requeue -> note [style=invis];
    """)


def kafka_topic_partitions():
    render("5-1-kafka-topic-partitions", f"""
    rankdir=LR;
    producer [label="Producer\\l(writes with a KEY, e.g. blog_id)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    hash [label="partition = hash(key) % N", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    p0 [label="partition 0", fillcolor="{GRAY}", color="{SLATE}"];
    p1 [label="partition 1\\l[blog_101: created]\\l[blog_101: published]\\l[blog_101: edited]", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    p2 [label="partition 2", fillcolor="{GRAY}", color="{SLATE}"];
    p3 [label="partition 3", fillcolor="{GRAY}", color="{SLATE}"];

    producer -> hash;
    hash -> p0; hash -> p1; hash -> p2; hash -> p3;

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Verified: every 'blog_101' event landed on the SAME partition, every time -\\lsame key always hashes to the same partition, so per-key order is preserved\\lwithin a partition. There is NO ordering guarantee ACROSS partitions.\\l"];
    p1 -> note [style=invis];
    """)


def consumer_partition_limit():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    groups = ["2 consumers\n(4 partitions)", "4 consumers\n(4 partitions)", "6 consumers\n(4 partitions)"]
    active = [2, 4, 4]
    idle = [0, 0, 2]
    x = range(len(groups))
    ax.bar(x, active, color=TEAL, label="consumers WITH a partition")
    ax.bar(x, idle, bottom=active, color=RED, label="consumers IDLE (no partition)")
    for i, (a, d) in enumerate(zip(active, idle)):
        if d:
            ax.text(i, a + d + 0.15, f"{d} idle", ha="center", fontsize=9, color=RED)
    ax.set_ylabel("consumers")
    ax.set_ylim(0, 7)
    ax.set_title("Measured: a consumer group can never usefully exceed\nits topic's partition count", loc="left", pad=10, fontsize=10.5)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "5-1-consumer-partition-limit")


def queue_vs_log():
    render("5-1-queue-vs-log", f"""
    rankdir=LR;

    subgraph cluster_queue {{
        label="Message queue (RabbitMQ, SQS)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        q1 [label="message consumed\\l+ ACKed -> GONE\\lfrom the queue", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        qnote [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}", label="a late-joining consumer\\lgets NOTHING that already\\lwas consumed and acked"];
        q1 -> qnote [style=invis];
    }}

    subgraph cluster_log {{
        label="Message log (Kafka)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        l1 [label="message stays in the log\\l(retention period), each\\lconsumer GROUP tracks its\\lOWN offset", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        lnote [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}", label="a late-joining consumer\\lGROUP can replay the\\lentire retained log"];
        l1 -> lnote [style=invis];
    }}
    """)


if __name__ == "__main__":
    async_decoupling_motivation()
    broker_requeue_mechanics()
    kafka_topic_partitions()
    consumer_partition_limit()
    queue_vs_log()
