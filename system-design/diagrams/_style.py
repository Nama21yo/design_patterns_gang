"""Shared styling for system-design note diagrams.

Graphviz helpers produce clean, consistent architecture/flow diagrams.
matplotlib helper sets a restrained house style for quantitative charts.

Palette (colorblind-safe-ish, muted):
  ink     #1f2933  text / borders
  slate   #52606d  secondary text
  paper   #ffffff  background
  blue    #2f6f9f  primary accent (services, active path)
  teal    #2a9d8f  data stores
  amber   #e9a13b  queues / async
  red     #d1495b  failure / hot path warnings
  gray    #e4e7eb  fills / muted boxes
"""
import os
import subprocess

INK = "#1f2933"
SLATE = "#52606d"
BLUE = "#2f6f9f"
TEAL = "#2a9d8f"
AMBER = "#e9a13b"
RED = "#d1495b"
GRAY = "#e4e7eb"
LIGHTBLUE = "#dbeafe"
LIGHTTEAL = "#d5f0ec"
LIGHTAMBER = "#fbedd7"

IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")

GRAPH_ATTRS = {
    "fontname": "DejaVu Sans",
    "bgcolor": "white",
    "rankdir": "TB",
    "splines": "spline",
    "nodesep": "0.35",
    "ranksep": "0.55",
    "pad": "0.3",
    "dpi": "160",
}
NODE_ATTRS = {
    "fontname": "DejaVu Sans",
    "fontsize": "11",
    "shape": "box",
    "style": "rounded,filled",
    "fillcolor": "white",
    "color": SLATE,
    "fontcolor": INK,
    "penwidth": "1.4",
    "margin": "0.14,0.09",
}
EDGE_ATTRS = {
    "fontname": "DejaVu Sans",
    "fontsize": "9.5",
    "color": SLATE,
    "fontcolor": SLATE,
    "penwidth": "1.3",
    "arrowsize": "0.8",
}


def _attr_str(d):
    return ", ".join(f'{k}="{v}"' for k, v in d.items())


def render(name, body, engine="dot"):
    """body: the inner DOT statements. Writes images/<name>.png, returns path."""
    dot = [
        f"digraph {{",
        f"  graph [{_attr_str(GRAPH_ATTRS)}];",
        f"  node [{_attr_str(NODE_ATTRS)}];",
        f"  edge [{_attr_str(EDGE_ATTRS)}];",
        body,
        "}",
    ]
    src = "\n".join(dot)
    os.makedirs(IMG_DIR, exist_ok=True)
    out = os.path.join(IMG_DIR, f"{name}.png")
    p = subprocess.run([engine, "-Tpng", "-o", out], input=src, text=True,
                       capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"{name}: {p.stderr}\n---\n{src}")
    # trim + pad white border for consistent look
    subprocess.run(["convert", out, "-trim", "+repage", "-bordercolor", "white",
                    "-border", "18", out], check=True)
    print("wrote", out)
    return out


def mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.edgecolor": SLATE,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": SLATE,
        "ytick.color": SLATE,
        "axes.titlecolor": INK,
        "axes.titleweight": "bold",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.dpi": 160,
        "savefig.bbox": "tight",
    })
    return plt


def save_mpl(fig, name):
    os.makedirs(IMG_DIR, exist_ok=True)
    out = os.path.join(IMG_DIR, f"{name}.png")
    fig.savefig(out)
    print("wrote", out)
    return out
