#!/usr/bin/env python3
"""Generate Imagine-style electron cloud artwork for Z = 1–180."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.elements import EXPLORER_Z_MAX, KNOWN_ELEMENT_MAX, get_element, shell_occupancies

OUT_DIR = ROOT / "app" / "assets" / "elements"
SUPERHEAVY_DIR = ROOT / "app" / "assets" / "superheavy"
PROMPTS_FILE = OUT_DIR / "imagine_prompts.txt"
SUPERHEAVY_PROMPTS = OUT_DIR / "imagine_prompts_superheavy.txt"
LEGACY_DIR = ROOT / "app" / "assets" / "noble_gases"
IMAGINE_INBOX = ROOT / "app" / "assets" / "elements_imagine"


def imagine_prompt(z: int, name: str, symbol: str, n_shells: int, *, synthetic: bool = False) -> str:
    shell_phrase = (
        "one perfect spherical shell"
        if n_shells <= 1
        else f"{n_shells} concentric glowing cyan shells"
    )
    tone = (
        "theoretical superheavy violet-magenta probability clouds with unstable golden Hopf fibers"
        if synthetic
        else "glowing soft cyan probability density"
    )
    return (
        f"Dark scientific illustration of the electron cloud for {name}, Z={z}. "
        f"{tone} forming {shell_phrase}. "
        f"Subtle golden Hopf fibration fiber texture woven through the cloud. "
        f"Dark navy background (#0a1628), elegant mathematical aesthetic, high contrast, "
        f"minimalist. No text, no labels. Cinematic lighting."
    )


def _radial_glow(ax, r: float, color: str, alpha: float, n: int = 80) -> None:
    rs = np.linspace(r * 0.65, r * 1.25, n)
    for i, rad in enumerate(rs):
        t = np.linspace(0, 2 * np.pi, 200)
        fade = alpha * (1.0 - i / n) ** 1.6
        ax.plot(rad * np.cos(t), rad * np.sin(t), color=color, alpha=fade, lw=2.5)


def _hopf_fibers(ax, n: int = 8, *, synthetic: bool = False) -> None:
    t = np.linspace(0, 2 * np.pi, 320)
    color = "#c9a227" if not synthetic else "#e8b84a"
    for k in range(n):
        phase = k * np.pi / n
        r = 0.58 + 0.1 * np.sin(4 * t + phase) + 0.04 * np.cos(7 * t)
        ax.plot(
            r * np.cos(t + phase * 0.4),
            r * np.sin(t + phase * 0.4),
            color=color,
            alpha=0.32 if not synthetic else 0.42,
            lw=0.9,
        )


def _nucleus_glow(ax, *, synthetic: bool = False) -> None:
    core = "#ef553b" if not synthetic else "#ff6b9d"
    for size, alpha in ((0.09, 0.35), (0.05, 0.7), (0.025, 1.0)):
        ax.add_patch(Circle((0, 0), size, color=core, alpha=alpha, zorder=6))


def render_element(z: int, out: Path, *, synthetic: bool = False) -> None:
    el = get_element(z)
    if el is None:
        return
    shells = shell_occupancies(z)
    fig, ax = plt.subplots(figsize=(5.12, 5.12), facecolor="#0a1628")
    ax.set_facecolor("#0a1628")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)

    # Background vignette
    xx, yy = np.meshgrid(np.linspace(-1, 1, 200), np.linspace(-1, 1, 200))
    rr = np.sqrt(xx**2 + yy**2)
    cmap = LinearSegmentedColormap.from_list("kc", ["#0a1628", "#0d2137", "#0a1628"])
    ax.imshow(rr, cmap=cmap, alpha=0.55, extent=(-1, 1, 1, -1), zorder=0)

    _hopf_fibers(ax, n=min(10, max(5, len(shells) + 2)), synthetic=synthetic)

    shell_color = "#7b4dff" if synthetic else "#00c9b7"
    dot_color = "#c77dff" if synthetic else "#4cc9f0"
    ring_color = "#1a8fe3" if not synthetic else "#9d6bff"

    for shell_n, count in shells:
        r = 0.16 + 0.1 * shell_n
        _radial_glow(ax, r, shell_color, min(0.55, 0.18 + 0.05 * count))
        theta = np.linspace(0, 2 * np.pi, 320)
        alpha = min(0.75, 0.12 + 0.06 * count)
        ax.fill(r * np.cos(theta), r * np.sin(theta), color=shell_color, alpha=alpha, zorder=2)
        ax.plot(r * np.cos(theta), r * np.sin(theta), color=ring_color, alpha=0.55, lw=1.1, zorder=3)
        rng = np.random.default_rng(z * 1000 + shell_n)
        pts = max(160, 900 // max(len(shells), 1))
        ang = rng.uniform(0, 2 * np.pi, pts)
        rad = rng.normal(r, 0.024 + 0.008 * shell_n, pts)
        ax.scatter(rad * np.cos(ang), rad * np.sin(ang), s=3, c=dot_color, alpha=0.38, zorder=4)

    _nucleus_glow(ax, synthetic=synthetic)
    # No on-image text — matches Grok Imagine prompt (labels live in the UI card)

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=fig.get_facecolor(), pad_inches=0.02)
    plt.close(fig)


def _write_prompts(path: Path, start: int, end: int) -> int:
    lines: list[str] = []
    for z in range(start, end + 1):
        el = get_element(z)
        if el is None:
            continue
        n = len(shell_occupancies(z))
        lines.append(
            f"Z={z} ({el.symbol}): {imagine_prompt(z, el.name, el.symbol, n, synthetic=el.is_synthetic)}"
        )
    path.write_text("\n\n".join(lines), encoding="utf-8")
    return len(lines)


def main() -> None:
    for z in range(1, KNOWN_ELEMENT_MAX + 1):
        el = get_element(z)
        if el is None:
            continue
        out = OUT_DIR / f"{el.symbol.lower()}.png"
        render_element(z, out, synthetic=False)
        print(f"Wrote {out}")

    for z in range(KNOWN_ELEMENT_MAX + 1, EXPLORER_Z_MAX + 1):
        el = get_element(z)
        if el is None:
            continue
        out = SUPERHEAVY_DIR / f"{el.symbol.lower()}.png"
        render_element(z, out, synthetic=True)
        # Mirror into elements/ for unified lookup
        render_element(z, OUT_DIR / f"{el.symbol.lower()}.png", synthetic=True)
        print(f"Wrote {out}")

    n1 = _write_prompts(PROMPTS_FILE, 1, KNOWN_ELEMENT_MAX)
    n2 = _write_prompts(SUPERHEAVY_PROMPTS, KNOWN_ELEMENT_MAX + 1, EXPLORER_Z_MAX)
    print(f"Wrote {PROMPTS_FILE} ({n1} prompts)")
    print(f"Wrote {SUPERHEAVY_PROMPTS} ({n2} prompts)")
    print(f"Drop Grok Imagine PNGs into {IMAGINE_INBOX}/ then run scripts/import_imagine_art.py")

    LEGACY_DIR.mkdir(parents=True, exist_ok=True)
    for z in (2, 10, 18, 36, 54, 86, 118):
        el = get_element(z)
        if el is None:
            continue
        src = OUT_DIR / f"{el.symbol.lower()}.png"
        if src.is_file():
            (LEGACY_DIR / f"{el.symbol.lower()}.png").write_bytes(src.read_bytes())


if __name__ == "__main__":
    main()