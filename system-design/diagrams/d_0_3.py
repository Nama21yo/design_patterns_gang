"""Diagrams for note 0.3 - Back-of-the-envelope estimation + latency numbers."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


LAT = [
    ("L1 cache reference", 1e0),
    ("Branch mispredict", 3e0),
    ("L2 cache reference", 4e0),
    ("Mutex lock/unlock", 17e0),
    ("Main memory reference (RAM)", 100e0),
    ("Compress 1 KB (Zippy/Snappy)", 2e3),
    ("Read 1 MB sequentially from RAM", 3e3),
    ("Send 1 KB over 1 Gbps network", 10e3),
    ("SSD random read", 16e3),
    ("Read 1 MB sequentially from SSD", 49e3),
    ("Round trip within same datacenter", 500e3),
    ("Read 1 MB sequentially from disk (HDD)", 825e3),
    ("Disk (HDD) seek", 2e6),
    ("Packet round trip CA -> Netherlands -> CA", 150e6),
]


def latency_ladder():
    plt = mpl()
    labels = [x[0] for x in LAT][::-1]
    vals = [x[1] for x in LAT][::-1]
    colors = []
    for v in vals:
        if v < 1e3:
            colors.append(TEAL)        # nanoseconds
        elif v < 1e6:
            colors.append(BLUE)        # microseconds
        else:
            colors.append(RED)         # milliseconds
    fig, ax = plt.subplots(figsize=(11, 5.4))
    ax.barh(range(len(vals)), vals, color=colors, edgecolor="white", height=0.68)
    ax.set_xscale("log")
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("nanoseconds (log scale)")
    for i, v in enumerate(vals):
        if v >= 1e6:
            txt = f"{v/1e6:g} ms"
        elif v >= 1e3:
            txt = f"{v/1e3:g} us"
        else:
            txt = f"{v:g} ns"
        ax.text(v * 1.15, i, txt, va="center", fontsize=8, color=SLATE)
    ax.set_xlim(0.6, 3e9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("Latency numbers every engineer should know   "
                 "(teal = ns,  blue = us,  red = ms)",
                 loc="left", pad=12, fontsize=11)
    return save_mpl(fig, "0-3-latency-ladder")


def latency_human():
    """Scale every latency by 1 billion so 1 ns -> 1 s."""
    plt = mpl()
    picks = [
        ("L1 cache (1 ns)", "1 second", "one heartbeat"),
        ("Main memory (100 ns)", "~2 minutes", "brew a coffee"),
        ("SSD random read (16 us)", "~4.5 hours", "a work day"),
        ("Same-datacenter round trip (0.5 ms)", "~6 days", "a short vacation"),
        ("HDD seek (2 ms)", "~3 weeks", ""),
        ("CA <-> Europe round trip (150 ms)", "~5 years", "a degree"),
    ]
    fig, ax = plt.subplots(figsize=(10, 3.3))
    ax.axis("off")
    ax.set_title("If 1 nanosecond = 1 second (multiply real latency by 1 billion)",
                 loc="left", pad=10)
    y = len(picks)
    ax.text(0.02, y + 0.4, "operation", fontsize=9, fontweight="bold")
    ax.text(0.52, y + 0.4, "human-scale time", fontsize=9, fontweight="bold")
    ax.text(0.78, y + 0.4, "feels like", fontsize=9, fontweight="bold")
    for i, (op, ht, feel) in enumerate(picks):
        yy = y - i - 0.3
        ax.text(0.02, yy, op, fontsize=9, va="center")
        ax.text(0.52, yy, ht, fontsize=9, va="center", color=BLUE, fontweight="bold")
        ax.text(0.78, yy, feel, fontsize=8.5, va="center", color=SLATE)
        ax.axhline(yy - 0.35, xmin=0.02, xmax=0.98, color=GRAY, lw=0.6)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, y + 0.8)
    return save_mpl(fig, "0-3-latency-human")


def estimation_flow():
    render("0-3-estimation-flow", f"""
    rankdir=TB;
    node [shape=box];

    dau [label="DAU\\l(daily active users)", fillcolor="{INK}", fontcolor="white", color="{INK}"];

    rpu  [label="x  actions per user per day", shape=plaintext, fillcolor="none", color="none"];
    dreq [label="Requests / day", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    avg  [label="/ 86,400 s  (~1e5)\\l= Average QPS", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    peak [label="x 2 to 10\\l= Peak QPS   <-- design to this", fillcolor="{LIGHTBLUE}", color="{BLUE}", penwidth="2"];

    wr   [label="writes/day x record size\\lx retention (days/years)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    stor [label="Storage (project 1y and 5y)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    bw   [label="Peak QPS x payload size\\l= Bandwidth (in / out)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    mem  [label="hot 20% of daily data\\l= Cache RAM needed", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    srv  [label="Peak QPS / throughput-per-box\\l= Number of servers", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    dau -> dreq; dreq -> avg -> peak;
    dau -> stor [style=invis];
    dreq -> wr [style=dashed, color="{SLATE}"];
    wr -> stor;
    peak -> bw;
    peak -> srv;
    dreq -> mem [style=dashed, color="{SLATE}"];

    {{ rank=same; peak; stor }}
    {{ rank=same; bw; srv; mem }}
    """)


def availability_table():
    plt = mpl()
    rows = [
        ("90%      (one nine)", "36.5 days", "3 days", "2.4 h"),
        ("99%      (two nines)", "3.65 days", "7.2 h", "14 min"),
        ("99.9%    (three nines)", "8.76 h", "43 min", "1.4 min"),
        ("99.99%   (four nines)", "52.6 min", "4.3 min", "8.6 s"),
        ("99.999%  (five nines)", "5.26 min", "26 s", "0.86 s"),
    ]
    fig, ax = plt.subplots(figsize=(9.5, 2.9))
    ax.axis("off")
    ax.set_title("Availability: allowed downtime", loc="left", pad=10)
    cols = ["availability", "per year", "per month", "per day"]
    xs = [0.02, 0.42, 0.63, 0.83]
    for x, c in zip(xs, cols):
        ax.text(x, len(rows) + 0.3, c, fontsize=9, fontweight="bold")
    for i, r in enumerate(rows):
        yy = len(rows) - i - 0.4
        color = INK if i < 2 else (BLUE if i < 4 else TEAL)
        for x, cell in zip(xs, r):
            ax.text(x, yy, cell, fontsize=9, va="center",
                    color=color, family="DejaVu Sans Mono" if x == xs[0] else "DejaVu Sans")
        ax.axhline(yy - 0.4, xmin=0.02, xmax=0.98, color=GRAY, lw=0.6)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.4, len(rows) + 0.7)
    return save_mpl(fig, "0-3-availability")


def worked_example():
    plt = mpl()
    lines = [
        ("Design Twitter - back of the envelope", "title"),
        ("", ""),
        ("Assume:  300M DAU   |   2 tweets/user/day written   |   read:write = 100:1", ""),
        ("", ""),
        ("WRITES", "h"),
        ("  300M x 2            = 600M tweets/day", ""),
        ("  600M / 1e5 s        = 6,000 writes/sec  (avg)", ""),
        ("  x5 peak             = 30,000 writes/sec  (peak)", ""),
        ("", ""),
        ("READS", "h"),
        ("  100 x 600M          = 60B timeline reads/day", ""),
        ("  60B / 1e5 s         = 600,000 reads/sec  (avg)  ->  ~3M/sec peak", ""),
        ("", ""),
        ("STORAGE (tweet text)", "h"),
        ("  600M x 300 bytes    = ~180 GB/day  ->  ~65 TB/year  ->  ~325 TB / 5 yr", ""),
        ("  media goes to blob store, not the DB", ""),
        ("", ""),
        ("IMPLICATION", "h"),
        ("  3M read QPS cannot hit a DB -> heavy caching + fan-out-on-write timelines", ""),
        ("  65 TB/year -> partitioned store, not a single Postgres box", ""),
    ]
    fig, ax = plt.subplots(figsize=(10.5, 6))
    ax.axis("off")
    y = len(lines)
    for i, (txt, kind) in enumerate(lines):
        yy = y - i
        if kind == "title":
            ax.text(0.02, yy, txt, fontsize=12, fontweight="bold", color=INK)
        elif kind == "h":
            ax.text(0.02, yy, txt, fontsize=10, fontweight="bold", color=BLUE)
        else:
            ax.text(0.02, yy, txt, fontsize=9.5, family="DejaVu Sans Mono", color=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, y + 1)
    fig.patch.set_edgecolor(GRAY)
    fig.patch.set_linewidth(2)
    return save_mpl(fig, "0-3-worked-twitter")


if __name__ == "__main__":
    latency_ladder()
    latency_human()
    estimation_flow()
    availability_table()
    worked_example()
