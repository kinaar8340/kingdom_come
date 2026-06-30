"""Periodic flux flywheel validation trends — Observations tab."""

from __future__ import annotations

import plotly.graph_objects as go

from kingdom.viz.observations_trends import (
    DEFAULT_TREND_PERIODS,
    load_observations_trend_figures,
)

FLUX_TRENDS_MD = """
### Periodic Trends & Model Validation

Cross-table views of how the flux flywheel model tracks laboratory observables.
Points are colored by **period**; fidelity uses the composite score (μ 48% · IE 28% · EA 12% · radius 12%).

| Plot | What it shows |
|------|----------------|
| **Fidelity vs Z** | Where the full validation stack agrees with experiment |
| **Stability vs IE** | Global correlation of model stability with real ionization energy |
| **SOC μ vs Experimental** | Visual check of spin-orbit magnetic moment improvement |

**Click any point** to jump that element in the **Flux Flywheel** tab. Use the period filter to focus on specific rows.
"""


def _normalize_periods(periods: list[str] | list[int] | None) -> tuple[int, ...]:
    if not periods:
        return DEFAULT_TREND_PERIODS
    return tuple(sorted({int(p) for p in periods}))


def render_flux_trend_plots(
    periods: list[str] | list[int] | None = None,
) -> tuple[go.Figure, go.Figure, go.Figure]:
    """Build all three validation trend figures for Gradio Plot outputs."""
    return load_observations_trend_figures(118, _normalize_periods(periods))