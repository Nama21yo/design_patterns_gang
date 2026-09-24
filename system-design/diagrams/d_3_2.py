"""Diagrams for note 3.2 - SQL vs NoSQL and data models."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def acid_pillars():
    render("3-2-acid-pillars", f"""
    rankdir=LR;
    a [label="Atomicity\\lall-or-nothing\\l(the whole tx applies,\\lor none of it does)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    c [label="Consistency\\lconstraints, cascades,\\ltriggers always hold\\l(app + DB rules)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    i [label="Isolation\\lconcurrent transactions\\ldon't see each other's\\lhalf-finished work", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    d [label="Durability\\lonce committed, survives\\la crash right after\\l(on disk / WAL)", fillcolor="{GRAY}", color="{SLATE}"];
    a -> c -> i -> d [style=invis];
    """)


def data_model_quadrant():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    points = [
        ("Relational\n(Postgres, MySQL)", 2.0, 8.7, BLUE),
        ("Document\n(MongoDB)", 5.8, 6.8, TEAL),
        ("Wide-column\n(Cassandra, Bigtable)", 8.3, 4.2, AMBER),
        ("Key-value\n(Redis, DynamoDB)", 9.3, 1.8, RED),
        ("Graph\n(Neo4j, Neptune)", 3.2, 3.0, INK),
        ("Time-series\n(Timescale, InfluxDB)", 7.0, 7.5, "#7c5cbf"),
    ]
    for label, x, y, color in points:
        ax.scatter([x], [y], s=260, color=color, zorder=3, edgecolor="white", linewidth=1.5)
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(0, -22 if y > 5 else 18),
                    ha="center", fontsize=9, color=INK)
    ax.axhline(5, color=GRAY, lw=1, zorder=1)
    ax.axvline(5, color=GRAY, lw=1, zorder=1)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 10.5)
    ax.set_xlabel("effortless horizontal scale  ->", fontsize=10)
    ax.set_ylabel("query flexibility (joins, ad-hoc filters, aggregation)  ->", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("Where each data model sits on the two axes that matter most",
                 loc="left", pad=12)
    return save_mpl(fig, "3-2-data-model-quadrant")


def decision_tree():
    render("3-2-decision-tree", f"""
    rankdir=TB;
    start [label="What does this data need?", fillcolor="{INK}", fontcolor=white, color="{INK}"];

    q1 [label="Complex queries, joins,\\lmulti-row transactions,\\lstrong consistency?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    q2 [label="Deep, many-hop\\lrelationship traversal\\l(friends-of-friends,\\lfraud rings)?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    q3 [label="Access is always\\l'give me the value\\lfor this one key'?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    q4 [label="Flexible / nested schema,\\lbut still query by\\lspecific attributes?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    rel [label="Relational\\l(Postgres, MySQL)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    graphdb [label="Graph DB\\l(Neo4j, Neptune)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    kv [label="Key-value store\\l(Redis, DynamoDB)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    doc [label="Document DB\\l(MongoDB)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    wide [label="Wide-column\\l(Cassandra) - huge\\lwrite volume, simple\\lquery, need range scans", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    start -> q1;
    q1 -> rel [label="  yes"];
    q1 -> q2 [label="  no, need\\l  horizontal scale"];
    q2 -> graphdb [label="  yes"];
    q2 -> q3 [label="  no"];
    q3 -> kv [label="  yes"];
    q3 -> q4 [label="  no"];
    q4 -> doc [label="  yes"];
    q4 -> wide [label="  no, it's write-\\l  heavy + simple"];
    """)


def isolation_matrix():
    plt = mpl()
    rows = [
        ("Read Uncommitted", "possible", "possible", "possible", RED),
        ("Read Committed", "prevented", "possible", "possible", AMBER),
        ("Repeatable Read", "prevented", "prevented", "possible*", BLUE),
        ("Serializable", "prevented", "prevented", "prevented", TEAL),
    ]
    fig, ax = plt.subplots(figsize=(9.5, 3.4))
    ax.axis("off")
    ax.set_title("Isolation levels vs. the anomalies they prevent (SQL standard)", loc="left", pad=10)
    cols = ["level", "dirty read", "non-repeatable read", "phantom read"]
    xs = [0.02, 0.40, 0.60, 0.83]
    for x, c in zip(xs, cols):
        ax.text(x, len(rows) + 0.3, c, fontsize=9, fontweight="bold")
    for i, (level, a, b, c, color) in enumerate(rows):
        yy = len(rows) - i - 0.4
        ax.text(xs[0], yy, level, fontsize=9.5, va="center", color=color, fontweight="bold")
        for x, val in zip(xs[1:], (a, b, c)):
            vcolor = TEAL if val == "prevented" else (SLATE if "*" in val else RED)
            ax.text(x, yy, val, fontsize=9, va="center", color=vcolor)
        ax.axhline(yy - 0.4, xmin=0.02, xmax=0.98, color=GRAY, lw=0.6)
    ax.text(0.02, -0.55, "* Postgres's Repeatable Read is implemented as a full-transaction MVCC "
           "snapshot, which in practice also prevents phantom reads - stricter than the standard requires. Verified below.",
           fontsize=8, color=SLATE, style="italic")
    ax.set_xlim(0, 1)
    ax.set_ylim(-1, len(rows) + 0.7)
    return save_mpl(fig, "3-2-isolation-matrix")


if __name__ == "__main__":
    acid_pillars()
    data_model_quadrant()
    decision_tree()
    isolation_matrix()
