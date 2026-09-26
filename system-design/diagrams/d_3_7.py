"""Diagrams for note 3.7 - Distributed transactions."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def two_phase_commit():
    render("3-7-two-phase-commit", f"""
    rankdir=TB;
    coord [label="Coordinator", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    pa [label="Participant A", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    pb [label="Participant B", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    p1 [label="Phase 1 - PREPARE\\lcoordinator asks everyone\\l'can you commit?'", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    p2 [label="Each participant locks its\\lrows, writes to its own log,\\lvotes YES or NO - but does\\lNOT commit yet", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    crash [label="*** if the coordinator crashes\\lHERE, after collecting votes,\\lbefore phase 2 ***", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    stuck [label="Every participant that voted\\lYES is stuck holding its locks\\l- can't commit (might need to\\labort) or abort (might need to\\lcommit) without hearing back", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    p3 [label="Phase 2 - COMMIT (if all YES)\\lor ABORT (if any NO)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    coord -> p1 -> p2 -> crash -> stuck;
    p2 -> p3 [style=dashed, label="  (happy path)", color="{SLATE}"];
    """)


def three_phase_commit():
    render("3-7-three-phase-commit", f"""
    rankdir=LR;
    p1 [label="1. CanCommit?\\l(just a check, no locks yet)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    p2 [label="2. PreCommit\\l(everyone now knows the\\loutcome will be commit,\\lbefore anyone commits)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    p3 [label="3. DoCommit", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    p1 -> p2 -> p3;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="The extra PreCommit round means a participant that hasn't heard\\lfrom the coordinator can safely time out and proceed on its own -\\lit already knows what everyone agreed to. Reduces (does not\\leliminate) blocking, at the cost of an extra network round trip\\lon every transaction. Rarely used in practice: still fails under a\\lnetwork PARTITION (not just a crash), and that extra latency is a\\lreal, permanent tax paid on every single transaction.\\l"];
    p3 -> note [style=invis];
    """)


def saga_pattern():
    render("3-7-saga-pattern", f"""
    rankdir=LR;
    order [label="1. Create order\\l(local tx, commits)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    pay [label="2. Charge payment\\l(local tx, commits)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    ship [label="3. Reserve shipping\\l(FAILS)", fillcolor="{RED}", fontcolor=white, color="{RED}"];

    order -> pay -> ship;

    comp2 [label="Compensate: refund payment\\l(a new, separate transaction -\\lnot a rollback)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    comp1 [label="Compensate: cancel order", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    ship -> comp2 -> comp1 [label="  run compensations\\l  in reverse order"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Orchestration: one saga-coordinator service explicitly calls\\leach step and its compensation (shown above). Choreography:\\lno central coordinator - each service reacts to the previous\\lservice's event and emits its own, compensations included.\\lOrchestration is easier to reason about; choreography has no\\lsingle point of control (or failure) but the overall flow is\\limplicit, spread across every service's event handlers.\\l"];
    comp1 -> note [style=invis];
    """)


def transactional_outbox():
    render("3-7-transactional-outbox", f"""
    rankdir=LR;
    app [label="App: one local\\lACID transaction", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    row [label="1. write the actual\\lrow (e.g. orders)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    outbox [label="2. write an outbox row\\l(same tx, same commit)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    relay [label="Separate relay process\\l(polls the outbox table,\\lor a CDC connector - 3.8)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    queue [label="Message queue /\\levent stream", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    app -> row; app -> outbox;
    outbox -> relay [label="  reads, then\\l  marks published"];
    relay -> queue;

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Solves 'write to the DB and publish to a queue, atomically' -\\lwithout a distributed transaction. Either both the row and the\\loutbox entry commit together (one local tx), or neither does.\\lThe relay might publish a message twice on retry (crash after\\lpublish, before marking it done) - which is exactly why the\\lconsumer on the other end needs to be idempotent.\\l"];
    queue -> note [style=invis];
    """)


if __name__ == "__main__":
    two_phase_commit()
    three_phase_commit()
    saga_pattern()
    transactional_outbox()
