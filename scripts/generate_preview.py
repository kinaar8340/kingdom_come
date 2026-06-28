#!/usr/bin/env python3
"""Generate README / Space thumbnail preview for Hopf visualizer."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.hopf import sample_fiber_family

OUT = ROOT / "app" / "assets" / "hopf_preview.png"
COLORS = ("#1a8fe3", "#00c9b7", "#4cc9f0", "#48bfe3", "#64dfdf", "#c9a227")


def main() -> None:
    fibers = sample_fiber_family(n_fibers=10, n_points=140)
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#0a1628")
    ax.set_facecolor("#0a1628")

    for i, fiber in enumerate(fibers):
        ax.plot(
            fiber["px"],
            fiber["py"],
            color=COLORS[i % len(COLORS)],
            linewidth=2.2,
            alpha=0.9,
        )

    ax.set_title(
        "Kingdom Come — Hopf Fibration (stereographic xy)",
        color="#e8f4ff",
        fontsize=14,
        pad=12,
    )
    ax.set_xlabel("x", color="#8ecae6")
    ax.set_ylabel("y", color="#8ecae6")
    ax.tick_params(colors="#8ecae6")
    for spine in ax.spines.values():
        spine.set_color("#1e3a5f")
    ax.set_aspect("equal")
    ax.grid(True, color="#1e3a5f", alpha=0.35)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()