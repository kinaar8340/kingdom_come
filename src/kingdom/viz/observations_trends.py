"""Periodic trend plots for flux flywheel model validation."""

from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from kingdom.core.elements import get_element
from kingdom.core.experimental_data import get_period
from kingdom.core.flux_explorer import build_observables_validation
from kingdom.core.flux_flywheel import map_z_to_flywheel_extended
from kingdom.core.periodic_meta import period_group_category
from kingdom.viz.hopf_plotly import kingdom_dark_theme

_PERIOD_COLORS = (
    "#1a8fe3",
    "#00c9b7",
    "#4cc9f0",
    "#ffd45a",
    "#ffb4a2",
    "#c77dff",
    "#48bfe3",
    "#ef553b",
)


@lru_cache(maxsize=4)
def observations_trends_dataframe(z_max: int = 118) -> pd.DataFrame:
    """Build validation metrics for Z = 1 … z_max (cached)."""
    records: list[dict] = []
    for z in range(1, z_max + 1):
        extended = map_z_to_flywheel_extended(z)
        validation = build_observables_validation(z, extended)
        element = get_element(z)
        symbol = element.symbol if element else f"Z{z}"
        name = element.name if element else f"Z = {z}"
        period = get_period(z)
        if z <= 118:
            _p, _g, category = period_group_category(z)
        else:
            category = "superheavy"

        comps = validation["comparisons"]
        mu_cmp = comps["magnetic_moment"]
        details = validation["fidelity_details"]

        records.append({
            "Z": z,
            "element": symbol,
            "name": name,
            "period": period,
            "category": category,
            "fidelity_score": validation["fidelity_score"],
            "magnetic_moment_score": details.get("magnetic_moment"),
            "ie_score": details.get("ionization_energy"),
            "ea_score": details.get("electron_affinity"),
            "model_stability": extended["stability_score"],
            "experimental_ie": extended["real_ionization_energy_eV"],
            "soc_mu_BM": extended.get("magnetic_moment_soc_BM"),
            "experimental_mu_BM": mu_cmp.get("experimental_value")
            if mu_cmp.get("available")
            else None,
            "mu_exp_available": mu_cmp.get("available", False),
        })

    return pd.DataFrame(records)


def _apply_dark_theme(fig: go.Figure, *, height: int = 440) -> go.Figure:
    fig.update_layout(**kingdom_dark_theme(), height=height)
    fig.update_xaxes(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f")
    fig.update_yaxes(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f")
    return fig


def create_fidelity_trend_plot(data: pd.DataFrame | None = None) -> go.Figure:
    """Fidelity score vs atomic number, colored by period."""
    df = observations_trends_dataframe() if data is None else data
    plot_df = df.dropna(subset=["fidelity_score"]).copy()
    fig = go.Figure()

    for i, period in enumerate(sorted(plot_df["period"].unique())):
        sub = plot_df[plot_df["period"] == period]
        color = _PERIOD_COLORS[int(period - 1) % len(_PERIOD_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=sub["Z"],
                y=sub["fidelity_score"],
                mode="markers",
                name=f"Period {int(period)}",
                marker=dict(size=9, color=color, line=dict(width=0.5, color="#0a1628")),
                customdata=np.stack(
                    [sub["element"], sub["magnetic_moment_score"], sub["ie_score"]],
                    axis=-1,
                ),
                hovertemplate=(
                    "%{customdata[0]} (Z=%{x})<br>"
                    "Fidelity: %{y:.1f}/10<br>"
                    "μ score: %{customdata[1]}<br>"
                    "IE score: %{customdata[2]}<extra></extra>"
                ),
            )
        )

    fig.add_hline(y=8.5, line_dash="dash", line_color="#00c9b7", opacity=0.7)
    fig.add_hline(y=7.0, line_dash="dash", line_color="#ffd45a", opacity=0.7)
    fig.add_annotation(
        x=0.99,
        y=8.55,
        xref="paper",
        yref="y",
        text="Excellent (8.5)",
        showarrow=False,
        font=dict(size=10, color="#00c9b7"),
        xanchor="right",
    )
    fig.add_annotation(
        x=0.99,
        y=7.05,
        xref="paper",
        yref="y",
        text="Good (7.0)",
        showarrow=False,
        font=dict(size=10, color="#ffd45a"),
        xanchor="right",
    )

    fig.update_layout(
        title="Comparison Fidelity Score vs Atomic Number",
        xaxis_title="Atomic Number (Z)",
        yaxis_title="Fidelity Score (0–10)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return _apply_dark_theme(fig)


def create_stability_vs_ie_plot(data: pd.DataFrame | None = None) -> go.Figure:
    """Model stability vs experimental IE with OLS trend and Pearson r."""
    df = observations_trends_dataframe() if data is None else data
    fig = go.Figure()

    for i, period in enumerate(sorted(df["period"].unique())):
        sub = df[df["period"] == period]
        color = _PERIOD_COLORS[int(period - 1) % len(_PERIOD_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=sub["model_stability"],
                y=sub["experimental_ie"],
                mode="markers",
                name=f"Period {int(period)}",
                marker=dict(size=8, color=color, line=dict(width=0.5, color="#0a1628")),
                customdata=np.stack([sub["element"], sub["Z"], sub["fidelity_score"]], axis=-1),
                hovertemplate=(
                    "%{customdata[0]} (Z=%{customdata[1]})<br>"
                    "Stability: %{x:.2f}<br>"
                    "IE: %{y:.2f} eV<br>"
                    "Fidelity: %{customdata[2]}<extra></extra>"
                ),
            )
        )

    x = df["model_stability"].to_numpy(dtype=float)
    y = df["experimental_ie"].to_numpy(dtype=float)
    if len(x) >= 2:
        coef = np.polyfit(x, y, 1)
        x_line = np.linspace(float(x.min()), float(x.max()), 60)
        y_line = coef[0] * x_line + coef[1]
        corr = float(np.corrcoef(x, y)[0, 1])
        fig.add_trace(
            go.Scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                name="OLS trend",
                line=dict(color="#8ecae6", width=2, dash="dash"),
                hoverinfo="skip",
            )
        )
        fig.add_annotation(
            x=0.03,
            y=0.97,
            xref="paper",
            yref="paper",
            text=f"Pearson r = {corr:+.3f}",
            showarrow=False,
            font=dict(size=12, color="#8ecae6"),
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(10, 22, 40, 0.75)",
            bordercolor="#1e3a5f",
            borderwidth=1,
        )

    fig.update_layout(
        title="Model Stability Score vs Experimental Ionization Energy",
        xaxis_title="Model Stability Score",
        yaxis_title="Experimental IE (eV)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return _apply_dark_theme(fig)


def create_soc_mu_vs_experimental_plot(data: pd.DataFrame | None = None) -> go.Figure:
    """SOC magnetic moment vs experimental μ (elements with anchors)."""
    df = observations_trends_dataframe() if data is None else data
    plot_df = df[df["mu_exp_available"]].dropna(subset=["soc_mu_BM", "experimental_mu_BM"]).copy()
    fig = go.Figure()

    if plot_df.empty:
        fig.add_annotation(
            text="No experimental μ anchors in range",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=13, color="#8ecae6"),
        )
        return _apply_dark_theme(fig, height=380)

    max_mu = float(
        max(plot_df["soc_mu_BM"].max(), plot_df["experimental_mu_BM"].max()) * 1.05
    )
    fig.add_trace(
        go.Scatter(
            x=[0, max_mu],
            y=[0, max_mu],
            mode="lines",
            name="Perfect agreement",
            line=dict(color="#6a9bb8", width=1, dash="dot"),
            hoverinfo="skip",
        )
    )

    for i, period in enumerate(sorted(plot_df["period"].unique())):
        sub = plot_df[plot_df["period"] == period]
        color = _PERIOD_COLORS[int(period - 1) % len(_PERIOD_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=sub["experimental_mu_BM"],
                y=sub["soc_mu_BM"],
                mode="markers",
                name=f"Period {int(period)}",
                marker=dict(size=9, color=color, line=dict(width=0.5, color="#0a1628")),
                customdata=np.stack([sub["element"], sub["Z"]], axis=-1),
                hovertemplate=(
                    "%{customdata[0]} (Z=%{customdata[1]})<br>"
                    "Exp μ: %{x:.2f} BM<br>"
                    "SOC μ: %{y:.2f} BM<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title="SOC Magnetic Moment vs Experimental μ",
        xaxis_title="Experimental μ (BM)",
        yaxis_title="SOC μ (BM)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return _apply_dark_theme(fig, height=380)


def load_observations_trend_figures(z_max: int = 118) -> tuple[go.Figure, go.Figure, go.Figure]:
    """Return (fidelity trend, stability vs IE, SOC μ validation) figures."""
    df = observations_trends_dataframe(z_max)
    return (
        create_fidelity_trend_plot(df),
        create_stability_vs_ie_plot(df),
        create_soc_mu_vs_experimental_plot(df),
    )