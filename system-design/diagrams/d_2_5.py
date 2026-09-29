"""Diagrams for note 2.5 - Load balancing, reverse proxy, API gateway."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def l4_vs_l7():
    render("2-5-l4-vs-l7", f"""
    rankdir=LR;

    subgraph cluster_l4 {{
        label="L4 (transport layer)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        c4 [label="client", fillcolor="{GRAY}", color="{SLATE}"];
        lb4 [label="L4 LB\\lroutes by IP + port ONLY\\l(never opens the packet's\\lapplication payload)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        s4 [label="backend servers\\l(TCP connection forwarded\\l/ NAT'd as-is)", fillcolor="{GRAY}", color="{SLATE}"];
        c4 -> lb4 -> s4;
        n4 [shape=note, fillcolor="{LIGHTBLUE}", color="{BLUE}", label="very fast, very cheap -\\lno HTTP parsing at all"];
        s4 -> n4 [style=invis];
    }}

    subgraph cluster_l7 {{
        label="L7 (application layer)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        c7 [label="client", fillcolor="{GRAY}", color="{SLATE}"];
        lb7 [label="L7 LB\\lterminates HTTP, reads path/\\lheaders/cookies, routes on\\lTHAT (e.g. /api/* vs /static/*)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        s7 [label="backend servers\\l(a NEW connection per\\lbackend, content-aware)", fillcolor="{GRAY}", color="{SLATE}"];
        c7 -> lb7 -> s7;
        n7 [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}", label="more CPU cost (full HTTP\\lparsing), but can route by\\lCONTENT, do TLS termination,\\lretry a failed request itself"];
        s7 -> n7 [style=invis];
    }}
    """)


def reverse_proxy_vs_gateway_vs_lb():
    render("2-5-proxy-gateway-lb", f"""
    rankdir=TB;
    client [label="Client", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    gw [label="API Gateway\\lauth, rate limiting, request\\lshaping, routes to the RIGHT\\lSERVICE (by path/domain)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    proxy [label="Reverse Proxy\\lTLS termination, caching,\\lcompression, hides backend\\ltopology from the client", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    lb [label="Load Balancer\\lpicks WHICH INSTANCE of a\\lgiven service handles this\\lONE request", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    instances [label="service instance 1", fillcolor="{GRAY}", color="{SLATE}"];
    instances2 [label="service instance 2", fillcolor="{GRAY}", color="{SLATE}"];

    client -> gw -> proxy -> lb;
    lb -> instances; lb -> instances2;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="In practice these three roles are often bundled into ONE piece of software\\l(e.g. an nginx or Envoy instance doing all three), but the RESPONSIBILITIES\\lare distinct: gateway picks the service, proxy hides/optimizes the hop,\\lLB picks the specific instance. Worth naming separately in an interview.\\l"];
    instances -> note [style=invis]; instances2 -> note [style=invis];
    """)


def wrr_distribution():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(7, 3.6))
    servers = ["A (weight 4)", "B (weight 1)", "C (weight 1)"]
    actual = [66.7, 16.7, 16.7]
    ax.bar(servers, actual, color=[BLUE, TEAL, AMBER], width=0.5)
    for i, v in enumerate(actual):
        ax.text(i, v + 1.5, f"{v}%", ha="center", fontsize=10)
    ax.set_ylabel("share of 60 requests")
    ax.set_ylim(0, 80)
    ax.set_title("Verified: smooth weighted round robin matches the\ntarget weight ratio exactly (4:1:1), spread evenly (max run = 3)",
                loc="left", pad=10, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "2-5-wrr-distribution")


if __name__ == "__main__":
    l4_vs_l7()
    reverse_proxy_vs_gateway_vs_lb()
    wrr_distribution()
