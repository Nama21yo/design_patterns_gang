"""Diagrams for note 4.5 - Probabilistic data structures."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def bloom_motivation():
    render("4-5-bloom-motivation", f"""
    rankdir=LR;
    watch [label="User watches reel #48213", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    naive [label="Naive: store every\\lwatched reel ID in a set\\l(a hashmap/DB row per view)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    grow [label="Set grows FOREVER, per\\luser - millions of rows,\\lunbounded memory or an\\lever-slower lookup", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    insight [label="Key insight: once watched,\\lit CAN'T be un-watched -\\lyou never need to remove\\lan entry, and you never\\lneed the exact ID back,\\lonly 'have I seen this?'", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    bloom [label="-> store a compact YES/NO\\lfilter instead of the\\lactual IDs", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    watch -> naive -> grow;
    grow -> insight [style=dashed, color="{SLATE}", label="  the fix starts here"];
    insight -> bloom;
    """)


def bloom_structure():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(10, 3.6))
    m = 20
    for i in range(m):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor="white", edgecolor=SLATE))
    hit_bits_a = [2, 7, 13]
    hit_bits_b = [5, 7, 16]
    for b in hit_bits_a:
        ax.add_patch(plt.Rectangle((b, 0), 1, 1, facecolor=LIGHTBLUE, edgecolor=BLUE, linewidth=2))
        ax.text(b + 0.5, 0.5, "1", ha="center", va="center", fontsize=11, color=BLUE, fontweight="bold")
    for b in hit_bits_b:
        if b in hit_bits_a:
            ax.text(b + 0.5, 0.5, "1", ha="center", va="center", fontsize=11, color=INK, fontweight="bold")
        else:
            ax.add_patch(plt.Rectangle((b, 0), 1, 1, facecolor=LIGHTTEAL, edgecolor=TEAL, linewidth=2))
            ax.text(b + 0.5, 0.5, "1", ha="center", va="center", fontsize=11, color=TEAL, fontweight="bold")
    ax.text(-0.3, 1.6, 'add("reel_A"): h1,h2,h3 -> bits 2,7,13 (blue)', fontsize=9.5, color=BLUE, ha="left")
    ax.text(-0.3, 2.1, 'add("reel_B"): h1,h2,h3 -> bits 5,7,16 (teal) - bit 7 already set, shared', fontsize=9.5, color=TEAL, ha="left")
    ax.text(-0.3, -0.7, 'contains("reel_C")? if its 3 hash bits happen to ALL already be set\nby other items -> false positive. If even ONE bit is 0 -> definitely not present.',
           fontsize=9, color=SLATE, ha="left")
    ax.set_xlim(-0.5, m + 0.5)
    ax.set_ylim(-1.6, 2.6)
    ax.axis("off")
    ax.set_title("Bloom filter: an m-bit array, k hash functions per item",
                 loc="left", pad=6)
    return save_mpl(fig, "4-5-bloom-structure")


def bloom_fp_growth():
    plt = mpl()
    labels = ["5,000\n(0.5x)", "10,000\n(1.0x)", "20,000\n(2.0x)", "40,000\n(4.0x)"]
    rates = [0.03, 0.92, 15.75, 67.83]
    colors = [TEAL, BLUE, AMBER, RED]
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.bar(labels, rates, color=colors, width=0.55)
    for i, v in enumerate(rates):
        ax.text(i, v + 1.5, f"{v:.2f}%", ha="center", fontsize=10)
    ax.set_ylabel("empirical false-positive rate")
    ax.set_xlabel("items actually added (filter sized/planned for 10,000)")
    ax.set_title("Measured: false-positive rate grows sharply once you exceed\nthe capacity a fixed-size filter was planned for",
                 loc="left", pad=10, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "4-5-bloom-fp-growth")


def bloom_when_to_use():
    render("4-5-bloom-when-to-use", f"""
    rankdir=TB;
    q [label="Should I use a Bloom filter?", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    q1 [label="Do you only INSERT,\\lnever remove?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    q2 [label="Do you need a 'definitely\\lNOT present' answer with\\l100% certainty?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    q3 [label="Is an occasional false\\l'maybe present' okay?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    yes [label="Good fit - dedup a feed,\\lweb crawler URL dedup,\\lrecommendation-already-\\lshown filters", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    no [label="Use a Counting Bloom\\lFilter instead (below),\\lor a different structure", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    q -> q1;
    q1 -> q2 [label="  yes"];
    q1 -> no [label="  no, I need\\l  deletion"];
    q2 -> q3 [label="  yes"];
    q3 -> yes [label="  yes"];
    """)


def hyperloglog_mechanism():
    render("4-5-hyperloglog-mechanism", f"""
    rankdir=LR;
    item [label="hash(item)\\l(a long random-looking\\lbit string)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    bucket [label="low bits -> which of\\lm buckets (registers)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    rank [label="rest of the bits ->\\lcount LEADING ZEROS\\l+ 1 ('rank')", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    reg [label="that bucket keeps the\\lMAX rank ever seen", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    item -> bucket; item -> rank; rank -> reg;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="A run of k leading zeros in a random hash has probability 2^-k - rare.\\lSeeing rank k at all suggests roughly 2^k DISTINCT items were hashed into\\lthat bucket. Average (harmonic mean, bias-corrected) across m buckets to\\lcut variance down to a usable estimate - verified: ~1-2% error using only\\l4 KB of memory, whether the true count is 1,000 or 1,000,000.\\l"];
    reg -> note [style=invis];
    """)


def hyperloglog_accuracy():
    plt = mpl()
    labels = ["1,000", "100,000", "1,000,000"]
    errors = [1.95, 0.85, 1.92]
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    ax.bar(labels, errors, color=TEAL, width=0.45)
    for i, v in enumerate(errors):
        ax.text(i, v + 0.06, f"{v:.2f}%", ha="center", fontsize=10)
    ax.set_ylabel("estimation error")
    ax.set_xlabel("true distinct count")
    ax.set_ylim(0, 2.6)
    ax.set_title("Measured HyperLogLog error - SAME 4 KB of memory\nacross 3 orders of magnitude of true cardinality",
                 loc="left", pad=10, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "4-5-hyperloglog-accuracy")


def tdigest_concept():
    render("4-5-tdigest-concept", f"""
    rankdir=LR;
    stream [label="Stream of 200,000\\llatency samples", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    centroids [label="A bounded set of\\lweighted centroids\\l(here: 200)\\leach = (mean, count)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    merge [label="New value near an\\lexisting centroid ->\\lMERGE into it (update\\lthe running mean)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    query [label="quantile(0.99): walk\\lcentroids by cumulative\\lweight to the target point", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    stream -> centroids -> merge;
    centroids -> query;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Real t-digest concentrates MORE, smaller centroids near the tails\\l(p99, p99.9) where precision matters most, and fewer/bigger ones near\\lthe median where it doesn't - this simplified version already gets\\lwithin ~0.5 of the true p99 using 1000x fewer stored values than the\\lraw stream (verified: p50/p90/p99/p99.9 all matched closely).\\l"];
    query -> note [style=invis];
    """)


def probabilistic_summary():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(10.5, 3.6))
    ax.axis("off")
    rows = [
        ("structure", "answers", "verified result"),
        ("Bloom filter", "is X definitely absent / maybe present?", "0 false negatives, FP rate matched theory exactly"),
        ("Counting Bloom", "same, but supports DELETE", "removal didn't affect other items"),
        ("Count-Min Sketch", "approx. frequency of X (9.5)", "0 undercounts, error within the proven bound"),
        ("HyperLogLog", "approx. count of DISTINCT items", "1-2% error, 4KB flat, 1K to 1M items"),
        ("t-digest", "approx. percentile / quantile", "~0.02-0.46 error, 1000x fewer values kept"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.02, y, row[0], fontsize=9.3, fontweight=weight, color=BLUE)
        ax.text(0.24, y, row[1], fontsize=9.0, fontweight=weight, color=INK)
        ax.text(0.60, y, row[2], fontsize=8.6, fontweight=weight, color=SLATE)
        ax.axhline(y - 0.35, xmin=0.02, xmax=0.98, color=(INK if i == 0 else GRAY), lw=(1.2 if i == 0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 0.6)
    ax.set_title("Probabilistic structures covered in this note, at a glance", loc="left", pad=10)
    return save_mpl(fig, "4-5-probabilistic-summary")


if __name__ == "__main__":
    bloom_motivation()
    bloom_structure()
    bloom_fp_growth()
    bloom_when_to_use()
    hyperloglog_mechanism()
    hyperloglog_accuracy()
    tdigest_concept()
    probabilistic_summary()
