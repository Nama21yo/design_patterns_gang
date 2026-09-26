"""Diagrams for note 3.6 - Consensus and coordination."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def orchestrator_recovery_problem():
    render("3-6-orchestrator-recovery-problem", f"""
    rankdir=TB;

    subgraph cluster_bad {{
        label="Single orchestrator: a new single point of failure";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        orch [label="Orchestrator\\l(watches the workers)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
        w1 [label="Worker 1", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        w2 [label="Worker 2", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        orch -> w1 [label="  health check"]; orch -> w2;
        q [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
          label="Worker 2 dies -> orchestrator restarts it. Good.\\lOrchestrator itself dies -> WHO restarts THAT?\\l"];
        orch -> q [style=invis];
    }}

    subgraph cluster_good {{
        label="Orchestrator cluster: leader-follower, all the way down";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        ol [label="Orchestrator LEADER\\l(watches the workers)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
        of1 [label="Orchestrator\\nFOLLOWER", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        of2 [label="Orchestrator\\nFOLLOWER", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        wa [label="Worker A", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        wb [label="Worker B", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

        ol -> wa [label="  health check"]; ol -> wb;
        of1 -> ol [label="  watch (heartbeat)", style=dashed, color="{SLATE}"];
        of2 -> ol [style=dashed, color="{SLATE}"];
        {{ rank=same; of1; of2 }}

        note2 [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
              label="Leader dies -> followers notice the missing heartbeat,\\lrun LEADER ELECTION among themselves, one becomes\\lthe new leader, resumes watching the workers.\\lNo single point of failure, anywhere in the chain.\\l"];
        ol -> note2 [style=invis];
    }}
    """)


def bully_algorithm():
    render("3-6-bully-algorithm", f"""
    rankdir=LR;
    n3 [label="Node 3\\lnotices no leader,\\lstarts an election", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    n4 [label="Node 4\\l(higher id, alive)\\l'I've got this'", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    n5 [label="Node 5\\l(highest id, DEAD)\\lno response", fillcolor="{GRAY}", color="{SLATE}"];
    win [label="Node 4 declares itself\\lleader (nobody HIGHER\\lthan it answered)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    n3 -> n4 [label="  election msg\\l  (to all higher ids)"];
    n3 -> n5 [style=dashed];
    n4 -> n5 [label="  election msg\\l  (to all higher ids)", style=dashed];
    n4 -> win [label="  timeout,\\l  no answer"];
    """)


def raft_election_timeline():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(9.5, 3.6))
    nodes = [1, 2, 3, 4, 5]
    timeouts = {1: 250, 2: 155, 3: 210, 4: 270, 5: 190}
    colors = {1: SLATE, 2: TEAL, 3: SLATE, 4: SLATE, 5: SLATE}
    for i, n in enumerate(nodes):
        y = len(nodes) - i
        ax.barh(y, timeouts[n], color=colors[n], height=0.5,
               alpha=1.0 if n == 2 else 0.35)
        ax.text(timeouts[n] + 4, y, f"{timeouts[n]} ms" + ("  <- fires first, becomes candidate" if n == 2 else ""),
               va="center", fontsize=9, color=INK)
        ax.text(-8, y, f"node {n}", va="center", ha="right", fontsize=9, color=SLATE)
    ax.set_xlim(-40, 340)
    ax.set_ylim(0.3, len(nodes) + 0.7)
    ax.set_xlabel("randomized election timeout (ms)")
    ax.set_yticks([])
    ax.set_title("Raft: whoever's randomized timeout fires first becomes\ncandidate and requests votes",
                 loc="left", pad=12)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "3-6-raft-election-timeline")


def raft_log_replication():
    render("3-6-raft-log-replication", f"""
    rankdir=LR;
    client [label="Client: write(x=5)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    leader [label="Leader\\lappends to its OWN log\\l(uncommitted)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    f1 [label="Follower 1\\lreplicates entry,\\lACKs", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    f2 [label="Follower 2\\lreplicates entry,\\lACKs", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    f3 [label="Follower 3\\l(slow/unreachable)", fillcolor="{GRAY}", color="{SLATE}"];
    commit [label="Majority (3 of 5,\\lincl. leader) has it\\l-> COMMITTED\\l-> apply + reply to client", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    client -> leader;
    leader -> f1; leader -> f2; leader -> f3;
    f1 -> commit; f2 -> commit;

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Only a majority needs to have it - the slow/unreachable\\lfollower catches up later by replaying the log. Same\\lidea as the quorum writes in 3.5's leaderless replication.\\l"];
    commit -> note [style=invis];
    """)


def paxos_roles():
    render("3-6-paxos-roles", f"""
    rankdir=LR;
    proposer [label="Proposer\\l'I propose value V\\lwith proposal number N'", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    a1 [label="Acceptor 1", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    a2 [label="Acceptor 2", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    a3 [label="Acceptor 3", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    learner [label="Learner\\llearns the value once\\la majority accepted it", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    proposer -> a1 [label="  prepare(N) / accept(N,V)", dir=both];
    proposer -> a2 [dir=both];
    proposer -> a3 [dir=both];
    a1 -> learner; a2 -> learner;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Two round trips per decision (prepare, then accept) and the\\lprotocol for handling competing proposers is notoriously\\lhard to follow - which is exactly the gap Raft was designed\\lto close: same guarantees, an explicit leader, one round trip\\lper entry in the common case, and a spec people can implement\\lcorrectly on the first try.\\l"];
    learner -> note [style=invis];
    """)


def coordination_service():
    render("3-6-coordination-service", f"""
    rankdir=LR;
    n1 [label="App instance 1", fillcolor="{GRAY}", color="{SLATE}"];
    n2 [label="App instance 2", fillcolor="{GRAY}", color="{SLATE}"];
    n3 [label="App instance 3", fillcolor="{GRAY}", color="{SLATE}"];

    zk [label="ZooKeeper / etcd\\l(itself a Raft/ZAB-\\lreplicated cluster)", fillcolor="{INK}", fontcolor=white, color="{INK}"];

    n1 -> zk [label="  try to create\\l  /leader (ephemeral)", dir=both];
    n2 -> zk [style=dashed, dir=both];
    n3 -> zk [style=dashed, dir=both];

    note [shape=note, fillcolor="{LIGHTAMBER}", color="{AMBER}",
         label="Whoever creates the ephemeral node first IS the leader.\\lIf that instance dies, its session ends and the node is\\lauto-deleted -> everyone watching gets notified -> next\\linstance races to create it again. Leader election, service\\ldiscovery, distributed locks and config storage all reduce\\lto 'a small piece of consensus-backed shared state with\\lnotifications on change' - which is what these systems sell.\\l"];
    zk -> note [style=invis];
    """)


if __name__ == "__main__":
    orchestrator_recovery_problem()
    bully_algorithm()
    raft_election_timeline()
    raft_log_replication()
    paxos_roles()
    coordination_service()
