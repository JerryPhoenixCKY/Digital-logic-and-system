r"""Layout QA for one figure script: text overlap + out-of-canvas check.

Text-only agents cannot see the PNG, so this renders the figure through the
patched ``save_fig`` hook, then walks every text artist's bounding box looking
for (a) labels that overlap each other and (b) labels that fall outside the
figure canvas.  Nested boxes (e.g. a label inside its own framed box) are not
counted as overlaps.

Usage:
    D:\anaconda\python.exe Tools\figcheck.py signed-division-restoring
    D:\anaconda\python.exe Tools\figcheck.py --all      # every script that uses matplotlib
"""
from __future__ import annotations

import importlib.util
import itertools
import pathlib
import sys

VAULT = pathlib.Path(__file__).resolve().parent.parent
FIGDIR = VAULT / "Tools" / "figures"
sys.path.insert(0, str(VAULT / "Tools"))

import figstyle as fs_mod  # noqa: E402

CAPTURED: dict = {}


def _capture(fig, name, png=True, dpi=200):
    CAPTURED["fig"] = fig
    CAPTURED["name"] = name
    return VAULT / "Figures" / (name + ".svg")


def _capture_svg(d, name, png=True, dpi=200):
    """schemdraw drawings cannot be introspected this way."""
    CAPTURED["schemdraw"] = name
    return VAULT / "Figures" / (name + ".svg")


fs_mod.save_fig = _capture
fs_mod.save_svg = _capture_svg


def _texts(fig):
    out = []
    for ax in fig.axes:
        cand = list(ax.texts) + [ax.title, ax.xaxis.label, ax.yaxis.label]
        if ax.axison:                    # tick labels only when the axis is drawn
            cand += list(ax.get_xticklabels()) + list(ax.get_yticklabels())
        for t in cand:
            try:
                if not t.get_text().strip() or not t.get_visible():
                    continue
                out.append((t.get_text().replace("\n", " ")[:28],
                            t.get_window_extent(fig.canvas.get_renderer())))
            except Exception:
                continue
    return out


def check(name: str) -> list[str]:
    CAPTURED.clear()
    path = FIGDIR / f"{name}.py"
    if not path.exists():
        return [f"{name}: no such script"]
    spec = importlib.util.spec_from_file_location("fig_" + name.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)              # module-level scripts render here
    if hasattr(mod, "main"):
        mod.main()                            # function-style scripts render here

    if "fig" not in CAPTURED:
        return [] if "schemdraw" in CAPTURED else [f"{name}: nothing rendered"]

    fig = CAPTURED["fig"]
    fig.canvas.draw()
    items = _texts(fig)
    fbox = fig.bbox
    problems: list[str] = []

    for (n1, b1), (n2, b2) in itertools.combinations(items, 2):
        ix = min(b1.x1, b2.x1) - max(b1.x0, b2.x0)
        iy = min(b1.y1, b2.y1) - max(b1.y0, b2.y0)
        if ix <= 1 or iy <= 1:
            continue
        contained = ((b1.x0 <= b2.x0 and b1.y0 <= b2.y0 and b1.x1 >= b2.x1 and b1.y1 >= b2.y1)
                     or (b2.x0 <= b1.x0 and b2.y0 <= b1.y0 and b2.x1 >= b1.x1 and b2.y1 >= b1.y1))
        if not contained:
            problems.append(f"text overlap: {n1!r} <-> {n2!r} ({ix:.0f}x{iy:.0f} px)")

    for n, b in items:
        if b.x0 < fbox.x0 - 1 or b.y0 < fbox.y0 - 1 or b.x1 > fbox.x1 + 1 or b.y1 > fbox.y1 + 1:
            problems.append(f"outside canvas: {n!r}")
    return problems


def _mpl_scripts() -> list[str]:
    out = []
    for p in sorted(FIGDIR.glob("*.py")):
        if p.stem.startswith("_"):
            continue
        if "apply_mpl_style" in p.read_text(encoding="utf-8", errors="replace"):
            out.append(p.stem)
    return out


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    names = _mpl_scripts() if args[0] == "--all" else args
    bad = 0
    for name in names:
        problems = check(name)
        status = "OK" if not problems else f"{len(problems)} problem(s)"
        print(f"{name}: {status}")
        for p in problems:
            print("   X", p)
        bad += len(problems)
    print(f"\ntotal problems: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
