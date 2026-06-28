"""Combined flux flywheel + element explorer."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import plotly.graph_objects as go

from kingdom.core.elements import NOBLE_GAS_Z, get_element, is_real_element
from kingdom.core.flux_flywheel import map_z_to_flywheel
from kingdom.viz.electron_cloud import build_chemistry_vs_toe_figure, build_electron_cloud_figure
from kingdom.viz.hopf_plotly import kingdom_dark_theme
from kingdom.viz.magic_island import build_magic_island_heatmap

_ASSETS = Path(__file__).resolve().parents[3] / "app" / "assets" / "noble_gases"


def _placeholder_figure(message: str, height: int = 300) -> go.Figure:
    fig = go.Figure()
    theme = kingdom_dark_theme()
    fig.update_layout(
        **theme,
        height=height,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=13, color="#8ecae6"),
    )
    return fig


@lru_cache(maxsize=256)
def _cached_electron_cloud(z: int, stability: float) -> dict:
    element = get_element(z)
    if element is None:
        fig = _placeholder_figure("No standard element — flux metrics only (Z ∉ 1–118)")
    else:
        fig = build_electron_cloud_figure(element, stability_score=stability)
    return fig.to_dict()


@lru_cache(maxsize=256)
def _cached_compare_figure(z: int, stability: float) -> dict:
    element = get_element(z)
    if element is None:
        fig = _placeholder_figure("Synthetic Z — no chemistry comparison", height=220)
    else:
        fig = build_chemistry_vs_toe_figure(element, stability)
    return fig.to_dict()


def noble_gas_art_path(z: int) -> str | None:
    """Return path to pre-generated noble-gas artwork, or None."""
    if z not in NOBLE_GAS_Z:
        return None
    el = get_element(z)
    if el is None:
        return None
    for name in (el.symbol.lower(), el.symbol):
        path = _ASSETS / f"{name}.png"
        if path.is_file():
            return str(path)
    return None


def explore_flux_element(z: int) -> dict:
    """Full Flux Flywheel tab payload for atomic number Z."""
    z = max(1, min(180, int(z)))
    flywheel = map_z_to_flywheel(z)
    element = get_element(z) if is_real_element(z) else None
    stability = flywheel["stability_score"]

    metrics_md = (
        f"### Flux metrics (Z = {z})\n\n"
        f"- **Stability score:** {stability}\n"
        f"- **Class:** {flywheel['stability_class']}\n"
        f"- **δω:** {flywheel['delta_omega']} · **ω_L:** {flywheel['omega_L']} · "
        f"**ω_R:** {flywheel['omega_R']}\n"
        f"- **Gauge:** {flywheel['gauge_strength']} · **Layers:** {flywheel['num_layers']} · "
        f"**Polarities:** {flywheel['num_polarities']}\n"
        f"- **pseudo_Z (sweep ID):** {flywheel['pseudo_Z']}\n"
        f"- **Notes:** {flywheel['notes']}\n"
        f"- *{flywheel['sweep_reference']}*\n"
    )

    return {
        "z": z,
        "flywheel": flywheel,
        "element": element,
        "metrics_md": metrics_md,
        "cloud_fig": _cached_electron_cloud(z, stability),
        "compare_fig": _cached_compare_figure(z, stability),
        "magic_island": build_magic_island_heatmap(z).to_dict(),
        "noble_gas_art": noble_gas_art_path(z),
        "is_noble": z in NOBLE_GAS_Z,
        "is_magic": element.is_magic_number if element else False,
        "is_synthetic": element is None or z > 118,
        "is_pseudo_z": z == 129,
    }