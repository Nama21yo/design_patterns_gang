# Note-writing workflow

Per note, repeat:

1. **Pick the page** from `SYLLABUS.md`. Get its Notion id from `notion_pages.json`
   (key = slug, e.g. `1.4-cap-pacelc`).
2. **Diagrams**: write `diagrams/d_<slug>.py` importing from `_style.py`. Use
   `render(name, dot_body)` for architecture/flow (Graphviz), `mpl()` + `save_mpl()`
   for quantitative charts. Output goes to `images/<name>.png`. Review each PNG.
3. **Note**: write `notes/<slug>.md`. Start with frontmatter `title: "..."` (quoted -
   an unquoted `:` breaks it). Do NOT add an H1 matching the title. Embed images with
   `![caption](https://raw.githubusercontent.com/Nama21yo/design_patterns_gang/main/system-design/images/<name>.png)`.
4. **Commit + push** `system-design/` to `main` (raw URLs need the files on main).
5. **Publish**: `cd <scratch>; ntn pages edit <page-id> < notes/<slug>.md`
   (replaces page content; strips frontmatter; sets nothing but body).
6. **Verify**: `ntn api "v1/blocks/<page-id>/children?page_size=100" | jq -r '.results[].type' | sort | uniq -c`
   and spot-check `ntn pages get <page-id>`.

## House rules
- No emojis anywhere.
- As many explanatory diagrams as the topic warrants; prefer self-drawn.
- Every design note follows the 0.2 framework structure.
- Bloomberg (`[bl]`) pages: keep the verbatim prompt block at top, then the worked design.

## Progress
- [x] Part 0 - Orientation (0.1 study plan, 0.2 interview framework, 0.3 estimation) - COMPLETE
- [ ] Part 1 - Fundamentals (next)
- [ ] everything else
