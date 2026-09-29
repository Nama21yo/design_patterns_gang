"""Diagrams for note 2.7 - Data redundancy and recovery."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def stateless_vs_stateful():
    render("2-7-stateless-vs-stateful", f"""
    rankdir=LR;

    subgraph cluster_app {{
        label="Stateless API servers";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        a1 [label="instance dies"]; a2 [label="load balancer removes\\lit, spins up a new one\\l(2.5)"]; a3 [label="NOTHING lost - it held\\lno unique data"];
        a1 -> a2 -> a3;
    }}

    subgraph cluster_db {{
        label="Stateful database";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        d1 [label="node dies", fillcolor="{RED}", fontcolor=white, color="{RED}"]; d2 [label="a NEW empty node\\lisn't the same data", fillcolor="{RED}", fontcolor=white, color="{RED}"]; d3 [label="data is GONE unless a\\lcopy exists somewhere else", fillcolor="{RED}", fontcolor=white, color="{RED}"];
        d1 -> d2 -> d3;
    }}
    """)


def backup_vs_continuous():
    render("2-7-backup-vs-continuous", f"""
    rankdir=TB;
    q [label="How current does the recovered\\lcopy need to be?", fillcolor="{INK}", fontcolor=white, color="{INK}"];

    backup [label="Periodic BACKUP + RESTORE\\l(full snapshot, e.g. nightly,\\l+ continuously archived WAL\\lfor point-in-time recovery)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    cont [label="CONTINUOUS replication\\l(3.5: leader streams its WAL\\lto a standby in near real time)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    q -> backup [label="  RPO of minutes-to-hours\\l  is acceptable"];
    q -> cont [label="  need RPO close to zero"];

    bnote [shape=note, fillcolor="{LIGHTBLUE}", color="{BLUE}", label="cheaper, simpler, but\\lrecovery = restore + WAL\\lreplay, takes real time (RTO)"];
    cnote [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}", label="a standby is ALREADY\\lcaught up (or nearly) -\\lpromote it, much faster RTO"];
    backup -> bnote [style=invis]; cont -> cnote [style=invis];
    """)


def pitr_timeline():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.axis("off")
    import matplotlib.patches as mpatches
    ax.annotate("", xy=(9.5, 1), xytext=(0.5, 1), arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.5))
    events = [
        (1, "base backup\ntaken", BLUE),
        (3.5, "good data\ninserted\n(recovery target)", TEAL),
        (6, "BAD change\n(disaster)", RED),
        (8.5, "now", SLATE),
    ]
    for x, label, color in events:
        ax.plot([x], [1], marker="o", markersize=10, color=color, zorder=3)
        ax.text(x, 1.35, label, ha="center", fontsize=8.5, color=color)
    ax.axvspan(1, 3.5, ymin=0.35, ymax=0.55, color=TEAL, alpha=0.3)
    ax.text(2.25, 0.25, "WAL replayed during recovery\n(base backup -> recovery target)", ha="center", fontsize=8, color=TEAL)
    ax.axvspan(3.5, 6, ymin=0.35, ymax=0.55, color=RED, alpha=0.15)
    ax.text(4.75, -0.15, "NOT replayed - this is what\nrecovery_target_time excludes", ha="center", fontsize=8, color=RED)
    ax.set_xlim(0, 10); ax.set_ylim(-0.5, 1.7)
    ax.set_title("Point-in-time recovery: replay WAL from the base backup up\nto (but not past) the recovery target time",
                loc="left", pad=10, fontsize=10.5)
    return save_mpl(fig, "2-7-pitr-timeline")


def geo_backup():
    render("2-7-geo-backup", f"""
    rankdir=LR;
    primary [label="Primary DB\\l(region A)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    localbackup [label="local backup\\l(same region)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    georeplica [label="cross-region copy\\l(region B)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    primary -> localbackup [label="  fast to restore,\\l  useless if region A\\l  itself goes down"];
    primary -> georeplica [label="  survives a whole-\\l  region outage"];

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="3.9's object storage (S3-style) commonly offers built-in cross-region\\lreplication for backup artifacts - storing ONE copy across regions is\\lusually 'point backups at a bucket with cross-region replication enabled'\\lrather than a custom mechanism.\\l"];
    georeplica -> note [style=invis];
    """)


if __name__ == "__main__":
    stateless_vs_stateful()
    backup_vs_continuous()
    pitr_timeline()
    geo_backup()
