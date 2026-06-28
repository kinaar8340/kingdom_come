#!/usr/bin/env python3
"""Generate Kingdom Come demo GIF for README / Space card."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.hopf import sample_fiber, sample_fiber_family

OUT = ROOT / "app" / "assets" / "kingdom_demo.gif"
COLORS = ("#1a8fe3", "#00c9b7", "#4cc9f0", "#48bfe3", "#64dfdf", "#c9a227")
N_FRAMES = 36
DURATION_MS = 90


def render_frame(xi1: float) -> Image.Image:
    fibers = sample_fiber_family(n_fibers=8, n_points=120)
    highlight = sample_fiber(0.6, xi1, n_points=160)

    fig, ax = plt.subplots(figsize=(8, 5), facecolor="#0a1628")
    ax.set_facecolor("#0a1628")

    for i, fiber in enumerate(fibers):
        ax.plot(fiber["px"], fiber["py"], color=COLORS[i % len(COLORS)], linewidth=2.0, alpha=0.85)

    ax.plot(
        highlight["px"],
        highlight["py"],
        color=COLORS[-1],
        linewidth=3.5,
        alpha=1.0,
        label="highlight fiber",
    )

    ax.set_title("Kingdom Come — Hopf fibers (ξ₁ sweep)", color="#e8f4ff", fontsize=13)
    ax.set_aspect("equal")
    ax.grid(True, color="#1e3a5f", alpha=0.3)
    ax.tick_params(colors="#8ecae6", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#1e3a5f")

    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    plt.close(fig)
    return Image.fromarray(buf).convert("P", palette=Image.Palette.ADAPTIVE)


def main() -> None:
    frames: list[Image.Image] = []
    xi1_vals = np.linspace(0.0, 2.0 * np.pi, N_FRAMES, endpoint=False)
    for xi1 in xi1_vals:
        frames.append(render_frame(float(xi1)))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {OUT} ({len(frames)} frames)")


if __name__ == "__main__":
    main()