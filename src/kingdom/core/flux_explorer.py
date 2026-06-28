"""Combined flux flywheel + element explorer."""

from __future__ import annotations

from kingdom.core.elements import get_element, is_real_element
from kingdom.core.flux_flywheel import map_z_to_flywheel
import plotly.graph_objects as go

from kingdom.viz.electron_cloud import build_chemistry_vs_toe_figure, build_electron_cloud_figure
from kingdom.viz.hopf_plotly import BG_DARK, kingdom_dark_theme


def _placeholder_figure(message: str, height: int = 300) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        **kingdom_dark_theme(),
        height=height,
        paper_bgcolor=BG_DARK,
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


def explore_flux_element(z: int) -> dict:
    """Full Flux Flywheel tab payload for atomic number Z."""
    flywheel = map_z_to_flywheel(int(z))
    element = get_element(int(z)) if is_real_element(int(z)) else None

    metrics_md = (
        f"### Flux metrics (Z = {z})\n\n"
        f"- **Stability score:** {flywheel['stability_score']}\n"
        f"- **Class:** {flywheel['stability_class']}\n"
        f"- **δω:** {flywheel['delta_omega']} · **ω_L:** {flywheel['omega_L']} · "
        f"**ω_R:** {flywheel['omega_R']}\n"
        f"- **Gauge:** {flywheel['gauge_strength']} · **Layers:** {flywheel['num_layers']} · "
        f"**Polarities:** {flywheel['num_polarities']}\n"
        f"- **pseudo_Z (sweep ID):** {flywheel['pseudo_Z']}\n"
        f"- **Notes:** {flywheel['notes']}\n"
        f"- *{flywheel['sweep_reference']}*\n"
    )

    if element is None:
        cloud = _placeholder_figure("No standard element — flux metrics only (Z ∉ 1–118)")
        compare = _placeholder_figure("Synthetic Z — no chemistry comparison", height=220)
    else:
        cloud = build_electron_cloud_figure(element, stability_score=flywheel["stability_score"])
        compare = build_chemistry_vs_toe_figure(element, flywheel["stability_score"])

    return {
        "flywheel": flywheel,
        "element": element,
        "metrics_md": metrics_md,
        "cloud_fig": cloud,
        "compare_fig": compare,
    }