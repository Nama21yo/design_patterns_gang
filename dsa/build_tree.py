#!/usr/bin/env python3
"""Create the Notion "DSA" page tree via the ntn CLI.

Three levels:  DSA  ->  Part N  ->  leaf page (primer / question / index).

Idempotent: reads dsa/notion_pages.json and skips anything already created, keyed by a
stable slug. Safe to re-run after a partial failure.

If `notes/<slug>.md` exists it is published as the page body; otherwise a "not yet written"
stub with a checklist goes up, and `publish.py` fills it in later.

Usage:
    python3 build_tree.py            # whole tree
    python3 build_tree.py p14 p15    # only these parts (by part slug, or 'p0', 'bank', ...)
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from topics import PATTERNS  # noqa: E402
from data.interview_bank import BANK, SYSTEM_DESIGN_ROUNDS  # noqa: E402

MAP_PATH = os.path.join(HERE, "notion_pages.json")
NOTES_DIR = os.path.join(HERE, "notes")
WORKDIR = os.path.join(HERE, ".ntnwork")
QS = json.load(open(os.path.join(HERE, "data", "bb_questions.json")))

os.makedirs(WORKDIR, exist_ok=True)
PAGES = json.load(open(MAP_PATH)) if os.path.exists(MAP_PATH) else {}


def save():
    with open(MAP_PATH, "w") as f:
        json.dump(PAGES, f, indent=1)


def create(slug, title, parent_id, body):
    """Create one Notion page. Returns its id. No-op if the slug is already mapped."""
    if slug in PAGES and PAGES[slug].get("id"):
        return PAGES[slug]["id"]
    # Quote the title: an unquoted ':' in YAML frontmatter makes ntn drop the page name.
    safe = title.replace('"', "'")
    content = f'---\ntitle: "{safe}"\n---\n\n{body}\n'
    cmd = ["ntn", "pages", "create", "--json", "-v"]
    if parent_id:
        cmd += ["--parent", f"page:{parent_id}"]
    # The public API returns transient failures under sustained load; retry with backoff.
    for attempt in range(5):
        p = subprocess.run(cmd, input=content, capture_output=True, text=True, cwd=WORKDIR)
        if p.returncode == 0:
            break
        print(f"retry {attempt + 1}/5  {slug}: {p.stderr.strip()[:200]}", file=sys.stderr)
        time.sleep(2 * (attempt + 1))
    else:
        print(f"FAIL  {slug}\n{p.stderr}", file=sys.stderr)
        save()
        sys.exit(1)
    data = json.loads(p.stdout)
    PAGES[slug] = {"id": data["id"], "title": title, "url": data["url"], "parent": parent_id}
    save()
    print(f"made  {slug}")
    time.sleep(0.35)
    return data["id"]


def note_or(slug, fallback):
    """Published body: the real note if it exists, otherwise the stub."""
    path = os.path.join(NOTES_DIR, f"{slug}.md")
    if os.path.exists(path):
        text = open(path).read()
        # strip frontmatter - ntn only needs it for the title, which create() supplies
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                text = text[end + 4:].lstrip("\n")
        return text
    return fallback


def stub(intro, todos):
    lines = ["> Status: not yet written.", "", intro, "", "**To cover:**", ""]
    lines += [f"- [ ] {t}" for t in todos]
    return "\n".join(lines)


def q_stub(slug, q):
    """Stub for a Tier A question page - already carries the link and the facts."""
    freq = " | ".join(f"{k}: {v:.0f}%" for k, v in q["freq"].items() if v is not None)
    tags = ", ".join(q["tags"])
    lines = [
        "> Status: not yet written.", "",
        f"**Link:** {q['url']}", "",
        f"**Difficulty:** {q['diff']}  |  **LeetCode #{q['lcid']}**"
        f"{'  |  premium' if q['paid'] else ''}", "",
        f"**Bloomberg frequency:** {freq}", "",
        f"**LeetCode tags:** {tags}", "",
        "**To write:**", "",
    ]
    lines += [f"- [ ] {s}" for s in [
        "Problem statement (restated, with examples)",
        "Clarifying questions to ask first",
        "Intuition - the one idea that unlocks it",
        "Approach, brute force to optimal",
        "Python solution, clean and commented",
        "Time and space complexity, justified",
        "How to present it out loud",
        "Follow-ups and variations",
        "Pitfalls",
    ]]
    return "\n".join(lines)


def freq_cell(q):
    for k in ("30d", "3mo", "6mo", "all"):
        v = q["freq"].get(k)
        if v is not None:
            return f"{v:.0f}% ({k})"
    return "-"


def recency_rank(q):
    order = {"30d": 0, "3mo": 1, "6mo": 2}
    for k, r in order.items():
        if q["freq"].get(k) is not None:
            return r
    return 3


def sort_key(q):
    best = max((v for v in q["freq"].values() if v is not None), default=0)
    return (recency_rank(q), -best, q["lcid"])


def index_body(title, qs):
    """The 'full question index' leaf: every Bloomberg-tagged question in this topic."""
    lines = [
        f"Every Bloomberg-tagged LeetCode question that classifies into **{title}**, "
        f"{len(qs)} in total, ordered by how recently it was reported and then by frequency.",
        "",
        "`A` = has its own note page in this Part. `B` = on the list, note on request.",
        "",
        "| # | Question | Diff | Tier | Bloomberg freq |",
        "|---|----------|------|------|----------------|",
    ]
    for q in qs:
        star = " (premium)" if q["paid"] else ""
        lines.append(f"| {q['lcid']} | [{q['title']}]({q['url']}){star} | {q['diff'][0]} "
                     f"| {q['tier']} | {freq_cell(q)} |")
    lines += ["", "Windows: `30d` = asked in the last 30 days, `3mo` / `6mo` likewise, "
              "`all` = all-time list only. More recent beats higher frequency."]
    return "\n".join(lines)


def bank_stub(e):
    lines = [f"> Reported {e['reports']} time(s) in {', '.join(sorted(set(e['rounds'])))} "
             f"on {', '.join(e['dates'])}.", "",
             "## Prompt as given", "", "```", e["prompt"], "```", ""]
    if e["lc"]:
        lines += ["## Closest LeetCode problems", ""]
        lines += [f"- [{t}]({u})" for t, u in e["lc"]]
        lines.append("")
    lines += ["## Follow-ups actually asked", ""]
    lines += [f"- {f}" for f in e["followups"]]
    lines += ["", "**To write:**", ""]
    lines += [f"- [ ] {s}" for s in [
        "Clarifying questions to ask first",
        "Intuition",
        "Approach",
        "Python solution",
        "Complexity",
        "How to present it out loud",
        "Worked answers to each follow-up above",
        "Pitfalls (including what the reporting candidates got wrong)",
    ]]
    return "\n".join(lines)


ORIENTATION = [
    ("0.1-study-plan", "0.1 How to use this syllabus + 8-week study plan",
     "The plan that turns this tree into daily work.",
     ["Week-by-week schedule", "How to use a question page", "Spaced review rules",
      "What to do when you are stuck", "Tracking what you got wrong"]),
    ("0.2-bloomberg-loop", "0.2 The Bloomberg coding interview: the loop and what each round tests",
     "Rounds, format, timing, and the signals each interviewer is scoring.",
     ["Phone screen / Round 1", "Round 2 technical", "Round 3 system or OOP design",
      "Engineering manager round", "Timing and pacing", "What the reports say about each round"]),
    ("0.3-solving-framework", "0.3 The solving framework",
     "Clarify, examples, brute force, optimise, code, test - the loop to run every time.",
     ["Restate the problem", "Ask the clarifying questions", "Work a small example by hand",
      "State the brute force and its cost", "Find the bottleneck and remove it",
      "Write the code", "Test it out loud"]),
    ("0.4-how-to-present", "0.4 How to present a solution out loud",
     "The script that turns a correct answer into a hire signal.",
     ["Narrating while you think", "Announcing the approach before coding",
      "What to write on the shared editor", "Handling a hint gracefully",
      "Recovering when your approach is wrong", "Closing: complexity + edge cases + follow-ups"]),
    ("0.5-complexity", "0.5 Complexity analysis cheat sheet",
     "How to state a bound and defend it.",
     ["Big-O, Theta, Omega - and which one to say", "Common recurrences and the Master Theorem",
      "Amortised analysis (dynamic array, union-find)",
      "Space: auxiliary vs total, recursion stack",
      "Costs of every Python operation you will use"]),
    ("0.6-python-toolkit", "0.6 Python toolkit for interviews",
     "The standard library you are allowed to use, and what it costs.",
     ["collections: defaultdict, Counter, deque, OrderedDict",
      "heapq and the tuple-key idiom", "bisect", "itertools", "functools.lru_cache and cmp_to_key",
      "sort with key, and stability", "String and list operation costs",
      "Things that look O(1) but are not"]),
    ("0.7-testing-in-the-room", "0.7 Testing your own code in the room",
     "Finding your own bug before the interviewer does.",
     ["The standard edge-case checklist", "Dry-running on the example",
      "Invariants and assertions", "Off-by-one audit", "What to do when a test fails"]),
]

OOD = [
    ("24.1-lld-round", "24.1 The LLD round: requirements to code", []),
    ("24.2-solid", "24.2 SOLID in practice", []),
    ("24.3-patterns", "24.3 The design patterns that come up", []),
    ("24.4-object-indexing", "24.4 Indexing and denormalisation inside an object model", []),
    ("24.5-backward-compatible", "24.5 Backward-compatible refactoring", []),
    ("24.6-lld-classics", "24.6 Worked: parking lot, elevator, deck of cards, order book", []),
    ("24.7-appstore-worked", "24.7 Worked: the App Store question, end to end", []),
]

MOCK = [
    ("25.1-eight-week", "25.1 The 8-week schedule", []),
    ("25.2-daily-loop", "25.2 The daily loop", []),
    ("25.3-mock-protocol", "25.3 Timed mock protocol", []),
    ("25.4-review-log", "25.4 Review log and the wrong-answer list", []),
    ("25.5-week-before", "25.5 The week before", []),
]

RESOURCES = [
    ("26.1-sources", "26.1 The source lists and how to regenerate them", []),
    ("26.2-behavioural", "26.2 Behavioural prep for this loop", []),
    ("26.3-system-design-xref", "26.3 Cross-reference to the system design course", []),
]


def build(only=None):
    root = create("root", "DSA", None,
                  "Bloomberg-focused data structures and algorithms course.\n\n"
                  "Part 0 is orientation. Parts 1-22 are patterns, each with a primer, one page "
                  "per high-priority question, and a full index of every Bloomberg-tagged "
                  "question in that topic. Part 23 is the bank of questions reported from real "
                  "rounds - start there. Parts 24-26 are OOP design, the mock plan, and resources.")

    by_bucket = {}
    for slug, q in QS.items():
        by_bucket.setdefault(q["bucket"], []).append(dict(q, slug=slug))

    # Part 0
    if not only or "p0" in only:
        pid = create("p0", "Part 0 - Orientation", root,
                     "How to run a coding round, and how to use the rest of this tree.")
        for slug, title, intro, todos in ORIENTATION:
            create(slug, title, pid, note_or(slug, stub(intro, todos)))

    # Parts 1-22
    for part_slug, num, title, buckets, tagline, primer in PATTERNS:
        key = f"p{num}"
        if only and key not in only and part_slug not in only:
            continue
        qs = sorted((q for b in buckets for q in by_bucket.get(b, [])), key=sort_key)
        a = [q for q in qs if q["tier"] == "A"]
        pid = create(key, f"Part {num} - {title}", root,
                     f"*{tagline}*\n\n{len(qs)} Bloomberg-tagged questions: "
                     f"{len(a)} with full notes, {len(qs) - len(a)} in the index.")
        primer_slug = f"{num}.0-primer"
        create(primer_slug, f"{num}.0 {title} - pattern primer", pid,
               note_or(primer_slug, stub(tagline, primer)))
        for i, q in enumerate(a, 1):
            leaf = f"{num}.{i}-{q['slug']}"
            create(leaf, f"{num}.{i} {q['title']}", pid, note_or(leaf, q_stub(leaf, q)))
        idx = f"{num}.{len(a) + 1}-index"
        create(idx, f"{num}.{len(a) + 1} Full Bloomberg index - {title}", pid,
               index_body(title, qs))

    # Part 23 - the bank
    if not only or "bank" in only or "p23" in only:
        pid = create("p23", "Part 23 - Bloomberg Real Interview Bank", root,
                     "Questions reported from actual Bloomberg rounds, Oct-Dec 2025, with the "
                     "follow-ups the interviewers actually used. Ordered by how many separate "
                     "candidates reported each one - the repeat rate is the signal.\n\n"
                     "Work through this Part first.")
        for i, e in enumerate(sorted(BANK, key=lambda x: -x["reports"]), 1):
            leaf = f"23.{i}-{e['slug']}"
            create(leaf, f"23.{i} {e['title']}", pid, note_or(leaf, bank_stub(e)))

    # Parts 24-26
    simple = [("p24", "Part 24 - OOP and Low-Level Design",
               "Bloomberg sometimes replaces the distributed design round with a class-design "
               "round in an editor. This Part prepares for that.", OOD),
              ("p25", "Part 25 - Mock Interview Plan and Spaced Repetition",
               "The schedule and the review discipline.", MOCK),
              ("p26", "Part 26 - Resources",
               "Where the lists came from and what else to read.", RESOURCES)]
    for key, title, intro, leaves in simple:
        if only and key not in only:
            continue
        pid = create(key, title, root, intro)
        for slug, ltitle, todos in leaves:
            create(slug, ltitle, pid,
                   note_or(slug, stub("", todos or ["written on request"])))

    save()
    print(f"\nDONE. {len(PAGES)} pages mapped in {MAP_PATH}")


if __name__ == "__main__":
    build(set(sys.argv[1:]) or None)
