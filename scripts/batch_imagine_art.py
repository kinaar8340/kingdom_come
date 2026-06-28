#!/usr/bin/env python3
"""Parse Imagine prompts and report batch import status."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.elements import EXPLORER_Z_MAX, KNOWN_ELEMENT_MAX, get_element

PROMPTS_KNOWN = ROOT / "app" / "assets" / "elements" / "imagine_prompts.txt"
PROMPTS_SH = ROOT / "app" / "assets" / "elements" / "imagine_prompts_superheavy.txt"
INBOX = ROOT / "app" / "assets" / "elements_imagine"
SH_INBOX = INBOX / "superheavy"
MANIFEST = INBOX / "batch_manifest.json"

_LINE = re.compile(r"^Z=(\d+)\s+\((\w+)\):\s*(.+)$", re.MULTILINE)


def _parse_prompts(path: Path) -> dict[int, dict]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    out: dict[int, dict] = {}
    for z_s, sym, prompt in _LINE.findall(text):
        z = int(z_s)
        out[z] = {"symbol": sym, "prompt": prompt.strip()}
    return out


def _inbox_path(z: int, symbol: str) -> Path:
    el = get_element(z)
    folder = SH_INBOX if el and el.is_synthetic else INBOX
    return folder / f"{symbol.lower()}.png"


def build_manifest() -> dict:
    prompts = _parse_prompts(PROMPTS_KNOWN)
    prompts.update(_parse_prompts(PROMPTS_SH))
    entries = []
    for z in range(1, EXPLORER_Z_MAX + 1):
        el = get_element(z)
        if el is None:
            continue
        meta = prompts.get(z, {})
        sym = meta.get("symbol", el.symbol)
        path = _inbox_path(z, sym)
        imported = (ROOT / "app" / "assets" / "elements" / f"{sym.lower()}.png").is_file()
        inbox = path.is_file()
        entries.append(
            {
                "z": z,
                "symbol": sym,
                "name": el.name,
                "synthetic": el.is_synthetic,
                "prompt": meta.get("prompt", ""),
                "inbox": str(path.relative_to(ROOT)),
                "inbox_ready": inbox,
                "imported": imported,
            }
        )
    ready = sum(1 for e in entries if e["inbox_ready"])
    return {
        "total": len(entries),
        "inbox_ready": ready,
        "pending": len(entries) - ready,
        "entries": entries,
    }


def main() -> None:
    manifest = build_manifest()
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Manifest: {MANIFEST}")
    print(f"Imagine inbox ready: {manifest['inbox_ready']}/{manifest['total']}")
    print(f"Pending: {manifest['pending']}")
    pending = [e for e in manifest["entries"] if not e["inbox_ready"]][:10]
    if pending:
        print("Next pending:")
        for e in pending:
            print(f"  Z={e['z']:3d} {e['symbol']:3s} -> {e['inbox']}")


if __name__ == "__main__":
    main()