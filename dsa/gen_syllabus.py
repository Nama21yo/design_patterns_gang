#!/usr/bin/env python3
"""Generate SYLLABUS.md from topics.py + data/bb_questions.json + data/interview_bank.py.

Run after changing any of those. The prose header lives in HEADER below.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from topics import PATTERNS  # noqa: E402
from data.interview_bank import BANK, SYSTEM_DESIGN_ROUNDS  # noqa: E402

QS = json.load(open(os.path.join(HERE, "data", "bb_questions.json")))

HEADER = """# DSA - Study Syllabus (Bloomberg-focused)

Local source of truth for the Notion "DSA" page tree. Every leaf below becomes one Notion
subpage. Companion to `../system-design/SYLLABUS.md` - that one covers the design round,
this one covers the coding rounds.

## What this is built from

1. **Real interview reports** from a candidate group chat covering the Oct-Dec 2025
   Bloomberg new-grad and internship loops. These are questions that were *actually asked*,
   with the *actual* follow-ups. Part 23 is the bank; it is the highest-value section here.
2. **The company-tagged LeetCode list** (`snehasishroy/leetcode-companywise-interview-questions`,
   bloomberg): {nq} questions, each with a recency window (30 days / 3 months / 6 months / all
   time) and a frequency score.
3. **Topic tags pulled from the LeetCode API** for all {nq} questions, so the classification
   into patterns is authoritative rather than guessed.
4. The user's existing notebooks in `../dsa_notes/`.

## Tiers

- **Tier A ({na} questions)** - appeared in the 30-day or 3-month window, or scored >= 50%
  frequency in the 6-month window. These get a full note: link, problem statement, intuition,
  approach, clean Python solution, how to present it out loud, follow-ups and variations,
  time and space complexity.
- **Tier B ({nb} questions)** - the rest of the tagged list. These live in a per-topic index
  page (title, difficulty, link, recency, frequency) so nothing is left behind, and get
  promoted to Tier A on request.

## Note format (every Tier A + Part 23 page)

    Link  |  Difficulty  |  Reported in round  |  Frequency
    1. Problem statement          (restated precisely, with the examples)
    2. Clarifying questions       (what to ask before writing anything)
    3. Intuition                  (the one idea that unlocks it)
    4. Approach                   (numbered steps, brute force -> optimal)
    5. Solution                   (clear, commented Python)
    6. Complexity                 (time and space, justified)
    7. How to present it          (the script: what to say, in what order, what to draw)
    8. Follow-ups and variations  (including what the interviewer can change)
    9. Pitfalls                   (the mistakes people actually made)

## Legend

`[bl]` = reported verbatim from a real Bloomberg round.
"""

FOOTER_PARTS = """
## Part 0 - Orientation

- 0.1 How to use this syllabus + an 8-week study plan
- 0.2 The Bloomberg coding interview: the loop, what each round tests, timing
- 0.3 The solving framework: clarify -> examples -> brute force -> optimise -> code -> test
- 0.4 How to present a solution out loud (the script that earns the hire signal)
- 0.5 Complexity analysis cheat sheet (including amortised and recursive costs)
- 0.6 Python toolkit for interviews (collections, heapq, bisect, itertools, and their costs)
- 0.7 Testing your own code in the room: edge cases, dry runs, invariants
"""


def freq_str(q):
    f = q["freq"]
    for k in ("30d", "3mo", "6mo", "all"):
        if f.get(k) is not None:
            return f"{f[k]:.0f}% / {k}"
    return "-"


def recency(q):
    f = q["freq"]
    for k in ("30d", "3mo", "6mo"):
        if f.get(k) is not None:
            return k
    return "older"


def sort_key(q):
    """Most recent window first, then by frequency, then by LeetCode id."""
    order = {"30d": 0, "3mo": 1, "6mo": 2, "older": 3}
    f = q["freq"]
    best = max((v for v in f.values() if v is not None), default=0)
    return (order[recency(q)], -best, q["lcid"])


def main():
    out = [HEADER.format(nq=len(QS), na=sum(1 for q in QS.values() if q["tier"] == "A"),
                         nb=sum(1 for q in QS.values() if q["tier"] == "B")),
           FOOTER_PARTS]

    by_part = {}
    for slug, q in QS.items():
        by_part.setdefault(q["bucket"], []).append(dict(q, slug=slug))

    for part_slug, num, title, buckets, tagline, primer in PATTERNS:
        qs = []
        for b in buckets:
            qs += by_part.get(b, [])
        qs.sort(key=sort_key)
        a = [q for q in qs if q["tier"] == "A"]
        b_ = [q for q in qs if q["tier"] == "B"]
        out.append(f"\n## Part {num} - {title}\n")
        out.append(f"*{tagline}*\n")
        out.append(f"{len(qs)} Bloomberg-tagged questions: {len(a)} Tier A, {len(b_)} Tier B.\n")
        out.append(f"- {num}.0 Pattern primer")
        for t in primer:
            out.append(f"    - {t}")
        out.append("")
        for i, q in enumerate(a, 1):
            paid = " [premium]" if q["paid"] else ""
            out.append(f"- {num}.{i} [{q['diff'][0]}] {q['title']}{paid}  "
                       f"({freq_str(q)})")
        out.append(f"- {num}.{len(a) + 1} Full Bloomberg question index for this topic "
                   f"({len(qs)} questions)")

    out.append("\n## Part 23 - Bloomberg Real Interview Bank  [bl]\n")
    out.append("Questions reported from actual Oct-Dec 2025 rounds. Ordered by how many\n"
               "separate candidates reported them - the repeat rate is the signal.\n")
    for i, e in enumerate(sorted(BANK, key=lambda x: -x["reports"]), 1):
        out.append(f"- 23.{i} [bl] {e['title']}  "
                   f"({e['reports']} report{'s' if e['reports'] > 1 else ''}, "
                   f"{'/'.join(sorted(set(e['rounds'])))})")

    out.append("\n## Part 24 - OOP and Low-Level Design\n")
    out.append("*Bloomberg sometimes replaces the distributed-design round with a class-design "
               "round in an editor.*\n")
    for i, t in enumerate([
            "The LLD round: requirements -> entities -> relationships -> API -> code",
            "SOLID in practice, with the refactor each principle implies",
            "The design patterns that come up: strategy, observer, factory, adapter, "
            "singleton, decorator",
            "Indexing and denormalisation inside an object model (the App Store question)",
            "Backward-compatible refactoring: keeping an interface while changing storage",
            "Worked: parking lot, elevator, deck of cards, rate limiter, order book",
            "Worked: the App Store question, end to end"], 1):
        out.append(f"- 24.{i} {t}")

    out.append("\n## Part 25 - Mock Interview Plan and Spaced Repetition\n")
    for i, t in enumerate([
            "The 8-week schedule, week by week",
            "Daily loop: 1 new pattern problem + 2 review + 1 timed",
            "Timed mock protocol (45 minutes, talking out loud, no IDE help)",
            "Review log and the 'problems I got wrong' list",
            "The week before: what to do and what to stop doing"], 1):
        out.append(f"- 25.{i} {t}")

    out.append("\n## Part 26 - Resources\n")
    for i, t in enumerate([
            "The source lists and how to regenerate them",
            "Behavioural prep: the questions this loop actually asks",
            "Cross-reference to the system design course"], 1):
        out.append(f"- 26.{i} {t}")

    out.append("\n### System design rounds reported in the same chat\n")
    out.append("Full notes live in `../system-design/` (Part 10). Listed here for cross-reference:\n")
    for s in SYSTEM_DESIGN_ROUNDS:
        out.append(f"- {s}")

    text = "\n".join(out) + "\n"
    with open(os.path.join(HERE, "SYLLABUS.md"), "w") as f:
        f.write(text)
    print(f"wrote SYLLABUS.md ({len(text.splitlines())} lines)")


if __name__ == "__main__":
    main()
