"""ECE2050 figure style module — the single source of visual truth for this vault.

Ported verbatim (palette, line widths, fonts, helpers) from the ECE2001 library
so that both vaults share one visual language.


Every figure in ``Figures/`` is produced by a script in ``Tools/figures/``.
Figure scripts must NOT hand-pick colors, line widths or fonts: import them
from here so that all figures share one visual language.

    Schematics  (element drawings, topologies)  -> schemdraw
    Curves      (i-v, transient, Bode, ...)     -> matplotlib

Typical schematic script::

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from figstyle import schematic, save_svg, elm, INK, HILITE, ACCENT

    d = schematic()
    d += elm.Resistor().right().label('$R_1$')
    save_svg(d, 'my-figure')

Typical curve script::

    from figstyle import apply_mpl_style, save_fig
    import matplotlib.pyplot as plt
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ...
    save_fig(fig, 'my-curve')

Each helper writes the SVG that gets embedded in the note (``![[name.svg]]``)
and a PNG backup under ``.scratch/png/`` used for visual checking.
"""
from __future__ import annotations

import os
from pathlib import Path

# --------------------------------------------------------------------------
# paths
# --------------------------------------------------------------------------
VAULT = Path(__file__).resolve().parent.parent
FIG_DIR = VAULT / "Figures"
PNG_DIR = VAULT / ".scratch" / "png"


def _ensure_dirs() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------
# one palette / one batch for the whole vault
# --------------------------------------------------------------------------
INK = "#222831"      # element strokes, wires, axes, default text
HILITE = "#c1443c"   # highlighted branch, current arrow, key result
ACCENT = "#1f6f8b"   # secondary emphasis: voltage labels, second curve
MUTED = "#9aa5b1"    # construction lines, dashed helpers, grid
FILL = "#e8eef2"     # light fill for blocks / boxes / supernode regions
GOOD = "#2e7d32"     # "valid / absorbing" marks
BAD = "#b3261e"      # "invalid / warning" marks

LW = 2.0             # schemdraw line width (element geometry unchanged)
FS = 15.0            # schemdraw label font size
MPL_LW = 2.2         # matplotlib line width
MPL_FS = 13.0        # matplotlib base font size

# element defaults for schemdraw (zig-zag resistor geometry is schemdraw's own)
SD_CONFIG = dict(
    unit=3.0,
    inches_per_unit=0.5,
    fontsize=FS,
    font="sans-serif",
    color=INK,
    lw=LW,
    ls="-",
    margin=0.15,
    bgcolor="white",
)


# --------------------------------------------------------------------------
# schemdraw
# --------------------------------------------------------------------------
def schematic(fontsize: float = FS, unit: float = 3.0, lw: float = LW):
    """Return a schemdraw Drawing configured with the vault-wide style."""
    import schemdraw

    cfg = dict(SD_CONFIG)
    cfg["fontsize"] = fontsize
    cfg["unit"] = unit
    cfg["lw"] = lw
    schemdraw.config(**cfg)
    try:  # keep SVG text as real text (crisp, theme independent)
        schemdraw.svgconfig.text = "text"
    except Exception:
        pass
    return schemdraw.Drawing()


def dot(d, xy, color: str = INK, r: float = 0.055):
    """Filled node dot (the vault convention for a connection node)."""
    import schemdraw.elements as elm

    d += elm.Dot(radius=r, color=color).at(xy)
    return d


def gnd(d, xy=None, color: str = INK):
    """Reference ground symbol; always drawn at the bottom bus."""
    import schemdraw.elements as elm

    g = elm.Ground(color=color)
    if xy is not None:
        g = g.at(xy)
    d += g
    return d


def _resolve(name: str) -> Path:
    _ensure_dirs()
    p = Path(name)
    if p.suffix.lower() != ".svg":
        p = p.with_suffix(".svg")
    return p if p.is_absolute() else (FIG_DIR / p.name)


def save_svg(d, name: str, png: bool = True, dpi: float = 200):
    """Save a schemdraw drawing as SVG (embedded) + PNG backup (checking)."""
    path = _resolve(name)
    d.save(str(path), transparent=False)
    if png:
        d.save(str(PNG_DIR / (path.stem + ".png")), transparent=False, dpi=dpi)
    print("wrote", path)
    return path


# --------------------------------------------------------------------------
# matplotlib
# --------------------------------------------------------------------------
def apply_mpl_style() -> None:
    """Apply the vault-wide matplotlib style. Call once per figure script."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": MPL_FS,
            "text.color": INK,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "axes.labelsize": MPL_FS,
            "axes.titlesize": MPL_FS + 2,
            "axes.titleweight": "bold",
            "axes.linewidth": 1.2,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": MUTED,
            "grid.alpha": 0.35,
            "grid.linewidth": 0.9,
            "xtick.color": INK,
            "ytick.color": INK,
            "xtick.labelsize": MPL_FS - 1,
            "ytick.labelsize": MPL_FS - 1,
            "legend.frameon": False,
            "legend.fontsize": MPL_FS - 1,
            "lines.linewidth": MPL_LW,
            "lines.solid_capstyle": "round",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "figure.dpi": 150,
            "svg.fonttype": "none",
        }
    )


def save_fig(fig, name: str, png: bool = True, dpi: float = 200):
    """Save a matplotlib figure as SVG (embedded) + PNG backup (checking)."""
    path = _resolve(name)
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.05,
                facecolor="white")
    if png:
        fig.savefig(PNG_DIR / (path.stem + ".png"), format="png", dpi=dpi,
                    bbox_inches="tight", facecolor="white")
    print("wrote", path)
    return path


# convenience re-exports so figure scripts need a single import
try:  # pragma: no cover
    import schemdraw.elements as elm  # noqa: F401
except Exception:  # pragma: no cover
    elm = None
