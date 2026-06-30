"""Monster group irrep fingerprint tab — supersingular prime heatmap."""

from __future__ import annotations

from kingdom.viz.monster_irreps import build_monster_irrep_heatmap

MONSTER_INTRO_MD = """
### Monster Fingerprints

Interactive view of [**irreps_sum.tsv**](https://github.com/meta-introspector/monster/blob/main/irreps_sum.tsv)
from [meta-introspector/monster](https://github.com/meta-introspector/monster): the **194 irreducible
representations** of the Monster group **M**, encoded as exponent vectors over the
**15 supersingular primes**.

| Axis | Meaning |
|------|---------|
| **Rows** | Irrep index (0–193) with total exponent mass |
| **Columns** | Primes 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71 |
| **Cell value** | Exponent of that prime in the irrep **degree** (OEIS [A001379](https://oeis.org/A001379)) |

This is a **finite symmetry manifold** companion to the 118-element toroidal coil — not a physics
claim, but a rigorously defined second topology for exploration. Hover any cell for degree,
factorization, and exponent sum.
"""

MOONSHINE_ANCHOR_MD = """
#### Monstrous Moonshine anchor

The first non-trivial Monster irrep has degree **196883**. Modular moonshine gives:

$$
j(\\tau) = q^{-1} + 744 + 196884\\,q + \\cdots
$$

so **196884 = 196883 + 1** — the famous coefficient tying the **j-invariant** to the Monster.
Kingdom Come’s harmonic invariants ($W_g = 350/\\pi$, flux flywheel locks, toroidal periodic topology)
sit in the same conceptual family: **closed topologies with quantized stability thresholds**.

*Data: [meta-introspector/monster](https://github.com/meta-introspector/monster) ·
degrees: [OEIS A001379](https://oeis.org/A001379)*
"""


def render_monster_heatmap(
    sort_mode: str,
    color_mode: str,
    highlight_irrep: float,
):
    highlight = int(highlight_irrep) if int(highlight_irrep) >= 0 else None
    mode_map = {
        "Exponent sum (heavy first)": "exponent_sum_desc",
        "Irrep index (0–193)": "irrep_index_asc",
        "Degree (ascending)": "degree_asc",
        "Degree (descending)": "degree_desc",
    }
    sort_key = mode_map.get(sort_mode, "exponent_sum_desc")
    return build_monster_irrep_heatmap(
        sort_mode=sort_key,  # type: ignore[arg-type]
        color_mode=color_mode,
        highlight_irrep=highlight,
    )