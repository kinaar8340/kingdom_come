"""Exploratory Z ↔ Monster irrep mappings for the toroidal hybrid."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from kingdom.core.elements import NOBLE_GAS_Z
from kingdom.core.periodic_meta import period_group_category
from kingdom.viz.monster_irreps import load_monster_irreps_table
from kingdom.viz.toroidal_periodic import Z_MAX, coil_uv, torus_point

IRREP_MAX = 194

ZIrrepScheme = Literal["linear", "stability_rank", "noble_lock", "period_group"]
ManifoldMode = Literal["elements", "irreps", "dual"]


@lru_cache(maxsize=8)
def z_to_irrep_map(scheme: ZIrrepScheme) -> dict[int, int]:
    """Map atomic number Z (1–118) → Monster irrep index (0–193). Exploratory only."""
    if scheme == "linear":
        return {z: z - 1 for z in range(1, Z_MAX + 1)}

    if scheme == "period_group":
        out: dict[int, int] = {}
        for z in range(1, Z_MAX + 1):
            period, group, _ = period_group_category(z)
            out[z] = ((period - 1) * 18 + (group - 1)) % IRREP_MAX
        return out

    df = load_monster_irreps_table()
    by_sum = df.sort_values(["row_exponent_sum", "irrep_index"])
    irrep_low_to_high = [int(i) for i in by_sum["irrep_index"]]

    if scheme == "stability_rank":
        from kingdom.viz.toroidal_periodic import _element_layout

        elements = sorted(_element_layout(), key=lambda r: (r["stability"], r["z"]))
        return {
            int(row["z"]): irrep_low_to_high[i]
            for i, row in enumerate(elements)
        }

    # noble_lock: lowest-exponent irreps ↔ noble gases; others stability-ranked on remainder
    nobles = sorted(NOBLE_GAS_Z)
    noble_irreps = irrep_low_to_high[: len(nobles)]
    used = set(noble_irreps)
    remaining_irreps = [i for i in irrep_low_to_high if i not in used]
    from kingdom.viz.toroidal_periodic import _element_layout

    non_nobles = sorted(
        [r for r in _element_layout() if r["z"] not in NOBLE_GAS_Z],
        key=lambda r: (r["stability"], r["z"]),
    )
    mapping = {z: noble_irreps[i] for i, z in enumerate(nobles)}
    for i, row in enumerate(non_nobles):
        mapping[int(row["z"])] = remaining_irreps[i % len(remaining_irreps)]
    return mapping


def irrep_for_z(z: int, scheme: ZIrrepScheme) -> int:
    z_clamped = max(1, min(Z_MAX, int(z)))
    return z_to_irrep_map(scheme)[z_clamped]


def _complexity_color(exponent_sum: int, *, max_sum: int = 56) -> str:
    t = max(0.0, min(1.0, exponent_sum / max_sum))
    # deep purple → teal → gold
    if t < 0.5:
        u = t / 0.5
        r = int(60 + u * (0 - 60))
        g = int(40 + u * (201 - 40))
        b = int(100 + u * (183 - 100))
    else:
        u = (t - 0.5) / 0.5
        r = int(0 + u * (201 - 0))
        g = int(201 + u * (162 - 201))
        b = int(183 + u * (39 - 183))
    return f"rgb({r},{g},{b})"


def irrep_toroidal_layout(
    *,
    major_r: float = 2.15,
    minor_r: float = 0.55,
) -> list[dict]:
    """(1,7) coil placement for 194 Monster irreps on a secondary torus."""
    df = load_monster_irreps_table().set_index("irrep_index")
    rows: list[dict] = []
    for slot in range(1, IRREP_MAX + 1):
        irrep_index = slot - 1
        row = df.loc[irrep_index]
        u, v = coil_uv(slot, z_max=IRREP_MAX)
        x, y, zc = torus_point(u, v, major_r=major_r, minor_r=minor_r)
        exp_sum = int(row["row_exponent_sum"])
        rows.append({
            "irrep_index": irrep_index,
            "slot": slot,
            "degree": int(row["degree"]),
            "row_exponent_sum": exp_sum,
            "x": x,
            "y": y,
            "zc": zc,
            "u": u,
            "v": v,
            "color": _complexity_color(exp_sum),
            "label": str(irrep_index),
        })
    return rows


def irrep_hover(row: dict) -> str:
    return (
        f"<b>Irrep {row['irrep_index']}</b> (slot {row['slot']}/194)<br>"
        f"Degree: {row['degree']:,}<br>"
        f"Exponent sum: {row['row_exponent_sum']}"
    )