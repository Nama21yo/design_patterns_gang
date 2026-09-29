"""Diagrams for note 2.1 - Network stack for backend: TCP/UDP, HTTP/1.1/2/3, TLS."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def tcp_handshake_teardown():
    render("2-1-tcp-handshake-teardown", f"""
    rankdir=LR;

    subgraph cluster_setup {{
        label="Setup: 3-way handshake";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        h1 [label="Client -> Server\\lSYN (seq=x)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        h2 [label="Server -> Client\\lSYN-ACK (seq=y, ack=x+1)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        h3 [label="Client -> Server\\lACK (ack=y+1)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        h1 -> h2 -> h3;
    }}

    subgraph cluster_teardown {{
        label="Teardown: 4-way (each side closes ITS OWN direction)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        t1 [label="Client -> Server\\lFIN (client done sending)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        t2 [label="Server -> Client\\lACK", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        t3 [label="Server -> Client\\lFIN (server done sending)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        t4 [label="Client -> Server\\lACK", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        t1 -> t2 -> t3 -> t4;
    }}

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Handshake: BOTH sides must exchange sequence numbers before either can send\\ldata (full-duplex, so each direction needs its own SYN+ACK). Teardown is\\lFOUR messages because TCP is full-duplex - a FIN only closes ONE direction;\\lthe connection isn't fully closed until BOTH sides have sent their own FIN.\\l(Sometimes seen as 3 packets if the server's ACK+FIN are combined into one.)\\l"];
    h3 -> note [style=invis];
    t4 -> note [style=invis];
    """)


def tcp_reliability_mechanisms():
    render("2-1-tcp-reliability", f"""
    rankdir=TB;
    seq [label="Sequence numbers + ACKs\\levery byte is numbered; receiver\\lACKs what it has, sender knows\\lwhat still needs (re)sending", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    window [label="Sliding window (flow control)\\lreceiver advertises how much\\lbuffer it has -> sender never\\loverwhelms a slow receiver", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    congestion [label="Congestion control\\lslow start -> additive increase /\\lmultiplicative decrease (AIMD) on\\lloss -> sender never overwhelms\\lthe NETWORK either", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    retransmit [label="Retransmission\\lunacked data after a timeout (or\\l3 duplicate ACKs) is resent -\\lloss is invisible to the app layer", fillcolor="{GRAY}", color="{SLATE}"];

    seq -> window -> congestion -> retransmit;

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Verified live: sent 5,000 messages into a receive buffer sized for only\\l4KB - TCP delivered ALL 5,000, in order, on EVERY run (flow control\\lblocked the sender rather than dropping data). The same test over UDP\\ldropped SOME messages on every single run - the count varies with OS\\lscheduling (7 to 2,708 dropped across 6 runs), but it never once hit zero.\\l"];
    retransmit -> note [style=invis];
    """)


def tcp_vs_udp_verified():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8, 3.8))
    runs = ["run 1", "run 2", "run 3", "run 4", "run 5", "run 6\n(outlier)"]
    tcp_dropped = [0, 0, 0, 0, 0, 0]
    udp_dropped = [40, 7, 15, 10, 46, 2708]
    x = range(len(runs))
    width = 0.35
    ax.bar([i - width/2 for i in x], tcp_dropped, width, label="TCP dropped", color=TEAL)
    ax.bar([i + width/2 for i in x], udp_dropped, width, label="UDP dropped", color=RED)
    for i, v in enumerate(udp_dropped):
        ax.text(i + width/2, v + 40, str(v), ha="center", fontsize=8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(runs, fontsize=8.5)
    ax.set_ylabel("messages dropped (out of 5,000 sent)")
    ax.set_title("Measured across 6 runs: TCP dropped 0 every time - UDP\ndropped SOME every time, but the amount is highly variable",
                loc="left", pad=10, fontsize=10.5)
    ax.legend(frameon=False, fontsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "2-1-tcp-vs-udp-verified")


def http_versions():
    render("2-1-http-versions", f"""
    rankdir=TB;

    subgraph cluster_h1 {{
        label="HTTP/1.1 - one request in flight per TCP connection";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        h1a [label="TCP conn 1: request A"]; h1b [label="TCP conn 2: request B"]; h1c [label="TCP conn 1 (reused,\\lkeep-alive): request C"];
        n1 [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}", label="head-of-line blocking: request C must\\lwait for request A to fully finish on\\lthat same connection. Browsers open\\lmultiple parallel connections to cope."];
        h1c -> n1 [style=invis];
    }}

    subgraph cluster_h2 {{
        label="HTTP/2 - many MULTIPLEXED streams, ONE TCP connection";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        h2 [label="ONE TCP connection\\lstream 1, 3, 5... interleaved,\\lbinary framing, header compression (HPACK)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        n2 [shape=note, fillcolor="{LIGHTBLUE}", color="{BLUE}", label="fixes HTTP-level HOL blocking, but ONE\\llost TCP packet still stalls EVERY\\lstream (TCP itself is still ordered)"];
        h2 -> n2 [style=invis];
    }}

    subgraph cluster_h3 {{
        label="HTTP/3 - multiplexed streams over QUIC (UDP-based)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        h3 [label="QUIC (built on UDP)\\leach stream has INDEPENDENT loss\\lrecovery - no shared TCP ordering", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        n3 [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}", label="fixes TRANSPORT-level HOL blocking too\\l- one stream's lost packet no longer\\lstalls the others. Faster handshake\\l(TLS 1.3 folded into QUIC's own setup)."];
        h3 -> n3 [style=invis];
    }}
    """)


def http11_keepalive_verified():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(7, 3.6))
    labels = ["new connection\nper request", "reused keep-alive\nconnection"]
    per_req = [0.599, 0.182]
    ax.bar(labels, per_req, color=[RED, TEAL], width=0.5)
    for i, v in enumerate(per_req):
        ax.text(i, v + 0.02, f"{v:.3f}ms", ha="center", fontsize=10)
    ax.set_ylabel("ms per request (loopback)")
    ax.set_title("Measured: 200 real HTTP/1.1 requests, over loopback -\nkeep-alive was 3.3x faster, purely from skipping the handshake",
                loc="left", pad=10, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "2-1-http11-keepalive-verified")


def tls_handshake():
    render("2-1-tls-handshake", f"""
    rankdir=LR;
    client [label="Client"]; server [label="Server"];
    client -> server [label="  ClientHello\\l  (supported TLS versions,\\l  cipher suites)"];
    server -> client [label="  ServerHello + certificate\\l  (server's public key, signed\\l  by a trusted CA)"];
    client -> server [label="  verify cert -> derive a\\l  shared session key\\l  (key exchange)"];
    both [label="Both sides now share a SYMMETRIC\\lsession key - all further traffic is\\lencrypted with it (much faster than\\lasymmetric crypto for bulk data)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    client -> both [style=invis]; server -> both [style=invis];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="TLS 1.3 cut this to ONE round trip (down from 2 in TLS 1.2) before\\lapplication data can flow. This handshake happens ON TOP of TCP's own\\l3-way handshake - which is exactly the extra round trip HTTP/3's QUIC\\lfolds away by doing its transport AND TLS handshake together.\\l"];
    both -> note [style=invis];
    """)


if __name__ == "__main__":
    tcp_handshake_teardown()
    tcp_reliability_mechanisms()
    tcp_vs_udp_verified()
    http_versions()
    http11_keepalive_verified()
    tls_handshake()
