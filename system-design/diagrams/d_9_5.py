"""Diagrams for note 9.5 - Top-K / Trending (Heavy Hitters)."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def naive_scaleout():
    render("9-5-naive-scaleout", f"""
    rankdir=LR;
    clients [label="Clients\\l(view / play / search events)", fillcolor="{GRAY}", color="{SLATE}"];
    lb      [label="Load balancer\\l(routes randomly / round-robin)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    p1 [label="Processor host 1\\lhashmap of counts it has seen", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    p2 [label="Processor host 2\\lhashmap of counts it has seen", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    p3 [label="Processor host 3\\lhashmap of counts it has seen", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    storage [label="Storage host\\l(accumulates everything)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    clients -> lb;
    lb -> p1; lb -> p2; lb -> p3;
    p1 -> storage; p2 -> storage; p3 -> storage;

    {{ rank=same; p1; p2; p3 }}
    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
          label="Problem: the SAME item's events land on different hosts\\l(routing ignores the key), so no single host's hashmap\\lholds the true count for anything. Every host's map also\\lgrows without bound as the key space grows - memory pressure\\lon both the processors and the storage host.\\l"];
    p2 -> note [style=invis];
    """)


def partitioned_scaleout():
    render("9-5-partitioned-scaleout", f"""
    rankdir=LR;
    clients [label="Clients", fillcolor="{GRAY}", color="{SLATE}"];
    part [label="Data partitioner\\lroute by hash(item_id)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    p1 [label="Processor 1\\lowns shard 1's keys\\llocal top-k heap", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    p2 [label="Processor 2\\lowns shard 2's keys\\llocal top-k heap", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    p3 [label="Processor 3\\lowns shard 3's keys\\llocal top-k heap", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    merge [label="Merger\\lk-way merge of the 3\\lsorted local top-k lists", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    storage [label="Storage host\\l(global top-k)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    clients -> part;
    part -> p1; part -> p2; part -> p3;
    p1 -> merge; p2 -> merge; p3 -> merge;
    merge -> storage;
    {{ rank=same; p1; p2; p3 }}

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
          label="Key correctness fact: partitioning by key means one item's\\lcount lives ENTIRELY inside one shard. So if an item is not\\lin its own shard's local top-k, at least k other items in\\lTHAT SAME shard already outscore it - it cannot be in the\\lglobal top-k either. Merging the local top-k lists is exact,\\lnot approximate.\\l"];
    p2 -> note [style=invis];
    """)


def window_counterexample():
    plt = mpl()
    lines = [
        ("Why per-minute top-3 lists don't merge into an hourly top-3", "title"),
        ("", ""),
        ("Setup: 60 one-minute windows. Item Z scores 5 every single minute", ""),
        ("(steady, total 5x60=300) but 5 noisier items always score 6-9 that", ""),
        ("minute - so Z is never in ANY minute's published top-3.", ""),
        ("", ""),
        ("(A) EXACT hourly top-3, computed from the raw per-minute counts:", "h"),
        ("      d: 457     a: 451     e: 448      ...      Z: 300 (true, but hidden)", ""),
        ("", ""),
        ("(B) top-3 from MERGING the 60 stored per-minute top-3 lists:", "h"),
        ("      a: 363     b: 306     d: 292", ""),
        ("", ""),
        ("(A) and (B) don't even agree on WHICH items are top-3 - because every", ""),
        ("minute an item drops out of that minute's top-3, its count for that", ""),
        ("minute is thrown away forever. Z's true total (300) never appears", ""),
        ("anywhere in the stored data at all.", ""),
        ("", ""),
        ("Conclusion: top-k does not compose. You cannot roll a longer window", "h"),
        ("up from shorter windows' top-k lists - only from the raw counts", "h"),
        ("(or a sketch built over the raw counts) for that whole window.", "h"),
    ]
    fig, ax = plt.subplots(figsize=(10.5, 6.6))
    ax.axis("off")
    y = len(lines)
    for i, (txt, kind) in enumerate(lines):
        yy = y - i
        if kind == "title":
            ax.text(0.02, yy, txt, fontsize=12.5, fontweight="bold", color=INK)
        elif kind == "h":
            ax.text(0.02, yy, txt, fontsize=9.8, fontweight="bold", color=BLUE)
        else:
            ax.text(0.02, yy, txt, fontsize=9.5, family="DejaVu Sans Mono", color=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, y + 1)
    fig.patch.set_edgecolor(GRAY)
    fig.patch.set_linewidth(2)
    return save_mpl(fig, "9-5-window-counterexample")


def hot_partition():
    plt = mpl()
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.2))
    balanced = [12, 11, 13, 12, 11, 12]
    skewed = [9, 8, 62, 7, 8, 6]
    labels = [f"shard {i}" for i in range(1, 7)]
    for ax, data, title in [(axes[0], balanced, "Balanced (typical day)"),
                            (axes[1], skewed, "Hot partition\n(one item goes viral)")]:
        colors = [RED if v == max(data) and title.startswith("Hot") else BLUE for v in data]
        ax.bar(labels, data, color=colors)
        ax.set_title(title, fontsize=10)
        ax.set_ylim(0, 70)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(axis="x", labelrotation=30, labelsize=8)
        ax.set_ylabel("% of traffic", fontsize=9)
    fig.suptitle("Hot partitions: one shard can take a hugely disproportionate share",
                 fontsize=11, x=0.02, ha="left")
    return save_mpl(fig, "9-5-hot-partition")


def cms_grid():
    plt = mpl()
    d, w = 4, 14
    fig, ax = plt.subplots(figsize=(11, 4.6))
    hits = [3, 9, 1, 11]  # column each row's hash picks for the queried item
    values = {
        (0, 3): 41, (1, 9): 27, (2, 1): 63, (3, 11): 27,
    }
    for r in range(d):
        for c in range(w):
            is_hit = (c == hits[r])
            val = values.get((r, c))
            face = LIGHTAMBER if is_hit else "white"
            edge = AMBER if is_hit else GRAY
            ax.add_patch(plt.Rectangle((c, d - r - 1), 1, 1, facecolor=face,
                                       edgecolor=edge, linewidth=1.6 if is_hit else 0.8))
            if val is not None:
                ax.text(c + 0.5, d - r - 0.5, str(val), ha="center", va="center",
                        fontsize=10, fontweight="bold" if is_hit else "normal",
                        color=INK)
        ax.text(-0.4, d - r - 0.5, f"h{r+1}", ha="right", va="center", fontsize=10,
                color=SLATE, fontweight="bold")
        ax.annotate("", xy=(hits[r] + 0.5, d - r), xytext=(-2.6, d - r - 0.5 + 0.0),
                    annotation_clip=False)
    ax.text(-2.7, d + 0.55, 'add("NEWS_42")\nquery("NEWS_42")', fontsize=10, color=INK,
            fontweight="bold", ha="left", va="center")
    for r in range(d):
        ax.annotate("", xy=(hits[r], d - r - 0.5), xytext=(-1.4, d + 0.2 - r*0 - (0.0)),
                    arrowprops=dict(arrowstyle="-", color=SLATE, lw=0.9,
                                    connectionstyle=f"arc3,rad={0.08*(r-1.5)}"))
    ax.set_xlim(-3.2, w + 0.5)
    ax.set_ylim(-0.5, d + 1.3)
    ax.axis("off")
    ax.set_title("Count-Min Sketch: d=4 hash functions (rows) x w=14 counters (width)",
                 loc="left", pad=4, fontsize=11)
    ax.text(0, -0.35,
           "add: +1 to the hashed cell in every row.   "
           "query: return the MIN of the 4 highlighted cells = min(41, 27, 63, 27) = 27.",
           fontsize=9.3, color=SLATE)
    ax.text(0, -0.85,
           "Collisions only ever ADD extra weight into a cell from other items, never remove it "
           "- so every cell is an overestimate, and the min across independent rows is the "
           "tightest overestimate available.",
           fontsize=9, color=SLATE, style="italic")
    return save_mpl(fig, "9-5-cms-grid")


def mapreduce_flow():
    render("9-5-mapreduce-flow", f"""
    rankdir=LR;
    node [shape=box];

    s1 [label="Split 1\\lAABAC", fillcolor="{GRAY}", color="{SLATE}"];
    s2 [label="Split 2\\lBCCDA", fillcolor="{GRAY}", color="{SLATE}"];
    s3 [label="Split 3\\lAABBCE", fillcolor="{GRAY}", color="{SLATE}"];

    m1 [label="map()\\lemit (item,1) per event", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    m2 [label="map()\\lemit (item,1) per event", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    m3 [label="map()\\lemit (item,1) per event", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    shuffle [label="shuffle + sort\\lgroup all emissions by key\\l(the framework does this)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    r1 [label="reduce('A', [1,1,1,1,1,1])\\l-> (A, 6)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    r2 [label="reduce('B', [1,1,1,1])\\l-> (B, 4)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    r3 [label="reduce('C', [1,1,1,1])\\l-> (C, 4)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    r4 [label="reduce('D',..) reduce('E',..)\\l-> (D,1) (E,1)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    out [label="Output: exact counts\\lA:6 B:4 C:4 D:1 E:1", fillcolor="{INK}", fontcolor="white", color="{INK}"];

    s1 -> m1; s2 -> m2; s3 -> m3;
    m1 -> shuffle; m2 -> shuffle; m3 -> shuffle;
    shuffle -> r1; shuffle -> r2; shuffle -> r3; shuffle -> r4;
    r1 -> out; r2 -> out; r3 -> out; r4 -> out;

    {{ rank=same; s1; s2; s3 }}
    {{ rank=same; m1; m2; m3 }}
    {{ rank=same; r1; r2; r3; r4 }}
    """)


def lambda_architecture():
    render("9-5-lambda-architecture", f"""
    rankdir=LR;
    ranksep=0.7;

    client [label="Terminal / app client\\l(view, play, search events)", fillcolor="{GRAY}", color="{SLATE}"];
    gw [label="API gateway\\lauth, TLS, rate limit\\l+ batches & flushes\\lclient events", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    kafka [label="Kafka\\lpartitioned, replicated\\ltopic of raw events", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    subgraph cluster_fast {{
        label="speed layer (seconds)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        fastproc [label="Fast processor\\lCount-Min Sketch + heap\\lper time window", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    }}

    subgraph cluster_slow {{
        label="batch layer (minutes / hours)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        partitioner [label="Data partitioner\\l(+ replication)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        partproc [label="Partition processor\\llocal pre-aggregation\\l(shrinks the data)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        dfs [label="Distributed file system\\lHDFS / S3", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        mr1 [label="MapReduce job 1\\lFrequency Count", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        mr2 [label="MapReduce job 2\\lTop-K", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        partitioner -> partproc -> dfs -> mr1 -> mr2;
    }}

    storage [label="Storage service\\l(serving layer)\\lserves fast result,\\lswaps in exact result\\lwhen the batch job lands", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    query [label="Client query\\ntopK(k, start, end)", fillcolor="{GRAY}", color="{SLATE}"];

    client -> gw -> kafka;
    kafka -> fastproc -> storage;
    kafka -> partitioner;
    mr2 -> storage;
    storage -> query [dir=both];
    """)


def rate_funnel():
    plt = mpl()
    stages = [
        ("API gateway\n(raw client events)", 1_000_000),
        ("Kafka\n(partitioned raw events)", 1_000_000),
        ("Partition processor\n(local pre-aggregation)", 20_000),
        ("MapReduce reduce output\n(per-item counts)", 500),
        ("Storage service\n(final top-k list)", 10),
    ]
    labels = [s[0] for s in stages]
    vals = [s[1] for s in stages]
    fig, ax = plt.subplots(figsize=(10.5, 3.6))
    colors = [BLUE, BLUE, AMBER, TEAL, INK]
    bars = ax.bar(range(len(vals)), vals, color=colors, width=0.55)
    ax.set_yscale("log")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=8.6)
    for i, v in enumerate(vals):
        ax.text(i, v * 1.3, f"~{v:,}/s" if v >= 100 else f"~{v}\nrows", ha="center",
                fontsize=8.5, color=INK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_ylabel("records / sec  (log scale)")
    ax.set_title("Record rate shrinks by ~5 orders of magnitude down the pipeline",
                 loc="left", pad=12)
    return save_mpl(fig, "9-5-rate-funnel")


def tumbling_vs_sliding():
    plt = mpl()
    fig, axes = plt.subplots(2, 1, figsize=(10.5, 3.6), sharex=True)

    ax = axes[0]
    for i in range(4):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=LIGHTBLUE, edgecolor=BLUE))
        ax.text(i + 0.5, 0.5, f"hour {i}", ha="center", va="center", fontsize=9)
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.3, 1.6)
    ax.axis("off")
    ax.set_title("Tumbling windows - fixed, non-overlapping, one bucket per period",
                 loc="left", fontsize=10.5)

    ax = axes[1]
    positions = [0, 0.6, 1.2, 1.8, 2.4]
    for i, x in enumerate(positions):
        y = 1.3 - i * 0.28
        ax.add_patch(plt.Rectangle((x, y), 3, 0.22, facecolor=LIGHTAMBER,
                                   edgecolor=AMBER, alpha=0.9))
    ax.annotate("", xy=(5.6, 0.15), xytext=(0.3, 0.15),
                arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.2))
    ax.text(5.7, 0.15, "time advances,\nwindow slides", fontsize=8.5, color=SLATE, va="center")
    ax.set_xlim(-0.3, 8.3)
    ax.set_ylim(-0.3, 1.6)
    ax.axis("off")
    ax.set_title("Sliding windows - same width, re-evaluated on every slide interval, overlapping",
                 loc="left", fontsize=10.5)

    return save_mpl(fig, "9-5-tumbling-vs-sliding")


def rollup_writes():
    render("9-5-rollup-writes", f"""
    rankdir=LR;
    event [label="One view event\\l(video X, t=14:23)", fillcolor="{GRAY}", color="{SLATE}"];
    proc [label="Stream processor\\l(Flink / Spark)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    minute [label="minute bucket\\lX @ 14:23  +1", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    hour [label="hour rollup\\lX @ 14:00  +1", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    day [label="day rollup\\lX @ (today)  +1", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    idx [label="each rollup table is independently\\lindexed on (bucket, count)\\l-> topK(window) is a near-O(1)\\lindex read, no aggregation at query time", shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    event -> proc;
    proc -> minute; proc -> hour; proc -> day;
    hour -> idx [style=invis];
    {{ rank=same; minute; hour; day }}
    """)


if __name__ == "__main__":
    naive_scaleout()
    partitioned_scaleout()
    window_counterexample()
    hot_partition()
    cms_grid()
    mapreduce_flow()
    lambda_architecture()
    rate_funnel()
    tumbling_vs_sliding()
    rollup_writes()
