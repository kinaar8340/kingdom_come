"""Periodic flux flywheel validation trends — Observations tab."""

from __future__ import annotations

import plotly.graph_objects as go

from kingdom.viz.observations_trends import load_observations_trend_figures

FLUX_TRENDS_MD = """
### Periodic Trends & Model Validation

Cross-table views of how the flux flywheel model tracks laboratory observables.
Points are colored by **period**; fidelity uses the composite score (μ 50% · IE 30% · EA 20%).

| Plot | What it shows |
|------|----------------|
| **Fidelity vs Z** | Where the full validation stack agrees with experiment |
| **Stability vs IE** | Global correlation of model stability with real ionization energy |
| **SOC μ vs Experimental** | Visual check of spin-orbit magnetic moment improvement |

Trends load once when you open this section (Z = 1–118).
"""


def render_flux_trend_plots() -> tuple[go.Figure, go.Figure, go.Figure]:
    """Build all three validation trend figures for Gradio Plot outputs."""
    return load_observations_trend_figures(118)