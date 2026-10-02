"""Diagrams for note 1.4 - CAP theorem and PACELC."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def cap_during_partition():
    render("1-4-cap-during-partition", f"""
    rankdir=TB;
    p [label="A network PARTITION happens\\l(it WILL happen eventually -\\lP isn't really optional)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    q [label="Can you still serve\\lrequests on BOTH sides?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    cp [label="CP: refuse requests on the\\lside that can't reach a\\lquorum - stay CONSISTENT,\\lsacrifice AVAILABILITY there", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    ap [label="AP: keep serving BOTH sides -\\lstay AVAILABLE, sacrifice\\lCONSISTENCY (the sides diverge)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    p -> q;
    q -> cp [label="  no"];
    q -> ap [label="  yes"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="CAP is ONLY about behavior DURING a partition - not a permanent 3-way\\ltrade-off a system picks once. A system can (and does) behave differently\\lunder normal conditions than it does mid-partition - which is exactly the\\lgap PACELC fills below.\\l"];
    cp -> note [style=invis]; ap -> note [style=invis];
    """)


def cp_vs_ap_verified():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8.5, 4))
    ax.axis("off")
    rows = [
        ("", "minority side (1 of 3)", "majority side (2 of 3)", "result"),
        ("CP system", "write REFUSED", "write succeeded", "no divergence - minority\nsacrificed availability"),
        ("AP system", "write succeeded\n(balance=500)", "write succeeded\n(balance=700)", "DIVERGED - needs read\nrepair (3.5) to reconcile"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.01, y, row[0], fontsize=9.3, fontweight=weight, color=BLUE)
        ax.text(0.20, y, row[1], fontsize=8.6, fontweight=weight, color=(TEAL if i==1 else RED) if i else SLATE)
        ax.text(0.47, y, row[2], fontsize=8.6, fontweight=weight, color=INK)
        ax.text(0.73, y, row[3], fontsize=8.3, fontweight=weight, color=SLATE)
        ax.axhline(y - 0.45, xmin=0.01, xmax=0.99, color=(INK if i == 0 else GRAY), lw=(1.2 if i == 0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 0.9)
    ax.set_title("Verified: same partition (3.5's R+W>N quorum), same cluster -\nCP refuses, AP diverges", loc="left", pad=10, fontsize=10.5)
    return save_mpl(fig, "1-4-cp-vs-ap-verified")


def pacelc_flow():
    render("1-4-pacelc-flow", f"""
    rankdir=TB;
    start [label="PACELC: is there a\\lPartition right now?", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    pac [label="P -> choose A or C\\l(exactly CAP, above)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    elc [label="Else (normal operation,\\lNO partition) -> choose\\lL(atency) or C(onsistency)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    start -> pac [label="  yes"];
    start -> elc [label="  no (the common case)"];

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="This is exactly 3.5's sync vs async replication choice, proven live even\\lwith NO partition: synchronous commit (favors C) blocked for 4.06s when\\lits standby was merely unreachable; asynchronous commit (favors L) never\\lblocks at all, at the cost of a measured ~1.24ms window where a replica\\lcan serve stale data. PACELC is this trade-off, named and generalized.\\l"];
    elc -> note [style=invis];
    """)


def pacelc_quadrants():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.axis("off")
    rows = [
        ("classification", "under partition", "else (normal ops)", "example"),
        ("PC/EC", "choose Consistency", "choose Consistency", "traditional RDBMS w/\nsynchronous replication"),
        ("PA/EL", "choose Availability", "choose Latency", "Dynamo, Cassandra\n(leaderless, 3.5)"),
        ("PC/EL", "choose Consistency", "choose Latency", "MongoDB (tunable per op)"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.01, y, row[0], fontsize=9.3, fontweight=weight, color=BLUE)
        ax.text(0.20, y, row[1], fontsize=8.6, fontweight=weight, color=INK)
        ax.text(0.47, y, row[2], fontsize=8.6, fontweight=weight, color=INK)
        ax.text(0.73, y, row[3], fontsize=8.3, fontweight=weight, color=SLATE)
        ax.axhline(y - 0.45, xmin=0.01, xmax=0.99, color=(INK if i == 0 else GRAY), lw=(1.2 if i == 0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 0.9)
    ax.set_title("PACELC classifications - most systems are NOT a single point on\nthe CAP triangle, they're one of these four combinations", loc="left", pad=10, fontsize=10)
    return save_mpl(fig, "1-4-pacelc-quadrants")


if __name__ == "__main__":
    cap_during_partition()
    cp_vs_ap_verified()
    pacelc_flow()
    pacelc_quadrants()
