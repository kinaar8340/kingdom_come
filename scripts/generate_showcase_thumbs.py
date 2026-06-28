#!/usr/bin/env python3
"""Generate distinct Showcase tab thumbnails for related projects."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "app" / "assets" / "showcase"
W, H = 560, 280
BG = "#0a1628"
FG = "#e8f4ff"
SUB = "#8ecae6"


def _base_fig(title: str):
    fig, ax = plt.subplots(figsize=(W / 100, H / 100), facecolor=BG, dpi=100)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.text(0.35, 4.55, title, color=FG, fontsize=9, fontweight="bold", va="top")
    return fig, ax


def _save(fig, name: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight", pad_inches=0.08, facecolor=BG)
    plt.close(fig)
    return path


def hopf_flux_bubble() -> Path:
    fig, ax = _base_fig("Hopf Flux Bubble")
    theta = np.linspace(0, 2 * np.pi, 200)
    for r, alpha in ((1.6, 0.35), (1.2, 0.55), (0.85, 0.75)):
        ax.plot(5 + r * np.cos(theta), 2.5 + r * np.sin(theta), color="#c9a227", lw=2, alpha=alpha)
    ax.add_patch(Circle((5, 2.5), 0.55, fill=False, ec="#00c9b7", lw=2.5))
    rng = np.random.default_rng(7)
    n = 120
    ang = rng.uniform(0, 2 * np.pi, n)
    rad = rng.normal(1.2, 0.18, n)
    ax.scatter(5 + rad * np.cos(ang), 2.5 + rad * np.sin(ang), s=8, c="#1a8fe3", alpha=0.55)
    ax.text(0.35, 0.35, "flux metrics · hopfion · analog gravity", color=SUB, fontsize=7)
    return _save(fig, "hopf_flux_bubble.png")


def orbital_braille_vqc() -> Path:
    fig, ax = _base_fig("Orbital Braille VQC")
    t = np.linspace(0, 4 * np.pi, 300)
    ax.plot(2.2 + 0.35 * np.cos(t), 2.5 + 0.35 * np.sin(t) + 0.25 * t / (4 * np.pi), color="#ea580c", lw=2.5)
    ax.plot(7.8 - 0.35 * np.cos(t), 2.5 + 0.35 * np.sin(t) + 0.25 * t / (4 * np.pi), color="#f97316", lw=2.5, alpha=0.85)
    for xi, yi in np.ndindex(6, 4):
        on = (xi + yi + int(xi * yi)) % 3 != 0
        if on:
            ax.scatter(1.2 + xi * 0.55, 0.55 + yi * 0.45, s=28, c="#fde68a", edgecolors="#7c2d12", linewidths=0.4)
    ax.text(0.35, 0.35, "quaternion OAM · helix beams · PWM orbits", color=SUB, fontsize=7)
    return _save(fig, "orbital_braille_vqc.png")


def qvpic() -> Path:
    fig, ax = _base_fig("QVpic")
    for row in range(4):
        for col in range(8):
            x, y = 1.0 + col * 1.05, 3.6 - row * 0.75
            hue = 0.55 + 0.08 * ((row + col) % 5)
            ax.add_patch(Rectangle((x, y), 0.75, 0.55, facecolor=plt.cm.plasma(hue), edgecolor="#1a8fe3", lw=0.6, alpha=0.85))
    theta = np.linspace(0, 2 * np.pi, 120)
    ax.plot(8.2 + 0.9 * np.cos(theta), 1.35 + 0.9 * np.sin(theta), color="#c9a227", lw=3)
    ax.scatter([8.2], [1.35], s=40, c="#ef553b", edgecolors="#fff", linewidths=0.5, zorder=5)
    ax.text(0.35, 0.35, "magic island sweeps · z-flywheel · lattice swarm", color=SUB, fontsize=7)
    return _save(fig, "qvpic.png")


def toe() -> Path:
    fig, ax = _base_fig("toe — gauged lattice")
    sites = np.linspace(1.2, 8.8, 14)
    for s in sites:
        ax.plot([s, s], [0.9, 4.1], color="#1e3a5f", lw=1, alpha=0.6)
    ax.plot(sites, [2.5] * len(sites), color="#1a8fe3", lw=1.5, alpha=0.5)
    ax.add_patch(FancyArrowPatch((3.2, 2.5), (4.4, 3.35), arrowstyle="-|>", mutation_scale=14, color="#c9a227", lw=2.5))
    ax.add_patch(FancyArrowPatch((6.8, 2.5), (7.9, 1.45), arrowstyle="-|>", mutation_scale=14, color="#ef553b", lw=2.5))
    ax.text(2.8, 3.55, "stable", color="#c9a227", fontsize=7)
    ax.text(6.4, 1.15, "chaotic", color="#ef553b", fontsize=7)
    ax.text(0.35, 0.35, "two-gyro lattice · RubikCone conduit", color=SUB, fontsize=7)
    return _save(fig, "toe.png")


def vqc_sims_public() -> Path:
    fig, ax = _base_fig("vqc_sims_public")
    t = np.linspace(0, 2 * np.pi, 400)
    p, q = 2, 3
    r = 0.9
    R = 2.0
    x = 5 + (R + r * np.cos(q * t)) * np.cos(p * t)
    y = 2.5 + (R + r * np.cos(q * t)) * np.sin(p * t)
    phase = np.sin(3 * t)
    for i in range(len(t) - 1):
        ax.plot(x[i : i + 2], y[i : i + 2], color=plt.cm.twilight(0.5 + 0.4 * phase[i]), lw=2)
    ax.plot(5 + R * np.cos(t), 2.5 + R * np.sin(t), color="#00c9b7", lw=1, alpha=0.35)
    ax.text(0.35, 0.35, "OAM knots · quaternion encode/decode", color=SUB, fontsize=7)
    return _save(fig, "vqc_sims_public.png")


def kingdom_come() -> Path:
    """Portal card — Hopf fibers + flux ring (distinct from hopf_flux_bubble sphere)."""
    sys.path.insert(0, str(ROOT / "src"))
    from kingdom.core.hopf import sample_fiber_family

    fig, ax = _base_fig("Kingdom Come")
    fibers = sample_fiber_family(n_fibers=7, n_points=100)
    colors = ("#1a8fe3", "#00c9b7", "#4cc9f0", "#48bfe3", "#c9a227")
    for i, fiber in enumerate(fibers):
        px_arr, py_arr = fiber["px"], fiber["py"]
        px = 1.0 + 8.0 * (px_arr - px_arr.min()) / (np.ptp(px_arr) + 1e-9)
        py = 0.7 + 3.6 * (py_arr - py_arr.min()) / (np.ptp(py_arr) + 1e-9)
        ax.plot(px, py, color=colors[i % len(colors)], lw=1.8, alpha=0.9)
    theta = np.linspace(0, 2 * np.pi, 100)
    ax.plot(8.0 + 0.55 * np.cos(theta), 1.2 + 0.55 * np.sin(theta), color="#c9a227", lw=3)
    ax.text(0.35, 0.35, "TOE portal · Hopf · flux flywheel · lattice", color=SUB, fontsize=7)
    return _save(fig, "kingdom_come.png")


def main() -> None:
    paths = [
        hopf_flux_bubble(),
        orbital_braille_vqc(),
        qvpic(),
        toe(),
        vqc_sims_public(),
        kingdom_come(),
    ]
    for p in paths:
        print(f"Wrote {p} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()