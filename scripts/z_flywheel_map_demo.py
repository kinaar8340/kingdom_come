#!/usr/bin/env python3
"""Demo: extended flux flywheel mapping with real atomic observables."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.flux_flywheel import map_z_to_flywheel_extended

DEMO_Z = (2, 10, 26, 79, 118)


def main() -> None:
    print("Extended Flux Flywheel Mapping — Model + Real Observables\n")
    for z in DEMO_Z:
        result = map_z_to_flywheel_extended(z)
        print(f"Z = {z:3d}")
        print(
            f"  Flywheel: Score={result['stability_score']:.1f} | "
            f"{result['stability_class']}"
        )
        print(
            f"  Real:     IE={result['real_ionization_energy_eV']:.2f} eV | "
            f"Unpaired e⁻={result['unpaired_electrons']} | "
            f"μ={result['magnetic_moment_BM']:.2f} BM"
        )
        print(f"  Alignment: {result['model_vs_reality_alignment']:.1f}/10")
        print(f"  → {result['validation_notes']}\n")


if __name__ == "__main__":
    main()