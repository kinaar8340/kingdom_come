#!/usr/bin/env python3
"""Generate electron cloud artwork for all elements Z=1–118 (dark theme, Hopf fibers)."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.elements import KNOWN_ELEMENT_MAX, get_element, shell_occupancies

OUT_DIR = ROOT / "app" / "assets" / "elements"
PROMPTS_FILE = OUT_DIR / "imagine_prompts.txt"
LEGACY_DIR = ROOT / "app" / "assets" / "noble_gases"


def imagine_prompt(z: int, name: str, symbol: str, n_shells: int) -> str:
    shell_phrase = (
        "one perfect spherical shell"
        if n_shells <= 1
        else f"{n_shells} concentric glowing cyan shells"
    )
    return (
        f"Dark scientific illustration of the electron cloud for {name}, Z={z}. "
        f"Glowing soft cyan probability density forming {shell_phrase}. "
        f"Subtle golden Hopf fibration fiber texture woven through the cloud. "
        f"Dark navy background, elegant mathematical aesthetic, high contrast, "
        f"minimalist. No text, no labels. Cinematic lighting."
    )


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
    fig, ax = plt.subplots(figsize=(5, 5), facecolor="#0a1628")
    ax.set_facecolor("#0a1628")
    ax.set_aspect("equal")
    ax.axis("off")
    _hopf_fibers(ax, n=min(8, max(4, len(shells))))

    for shell_n, count in shells:
        r = 0.18 + 0.11 * shell_n
        theta = np.linspace(0, 2 * np.pi, 280)
        alpha = min(0.85, 0.15 + 0.08 * count)
        ax.fill(r * np.cos(theta), r * np.sin(theta), color="#00c9b7", alpha=alpha)
        ax.plot(r * np.cos(theta), r * np.sin(theta), color="#1a8fe3", alpha=0.5, lw=1.0)
        rng = np.random.default_rng(z * 1000 + shell_n)
        pts = max(120, 600 // max(len(shells), 1))
        ang = rng.uniform(0, 2 * np.pi, pts)
        rad = rng.normal(r, 0.028, pts)
        ax.scatter(rad * np.cos(ang), rad * np.sin(ang), s=2, c="#4cc9f0", alpha=0.32)

    ax.scatter([0], [0], s=60, c="#ef553b", edgecolors="#fff", linewidths=0.4, zorder=5)
    ax.text(0, -0.9, f"{el.name} ({el.symbol})  Z={z}", ha="center", color="#e8f4ff", fontsize=9)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=120, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    prompts: list[str] = []
    for z in range(1, KNOWN_ELEMENT_MAX + 1):
        el = get_element(z)
        if el is None:
            continue
        out = OUT_DIR / f"{el.symbol.lower()}.png"
        render_element(z, out)
        prompts.append(f"Z={z} ({el.symbol}): {imagine_prompt(z, el.name, el.symbol, len(shell_occupancies(z)))}")
        print(f"Wrote {out}")

    PROMPTS_FILE.write_text("\n\n".join(prompts), encoding="utf-8")
    print(f"Wrote {PROMPTS_FILE} ({len(prompts)} prompts)")

    # Keep legacy noble_gases dir in sync for older paths
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