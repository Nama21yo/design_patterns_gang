"""Diagrams for note 0.1 - How to use this syllabus + study plan."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def dependency_map():
    render("0-1-dependency-map", f"""
    rankdir=LR;
    node [shape=box];

    p0  [label="0. Orientation\\lframework + estimation", fillcolor="{INK}", fontcolor="white", color="{INK}"];
    p1  [label="1. Fundamentals\\lCAP, consistency, ACID/BASE", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    p2  [label="2. Communication", fillcolor="white"];
    p3  [label="3. Storage", fillcolor="white"];
    p4  [label="4. Caching", fillcolor="white"];
    p5  [label="5. Messaging &\\ldata processing", fillcolor="white"];
    p6  [label="6. Infra & ops", fillcolor="white"];
    p7  [label="7. Security & time", fillcolor="white"];
    p8  [label="8. Product thinking", fillcolor="white"];
    p9  [label="9. Case studies\\l(12 blueprints)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    p10 [label="10. Bloomberg prep\\l(the target)", fillcolor="{LIGHTAMBER}", color="{AMBER}", penwidth="2"];

    p0 -> p1;
    p1 -> p2; p1 -> p3; p1 -> p4;
    p2 -> p5; p3 -> p5; p4 -> p5;
    p5 -> p6 -> p7;
    p1 -> p8 [style=dashed];
    p7 -> p9; p8 -> p9;
    p9 -> p10;
    p0 -> p10 [style=dashed, label="  pull forward\\l  what you need", color="{SLATE}", constraint=false];
    """)


def study_plan():
    plt = mpl()
    # (label, start_week, weeks, color)
    rows = [
        ("Part 0  framework + estimation", 0, 1, INK),
        ("Part 1  fundamentals", 1, 1.5, BLUE),
        ("Part 2  communication", 2, 1, BLUE),
        ("Part 3  storage", 2.5, 2, BLUE),
        ("Part 4  caching", 4, 1, BLUE),
        ("Part 5  messaging / streaming", 4.5, 1.5, BLUE),
        ("Part 6-7  infra, security, time", 6, 1.5, BLUE),
        ("Part 8  product thinking", 7, 0.5, TEAL),
        ("Part 9  case studies (ongoing)", 3, 5, TEAL),
        ("Part 10  Bloomberg questions", 6, 3, AMBER),
    ]
    fig, ax = plt.subplots(figsize=(11, 4.2))
    for i, (label, start, dur, color) in enumerate(rows):
        y = len(rows) - i
        ax.barh(y, dur, left=start, height=0.62, color=color, edgecolor="white")
        ax.text(-0.15, y, label, ha="right", va="center", fontsize=9)
    # mock interview markers
    for wk in (4, 6, 8, 9):
        ax.axvline(wk, color=RED, lw=1.2, ls=(0, (4, 3)))
        ax.text(wk, len(rows) + 0.75, f"mock\nwk {wk}", ha="center", va="bottom",
                fontsize=8, color=RED)
    ax.set_xlim(-4.2, 9.4)
    ax.set_ylim(0.2, len(rows) + 1.8)
    ax.set_yticks([])
    ax.set_xticks(range(0, 10))
    ax.set_xlabel("week")
    ax.set_title("An ~9-week plan (compress or stretch to your timeline)", loc="left", pad=26)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "0-1-study-plan")


def practice_loop():
    render("0-1-practice-loop", f"""
    rankdir=LR;
    a [label="1. Pick a problem\\l(Part 9 or 10)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    b [label="2. Solve solo, out loud,\\l40 min, one timer", fillcolor="white"];
    c [label="3. Record audio +\\lphoto the board", fillcolor="white"];
    d [label="4. Compare to a\\lreference design", fillcolor="white"];
    e [label="5. Write down 3 gaps\\l(missed requirement,\\lweak deep dive, ...)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    f [label="6. Redo only the\\lweak part", fillcolor="white"];
    a -> b -> c -> d -> e -> f;
    f -> a [label="  next day /\\l  next problem", color="{SLATE}"];
    """)


if __name__ == "__main__":
    dependency_map()
    study_plan()
    practice_loop()
