"""Diagrams for note 4.2 - Cache invalidation and stampede protection."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def stampede_before_after():
    plt = mpl()
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))

    ax = axes[0]
    ax.set_title("Naive: 30 concurrent misses ->\n30 DB hits (measured)", fontsize=10.5)
    ax.bar(["DB queries fired"], [30], color=RED, width=0.4)
    ax.text(0, 31, "30", ha="center", fontsize=11)
    ax.set_ylim(0, 35)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    ax = axes[1]
    ax.set_title("SETNX-locked: 30 concurrent misses\n-> 1 DB hit (measured)", fontsize=10.5)
    ax.bar(["DB queries fired"], [1], color=TEAL, width=0.4)
    ax.text(0, 2, "1", ha="center", fontsize=11)
    ax.set_ylim(0, 35)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    fig.suptitle("Cache stampede: same 30 concurrent requests on a cold key", fontsize=12, y=1.03)
    return save_mpl(fig, "4-2-stampede-before-after")


def stampede_lock_flow():
    render("4-2-stampede-lock-flow", f"""
    rankdir=TB;
    miss [label="Cache miss on a hot key\\l(N concurrent requests)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    lock [label="Try SETNX lock:key\\l(atomic - only ONE\\lrequest can succeed)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    winner [label="Winner: query the DB,\\lpopulate the cache,\\lrelease the lock", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    losers [label="Everyone else: short\\lpoll/wait, then read the\\l(now-populated) cache", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    miss -> lock;
    lock -> winner [label="  got it"];
    lock -> losers [label="  didn't"];
    winner -> losers [style=dashed, color="{SLATE}", label="  cache now has\\l  the value"];
    """)


def invalidation_strategies():
    render("4-2-invalidation-strategies", f"""
    rankdir=LR;
    ttl [label="TTL expiry\\lentry just times out\\l(simple, bounded staleness,\\lno coordination needed)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    explicit [label="Explicit invalidation on write\\lthe write path deletes/updates\\lthe cache entry itself\\l(fresher, more code paths\\lto get right)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    version [label="Versioned / keyed by content hash\\lold version just stops being\\lreferenced - no delete needed,\\lold entries age out naturally", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    ttl -> explicit -> version [style=invis];
    """)


def negative_caching_swr():
    render("4-2-negative-caching-swr", f"""
    rankdir=TB;

    subgraph cluster_neg {{
        label="Negative caching";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        n1 [label="Lookup for a key that\\lDOESN'T EXIST", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        n2 [label="Without it: every repeat\\llookup for that missing key\\lhits the DB again", fillcolor="{RED}", fontcolor=white, color="{RED}"];
        n3 [label="With it: cache the\\l'not found' result too\\l(short TTL)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        n1 -> n2 [style=invis]; n1 -> n3;
    }}

    subgraph cluster_swr {{
        label="Stale-while-revalidate";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        s1 [label="Entry just expired", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        s2 [label="Serve the STALE value\\limmediately (fast)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        s3 [label="...while refreshing it\\lin the background for\\lnext time", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        s1 -> s2; s2 -> s3;
    }}
    """)


if __name__ == "__main__":
    stampede_before_after()
    stampede_lock_flow()
    invalidation_strategies()
    negative_caching_swr()
