"""Diagrams for note 2.3 - Real-time: polling, SSE, WebSockets, pub/sub over the wire."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def short_vs_long_polling():
    render("2-3-short-vs-long-polling", f"""
    rankdir=TB;

    subgraph cluster_short {{
        label="Short polling";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        s1 [label="client asks 'anything new?'\\levery N seconds", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        s2 [label="server answers immediately\\l(usually: 'no, nothing yet')", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        s1 -> s2 -> s1 [label="  wait N seconds"];
        sn [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}", label="latency floor = N (an update can\\lsit unseen for up to N seconds);\\lmost requests answer 'nothing new'"];
        s2 -> sn [style=invis];
    }}

    subgraph cluster_long {{
        label="Long polling";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        l1 [label="client asks 'anything new?'", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        l2 [label="server HOLDS the request open\\l- doesn't answer until there IS\\lsomething new (or a timeout)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        l1 -> l2 -> l1 [label="  client immediately\\l  re-asks"];
        ln [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}", label="much lower latency (answers as\\lsoon as there's news), but a held-\\lopen request ties up a server\\lthread/connection the whole time"];
        l2 -> ln [style=invis];
    }}
    """)


def sse_diagram():
    render("2-3-sse", f"""
    rankdir=LR;
    client [label="Client\\lopens ONE HTTP request", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    conn [label="Connection stays open\\l(Content-Type: text/event-stream)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    server [label="Server pushes events\\lDOWN this same connection,\\lwhenever IT wants - no new\\lrequest needed per event", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    client -> conn -> server;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="ONE-DIRECTIONAL: server -> client only. Plain HTTP (no special upgrade,\\lworks through normal proxies), text-only, and browsers auto-reconnect a\\ldropped EventSource for free. The right fit whenever the client never\\lneeds to push anything back - live scores, a progress bar, a price ticker.\\l"];
    server -> note [style=invis];
    """)


def websocket_diagram():
    render("2-3-websocket", f"""
    rankdir=LR;
    handshake [label="HTTP Upgrade handshake\\l(Connection: Upgrade,\\lUpgrade: websocket)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    switched [label="101 Switching Protocols -\\lsame TCP connection, but no\\llonger speaking HTTP at all", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    frames [label="Lightweight binary/text FRAMES,\\lEITHER side can send at ANY\\ltime - true bidirectional,\\lfull-duplex channel", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    handshake -> switched -> frames;

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Why not just a persistent HTTP/1.1 connection instead? HTTP is\\lSTRUCTURALLY request/response, even kept alive - the server can't send\\lunsolicited data without the client already having an open request\\lwaiting (that's what long polling/SSE hack around). A WebSocket frame's\\loverhead is ~2-14 bytes; a full HTTP request/response is hundreds of\\lbytes of headers, repeated on every single message under polling.\\l"];
    frames -> note [style=invis];
    """)


def bytes_on_wire_verified():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(7, 3.8))
    labels = ["HTTP short polling\n(200 checks)", "WebSocket\n(200 messages,\n1 connection)"]
    bytes_used = [40400, 2000]
    ax.bar(labels, bytes_used, color=[RED, TEAL], width=0.5)
    for i, v in enumerate(bytes_used):
        ax.text(i, v + 800, f"{v:,} bytes", ha="center", fontsize=10)
    ax.set_ylabel("bytes on the wire")
    ax.set_title("Measured: same 200 updates delivered - polling's repeated\nHTTP headers cost 20x more bytes than WebSocket's tiny frames",
                loc="left", pad=10, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "2-3-bytes-on-wire-verified")


def pubsub_over_the_wire():
    render("2-3-pubsub-over-wire", f"""
    rankdir=LR;
    client1 [label="Client A\\l(subscribed to 'room:42')", fillcolor="{GRAY}", color="{SLATE}"];
    client2 [label="Client B\\l(subscribed to 'room:42')", fillcolor="{GRAY}", color="{SLATE}"];
    ws [label="WebSocket connections\\l(one per client, persistent)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    broker [label="Server-side pub/sub\\l(Redis Pub/Sub or Kafka - 5.5)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    client1 -> ws; client2 -> ws;
    ws -> broker [label="  subscribe('room:42')"];
    broker -> ws [label="  publish('room:42', msg)", style=dashed, color="{TEAL}"];
    ws -> client1 [style=dashed, color="{TEAL}"]; ws -> client2 [style=dashed, color="{TEAL}"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="'Pub/sub over the wire' is this exact bridge: a WebSocket (or SSE)\\lconnection is the CLIENT-facing transport, backed by a real pub/sub\\lsystem (5.5) doing the actual fan-out server-side. A chat room, a live\\ldocument's collaborators, a stock ticker's subscribers - all this shape.\\l"];
    client1 -> note [style=invis]; client2 -> note [style=invis];
    """)


if __name__ == "__main__":
    short_vs_long_polling()
    sse_diagram()
    websocket_diagram()
    bytes_on_wire_verified()
    pubsub_over_the_wire()
