#!/usr/bin/env python3
"""Convert session JPGs to elements_imagine PNGs and run import."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "app" / "assets" / "elements_imagine"
SH_INBOX = INBOX / "superheavy"


def ingest(mapping: dict[str, str], src_dir: Path) -> int:
    """mapping: source_filename -> dest_symbol.png (e.g. '8.jpg' -> 'h.png')"""
    count = 0
    for src_name, dst_name in mapping.items():
        src = src_dir / src_name
        if not src.is_file():
            print(f"Missing {src}")
            continue
        dst = (SH_INBOX if dst_name.startswith("superheavy/") else INBOX) / dst_name.replace("superheavy/", "")
        dst.parent.mkdir(parents=True, exist_ok=True)
        img = Image.open(src).convert("RGBA")
        w, h = img.size
        side = min(w, h)
        left, top = (w - side) // 2, (h - side) // 2
        img = img.crop((left, top, left + side, top + side)).resize((512, 512), Image.Resampling.LANCZOS)
        img.save(dst, format="PNG")
        print(f"Ingested {src_name} -> {dst}")
        count += 1
    return count


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: ingest_imagine_batch.py <session_images_dir> <mapping.json>")
        sys.exit(1)
    src_dir = Path(sys.argv[1])
    mapping = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    n = ingest(mapping, src_dir)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "import_imagine_art.py")], check=True)
    print(f"Batch ingest complete ({n} files)")


if __name__ == "__main__":
    main()