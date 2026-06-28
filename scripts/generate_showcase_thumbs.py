#!/usr/bin/env python3
"""Generate distinct Showcase tab thumbnails for related projects."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle
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


def six_string_optimizer() -> Path:
    fig, ax = _base_fig("6-String Optimizer")
    frets = np.linspace(1.0, 9.0, 7)
    for i, x in enumerate(frets):
        ax.plot([x, x], [0.7, 4.3], color="#5c4033", lw=3, alpha=0.85)
        ax.scatter([x], [4.45], s=18, c="#c9a227", edgecolors="#fff", linewidths=0.3)
    t = np.linspace(0, 3 * np.pi, 200)
    ax.plot(5 + 1.8 * np.cos(t), 2.5 + 0.9 * np.sin(2 * t), color="#ef553b", lw=2.5, alpha=0.9)
    ax.fill_between([0.5, 9.5], [0.5, 0.5], [0.65, 0.65], color="#1e3a5f", alpha=0.6)
    ax.text(0.35, 0.35, "Riemannian S³ burst · guitar audio spectrum", color=SUB, fontsize=7)
    return _save(fig, "six_string_optimizer.png")


def staging() -> Path:
    fig, ax = _base_fig("6-String Staging")
    x = np.linspace(1.0, 9.0, 80)
    for band, color, alpha in (
        (np.sin(3 * x) * 0.4 + 2.8, "#1a8fe3", 0.35),
        (np.sin(5 * x + 0.5) * 0.35 + 2.2, "#00c9b7", 0.45),
        (np.sin(7 * x + 1.2) * 0.3 + 1.6, "#c9a227", 0.55),
    ):
        ax.fill_between(x, band - 0.15, band + 0.15, color=color, alpha=alpha)
    ax.plot([1, 9], [0.55, 0.55], color="#8ecae6", lw=1.5, linestyle="--", alpha=0.7)
    ax.text(0.35, 0.35, "staging build · real-audio spectrum · S³ burst", color=SUB, fontsize=7)
    return _save(fig, "staging.png")


def mystery() -> Path:
    fig, ax = _base_fig("Mystery — φ e π")
    phi = (1 + 5**0.5) / 2
    labels = ("φ", "e", "π")
    vals = (phi, np.e, np.pi)
    colors = ("#c9a227", "#00c9b7", "#1a8fe3")
    for i, (lab, val, col) in enumerate(zip(labels, vals, colors)):
        bx = 1.5 + i * 2.8
        h = 2.2 * val / np.pi
        ax.add_patch(Rectangle((bx, 0.9), 1.6, h, facecolor=col, edgecolor="#e8f4ff", lw=1, alpha=0.85))
        ax.text(bx + 0.8, 0.65, lab, color=FG, fontsize=10, ha="center", fontweight="bold")
    ax.text(5, 4.1, "φ² + e² ≈ π²", color=FG, fontsize=9, ha="center", fontweight="bold")
    ax.text(0.35, 0.35, "emergent signature · CLI terminal · keypad UI", color=SUB, fontsize=7)
    return _save(fig, "mystery.png")


def qvpic() -> Path:
    fig, ax = _base_fig("QVPIC Identity Conduit")
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


def kingdom() -> Path:
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
    return _save(fig, "kingdom.png")


def main() -> None:
    paths = [
        kingdom(),
        six_string_optimizer(),
        staging(),
        qvpic(),
        hopf_flux_bubble(),
        orbital_braille_vqc(),
        mystery(),
    ]
    for p in paths:
        print(f"Wrote {p} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()