#!/usr/bin/env python3
"""Export Electron Cloud + flux flywheel PNGs for Z = 1..118 (z_knowns/frame_ZZZZ.png)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.elements import KNOWN_ELEMENT_MAX
from kingdom.core.flux_explorer import explore_flux_element
from kingdom.viz.electron_cloud import build_electron_cloud_figure

OUT_DIR = ROOT / "z_knowns"
FRAME_WIDTH = 798
FRAME_HEIGHT = 340


def frame_path(z: int) -> Path:
    return OUT_DIR / f"frame_{z:04d}.png"


def render_frame(z: int) -> None:
    payload = explore_flux_element(z)
    fig = build_electron_cloud_figure(
        payload["element"],
        stability_score=payload["flywheel"]["stability_score"],
        height=FRAME_HEIGHT,
    )
    path = frame_path(z)
    fig.write_image(str(path), width=FRAME_WIDTH, height=FRAME_HEIGHT, scale=1)
    print(f"Wrote {path.relative_to(ROOT)}  ({payload['element'].symbol}, Z={z})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from", dest="z_min", type=int, default=1)
    parser.add_argument("--to", dest="z_max", type=int, default=KNOWN_ELEMENT_MAX)
    parser.add_argument("--force", action="store_true", help="Overwrite existing frames")
    args = parser.parse_args()

    z_min = max(1, min(args.z_min, KNOWN_ELEMENT_MAX))
    z_max = max(z_min, min(args.z_max, KNOWN_ELEMENT_MAX))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0
    for z in range(z_min, z_max + 1):
        path = frame_path(z)
        if path.exists() and not args.force:
            skipped += 1
            continue
        render_frame(z)
        written += 1

    print(f"Done: {written} written, {skipped} skipped → {OUT_DIR}")


if __name__ == "__main__":
    main()