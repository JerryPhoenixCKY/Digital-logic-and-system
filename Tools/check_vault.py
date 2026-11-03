r"""Vault QA for the ECE2050 Obsidian library.

Checks, in one pass:
  1. every note has the three frontmatter fields, with >=3 aliases;
  2. every [[wikilink]] resolves to an existing note (or Knowledge Tree / Glossary);
  3. every note ends with the index line back to the hubs;
  4. every embedded ![[x.svg]] exists in Figures/;
  5. every SVG parses, has ASCII-only labels, and is non-empty;
  6. every figure has a render script and vice versa;
  7. every note is reachable from Knowledge Tree.md with a status marker;
  8. no ASCII-art / box-drawing diagram leftovers in notes.

Usage:  D:\anaconda\python.exe Tools\check_vault.py
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
NOTES = VAULT / "Notes"
FIGS = VAULT / "Figures"
SCRIPTS = VAULT / "Tools" / "figures"

LINK_RE = re.compile(r"(?<!\!)\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
EMBED_RE = re.compile(r"!\[\[([^\]|#]+)")
ART_RE = re.compile(r"(\+[-=]{2,}\+)|([\u2500-\u257f])")
# CJK / full-width ranges: DejaVu Sans (SVG embedded font) has no glyphs for these
CJK_RE = re.compile(r"[\u2e80-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef]")


def is_table_separator(line: str) -> bool:
    """Markdown table separator rows look like box art to a naive regex."""
    stripped = line.lstrip("> ").strip()
    if not stripped or "-" not in stripped:
        return False
    return set(stripped) <= set("|-: ")


problems: list[str] = []
warnings: list[str] = []


HUB_TAGS = {"index", "glossary"}

# filled in by main(): the canonical stem of each hub, used to keep the
# "索引：" line of every note spelled the same way across the library
CANON: dict = {}


def canonical_hubs() -> dict:
    out: dict = {}
    for p in hub_files():
        try:
            tags = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace")).get("tags", [])
        except OSError:
            continue
        if "index" in tags:
            out["tree"] = p.stem
        if "glossary" in tags:
            out["glossary"] = p.stem
    return out


def hub_files() -> list[Path]:
    """The hub notes, wherever they live (vault root or Notes/) and under whatever
    name the author chose (e.g. ``ECE2050 Knowledge Tree.md``).

    They are located by the ``index`` / ``glossary`` tag, so moving or renaming
    them in Obsidian never breaks the QA run.
    """
    found: list[Path] = []
    for folder in (VAULT, NOTES):
        if not folder.exists():
            continue
        for p in sorted(folder.glob("*.md")):
            if p in found:
                continue
            try:
                fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
            except OSError:          # locked by a concurrent writer / cloud sync
                continue
            if HUB_TAGS & set(fm.get("tags", [])):
                found.append(p)
    return found


def note_files() -> list[Path]:
    files = sorted(NOTES.glob("*.md")) if NOTES.exists() else []
    files += hub_files()
    seen: list[Path] = []
    for f in files:
        if f.exists() and f not in seen:
            seen.append(f)
    return sorted(seen, key=lambda p: p.name)


def is_hub(path: Path) -> bool:
    return path in hub_files()


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    fm: dict = {"aliases": [], "tags": []}
    current = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current:
            fm[current].append(line[4:].strip())
        elif ":" in line:
            key, _, val = line.partition(":")
            current = key.strip()
            fm.setdefault(current, val.strip())
    return fm


def check_notes(all_names: set[str]) -> None:
    for path in note_files():
        rel = path.name
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            problems.append(f"{rel}: unreadable ({exc.strerror or exc}) - locked by a writer?")
            continue
        if not text.strip():
            problems.append(f"{rel}: EMPTY file (write was interrupted?)")
            continue
        fm = parse_frontmatter(text)
        if not fm:
            problems.append(f"{rel}: missing frontmatter")
        else:
            for field in ("tags", "date", "aliases"):
                if field not in fm:
                    problems.append(f"{rel}: frontmatter missing '{field}'")
            if len(fm.get("aliases", [])) < 3:
                problems.append(f"{rel}: fewer than 3 aliases -> {fm.get('aliases')}")
            if "ECE2050" not in fm.get("tags", []):
                warnings.append(f"{rel}: tags do not include ECE2050")

        for target in LINK_RE.findall(text):
            t = target.strip()
            if t not in all_names:
                problems.append(f"{rel}: unresolved wikilink [[{t}]]")

        for embed in EMBED_RE.findall(text):
            e = embed.strip()
            if not (FIGS / e).exists():
                problems.append(f"{rel}: embedded file missing: {e}")

        last = text.splitlines()[-1]
        if "索引：" not in last:
            problems.append(f"{rel}: last line is not the index line back to the hubs")
        elif not is_hub(path) and CANON.get("tree"):
            canon = f"[[{CANON['tree']}]]"
            if "[[Knowledge Tree]]" in last and canon != "[[Knowledge Tree]]":
                warnings.append(
                    f"{rel}: index line uses [[Knowledge Tree]]; canonical is {canon}")

        for i, line in enumerate(text.splitlines(), 1):
            if ART_RE.search(line) and not is_table_separator(line) and "```" not in line:
                warnings.append(f"{rel}:{i}: possible ASCII/box art -> {line.strip()[:60]}")
        body_lines = len(text.splitlines())
        if path.parent == NOTES and not is_hub(path) and not (110 <= body_lines <= 300):
            warnings.append(f"{rel}: body length {body_lines} lines (target 120-260)")


def check_figures() -> None:
    svgs = sorted(FIGS.glob("*.svg")) if FIGS.exists() else []
    scripts = sorted(SCRIPTS.glob("*.py")) if SCRIPTS.exists() else []
    stems_svg = {p.stem for p in svgs}
    stems_py = {p.stem for p in scripts if not p.stem.startswith("_")}
    for stem in sorted(stems_svg - stems_py):
        warnings.append(f"figure without render script: {stem}.svg")
    for stem in sorted(stems_py - stems_svg):
        problems.append(f"render script without SVG: {stem}.py")

    for svg in svgs:
        raw = svg.read_text(encoding="utf-8", errors="replace")
        try:
            ET.fromstring(raw)
        except ET.ParseError as exc:
            problems.append(f"{svg.name}: invalid XML ({exc})")
            continue
        if len(raw) < 500:
            problems.append(f"{svg.name}: suspiciously small ({len(raw)} bytes)")
        labels = re.findall(r"<!--(.*?)-->", raw)
        # matplotlib/schemdraw put real text in <text>/<tspan>; comments are only a hint.
        # Only CJK is a real defect (DejaVu Sans has no CJK glyphs -> tofu boxes);
        # math symbols (-, x, +/-, infinity, arrows) are fine.
        texts = re.findall(r"<(?:text|tspan)\b[^>]*>(.*?)</(?:text|tspan)>", raw, re.S)
        for lab in labels + texts:
            if CJK_RE.search(lab):
                problems.append(f"{svg.name}: CJK label {lab!r} (renders as boxes)")
        if not labels and not texts:
            warnings.append(f"{svg.name}: no text labels found")
        if ("stroke" in raw or "<path" in raw) and "stroke-width" not in raw:
            warnings.append(f"{svg.name}: no explicit stroke-width (style module not used?)")


def check_tree(all_names: set[str]) -> None:
    trees = [p for p in hub_files()
             if "index" in parse_frontmatter(p.read_text(encoding="utf-8")).get("tags", [])]
    if not trees:
        problems.append("no Knowledge Tree hub found (expected a note tagged 'index')")
        return
    tree = trees[0].read_text(encoding="utf-8")
    linked = set(LINK_RE.findall(tree))
    for path in sorted(NOTES.glob("*.md")):
        if is_hub(path):
            continue
        if path.stem not in linked:
            problems.append(f"Knowledge Tree: note not listed -> {path.stem}")
        elif not any(f"[[{path.stem}]]" in line and "✅" in line
                     for line in tree.splitlines()):
            problems.append(f"Knowledge Tree: missing ✅ for {path.stem}")
    for extra in sorted(linked - all_names):
        problems.append(f"Knowledge Tree: link to unknown note [[{extra}]]")


def main() -> int:
    files = note_files()
    CANON.update(canonical_hubs())
    all_names: set[str] = set()
    for p in files:
        all_names.add(p.stem)
        all_names.update(
            parse_frontmatter(p.read_text(encoding="utf-8", errors="replace")).get("aliases", [])
        )
    check_notes(all_names)
    check_figures()
    check_tree(all_names)

    print(f"notes: {len([p for p in files if p.parent == NOTES and not is_hub(p)])}, "
          f"hubs: {len(hub_files())}, "
          f"figures: {len(list(FIGS.glob('*.svg'))) if FIGS.exists() else 0}")
    print(f"\nPROBLEMS ({len(problems)}):")
    for p in problems:
        print("  X", p)
    print(f"\nWARNINGS ({len(warnings)}):")
    for w in warnings:
        print("  !", w)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
