"""Diagrams for note 1.7 - Distributed system models and the fallacies."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def synchrony_models():
    render("1-7-synchrony-models", f"""
    rankdir=LR;
    sync [label="SYNCHRONOUS\\lbounded message delay AND\\lbounded processing time -\\la timeout can RELIABLY\\ldetect failure", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    async [label="ASYNCHRONOUS\\lNO bounds at all - can't\\ltell 'dead' from 'slow'.\\lThis is where FLP's\\limpossibility result (3.6)\\llives", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    partial [label="PARTIALLY SYNCHRONOUS\\lbounds EXIST but are unknown,\\lor only hold EVENTUALLY -\\lwhat real systems actually\\lassume; timeouts work\\l'well enough' in practice", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    sync -> async [style=dashed, color="{SLATE}", label="  weaken the model"];
    async -> partial [style=dashed, color="{SLATE}", label="  what's actually\\l  true in production"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Real networks are neither perfectly synchronous nor hopelessly\\lasynchronous - partial synchrony is the honest middle ground, and every\\ltimeout-based failure detector (2.4, 3.6) is an engineering answer built\\lfor exactly this model, not a 'solution' to FLP.\\l"];
    partial -> note [style=invis];
    """)


def failure_mode_spectrum():
    render("1-7-failure-modes", f"""
    rankdir=LR;
    cs [label="CRASH-STOP\\lfails once, NEVER comes\\lback. Simplest to model.", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    cr [label="CRASH-RECOVERY\\lfails, can RESTART -\\lmay have lost volatile\\lstate (3.1's WAL exists\\lfor exactly this)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    om [label="OMISSION\\lsome messages sent/received\\lare just DROPPED - otherwise\\lbehaves correctly", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    bz [label="BYZANTINE\\lARBITRARY behavior - lies,\\lsends different things to\\ldifferent peers, even\\lmaliciously. Hardest + most\\lexpensive to tolerate.", fillcolor="{RED}", fontcolor=white, color="{RED}"];

    cs -> cr -> om -> bz [label="  increasingly expensive\\l  to tolerate"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Raft and Paxos (3.6) assume crash-stop/crash-recovery ONLY - they are\\lNOT Byzantine fault tolerant. Tolerating Byzantine failures needs a\\lcompletely different class of protocol (PBFT, blockchain consensus) and\\lmany more nodes for the same fault count, proven below.\\l"];
    bz -> note [style=invis];
    """)


def byzantine_threshold_verified():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    labels = ["n=3, f=1\n(3 >= 3(1)+1? NO)", "n=4, f=1\n(4 >= 3(1)+1? YES)"]
    agreed = [0, 1]
    colors = [RED, TEAL]
    ax.bar(labels, agreed, color=colors, width=0.5)
    for i, v in enumerate(agreed):
        if v == 0:
            ax.text(i, 0.05, "DISAGREE", ha="center", fontsize=11, color=RED, fontweight="bold")
        else:
            ax.text(i, 0.05, "AGREE", ha="center", fontsize=11, color="white", fontweight="bold")
    ax.set_ylim(0, 1.3)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["honest nodes\nDISAGREE", "honest nodes\nAGREE"])
    ax.set_title("Verified (Lamport's OM(1) algorithm): the SAME 1-traitor attack\nfails at n=3, succeeds at n=4 - exactly the n >= 3f+1 threshold",
                loc="left", pad=10, fontsize=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "1-7-byzantine-threshold-verified")


def eight_fallacies():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.axis("off")
    fallacies = [
        "1. The network is reliable",
        "2. Latency is zero",
        "3. Bandwidth is infinite",
        "4. The network is secure",
        "5. Topology doesn't change",
        "6. There is one administrator",
        "7. Transport cost is zero",
        "8. The network is homogeneous",
    ]
    for i, f in enumerate(fallacies):
        y = len(fallacies) - i
        ax.text(0.05, y, f, fontsize=11, color=INK)
        ax.axhline(y - 0.4, xmin=0.03, xmax=0.97, color=GRAY, lw=0.6)
    ax.set_xlim(0, 1); ax.set_ylim(0, len(fallacies) + 0.8)
    ax.set_title("The 8 fallacies of distributed computing (Deutsch et al.) -\nevery one of them has already broken a design somewhere in this course",
                loc="left", pad=12, fontsize=11)
    return save_mpl(fig, "1-7-eight-fallacies")


if __name__ == "__main__":
    synchrony_models()
    failure_mode_spectrum()
    byzantine_threshold_verified()
    eight_fallacies()
