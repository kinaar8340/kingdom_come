#!/usr/bin/env python3
"""Generate noble-gas electron cloud artwork (dark theme, Hopf fiber texture)."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.elements import NOBLE_GAS_Z, get_element
from kingdom.core.elements import shell_occupancies

OUT_DIR = ROOT / "app" / "assets" / "noble_gases"

# Grok Imagine reference prompts (paste into image generator):
IMAGINE_PROMPTS = {
    2: "Dark scientific illustration of helium electron cloud Z=2. Glowing soft cyan spherical shell. Subtle golden Hopf fibration fiber texture. Dark navy background, mathematical aesthetic, no text.",
    10: "Dark illustration of neon Z=10. Two glowing cyan concentric shells with golden Hopf fiber texture. Dark navy, elegant, no text.",
    18: "Dark illustration of argon Z=18. Three cyan glowing shells, golden Hopf fibers. Navy background, no text.",
    36: "Dark illustration of krypton Z=36. Multiple cyan shells, intricate golden Hopf patterns. Navy background.",
    54: "Dark illustration of xenon Z=54. Concentric glowing shells, golden Hopf fibration fibers. Cinematic, no text.",
    86: "Dark illustration of radon Z=86. Deep cyan electron clouds, gold Hopf fiber weave. Navy background.",
    118: "Dark illustration of oganesson Z=118. Outer shell glow, golden topological fibers. Navy, minimalist.",
}


def _hopf_fibers(ax, n: int = 6) -> None:
    t = np.linspace(0, 2 * np.pi, 200)
    for k in range(n):
        phase = k * np.pi / n
        r = 0.55 + 0.08 * np.sin(3 * t + phase)
        ax.plot(r * np.cos(t + phase), r * np.sin(t + phase), color="#c9a227", alpha=0.25, lw=0.8)


def render_element(z: int, out: Path) -> None:
    el = get_element(z)
    if el is None:
        return
    shells = shell_occupancies(z)
    fig, ax = plt.subplots(figsize=(6, 6), facecolor="#0a1628")
    ax.set_facecolor("#0a1628")
    ax.set_aspect("equal")
    ax.axis("off")

    _hopf_fibers(ax)

    for i, (shell_n, count) in enumerate(shells):
        r = 0.2 + 0.14 * shell_n
        theta = np.linspace(0, 2 * np.pi, 300)
        alpha = min(0.85, 0.15 + 0.08 * count)
        ax.fill(r * np.cos(theta), r * np.sin(theta), color="#00c9b7", alpha=alpha)
        ax.plot(r * np.cos(theta), r * np.sin(theta), color="#1a8fe3", alpha=0.5, lw=1.2)

        rng = np.random.default_rng(z + shell_n)
        pts = 800 // max(len(shells), 1)
        ang = rng.uniform(0, 2 * np.pi, pts)
        rad = rng.normal(r, 0.03, pts)
        ax.scatter(rad * np.cos(ang), rad * np.sin(ang), s=3, c="#4cc9f0", alpha=0.35)

    ax.scatter([0], [0], s=80, c="#ef553b", edgecolors="#fff", linewidths=0.5, zorder=5)
    ax.text(0, -0.92, f"{el.name} ({el.symbol})  Z={z}", ha="center", color="#e8f4ff", fontsize=11)

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {out}")


def main() -> None:
    for z in sorted(NOBLE_GAS_Z):
        el = get_element(z)
        if el is None:
            continue
        render_element(z, OUT_DIR / f"{el.symbol.lower()}.png")
    print("Imagine prompts for external generators:")
    for z, prompt in IMAGINE_PROMPTS.items():
        print(f"  Z={z}: {prompt}")


if __name__ == "__main__":
    main()