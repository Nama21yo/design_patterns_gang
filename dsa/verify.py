#!/usr/bin/env python3
"""Execute the Python in a note and check every claimed output.

Convention used by the notes:

    ```python
    def solve(x): ...              # definition blocks: executed in order
    ```

    ```python
    solve(3)        # 7            <- expression + trailing comment = CHECKED
    solve("a")      # 'a'
    solve(-1)       # ValueError
    solve(2)        # 4  -- and here is a remark, so this one is NOT checked
    ```

Each top-level AST node is executed exactly once. A node that is a bare expression whose
last source line carries a trailing comment is *evaluated* once and its result compared
against that comment; everything else is executed. So side effects never run twice.

A comment is treated as prose (and skipped) when it contains " -- ", ends in a full stop
or question mark, or opens with an obvious English connective.

Usage:
    python3 verify.py                       # every note
    python3 verify.py 1.1-two-sum 2.3-...   # named notes
    python3 verify.py --part 5              # every note whose slug starts with "5."
"""
import ast
import contextlib
import io
import os
import re
import sys
import tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.join(HERE, "notes")
BLOCK = re.compile(r"```python\n(.*?)```", re.S)

# Word boundaries matter: without \b, "value" would match "ValueError" and silently
# turn an exception assertion into an unchecked comment.
PROSE_START = re.compile(
    r"^(and|or|the|a|an|so|then|this|that|now|note|same|see|still|already|both|drop|use|"
    r"was|wait|previously|kept|unchanged|new|returns|value|each|every|no|not|only|"
    r"skip|copy|higher|lower|it|we|you|i)\b(?!Error|Exception)|^o\(", re.I)


def is_prose(comment):
    c = comment.strip()
    if not c:
        return True
    if c.startswith("--"):
        return True
    if PROSE_START.match(c):
        return True
    # A comment that begins with a Python literal is an assertion, whatever follows it.
    if literal_prefix(c) is not None:
        return False
    if " -- " in c or c.endswith((".", "?", "!", ":")):
        return True
    return False


def literal_prefix(comment):
    """The longest leading slice of `comment` that parses as a Python literal.

    Lets a claim carry a trailing remark: `# 'Other Corp'   - untouched` asserts
    'Other Corp' and ignores the rest.
    """
    c = comment.strip()
    best = None
    for end in range(len(c), 0, -1):
        chunk = c[:end].strip()
        if not chunk:
            continue
        try:
            ast.literal_eval(chunk)
        except (ValueError, SyntaxError, MemoryError, TypeError):
            continue
        best = chunk
        break
    return best


def trailing_comments(source):
    """{line number: comment text} for comments that follow code on the same line."""
    out = {}
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return out
    code_lines = set()
    for tok in tokens:
        if tok.type not in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE,
                            tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER):
            code_lines.add(tok.start[0])
    for tok in tokens:
        if tok.type == tokenize.COMMENT and tok.start[0] in code_lines:
            out[tok.start[0]] = tok.string.lstrip("#").strip()
    return out


def matches(value, expected):
    """Does `value` satisfy the claim text? Exact repr/str, or the literal prefix."""
    if repr(value) == expected or str(value) == expected:
        return True
    lit = literal_prefix(expected)
    if lit is None:
        return False
    if repr(value) == lit or str(value) == lit:
        return True
    try:
        return value == ast.literal_eval(lit)
    except Exception:
        return False


def check_note(slug):
    path = os.path.join(NOTES, f"{slug}.md")
    if not os.path.exists(path):
        return None
    text = open(path).read()
    ns = {"__name__": "__note__"}
    checked = failed = 0
    problems = []

    skipped = 0
    for block in BLOCK.findall(text):
        if re.search(r"^\s*\.\.\.\s*$", block, re.M):
            continue                                    # explicitly elided block
        if block.lstrip().startswith("# fragment"):
            skipped += 1
            continue                                    # illustrative snippet, not runnable
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue                                    # pseudo-code / not Python
        comments = trailing_comments(block)

        for node in tree.body:
            comment = comments.get(getattr(node, "end_lineno", node.lineno))
            is_expr = isinstance(node, ast.Expr)

            if is_expr and comment and not is_prose(comment):
                checked += 1
                expected = comment.strip()
                exc_match = re.match(r"^([A-Za-z_]*(?:Error|Exception))\b", expected)
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        value = eval(compile(ast.Expression(node.value), "<note>", "eval"), ns)
                except Exception as e:
                    if exc_match and type(e).__name__ == exc_match.group(1):
                        continue                        # the raise was the claim
                    problems.append(
                        f"    {ast.unparse(node.value)[:70]}\n"
                        f"        claimed : {expected}\n"
                        f"        raised  : {type(e).__name__}: {e}")
                    failed += 1
                    continue
                if exc_match:
                    problems.append(
                        f"    {ast.unparse(node.value)[:70]}\n"
                        f"        claimed : {expected}\n"
                        f"        actual  : no exception, returned {value!r}")
                    failed += 1
                elif not matches(value, expected):
                    problems.append(
                        f"    {ast.unparse(node.value)[:70]}\n"
                        f"        claimed : {expected}\n"
                        f"        actual  : {value!r}")
                    failed += 1
                continue

            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(ast.Module([node], []), "<note>", "exec"), ns)
            except ModuleNotFoundError as e:
                problems.append(f"    (skipped, {e.name} not installed)")
                skipped += 1
                break                                   # rest of the block needs it
            except Exception as e:
                problems.append(f"    exec failed: {ast.unparse(node)[:70]}"
                                f"  -> {type(e).__name__}: {e}")
                failed += 1

    return checked, failed, problems, skipped


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--part" in sys.argv:
        part = sys.argv[sys.argv.index("--part") + 1]
        args = sorted(f[:-3] for f in os.listdir(NOTES)
                      if f.endswith(".md") and f.startswith(part + "."))
    slugs = args or sorted(f[:-3] for f in os.listdir(NOTES) if f.endswith(".md"))

    total_checked = total_failed = 0
    bad = []
    for slug in slugs:
        result = check_note(slug)
        if result is None:
            print(f"MISS  {slug}")
            continue
        c, f, problems, sk = result
        total_checked += c
        total_failed += f
        note = f", {sk} skipped" if sk else ""
        print(f"{'ok  ' if not f else 'FAIL'}  {slug:58} {c:3} checked, {f} failed{note}")
        for p in problems:
            print(p)
        if f:
            bad.append(slug)

    print(f"\n{total_checked} assertions checked, {total_failed} failed")
    if bad:
        print("notes needing fixes: " + ", ".join(bad))
    return 1 if total_failed else 0


if __name__ == "__main__":
    sys.exit(main())
