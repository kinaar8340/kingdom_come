"""Toroidal Periodic × Flux Flywheel hybrid tab."""

from __future__ import annotations

from pathlib import Path

from kingdom.viz.hopf_plotly import is_hf_space
from kingdom.viz.toroidal_periodic import build_toroidal_periodic_figure

TOROIDAL_DIR = Path(__file__).resolve().parents[1] / "assets" / "toroidal"
TOROIDAL_HYBRID_IMAGE = TOROIDAL_DIR / "toroidal_flux_hybrid.png"

TOROIDAL_GALLERY: tuple[tuple[Path, str], ...] = (
    (
        TOROIDAL_HYBRID_IMAGE,
        "Torus of Atomic Worlds — (1,7) coil × flux flywheel halos (Imagine Prompt 1)",
    ),
)

TOROIDAL_INTRO_MD = """
### Toroidal Periodic Table × Flux Flywheel

A **hybrid exploration** bridging the global toroidal (1,7) coil layout
(@introsp3ctor-style periodic manifold) with Kingdom Come’s per-element **flux flywheel**
stability scores and block color-coding.

| Layer | Meaning |
|-------|---------|
| **Wireframe torus** | Closed periodic topology — no rectangular boundaries |
| **Gold coil path** | Continuous (1,7) winding through all 118 elements |
| **Marker size** | Flux flywheel stability score (larger = more stable) |
| **Gold halos** | Noble-gas closed-shell locks |
| **Dashed/solid rings** | Local flux flywheel metaphor at selected / high-stability sites |
| **Period banding** | Faint color wash along the gold coil by IUPAC period |
| **Focus mode** | Dims the manifold to spotlight one element + its flux ring |
| **Hover** | Electron config, stability class, and chemistry ↔ flux note |
| **Manifold view** | Elements only · Monster irrep coil (194) · **Dual overlay** (gold + purple coils) |
| **Z↔irrep map** | Exploratory pairing schemes (linear, stability rank, noble lock, period×group) |

Use **Highlight Z** to inspect one element, then **Open in Flux Flywheel** for full
electron-shell + validation detail. In **Dual overlay**, dashed violet links connect Z to
its mapped Monster irrep (see **Monster Fingerprints** for the exponent heatmap).
"""

TOROIDAL_HF_NOTE_MD = """
**Rendering:** 2D projection on Hugging Face (no WebGL). Clone the
[GitHub repo](https://github.com/kinaar8340/kingdom_come) for interactive 3D rotation locally.
"""


def render_toroidal_periodic(
    z_highlight: int,
    major_r: float,
    minor_r: float,
    show_wireframe: bool,
    show_coil: bool,
    show_flux_rings: bool,
    show_noble_locks: bool,
    show_labels: bool,
    show_period_bands: bool,
    focus_mode: bool,
    projection_2d: str,
    manifold_view: str,
    z_irrep_mapping: str,
    show_z_irrep_links: bool,
    show_all_z_irrep_links: bool,
    view_mode: str,
):
    mode = "2d" if is_hf_space() or str(view_mode).lower().startswith("2") else "3d"
    z_val = int(z_highlight)
    proj = str(projection_2d).lower()
    if proj.startswith("xz"):
        projection: str = "xz"
    elif proj.startswith("yz"):
        projection = "yz"
    else:
        projection = "xy"
    return build_toroidal_periodic_figure(
        z_highlight=z_val if z_val >= 1 else None,
        major_r=float(major_r),
        minor_r=float(minor_r),
        show_wireframe=show_wireframe,
        show_coil=show_coil,
        show_flux_rings=show_flux_rings,
        show_noble_locks=show_noble_locks,
        show_labels=show_labels,
        show_period_bands=show_period_bands,
        focus_mode=bool(focus_mode),
        projection_2d=projection,  # type: ignore[arg-type]
        manifold_mode=manifold_view,
        z_irrep_scheme=z_irrep_mapping,
        show_z_irrep_links=bool(show_z_irrep_links),
        show_all_z_irrep_links=bool(show_all_z_irrep_links),
        view_mode=mode,  # type: ignore[arg-type]
    )