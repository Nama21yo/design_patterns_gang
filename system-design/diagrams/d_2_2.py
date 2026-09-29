"""Diagrams for note 2.2 - REST, RPC, gRPC, GraphQL."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def four_styles():
    render("2-2-four-styles", f"""
    rankdir=TB;

    rest [label="REST\\lresource-oriented (nouns)\\lGET /orders/42\\lHTTP verbs = CRUD", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    rpc [label="RPC (generic)\\lprocedure-oriented (verbs)\\lPOST /refundOrder\\lcalls a named action", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    grpc [label="gRPC\\lRPC + Protobuf schema +\\lHTTP/2 - binary, typed,\\lstreaming-capable", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    graphql [label="GraphQL\\lONE endpoint, client specifies\\lthe EXACT shape it wants\\lin a single query", fillcolor="{GRAY}", color="{SLATE}"];

    {{ rank=same; rest; rpc; grpc; graphql }}
    """)


def grpc_on_http2():
    render("2-2-grpc-http2", f"""
    rankdir=LR;
    proto [label=".proto schema\\l(shared contract)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    codegen [label="codegen: typed client\\l+ server stubs, many\\llanguages", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    http2 [label="runs on HTTP/2 (2.1)\\l- gets multiplexing,\\lheader compression FOR FREE", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    modes [label="4 call shapes: unary,\\lserver-streaming, client-\\lstreaming, bidirectional -\\lall using HTTP/2 STREAMS directly", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    proto -> codegen -> http2 -> modes;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Best fit: internal service-to-service calls where both ends share the\\l.proto schema and performance matters. Weaker fit: public browser-facing\\lAPIs - browsers can't speak raw gRPC without a grpc-web proxy, and it's\\lharder to explore ad hoc than curl + JSON.\\l"];
    modes -> note [style=invis];
    """)


def rest_vs_graphql_verified():
    plt = mpl()
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.8))
    labels = ["REST\n(naive)", "GraphQL\n(1 query)"]

    rt = [4, 1]
    axes[0].bar(labels, rt, color=[RED, TEAL], width=0.5)
    for i, v in enumerate(rt):
        axes[0].text(i, v + 0.08, str(v), ha="center", fontsize=10)
    axes[0].set_ylabel("round trips")
    axes[0].set_title("round trips for the SAME view", fontsize=10)
    for s in ("top", "right"):
        axes[0].spines[s].set_visible(False)

    by = [681, 157]
    axes[1].bar(labels, by, color=[RED, TEAL], width=0.5)
    for i, v in enumerate(by):
        axes[1].text(i, v + 30, f"{v:,}", ha="center", fontsize=10)
    axes[1].set_ylabel("bytes transferred")
    axes[1].set_title("bytes for the SAME view", fontsize=10)
    for s in ("top", "right"):
        axes[1].spines[s].set_visible(False)

    fig.suptitle("Measured: fetching 'user + 2 recent posts + comment counts' -\nREST's generic endpoints vs. one precisely-shaped GraphQL query", fontsize=10.5, y=1.04)
    return save_mpl(fig, "2-2-rest-vs-graphql-verified")


def binary_vs_json_verified():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(7, 3.8))
    labels = ["JSON", "binary\n(struct-packed)"]
    sizes = [78, 24]
    ax.bar(labels, sizes, color=[RED, TEAL], width=0.5)
    for i, v in enumerate(sizes):
        ax.text(i, v + 2, f"{v} bytes", ha="center", fontsize=10)
    ax.set_ylabel("bytes per message")
    ax.set_title("Measured: a stock-quote message, JSON vs. hand-packed binary -\nfield NAMES never appear in the binary form (a shared schema knows them)",
                loc="left", pad=10, fontsize=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "2-2-binary-vs-json-verified")


def when_to_use():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis("off")
    rows = [
        ("style", "best fit", "watch out for"),
        ("REST", "public APIs, simple CRUD, HTTP caching\nmatters (4.4)", "over/under-fetching, N+1 round trips\nfor nested/related data"),
        ("RPC (generic)", "action-oriented ops that don't map\nto CRUD (refund, send, approve)", "tight coupling to exact method\nsignatures, no uniform interface"),
        ("gRPC", "internal service-to-service calls,\nperformance-sensitive, streaming needs", "not browser-native, needs shared\n.proto schema on both ends"),
        ("GraphQL", "clients with very different data needs\n(web/mobile), avoiding over-fetching", "resolver N+1 problem, hard to cache\nvia HTTP, needs query depth limits"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.01, y, row[0], fontsize=9.3, fontweight=weight, color=BLUE)
        ax.text(0.16, y, row[1], fontsize=8.6, fontweight=weight, color=INK)
        ax.text(0.58, y, row[2], fontsize=8.4, fontweight=weight, color=SLATE)
        ax.axhline(y - 0.42, xmin=0.01, xmax=0.99, color=(INK if i == 0 else GRAY), lw=(1.2 if i == 0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 0.8)
    ax.set_title("Choosing among API styles", loc="left", pad=10)
    return save_mpl(fig, "2-2-when-to-use")


if __name__ == "__main__":
    four_styles()
    grpc_on_http2()
    rest_vs_graphql_verified()
    binary_vs_json_verified()
    when_to_use()
