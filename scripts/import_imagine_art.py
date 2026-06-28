#!/usr/bin/env python3
"""Import Grok Imagine PNGs from inbox folders into element asset paths.

Expected inbox layout (any of these filenames per element):
  app/assets/elements_imagine/he.png
  app/assets/elements_imagine/002_he.png
  app/assets/elements_imagine/Z002.png

Superheavy:
  app/assets/elements_imagine/superheavy/uue.png
  app/assets/superheavy_imagine/uue.png
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.elements import EXPLORER_Z_MAX, get_element

INBOX = ROOT / "app" / "assets" / "elements_imagine"
SH_INBOX = ROOT / "app" / "assets" / "superheavy_imagine"
OUT_ELEMENTS = ROOT / "app" / "assets" / "elements"
OUT_SUPERHEAVY = ROOT / "app" / "assets" / "superheavy"


def _match_z(path: Path) -> int | None:
    name = path.stem.lower()
    by_symbol = {get_element(z).symbol.lower(): z for z in range(1, EXPLORER_Z_MAX + 1) if get_element(z)}
    if name in by_symbol:
        return by_symbol[name]
    m = re.search(r"(\d{1,3})", name)
    if m:
        z = int(m.group(1))
        if get_element(z):
            return z
    return None


def _import_folder(folder: Path, *, superheavy: bool = False) -> int:
    if not folder.is_dir():
        return 0
    count = 0
    for src in sorted(folder.glob("*.png")):
        z = _match_z(src)
        if z is None:
            print(f"Skip (unmatched): {src.name}")
            continue
        el = get_element(z)
        if el is None:
            continue
        dest = (OUT_SUPERHEAVY if superheavy or el.is_synthetic else OUT_ELEMENTS) / f"{el.symbol.lower()}.png"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        if el.is_synthetic:
            shutil.copy2(src, OUT_ELEMENTS / f"{el.symbol.lower()}.png")
        print(f"Imported Z={z} {el.symbol} -> {dest}")
        count += 1
    return count


def main() -> None:
    n = _import_folder(INBOX)
    n += _import_folder(INBOX / "superheavy", superheavy=True)
    n += _import_folder(SH_INBOX, superheavy=True)
    print(f"Imported {n} Imagine artwork file(s)")


if __name__ == "__main__":
    main()