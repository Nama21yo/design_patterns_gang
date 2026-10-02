"""Diagrams for note 1.5 - Consistency models."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def consistency_spectrum():
    render("1-5-consistency-spectrum", f"""
    rankdir=LR;
    strong [label="STRONG\\levery read sees the\\lLATEST write, globally\\l(as if one copy existed)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    causal [label="CAUSAL\\lcausally-related ops seen\\lin order by everyone;\\lCONCURRENT ops may differ", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    eventual [label="EVENTUAL\\lno new writes -> replicas\\lconverge EVENTUALLY (no\\lbound on how long)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    strong -> causal -> eventual [label="  weaker guarantee,\\l  better availability/latency\\l  (1.4's PACELC trade)"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="READ-YOUR-WRITES and MONOTONIC READS (below) are 'session guarantees' -\\lthey don't sit ON this spectrum, they're ADDITIONAL per-client promises a\\lsystem can layer on top of an otherwise-eventual model to make it feel\\lmuch stronger from any ONE client's point of view, without paying strong\\lconsistency's full global cost.\\l"];
    eventual -> note [style=invis];
    """)


def read_your_writes_verified():
    render("1-5-read-your-writes-verified", f"""
    rankdir=LR;
    write [label="Client writes v3\\l(e.g. new profile pic)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    naive [label="naive read, random\\lreplica -> gets v1\\l(STALE - doesn't see\\lown write)", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    fixed [label="version-aware read,\\lrequires >= v3 -> routed\\lto leader -> gets v3\\l(CORRECT)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    write -> naive [label="  VIOLATION"];
    write -> fixed [label="  FIXED"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Verified: a naive read from a lagging replica returned the client's OWN\\lwrite 2 versions stale. Requiring the read to be routed to a replica at\\lor past the client's own last-written version fixed it exactly.\\l"];
    fixed -> note [style=invis];
    """)


def monotonic_reads_verified():
    render("1-5-monotonic-reads-verified", f"""
    rankdir=LR;
    r1 [label="Read 1: from a\\lless-lagged replica -> v2", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    r2naive [label="Read 2: from a MORE-\\llagged replica -> v1\\l(time went BACKWARDS)", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    r2fixed [label="Read 2: STICKY to the\\lSAME replica as read 1\\l-> v2 (never regresses)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    r1 -> r2naive [label="  VIOLATION"];
    r1 -> r2fixed [label="  FIXED"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Verified: reading from a different, more-lagged replica on the second\\lcall showed an OLDER version than the first read saw. Sticky routing\\l(same client always hits the same replica) fixed it exactly.\\l"];
    r2fixed -> note [style=invis];
    """)


def causal_verified():
    render("1-5-causal-verified", f"""
    rankdir=LR;
    events [label="post_1 (a question) and\\lreply_1 (depends on post_1),\\lreply_1's message happens\\lto ARRIVE FIRST", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    naive [label="naive delivery: shows\\lwhatever arrived first ->\\lreply shown BEFORE\\lthe question", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    fixed [label="causal delivery: reply_1\\lis BUFFERED until post_1\\lhas been delivered first", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    events -> naive [label="  VIOLATION"];
    events -> fixed [label="  FIXED"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Verified: naive delivery showed the reply before its own question.\\lBuffering a dependent event until its dependency has already been\\ldelivered fixed the ordering exactly - this is the real mechanism\\lbehind vector clocks / causal metadata in production systems.\\l"];
    fixed -> note [style=invis];
    """)


if __name__ == "__main__":
    consistency_spectrum()
    read_your_writes_verified()
    monotonic_reads_verified()
    causal_verified()
