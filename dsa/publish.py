#!/usr/bin/env python3
"""Push notes/<slug>.md into the matching Notion page, replacing its body.

build_tree.py creates every page once (with the note if it already existed, otherwise a
stub). Any note written afterwards is pushed with this script.

Usage:
    python3 publish.py                 # every note whose content differs from last push
    python3 publish.py 23.1-bl-invalid-transactions 23.2-bl-collatz
    python3 publish.py --all           # force re-push everything, ignoring the hash cache
    python3 publish.py --dry-run
"""
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
MAP_PATH = os.path.join(HERE, "notion_pages.json")
CACHE_PATH = os.path.join(HERE, ".published.json")
NOTES_DIR = os.path.join(HERE, "notes")
WORKDIR = os.path.join(HERE, ".ntnwork")

os.makedirs(WORKDIR, exist_ok=True)
PAGES = json.load(open(MAP_PATH))
CACHE = json.load(open(CACHE_PATH)) if os.path.exists(CACHE_PATH) else {}


def body_of(path):
    """Note text with the YAML frontmatter stripped - ntn only needs it for the title."""
    text = open(path).read()
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:].lstrip("\n")
    return text


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--all" in sys.argv
    dry = "--dry-run" in sys.argv

    slugs = args or sorted(
        f[:-3] for f in os.listdir(NOTES_DIR) if f.endswith(".md"))

    pushed = skipped = 0
    for slug in slugs:
        path = os.path.join(NOTES_DIR, f"{slug}.md")
        if not os.path.exists(path):
            print(f"MISS  {slug}: no notes/{slug}.md", file=sys.stderr)
            continue
        if slug not in PAGES:
            print(f"MISS  {slug}: no Notion page - run build_tree.py first", file=sys.stderr)
            continue

        body = body_of(path)
        digest = hashlib.sha256(body.encode()).hexdigest()
        if not force and CACHE.get(slug) == digest:
            skipped += 1
            continue

        page_id = PAGES[slug]["id"]
        if dry:
            print(f"would push  {slug} -> {page_id}")
            continue

        # The public API returns transient failures under sustained load; retry.
        for attempt in range(5):
            p = subprocess.run(["ntn", "pages", "edit", page_id],
                               input=body, capture_output=True, text=True, cwd=WORKDIR)
            if p.returncode == 0:
                break
            print(f"retry {attempt + 1}/5  {slug}: {p.stderr.strip()[:120]}",
                  file=sys.stderr)
            time.sleep(2 * (attempt + 1))
        else:
            print(f"FAIL  {slug}\n{p.stderr}", file=sys.stderr)
            json.dump(CACHE, open(CACHE_PATH, "w"), indent=1)
            sys.exit(1)
        CACHE[slug] = digest
        json.dump(CACHE, open(CACHE_PATH, "w"), indent=1)
        pushed += 1
        print(f"push  {slug}")
        time.sleep(0.35)

    print(f"\npushed {pushed}, unchanged {skipped}")


if __name__ == "__main__":
    main()
