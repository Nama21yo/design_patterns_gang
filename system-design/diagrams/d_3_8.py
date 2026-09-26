"""Diagrams for note 3.8 - CDC, event sourcing, CQRS."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def cdc_architecture():
    render("3-8-cdc-architecture", f"""
    rankdir=LR;
    app [label="App writes\\n(ordinary INSERT/\\lUPDATE/DELETE -\\lno CDC-aware code)", fillcolor="{GRAY}", color="{SLATE}"];
    db [label="Database\\l+ its WAL / binlog\\l(3.1, 3.5)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    connector [label="CDC connector\\l(Debezium, or a\\llogical replication\\lslot directly)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    stream [label="Change stream\\l(Kafka topic:\\lone event per row change)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    c1 [label="Consumer:\\lsearch index", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    c2 [label="Consumer:\\lcache invalidation", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    c3 [label="Consumer:\\lanalytics warehouse", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    app -> db -> connector -> stream;
    stream -> c1; stream -> c2; stream -> c3;

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="The connector reads the database's own commit log - the exact\\lmechanism already used for physical replication in 3.5, just\\ldecoded into logical row-level events instead of raw WAL bytes.\\lNo dual-write, no outbox table needed: every committed change\\lis captured by construction, because nothing can commit without\\lgoing through the WAL first.\\l"];
    stream -> note [style=invis];
    """)


def event_sourcing():
    render("3-8-event-sourcing", f"""
    rankdir=LR;
    e1 [label="AccountOpened\\l(balance=0)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    e2 [label="Deposited\\l(+100)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    e3 [label="Withdrew\\l(-30)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    e4 [label="Deposited\\l(+50)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    e1 -> e2 -> e3 -> e4 [label="  append-only log\\l  (the source of truth)"];

    fold [label="Current state = fold(events)\\l0 + 100 - 30 + 50 = 120", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    e4 -> fold [label="  replay / project"];

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="The events are the source of truth - the 'current balance' is\\lderived, not stored, and can be recomputed at any point in\\lhistory. Gives a full audit trail and time-travel for free, at\\lthe cost of replay time (mitigated with periodic snapshots) and\\lthe need to keep old event schemas readable forever.\\l"];
    fold -> note [style=invis];
    """)


def cqrs():
    render("3-8-cqrs", f"""
    rankdir=LR;
    write_client [label="Write request\\l(command)", fillcolor="{GRAY}", color="{SLATE}"];
    write_model [label="Write model\\l(normalized, optimized\\lfor correctness)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    events [label="Change stream\\l(CDC / event log)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    read_model [label="Read model(s)\\l(denormalized materialized\\lviews, one shape per\\lquery pattern)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    read_client [label="Read request\\l(query)", fillcolor="{GRAY}", color="{SLATE}"];

    write_client -> write_model -> events -> read_model -> read_client;

    note [shape=note, fillcolor="{LIGHTBLUE}", color="{BLUE}",
         label="Writes and reads go through COMPLETELY separate models. The\\lwrite side stays simple and correct; each read model is shaped\\lexactly for the query that hits it (9.5's rollup tables are an\\linstance of this). The cost: read models lag the write model by\\lhowever long the pipeline takes - eventual consistency between\\lwrite and read, by design, not by accident.\\l"];
    read_model -> note [style=invis];
    """)


if __name__ == "__main__":
    cdc_architecture()
    event_sourcing()
    cqrs()
