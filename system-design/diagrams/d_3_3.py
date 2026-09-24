"""Diagrams for note 3.3 - Indexing."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def btree_structure():
    render("3-3-btree-structure", f"""
    rankdir=TB;
    root [label="root\\l[ 40 | 80 ]", fillcolor="{INK}", fontcolor=white, color="{INK}"];

    n1 [label="[ 10 | 25 ]", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    n2 [label="[ 55 | 65 ]", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    n3 [label="[ 90 | 95 ]", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    l1 [label="leaf: keys < 10\\l-> row pointers", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l2 [label="leaf: 10 <= key < 25\\l-> row pointers", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l3 [label="leaf: 25 <= key < 40\\l-> row pointers", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l4 [label="leaf: 55 <= key < 65\\l-> row pointers", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l5 [label="leaf: 65 <= key < 80\\l-> row pointers", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    l6 [label="leaf: key >= 95\\l-> row pointers", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    root -> n1; root -> n2; root -> n3;
    n1 -> l1; n1 -> l2; n1 -> l3;
    n2 -> l4; n2 -> l5;
    n3 -> l6;

    l1 -> l2 -> l3 -> l4 -> l5 -> l6 [style=dashed, color="{SLATE}", constraint=false,
                                     label="  leaf nodes linked -> cheap range scans"];
    """)


def clustered_vs_nonclustered():
    render("3-3-clustered-vs-nonclustered", f"""
    rankdir=LR;

    subgraph cluster_a {{
        label="Clustered index (usually the primary key)";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        idxA [label="index on id\\l(the sort order)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        rowsA [label="table rows, physically\\lstored IN id order\\l= the leaves ARE the table", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        idxA -> rowsA [label="  IS the data"];
    }}

    subgraph cluster_b {{
        label="Non-clustered (secondary) index";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        idxB [label="index on email\\l(a separate sorted\\lstructure)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        rowsB [label="table rows, stored in\\lsome OTHER physical order\\l(often clustered-index order)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        idxB -> rowsB [label="  pointer / row id\\l  (extra hop)"];
    }}
    """)


def maintenance_cost():
    plt = mpl()
    n_indexes = [0, 1, 2, 4]
    seconds = [1.281, 1.859, 2.407, 5.510]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    colors = [TEAL, BLUE, AMBER, RED]
    ax.bar([str(n) for n in n_indexes], seconds, color=colors, width=0.55)
    for i, s in enumerate(seconds):
        ax.text(i, s + 0.1, f"{s:.2f}s", ha="center", fontsize=10, color=INK)
    ax.set_xlabel("number of secondary indexes on the table")
    ax.set_ylabel("time to INSERT 300,000 rows")
    ax.set_title("Every index is more work on every write (measured, Postgres 16)",
                 loc="left", pad=12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "3-3-maintenance-cost")


def inverted_index():
    render("3-3-inverted-index", f"""
    rankdir=LR;
    node [shape=box];

    docs [label="Documents\\l\\ldoc 1: 'stock market rally'\\ldoc 2: 'market update today'\\ldoc 3: 'stock split announced'", fillcolor="{GRAY}", color="{SLATE}"];

    idx [label="Inverted index\\l(term -> posting list)\\l\\l'stock'  -> [doc1, doc3]\\l'market' -> [doc1, doc2]\\l'rally'  -> [doc1]\\l'today'  -> [doc2]\\l'split'  -> [doc3]", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    q [label="Query: 'stock' AND 'market'\\l-> intersect [doc1,doc3] and [doc1,doc2]\\l-> [doc1]", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    docs -> idx [label="  build\\l  (tokenize)"];
    idx -> q [label="  lookup +\\l  intersect posting lists"];
    """)


if __name__ == "__main__":
    btree_structure()
    clustered_vs_nonclustered()
    maintenance_cost()
    inverted_index()
