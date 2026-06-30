"""Monster irrep representation complexity proxy for Flux Flywheel (exploratory)."""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd

from kingdom.data.monster_a001379 import MONSTER_IRREP_DEGREES

_IRREPS_TSV = (
    Path(__file__).resolve().parents[3] / "app" / "assets" / "monster" / "irreps_sum.tsv"
)
_MAX_EXPONENT_SUM = 56
_DEFAULT_SCHEME_LABEL = "linear Z−1 (exploratory)"


@lru_cache(maxsize=1)
def _irrep_table() -> pd.DataFrame:
    df = pd.read_csv(_IRREPS_TSV, sep="\t")
    df = df.rename(columns={"A001379index": "irrep_index"})
    df["degree"] = [MONSTER_IRREP_DEGREES[int(i)] for i in df["irrep_index"]]
    return df.set_index("irrep_index")


def irrep_index_for_z(z: int) -> tuple[int, bool]:
    """Return (irrep_index 0–193, extrapolated_beyond_118)."""
    z_val = int(z)
    if 1 <= z_val <= 118:
        return z_val - 1, False
    if z_val > 118:
        return (z_val - 1) % 194, True
    return 0, True


def _format_degree(degree: int) -> str:
    if degree < 1_000_000:
        return f"{degree:,}"
    exp = int(math.floor(math.log10(float(degree))))
    mant = degree / 10**exp
    return f"{mant:.3g}×10^{exp}"


def representation_complexity_payload(
    z: int,
    *,
    stability_score: float | None = None,
) -> dict[str, Any]:
    """
    Build Monster representation complexity fields for a flux flywheel record.

    Uses linear Z−1 → irrep mapping for Z ≤ 118; modular fallback for superheavy.
    """
    irrep_index, extrapolated = irrep_index_for_z(z)
    row = _irrep_table().loc[irrep_index]
    exp_sum = int(row["row_exponent_sum"])
    degree = int(row["degree"])
    complexity = round(10.0 * exp_sum / _MAX_EXPONENT_SUM, 1)

    delta = None
    if stability_score is not None:
        delta = round(float(stability_score) - complexity, 1)

    degree_str = _format_degree(degree)
    map_note = (
        f"mod {(z - 1) % 194} beyond known elements"
        if extrapolated
        else f"irrep {irrep_index} via {_DEFAULT_SCHEME_LABEL}"
    )
    tooltip = (
        f"Monster irrep {irrep_index} — {map_note}. "
        f"Prime exponent sum {exp_sum}/{_MAX_EXPONENT_SUM} → "
        f"representation complexity {complexity}/10. "
        f"Degree ≈ {degree_str}. "
    )
    if delta is not None:
        tooltip += (
            f"Flux stability {stability_score:.1f}/10 "
            f"(Δ flux−rep {delta:+.1f}). "
        )
    tooltip += (
        "Finite symmetry fingerprint (meta-introspector/monster); "
        "not a laboratory observable. Other maps in Toroidal Periodic tab."
    )

    return {
        "rep_irrep_index": irrep_index,
        "rep_exponent_sum": exp_sum,
        "rep_complexity_score": complexity,
        "rep_degree": degree,
        "rep_degree_display": degree_str,
        "rep_mapping_label": _DEFAULT_SCHEME_LABEL,
        "rep_extrapolated": extrapolated,
        "rep_flux_delta": delta,
        "rep_complexity_tooltip": tooltip,
    }


def attach_representation_complexity(record: dict[str, Any], z: int) -> dict[str, Any]:
    """Merge representation complexity fields into a flywheel/extended dict."""
    payload = representation_complexity_payload(
        z,
        stability_score=record.get("stability_score"),
    )
    return {**record, **payload}