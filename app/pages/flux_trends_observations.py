"""Periodic flux flywheel validation trends — Observations tab."""

from __future__ import annotations

import pandas as pd

from kingdom.viz.observations_trends import (
    DEFAULT_TREND_PERIODS,
    load_observations_trend_dataframes,
)

FLUX_TRENDS_MD = """
### Periodic Trends & Model Validation

Cross-table views of how the flux flywheel model tracks laboratory observables.
Points are colored by **period**; fidelity uses overall comparison score (μ 28% · IE 22% · radius 18% · EA 16% · EN 16%).

| Plot | What it shows |
|------|----------------|
| **Fidelity vs Z** | Where the full validation stack agrees with experiment |
| **Stability vs IE** | Global correlation of model stability with real ionization energy |
| **Stability vs Allen EN** | Period-relative stability proxy vs Allen electronegativity |
| **SOC μ vs Experimental** | Visual check of spin-orbit magnetic moment improvement |

**Drag a narrow region on any point** to jump that element in the **Flux Flywheel** tab. Use the period filter to focus on specific rows.
"""


def _normalize_periods(periods: list[str] | list[int] | None) -> tuple[int, ...]:
    if not periods:
        return DEFAULT_TREND_PERIODS
    return tuple(sorted({int(p) for p in periods}))


def render_flux_trend_plots(
    periods: list[str] | list[int] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Build all four validation trend tables for Gradio ScatterPlot outputs."""
    return load_observations_trend_dataframes(118, _normalize_periods(periods))