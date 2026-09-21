# DSA note-writing workflow

Companion to `../system-design/WORKFLOW.md`. Same idea, different pipeline: this course has
~340 pages, so the tree is generated rather than hand-built.

## Layout

```
dsa/
  SYLLABUS.md            generated - the outline, do not hand-edit
  gen_syllabus.py        regenerates SYLLABUS.md
  topics.py              the 22 pattern Parts and their primer outlines  (edit this)
  data/
    bb_questions.json    1213 Bloomberg-tagged LeetCode questions, classified
    interview_bank.py    real interview reports, Oct-Dec 2025             (edit this)
  build_tree.py          creates the Notion tree (idempotent)
  publish.py             pushes notes/<slug>.md into existing pages
  notion_pages.json      slug -> {id, url}                               (generated)
  .published.json        slug -> content hash, so publish.py skips unchanged notes
  notes/<slug>.md        the notes themselves
```

## Per note

1. **Pick the page** from `SYLLABUS.md`. Its slug is the key in `notion_pages.json`
   (e.g. `23.1-bl-invalid-transactions`, `14.0-primer`, `5.3-search-insert-position`).
2. **Write** `notes/<slug>.md`. Start with frontmatter `title: "..."` - **quoted**, because
   an unquoted `:` makes ntn silently drop the page title. Do not add an H1 matching the
   title; Notion already shows it.
3. **Run the code.** Every Python block in a note must have been executed against the
   examples in the prompt. Paste real output, not remembered output.
4. **Publish**: `python3 publish.py <slug>` (or bare `publish.py` for everything changed).
5. **Verify**:
   `ntn api "v1/blocks/<page-id>/children?page_size=100" | jq -r '.results[].type' | sort | uniq -c`

## Adding pages

- New pattern topic or primer outline -> edit `topics.py`, then
  `python3 gen_syllabus.py && python3 build_tree.py`.
- New real interview question -> append to `BANK` in `data/interview_bank.py`, then the same
  two commands. **Append, never insert**, because page titles carry the index (`23.7 ...`)
  and re-ordering would desynchronise them from the existing Notion pages.
- Promoting a Tier B question to Tier A -> flip `"tier"` in `data/bb_questions.json`, then
  rebuild. Note this shifts the numbering of later questions in that Part; prefer to batch
  promotions.
- `build_tree.py` skips any slug already in `notion_pages.json`, so re-running it is safe
  and only creates what is missing. Pass part slugs to limit it: `python3 build_tree.py p14`.

## Refreshing the source data

The Bloomberg list and the LeetCode tags were pulled on 2026-09-21. To refresh:

1. Re-download the five CSVs from
   `snehasishroy/leetcode-companywise-interview-questions/bloomberg`.
2. Re-pull topic tags from the LeetCode GraphQL endpoint (`problemsetQuestionList`,
   100 per page, `topicTags { slug }`).
3. Re-run the classifier to rebuild `data/bb_questions.json`.

Tier A is defined as: appeared in the 30-day or 3-month window, **or** scored >= 50%
frequency in the 6-month window.

## House rules

- **No emojis anywhere.** (Same rule as the system design course.)
- Every Tier A and Part 23 note follows the nine-section format in `SYLLABUS.md`:
  statement, clarifying questions, intuition, approach, solution, complexity, how to present
  it, follow-ups, pitfalls.
- Solution code is optimised for **reading aloud in an interview**, not for brevity. Real
  variable names, comments on the non-obvious line, no one-liner cleverness.
- The "how to present it" section is numbered and is a literal script. It is the part that
  distinguishes these notes from LeetCode's editorial.
- Part 23 pages keep the prompt **verbatim** in a fenced block, and the follow-ups are the
  ones actually asked, not invented ones. Invented follow-ups go in a clearly separate
  bullet.
- Where a circulating community solution is wrong, say so and say why - those are the bugs
  that get made under pressure.

## Progress

- [x] Tree built: 340 pages, 27 Parts
- [x] Part 23 - Bloomberg Real Interview Bank: 8 of 26 notes written
      (23.1 invalid transactions, 23.2 Collatz, 23.3 underground system, 23.4 fuel grid,
       23.5 remove 3+ consecutive, 23.6 lottery, 23.7 all paths, 23.8 CCTV top-N)
- [ ] Part 23 - remaining 18 notes
- [ ] Part 0 - Orientation (7 pages)
- [ ] Pattern primers (22 pages) - write these before the question notes in each Part
- [ ] Tier A question notes (212 pages)
- [ ] Parts 24-26
