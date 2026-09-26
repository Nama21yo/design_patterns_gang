"""Diagrams for note 3.9 - Object/blob storage and distributed file systems."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def object_storage_model():
    render("3-9-object-storage-model", f"""
    rankdir=LR;
    bucket [label="Bucket: my-app-bucket\\l(a flat namespace,\\lglobally unique name)", fillcolor="{INK}", fontcolor=white, color="{INK}"];

    k1 [label="Key:\\l'users/42/avatar.png'", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    k2 [label="Key:\\l'users/42/resume.pdf'", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    k3 [label="Key:\\l'users/7/avatar.png'", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    bucket -> k1; bucket -> k2; bucket -> k3;

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="There is no real 'users/42/' directory - that's a single string\\lkey with slashes in it. Listing with prefix='users/' and\\ldelimiter='/' makes the API group keys by their next '/' and\\lLOOK like folders (verified below) - a UI convenience over a\\lflat key-value space, not an actual filesystem tree underneath.\\l"];
    k1 -> note [style=invis];
    """)


def stateless_app_s3():
    render("3-9-stateless-app-s3", f"""
    rankdir=TB;

    subgraph cluster_before {{
        label="Before: files on local disk";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        b1 [label="App server 1\\l+ local files", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        b2 [label="App server 2\\l+ DIFFERENT local files", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        bnote [shape=note, fillcolor="{RED}", fontcolor=white, color="{RED}",
              label="a request MUST land on the server that has the file -\\lsticky routing, no free horizontal scaling, and losing\\lthat one disk loses that data for good\\l"];
        b1 -> bnote [style=invis];
    }}

    subgraph cluster_after {{
        label="After: stateless app + object storage";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        a1 [label="App server 1\\l(no local file state)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        a2 [label="App server 2\\l(no local file state)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        s3 [label="Object storage\\l(S3 / etc.)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        a1 -> s3; a2 -> s3;
        anote [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
              label="ANY app server can serve ANY request - route anywhere,\\lscale horizontally, replace a dead instance with zero data loss\\l"];
        s3 -> anote [style=invis];
    }}
    """)


def erasure_coding_vs_replication():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(9, 3.6))
    labels = ["3x replication\n(tolerates 2 node losses)", "Reed-Solomon 4+2\n(tolerates 2 node losses)"]
    overhead = [3.0, 1.5]
    colors = [BLUE, TEAL]
    ax.barh(labels, overhead, color=colors, height=0.5)
    for i, v in enumerate(overhead):
        ax.text(v + 0.05, i, f"{v}x storage", va="center", fontsize=10)
    ax.set_xlim(0, 3.8)
    ax.set_xlabel("storage overhead (multiple of raw data size)")
    ax.set_title("Same durability (survive 2 failures), very different cost",
                 loc="left", pad=12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "3-9-erasure-coding-vs-replication")


def metadata_service_scaling():
    render("3-9-metadata-service-scaling", f"""
    rankdir=LR;

    subgraph cluster_gfs {{
        label="GFS (3.1): one master";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        gm [label="Single master\\l(all metadata)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
        gc [label="Chunkservers", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        gm -> gc;
        gnote [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
              label="fine for a few thousand large files -\\lmetadata volume stays small\\l"];
        gm -> gnote [style=invis];
    }}

    subgraph cluster_s3 {{
        label="S3-scale: metadata is ITSELF sharded";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        m1 [label="Metadata shard 1\\l(hash of key range)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        m2 [label="Metadata shard 2", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        m3 [label="Metadata shard N", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        snote [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
              label="trillions of objects -> one master's memory/throughput isn't\\lenough. Partition metadata the same way 3.4 partitions any\\lother huge key space, replicate each shard (3.5) for its own\\lavailability - a distributed system to run a distributed system.\\l"];
        m1 -> snote [style=invis];
    }}
    """)


def blob_vs_database():
    render("3-9-blob-vs-database", f"""
    rankdir=TB;
    q [label="Where does this data go?", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    q1 [label="Large (>1MB), mostly\\limmutable, fetched whole,\\lno need to query its contents?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    blob [label="Blob storage\\l(images, video, backups,\\llogs, model weights)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    db [label="Database\\l(+ store a pointer/key\\lto the blob, if any)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    q -> q1;
    q1 -> blob [label="  yes"];
    q1 -> db [label="  no - needs queries,\\l  transactions, frequent\\l  small updates, or is small"];
    """)


if __name__ == "__main__":
    object_storage_model()
    stateless_app_s3()
    erasure_coding_vs_replication()
    metadata_service_scaling()
    blob_vs_database()
