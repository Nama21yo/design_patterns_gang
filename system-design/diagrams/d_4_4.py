"""Diagrams for note 4.4 - CDN and edge caching."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def cdn_geography():
    render("4-4-cdn-geography", f"""
    rankdir=TB;
    user [label="User in Nairobi", fillcolor="{GRAY}", color="{SLATE}"];
    dns [label="DNS / anycast routing\\l'which edge is nearest?'", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    near [label="Nairobi edge PoP\\l(nearest - low latency)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    far1 [label="London PoP", fillcolor="{GRAY}", color="{SLATE}"];
    far2 [label="Singapore PoP", fillcolor="{GRAY}", color="{SLATE}"];
    origin [label="Origin server\\l(your actual backend,\\lfar away)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    user -> dns -> near;
    near -> origin [label="  only on a MISS", style=dashed, color="{RED}"];
    far1 -> origin [style=invis]; far2 -> origin [style=invis];
    {{ rank=same; near; far1; far2 }}

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Every point of presence (PoP) is a full edge cache. Geography IS\\lthe latency win here (0.3's numbers: same-continent vs cross-\\locean round trip) - the CDN's whole value proposition is serving\\lfrom physically near the user instead of your one origin.\\l"];
    near -> note [style=invis];
    """)


def cdn_population_expiry():
    render("4-4-cdn-population-expiry", f"""
    rankdir=LR;
    req [label="Request for\\l/logo.png reaches\\lan edge PoP", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    hit [label="Cache HIT\\l(already have it,\\lnot expired)\\l-> serve instantly", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    miss [label="Cache MISS\\l(first request at THIS\\lPoP, or expired)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    origin [label="Pull from origin,\\lcache it, THEN serve\\l(lazy population)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    expiry [label="Cache-Control headers\\lset the expiry:\\lmax-age, s-maxage,\\lstale-while-revalidate (4.2)", fillcolor="{GRAY}", color="{SLATE}"];

    req -> hit;
    req -> miss -> origin;
    origin -> expiry [style=dashed, color="{SLATE}"];
    """)


def origin_shielding():
    render("4-4-origin-shielding", f"""
    rankdir=LR;

    subgraph cluster_without {{
        label="Without a shield";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        e1 [label="PoP: Nairobi"]; e2 [label="PoP: Lagos"]; e3 [label="PoP: Cairo"];
        o1 [label="Origin", fillcolor="{RED}", fontcolor=white, color="{RED}"];
        e1 -> o1; e2 -> o1; e3 -> o1;
        n1 [shape=note, fillcolor="{RED}", fontcolor=white, color="{RED}", label="every PoP's first miss hits\\lorigin independently - N\\lregional misses for 1 file\\l"];
        o1 -> n1 [style=invis];
    }}

    subgraph cluster_with {{
        label="With an origin shield";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        f1 [label="PoP: Nairobi"]; f2 [label="PoP: Lagos"]; f3 [label="PoP: Cairo"];
        shield [label="Shield PoP\\l(one designated\\lmid-tier cache)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        o2 [label="Origin", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        f1 -> shield; f2 -> shield; f3 -> shield; shield -> o2;
        n2 [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}", label="all regional misses funnel\\lthrough ONE shield ->\\lorigin sees only 1 miss\\l"];
        o2 -> n2 [style=invis];
    }}
    """)


def cdn_providers():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.axis("off")
    rows = [
        ("provider", "known for"),
        ("Cloudflare", "huge edge network, integrated security (WAF/DDoS), generous free tier"),
        ("Akamai", "one of the oldest/largest, deep enterprise footprint"),
        ("Fastly", "very fast cache purges, popular for dynamic/API content"),
        ("Amazon CloudFront", "tight AWS integration"),
        ("Cloudflare R2 / others", "CDN + S3-compatible storage combined (4.9's zero-egress point)"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.02, y, row[0], fontsize=9.5, fontweight=weight, color=BLUE)
        ax.text(0.24, y, row[1], fontsize=9.2, fontweight=weight, color=SLATE)
        ax.axhline(y - 0.35, xmin=0.02, xmax=0.98, color=(INK if i == 0 else GRAY), lw=(1.2 if i == 0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 0.6)
    ax.set_title("Some widely-used CDNs", loc="left", pad=10)
    return save_mpl(fig, "4-4-cdn-providers")


if __name__ == "__main__":
    cdn_geography()
    cdn_population_expiry()
    origin_shielding()
    cdn_providers()
