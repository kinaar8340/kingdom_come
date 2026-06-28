#!/usr/bin/env python3
"""Generate Flux Flywheel tab demo GIF (element tour with Imagine artwork)."""

from __future__ import annotations

import io
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.elements import get_element, shell_occupancies
from kingdom.core.flux_explorer import element_art_path, explore_flux_element

OUT = ROOT / "app" / "assets" / "flux_flywheel_demo.gif"
WIDTH, HEIGHT = 960, 540
DEMO_Z = (2, 26, 79, 129)
HOLD_FRAMES = 14
FADE_FRAMES = 6
DURATION_MS = 85
BG = (10, 22, 40)


def _cloud_mpl(z: int, stability: float, *, w: int = 560, h: int = 400) -> Image.Image:
    el = get_element(z)
    if el is None:
        return Image.new("RGB", (w, h), BG)
    shells = shell_occupancies(z)
    noble = el.is_noble_gas
    fig, ax = plt.subplots(figsize=(w / 100, h / 100), facecolor="#0a1628", dpi=100)
    ax.set_facecolor("#0a1628")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)

    max_r = 1.0
    for i, (shell_n, count) in enumerate(shells):
        r = 0.35 + 0.2 * shell_n
        max_r = max(max_r, r + 0.12)
        theta = np.linspace(0, 2 * np.pi, 80)
        ax.plot(r * np.cos(theta), r * np.sin(theta), color="#1a8fe3", lw=1.5, alpha=0.5)
        rng = np.random.default_rng(z * 1000 + shell_n)
        ang = rng.uniform(0, 2 * np.pi, 300)
        rad = rng.normal(r, 0.05, ang.size)
        ax.scatter(rad * np.cos(ang), rad * np.sin(ang), s=4, c="#4cc9f0", alpha=0.35)

    ax.scatter([0], [0], s=60, c="#ef553b", edgecolors="#fff", linewidths=0.5, zorder=5)
    fly_r = max_r * (0.52 + 0.045 * stability)
    ring_t = np.linspace(0, 2 * np.pi, 160)
    high = stability >= 7.5 or noble
    if high:
        glow = fly_r * 1.06
        ax.plot(glow * np.cos(ring_t), glow * np.sin(ring_t), color="#c9a227", alpha=0.35, lw=5)
    ax.plot(
        fly_r * np.cos(ring_t),
        fly_r * np.sin(ring_t),
        color="#c9a227",
        lw=5 if high else 2,
        linestyle="-" if high else "--",
    )
    ax.set_title(
        f"{el.name} ({el.symbol}) — electron shells + flux flywheel",
        color="#e8f4ff",
        fontsize=9,
        pad=6,
    )
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor(), pad_inches=0.05)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf).convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
    return img


def _load_art(z: int, size: int = 120) -> Image.Image | None:
    path = element_art_path(z)
    if not path:
        return None
    img = Image.open(path).convert("RGBA")
    return img.resize((size, size), Image.Resampling.LANCZOS)


def _render_panel(z: int) -> Image.Image:
    payload = explore_flux_element(z)
    el = payload["element"]
    fly = payload["flywheel"]
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, WIDTH, 52), fill=(18, 36, 61))
    draw.text((20, 14), "Kingdom Come — Flux Flywheel", fill=(232, 244, 255))
    draw.text((WIDTH - 200, 18), f"v0.5.0  ·  Z = {z}", fill=(142, 202, 230))

    card_x, card_y = 24, 68
    draw.rounded_rectangle(
        (card_x, card_y, card_x + 320, card_y + 200),
        radius=12,
        fill=(18, 36, 61),
        outline=(26, 143, 227),
    )
    if el:
        draw.text((card_x + 16, card_y + 12), el.symbol, fill=(0, 201, 183))
        draw.text((card_x + 56, card_y + 10), el.name[:18], fill=(232, 244, 255))
        draw.text((card_x + 16, card_y + 48), f"Period {el.period} · Group {el.group}", fill=(142, 202, 230))
        cfg = el.electron_config.replace(" (predicted)", "")
        draw.text((card_x + 16, card_y + 72), cfg[:40], fill=(142, 202, 230))
        if el.is_noble_gas:
            draw.text((card_x + 16, card_y + 98), "NOBLE GAS · FLUX LOCK", fill=(0, 245, 255))
        if el.is_synthetic:
            draw.text((card_x + 16, card_y + 118), "THEORETICAL SUPERHEAVY", fill=(255, 180, 162))
    draw.text(
        (card_x + 16, card_y + 150),
        f"Score {fly['stability_score']} · δω = {fly['delta_omega']}",
        fill=(212, 228, 247),
    )

    art = _load_art(z)
    if art:
        canvas.paste(art, (card_x + 190, card_y + 70), art)

    canvas.paste(_cloud_mpl(z, fly["stability_score"]), (360, 68))

    if el:
        cap = el.toe_narrative[:115] + ("…" if len(el.toe_narrative) > 115 else "")
        draw.text((24, HEIGHT - 36), cap, fill=(201, 162, 39))

    return canvas


def main() -> None:
    panels = [_render_panel(z) for z in DEMO_Z]
    frames: list[Image.Image] = []

    title = Image.new("RGB", (WIDTH, HEIGHT), BG)
    td = ImageDraw.Draw(title)
    td.text((240, HEIGHT // 2 - 50), "Flux Flywheel Element Explorer", fill=(232, 244, 255))
    td.text((270, HEIGHT // 2 - 10), "180 elements · Grok Imagine artwork", fill=(142, 202, 230))
    td.text((330, HEIGHT // 2 + 30), "He  →  Fe  →  Au  →  Z=129", fill=(201, 162, 39))
    frames.extend([title] * 10)

    for i, panel in enumerate(panels):
        frames.extend([panel] * HOLD_FRAMES)
        if i < len(panels) - 1:
            nxt = panels[i + 1]
            for f in range(1, FADE_FRAMES + 1):
                frames.append(Image.blend(panel, nxt, f / FADE_FRAMES))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
    )
    kb = OUT.stat().st_size // 1024
    print(f"Wrote {OUT} ({len(frames)} frames, {kb} KB)")


if __name__ == "__main__":
    main()