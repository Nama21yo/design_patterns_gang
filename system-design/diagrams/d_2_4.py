"""Diagrams for note 2.4 - Failure detection, timeouts, retries, backoff, idempotency."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def failure_detection():
    render("2-4-failure-detection", f"""
    rankdir=LR;
    call [label="Call a remote service,\\lno response yet", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    q [label="Is it dead, or just slow?\\lNO WAY TO TELL FOR SURE\\l(3.6's FLP result)", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    timeout [label="TIMEOUT: the practical\\lcompromise - assume failure\\lafter waiting T, accept a small\\lrisk of being wrong", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    call -> q -> timeout;

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Too short a timeout: false positives, wasted retries against a service\\lthat would have answered fine. Too long: wasted latency, and (2.6) threads\\lpile up waiting, risking cascading failure. There is no universally correct\\lvalue - it has to be tuned per call, informed by that call's own p99.\\l"];
    timeout -> note [style=invis];
    """)


def retry_decision():
    render("2-4-retry-decision", f"""
    rankdir=TB;
    q [label="A call failed or timed out.\\lShould I retry it?", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    q1 [label="Is the failure TRANSIENT?\\l(network blip, brief overload)\\lvs PERMANENT (bad request,\\lauth failure, not found)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    q2 [label="Is the operation IDEMPOTENT,\\lor do I have an idempotency\\lkey to make it safe?", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    retry [label="Retry - WITH exponential\\lbackoff + jitter", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    no1 [label="Don't retry - it will\\lfail the same way again", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    no2 [label="Don't retry blindly - risk\\lof a duplicate side effect\\l(double charge, double send)", fillcolor="{RED}", fontcolor=white, color="{RED}"];

    q -> q1;
    q1 -> no1 [label="  permanent"];
    q1 -> q2 [label="  transient"];
    q2 -> retry [label="  yes"];
    q2 -> no2 [label="  no"];
    """)


def backoff_jitter_verified():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8, 3.8))
    labels = ["without jitter\n(plain exponential)", "with full jitter"]
    peak = [2000, 152]
    ax.bar(labels, peak, color=[RED, TEAL], width=0.5)
    for i, v in enumerate(peak):
        ax.text(i, v + 40, f"{v:,}", ha="center", fontsize=10)
    ax.set_ylabel("clients retrying in the SAME 50ms window")
    ax.set_title("Measured: 2,000 clients, same outage, same exponential backoff -\njitter cuts the synchronized retry spike by 13x",
                loc="left", pad=10, fontsize=10.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "2-4-backoff-jitter-verified")


def idempotency_key_flow():
    render("2-4-idempotency-key-flow", f"""
    rankdir=LR;
    req1 [label="Client sends request\\l+ Idempotency-Key: K", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    process [label="Server processes it,\\lstores the result keyed by K", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    lost [label="Response is LOST\\l(network blip) - client\\lnever sees it, times out", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    retry [label="Client retries the SAME\\llogical request, SAME key K", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    lookup [label="Server sees K already\\lprocessed -> returns the\\lCACHED result, does NOT\\lredo the side effect", fillcolor="{LIGHTTEAL}", color="{TEAL}"];

    req1 -> process -> lost -> retry -> lookup;

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Verified: a naive retry (no key) double-charged a payment (1000 -> 800\\lfor one logical 100 charge). The SAME retry, with an idempotency key,\\lcorrectly charged once (1000 -> 900) and flagged the 2nd call as replayed.\\l"];
    lookup -> note [style=invis];
    """)


if __name__ == "__main__":
    failure_detection()
    retry_decision()
    backoff_jitter_verified()
    idempotency_key_flow()
