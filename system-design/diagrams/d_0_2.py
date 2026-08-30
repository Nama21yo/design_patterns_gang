"""Diagrams for note 0.2 - The system design interview framework."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def phases_timeline():
    """Horizontal time budget for a ~45 min round."""
    plt = mpl()
    phases = [
        ("Requirements\n& scope", 6, BLUE),
        ("Estimation", 4, TEAL),
        ("API\ndesign", 4, TEAL),
        ("Data\nmodel", 4, TEAL),
        ("High-level design", 12, BLUE),
        ("Deep dives (2-3 components)", 12, AMBER),
        ("Wrap-\nup", 3, SLATE),
    ]
    fig, ax = plt.subplots(figsize=(11, 2.6))
    start = 0
    for i, (label, dur, color) in enumerate(phases):
        ax.barh(0, dur, left=start, height=1.0, color=color, edgecolor="white")
        below = i % 2 == 1  # alternate label position for the narrow early segments
        if dur >= 10:
            ax.text(start + dur / 2, 0, label, ha="center", va="center",
                    color="white", fontsize=10, fontweight="bold")
        else:
            y = -1.05 if below else 1.05
            va = "top" if below else "bottom"
            ax.text(start + dur / 2, y, label, ha="center", va=va,
                    color=INK, fontsize=8.5)
            ax.plot([start + dur / 2, start + dur / 2], [0, y * 0.55],
                    color=SLATE, lw=0.8)
        ax.text(start, -0.75, f"{start}'", ha="center", va="top",
                color=SLATE, fontsize=8)
        start += dur
    ax.text(start, -0.75, f"{start}'", ha="center", va="top", color=SLATE, fontsize=8)
    ax.set_xlim(-1, start + 1)
    ax.set_ylim(-2.2, 2.2)
    ax.axis("off")
    ax.set_title("A 45-minute round: rough time budget", pad=10, loc="left")
    return save_mpl(fig, "0-2-phases-timeline")


def framework_flow():
    render("0-2-framework-flow", f"""
    rankdir=TB;
    node [shape=box];

    r  [label="1. Requirements & scope\\l   functional + non-functional, constraints\\l", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    e  [label="2. Back-of-envelope estimation\\l   DAU, QPS, storage, bandwidth\\l", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    a  [label="3. API design\\l   the contract between client and system\\l", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    d  [label="4. Data model\\l   entities, access patterns, store choice\\l", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    h  [label="5. High-level design\\l   boxes and arrows: the request path\\l", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    dd [label="6. Deep dives\\l   pick 2-3: scaling, storage, consistency...\\l", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    b  [label="7. Bottlenecks & trade-offs\\l   SPOFs, hot spots, failure modes\\l", fillcolor="{GRAY}", color="{SLATE}"];

    r -> e -> a -> d -> h -> dd -> b;
    dd -> h [label="  iterate", constraint=false, style=dashed, color="{SLATE}"];
    b -> dd [label="  revisit", constraint=false, style=dashed, color="{SLATE}"];
    """)


def requirements_tree():
    render("0-2-requirements-tree", f"""
    rankdir=LR;
    req [label="Requirements", fillcolor="{INK}", fontcolor="white", color="{INK}"];

    fn  [label="Functional\\l(what it does)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    nf  [label="Non-functional\\l(how well it does it)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    req -> fn; req -> nf;

    fn1 [label="Core user actions\\le.g. post, follow, search"];
    fn2 [label="Out of scope\\l(state explicitly)"];
    fn -> fn1; fn -> fn2;

    nf1 [label="Scale: users, QPS,\\ldata size, growth"];
    nf2 [label="Latency / throughput\\ltargets (p50, p99)"];
    nf3 [label="Availability &\\ldurability targets"];
    nf4 [label="Consistency needs\\l(strong vs eventual)"];
    nf5 [label="Read : write ratio\\l& access patterns"];
    nf6 [label="Cost, security,\\lcompliance"];
    nf -> nf1; nf -> nf2; nf -> nf3; nf -> nf4; nf -> nf5; nf -> nf6;
    """)


def hld_template():
    render("0-2-hld-template", f"""
    rankdir=LR;
    client [label="Clients\\l(web, mobile, API)", fillcolor="{GRAY}", color="{SLATE}"];
    dns    [label="DNS /\\lGeoDNS", fillcolor="white"];
    cdn    [label="CDN\\l(static, edge cache)", fillcolor="white"];
    lb     [label="Load\\lbalancer", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    gw     [label="API gateway\\lauth, rate limit", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    svc    [label="Stateless app\\lservers (N)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    cache  [label="Cache\\l(Redis)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    db     [label="Primary DB\\l+ replicas", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    q      [label="Message queue\\l(Kafka)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    wrk    [label="Async workers", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    blob   [label="Blob store\\l(S3)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    client -> dns -> cdn -> lb -> gw -> svc;
    svc -> cache [dir=both];
    svc -> db [dir=both];
    svc -> q -> wrk;
    wrk -> db;
    svc -> blob [dir=both];
    {{ rank=same; cache; db }}
    {{ rank=same; q; wrk }}
    """)


if __name__ == "__main__":
    phases_timeline()
    framework_flow()
    requirements_tree()
    hld_template()
