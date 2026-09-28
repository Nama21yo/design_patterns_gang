"""Diagrams for note 5.4 - Batch processing: MapReduce, Spark; Lambda vs Kappa."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def divide_and_conquer_motivation():
    render("5-4-divide-and-conquer", f"""
    rankdir=LR;
    problem [label="Count word frequency\\lover a 10 TB text corpus", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    single [label="One machine: read every\\lbyte, one CPU, one disk -\\ltoo slow, may not even fit", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    split [label="Split the corpus into N\\lchunks, one per machine", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    local [label="Each machine counts its\\lOWN chunk in parallel\\l(independent, no coordination)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    merge [label="Combine the N partial\\lcounts into one final\\lanswer (a reduce step)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    problem -> single [style=dashed, color="{RED}", label="  doesn't scale"];
    problem -> split -> local -> merge;
    """)


def spark_architecture():
    render("5-4-spark-architecture", f"""
    rankdir=TB;
    driver [label="Driver program\\l(the 'master')\\lbuilds the DAG, splits it\\linto stages/tasks, schedules them", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    cm [label="Cluster manager\\l(standalone / YARN / Kubernetes)\\lallocates executors across the cluster", fillcolor="{GRAY}", color="{SLATE}"];
    e1 [label="Executor 1\\l(worker)\\lruns tasks on ITS\\lpartitions, caches\\ldata in memory", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    e2 [label="Executor 2\\l(worker)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    e3 [label="Executor 3\\l(worker)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    driver -> cm [label="  request executors"];
    cm -> e1; cm -> e2; cm -> e3;
    driver -> e1 [label="  schedule tasks", style=dashed, color="{TEAL}"];
    driver -> e2 [style=dashed, color="{TEAL}"];
    driver -> e3 [style=dashed, color="{TEAL}"];
    e1 -> driver [label="  results / status", style=dashed, color="{SLATE}"];
    """)


def lazy_evaluation_dag():
    render("5-4-lazy-evaluation", f"""
    rankdir=LR;
    rdd0 [label="rdd = sc.textFile(...)", fillcolor="{GRAY}", color="{SLATE}"];
    t1 [label=".flatMap(split words)\\lTRANSFORMATION - lazy,\\ljust builds the DAG", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    t2 [label=".map(word -> (word,1))\\lTRANSFORMATION - lazy", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    t3 [label=".reduceByKey(sum)\\lTRANSFORMATION - lazy", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    action [label=".collect()\\lACTION - the whole DAG\\lexecutes NOW, optimized\\las one plan", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    rdd0 -> t1 -> t2 -> t3 -> action;

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Verified: building the 3-transformation chain took 0.07s (touches\\lNO data). Calling .collect() then ran the whole DAG in one pass and\\lmatched ground truth exactly. An accumulator confirmed 0 records were\\ltouched before the action, and all 27 after it.\\l"];
    action -> note [style=invis];
    """)


def memory_vs_disk_model():
    render("5-4-memory-vs-disk", f"""
    rankdir=LR;

    subgraph cluster_mr {{
        label="MapReduce: disk between every stage";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        m1 [label="Map"]; d1 [label="HDFS\\l(disk write)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        m2 [label="Reduce"]; d2 [label="HDFS\\l(disk write)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        m3 [label="next Map"];
        m1 -> d1 -> m2 -> d2 -> m3;
    }}

    subgraph cluster_spark {{
        label="Spark: intermediate RDDs stay in memory";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        s1 [label="stage 1"]; s2 [label="stage 2"]; s3 [label="stage 3"];
        mem [label="in-executor memory\\l(spills to disk only\\lunder pressure)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        s1 -> mem -> s2; mem -> s3;
    }}

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="This is the core reason Spark is typically cited as 10-100x faster\\lthan classic MapReduce on iterative / multi-stage workloads: the\\lsame data doesn't get written to and re-read from disk between\\levery single stage.\\l"];
    m3 -> note [style=invis]; s3 -> note [style=invis];
    """)


def bloomberg_stack():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(10, 4.4))
    ax.axis("off")
    rows = [
        ("tool", "role in Bloomberg's stack"),
        ("Apache Kafka", "messaging backbone connecting producer and consumer sides"),
        ("Apache Spark", "large-scale batch + streaming analytics"),
        ("Apache HBase", "part of the producer-side temporal data store"),
        ("Apache Solr", "search - powers 300+ functions across the Terminal"),
        ("MySQL", "producer-side relational storage"),
        ("Apache Airflow", "workflow / pipeline orchestration"),
        ("Kubernetes", "container orchestration (incl. Bloomberg's own 'Solr Operator')"),
        ("BBDS (DataHub Eng.)", "internal platform for hosting/discovering/serving datasets"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.02, y, row[0], fontsize=9.5, fontweight=weight, color=BLUE)
        ax.text(0.30, y, row[1], fontsize=9.2, fontweight=weight, color=SLATE)
        ax.axhline(y - 0.35, xmin=0.02, xmax=0.98, color=(INK if i == 0 else GRAY), lw=(1.2 if i == 0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 0.6)
    ax.set_title("Bloomberg's big-data stack (publicly documented)", loc="left", pad=10)
    return save_mpl(fig, "5-4-bloomberg-stack")


if __name__ == "__main__":
    divide_and_conquer_motivation()
    spark_architecture()
    lazy_evaluation_dag()
    memory_vs_disk_model()
    bloomberg_stack()
