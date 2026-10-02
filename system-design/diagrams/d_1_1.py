"""Diagrams for note 1.1 - Functional vs non-functional requirements."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def what_vs_how_well():
    render("1-1-what-vs-how-well", f"""
    rankdir=LR;
    req [label="A requirement", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    func [label="FUNCTIONAL\\lWHAT the system does\\l'a user can post a photo'\\l'a user can search by tag'", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    nonfunc [label="NON-FUNCTIONAL\\lHOW WELL / under what\\lCONSTRAINTS it does it\\l'search returns in under 200ms\\lat p99, for 50M photos'", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    req -> func; req -> nonfunc;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Functional requirements are usually EXPLICIT and negotiable (the\\linterviewer states them, scope can shrink). Non-functional requirements\\lare usually IMPLICIT and architecture-determining - getting them wrong\\lsilently produces a working demo that falls over at real scale.\\l"];
    nonfunc -> note [style=invis];
    """)


def same_function_different_nfr():
    render("1-1-same-function-different-arch", f"""
    rankdir=TB;
    func [label="SAME functional requirement:\\l'a user can search for a product'", fillcolor="{INK}", fontcolor=white, color="{INK}"];

    small [label="NFR: 10K products,\\l100 QPS, staleness OK", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    small_arch [label="-> a single Postgres\\linstance with a B-tree\\lindex (3.3) is plenty", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    big [label="NFR: 500M products,\\l200K QPS, p99 < 50ms", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    big_arch [label="-> sharded search index\\l(3.4), aggressive caching\\l(4.1-4.3), CDN (4.4)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    func -> small -> small_arch;
    func -> big -> big_arch;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="The FUNCTIONAL requirement never changed - 'search for a product' is\\lidentical in both cases. The entire architecture difference comes from\\lthe non-functional numbers. This is why 0.3's estimation phase and this\\lnote's vocabulary come before any box-and-arrow diagram gets drawn.\\l"];
    small_arch -> note [style=invis]; big_arch -> note [style=invis];
    """)


def nfr_taxonomy():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.axis("off")
    rows = [
        ("category", "the question", "covered in"),
        ("Scalability & performance", "how does it behave as load grows? latency vs throughput?", "1.3"),
        ("Availability & reliability", "how much uptime? does it keep working correctly under failure?", "1.2"),
        ("Consistency", "must a read always see the latest write?", "1.5"),
        ("Durability", "can a committed write ever be lost?", "1.2, 2.7"),
        ("Security", "authN/authZ, encryption, threat surface", "Part 7"),
        ("Maintainability", "how easy to understand, change, operate over time?", "1.3"),
        ("Cost", "infra spend per user/request, within budget", "1.3, 8.3"),
        ("Compliance", "data residency, retention, PII handling", "noted per case study"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.01, y, row[0], fontsize=9.3, fontweight=weight, color=BLUE)
        ax.text(0.30, y, row[1], fontsize=8.6, fontweight=weight, color=INK)
        ax.text(0.86, y, row[2], fontsize=8.6, fontweight=weight, color=TEAL)
        ax.axhline(y - 0.42, xmin=0.01, xmax=0.99, color=(INK if i == 0 else GRAY), lw=(1.2 if i == 0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 0.8)
    ax.set_title("The non-functional taxonomy - each gets its own vocabulary in this Part", loc="left", pad=10)
    return save_mpl(fig, "1-1-nfr-taxonomy")


if __name__ == "__main__":
    what_vs_how_well()
    same_function_different_nfr()
    nfr_taxonomy()
