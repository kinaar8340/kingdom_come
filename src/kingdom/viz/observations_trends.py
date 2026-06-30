"""Periodic trend plots for flux flywheel model validation."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from kingdom.core.elements import get_element
from kingdom.core.experimental_data import allen_electronegativity, get_period
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

PERIOD_COLOR_MAP: dict[str, str] = {
    str(period): _PERIOD_COLORS[(period - 1) % len(_PERIOD_COLORS)]
    for period in range(1, 8)
}

DEFAULT_TREND_PERIODS: tuple[int, ...] = tuple(range(1, 8))


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
            "en_score": details.get("electronegativity"),
            "ea_score": details.get("electron_affinity"),
            "radius_score": details.get("atomic_radius"),
            "experimental_en": allen_electronegativity(z),
            "model_stability": extended["stability_score"],
            "experimental_ie": extended["real_ionization_energy_eV"],
            "soc_mu_BM": extended.get("magnetic_moment_soc_BM"),
            "experimental_mu_BM": mu_cmp.get("experimental_value")
            if mu_cmp.get("available")
            else None,
            "mu_exp_available": mu_cmp.get("available", False),
        })

    return pd.DataFrame(records)


def filter_trends_by_period(
    df: pd.DataFrame,
    periods: list[int] | tuple[int, ...] | None,
) -> pd.DataFrame:
    """Subset trend dataframe to selected periods (all if empty/None)."""
    if not periods:
        return df
    period_set = {int(p) for p in periods}
    return df[df["period"].isin(period_set)].copy()


def _z_in_range(z: float | int) -> int | None:
    try:
        parsed = int(round(float(z)))
    except (TypeError, ValueError):
        return None
    if 1 <= parsed <= 180:
        return parsed
    return None


def _axis_bounds(index: tuple | list, start: int = 0) -> tuple[float, float] | None:
    try:
        lo = float(index[start])
        hi = float(index[start + 1])
    except (IndexError, TypeError, ValueError):
        return None
    return min(lo, hi), max(lo, hi)


def _pick_z_from_subset(sub: pd.DataFrame, df: pd.DataFrame, x_col: str, x_center: float) -> int | None:
    if sub.empty:
        idx = (df[x_col] - x_center).abs().idxmin()
        return _z_in_range(df.loc[idx, "Z"])
    if len(sub) == 1:
        return _z_in_range(sub.iloc[0]["Z"])
    idx = (sub[x_col] - x_center).abs().idxmin()
    return _z_in_range(sub.loc[idx, "Z"])


def z_from_scatter_select(
    evt: Any,
    df: pd.DataFrame,
    *,
    x_col: str = "Z",
    y_col: str | None = None,
) -> int | None:
    """
    Extract atomic number Z from a Gradio ScatterPlot region-select event.

    Native plots report axis bounds in ``SelectData.index``. When ``x_col`` is
    ``Z`` the midpoint is used directly; otherwise the matching row in ``df`` is
    resolved using optional ``y_col`` bounds when present.
    """
    if evt is None or getattr(evt, "selected", True) is False:
        return None
    if df is None or df.empty or "Z" not in df.columns or x_col not in df.columns:
        return None

    index = getattr(evt, "index", None)
    if not isinstance(index, (list, tuple)) or len(index) < 2:
        return z_from_plot_select(evt)

    x_bounds = _axis_bounds(index, 0)
    if x_bounds is None:
        return z_from_plot_select(evt)
    lo_x, hi_x = x_bounds
    x_center = (lo_x + hi_x) / 2

    if x_col == "Z":
        return _z_in_range(x_center)

    sub = df[(df[x_col] >= lo_x) & (df[x_col] <= hi_x)]
    if y_col and y_col in df.columns and len(index) >= 4:
        y_bounds = _axis_bounds(index, 2)
        if y_bounds is not None:
            lo_y, hi_y = y_bounds
            sub = sub[(sub[y_col] >= lo_y) & (sub[y_col] <= hi_y)]

    return _pick_z_from_subset(sub, df, x_col, x_center)


def z_from_plot_select(evt: Any) -> int | None:
    """Legacy Plotly customdata helper kept for unit tests."""
    if evt is None:
        return None

    value = getattr(evt, "value", None)
    if isinstance(value, (list, tuple)) and value:
        z = _z_in_range(value[0])
        if z is not None:
            return z

    index = getattr(evt, "index", None)
    if isinstance(index, (list, tuple)) and index:
        z = _z_in_range(index[0])
        if z is not None:
            return z

    return None


def fidelity_trend_dataframe(data: pd.DataFrame | None = None) -> pd.DataFrame:
    """ScatterPlot-ready fidelity vs Z table."""
    df = observations_trends_dataframe() if data is None else data
    plot_df = df.dropna(subset=["fidelity_score"]).copy()
    out = plot_df[
        ["Z", "element", "fidelity_score", "period", "magnetic_moment_score", "ie_score"]
    ].copy()
    out["period"] = out["period"].astype(int).astype(str)
    return out


def stability_ie_trend_dataframe(data: pd.DataFrame | None = None) -> pd.DataFrame:
    """ScatterPlot-ready stability vs experimental IE table."""
    df = observations_trends_dataframe() if data is None else data
    out = df[
        ["Z", "element", "model_stability", "experimental_ie", "period", "fidelity_score"]
    ].copy()
    out["period"] = out["period"].astype(int).astype(str)
    return out


def stability_en_trend_dataframe(data: pd.DataFrame | None = None) -> pd.DataFrame:
    """ScatterPlot-ready stability vs Allen electronegativity table."""
    df = observations_trends_dataframe() if data is None else data
    plot_df = df.dropna(subset=["experimental_en"]).copy()
    out = plot_df[
        [
            "Z",
            "element",
            "model_stability",
            "experimental_en",
            "period",
            "fidelity_score",
            "en_score",
        ]
    ].copy()
    out["period"] = out["period"].astype(int).astype(str)
    return out


def soc_mu_trend_dataframe(data: pd.DataFrame | None = None) -> pd.DataFrame:
    """ScatterPlot-ready SOC μ vs experimental μ table."""
    df = observations_trends_dataframe() if data is None else data
    plot_df = df[df["mu_exp_available"]].dropna(
        subset=["soc_mu_BM", "experimental_mu_BM"]
    ).copy()
    if plot_df.empty:
        return pd.DataFrame(
            columns=["Z", "element", "experimental_mu_BM", "soc_mu_BM", "period"]
        )
    out = plot_df[
        ["Z", "element", "experimental_mu_BM", "soc_mu_BM", "period"]
    ].copy()
    out["period"] = out["period"].astype(int).astype(str)
    return out


def load_observations_trend_dataframes(
    z_max: int = 118,
    periods: list[int] | tuple[int, ...] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return (fidelity, stability vs IE, stability vs EN, SOC μ) DataFrames."""
    df = filter_trends_by_period(observations_trends_dataframe(z_max), periods)
    return (
        fidelity_trend_dataframe(df),
        stability_ie_trend_dataframe(df),
        stability_en_trend_dataframe(df),
        soc_mu_trend_dataframe(df),
    )


def _apply_dark_theme(fig: go.Figure, *, height: int = 440) -> go.Figure:
    fig.update_layout(**kingdom_dark_theme(), height=height)
    fig.update_xaxes(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f")
    fig.update_yaxes(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f")
    fig.update_layout(
        clickmode="event+select",
        dragmode="zoom",
    )
    return fig


def create_fidelity_trend_plot(data: pd.DataFrame | None = None) -> go.Figure:
    """Fidelity score vs atomic number, colored by period."""
    df = observations_trends_dataframe() if data is None else data
    plot_df = df.dropna(subset=["fidelity_score"]).copy()
    fig = go.Figure()

    for period in sorted(plot_df["period"].unique()):
        sub = plot_df[plot_df["period"] == period].sort_values("Z")
        color = _PERIOD_COLORS[int(period - 1) % len(_PERIOD_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=sub["Z"],
                y=sub["fidelity_score"],
                mode="markers",
                name=f"Period {int(period)}",
                marker=dict(size=9, color=color, line=dict(width=0.5, color="#0a1628")),
                customdata=np.stack(
                    [
                        sub["Z"].astype(int),
                        sub["element"],
                        sub["magnetic_moment_score"],
                        sub["ie_score"],
                    ],
                    axis=-1,
                ),
                hovertemplate=(
                    "%{customdata[1]} (Z=%{customdata[0]})<br>"
                    "Fidelity: %{y:.1f}/10<br>"
                    "μ score: %{customdata[2]}<br>"
                    "IE score: %{customdata[3]}<br>"
                    "<i>Click to open in Flux Flywheel</i><extra></extra>"
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

    for period in sorted(df["period"].unique()):
        sub = df[df["period"] == period].sort_values("Z")
        color = _PERIOD_COLORS[int(period - 1) % len(_PERIOD_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=sub["model_stability"],
                y=sub["experimental_ie"],
                mode="markers",
                name=f"Period {int(period)}",
                marker=dict(size=8, color=color, line=dict(width=0.5, color="#0a1628")),
                customdata=np.stack(
                    [sub["Z"].astype(int), sub["element"], sub["fidelity_score"]],
                    axis=-1,
                ),
                hovertemplate=(
                    "%{customdata[1]} (Z=%{customdata[0]})<br>"
                    "Stability: %{x:.2f}<br>"
                    "IE: %{y:.2f} eV<br>"
                    "Fidelity: %{customdata[2]}<br>"
                    "<i>Click to open in Flux Flywheel</i><extra></extra>"
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


def create_stability_vs_en_plot(data: pd.DataFrame | None = None) -> go.Figure:
    """Model stability vs Allen electronegativity with OLS trend and Pearson r."""
    df = observations_trends_dataframe() if data is None else data
    plot_df = df.dropna(subset=["experimental_en"]).copy()
    fig = go.Figure()

    if plot_df.empty:
        fig.add_annotation(
            text="No Allen electronegativity data in range",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=13, color="#8ecae6"),
        )
        return _apply_dark_theme(fig)

    for period in sorted(plot_df["period"].unique()):
        sub = plot_df[plot_df["period"] == period].sort_values("Z")
        color = _PERIOD_COLORS[int(period - 1) % len(_PERIOD_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=sub["model_stability"],
                y=sub["experimental_en"],
                mode="markers",
                name=f"Period {int(period)}",
                marker=dict(size=8, color=color, line=dict(width=0.5, color="#0a1628")),
                customdata=np.stack(
                    [
                        sub["Z"].astype(int),
                        sub["element"],
                        sub["fidelity_score"],
                        sub["en_score"],
                    ],
                    axis=-1,
                ),
                hovertemplate=(
                    "%{customdata[1]} (Z=%{customdata[0]})<br>"
                    "Stability: %{x:.2f}<br>"
                    "Allen EN: %{y:.3f}<br>"
                    "Fidelity: %{customdata[2]}<br>"
                    "EN score: %{customdata[3]}<br>"
                    "<i>Click to open in Flux Flywheel</i><extra></extra>"
                ),
            )
        )

    x = plot_df["model_stability"].to_numpy(dtype=float)
    y = plot_df["experimental_en"].to_numpy(dtype=float)
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
        title="Model Stability Score vs Allen Electronegativity",
        xaxis_title="Model Stability Score",
        yaxis_title="Allen Electronegativity",
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

    for period in sorted(plot_df["period"].unique()):
        sub = plot_df[plot_df["period"] == period].sort_values("Z")
        color = _PERIOD_COLORS[int(period - 1) % len(_PERIOD_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=sub["experimental_mu_BM"],
                y=sub["soc_mu_BM"],
                mode="markers",
                name=f"Period {int(period)}",
                marker=dict(size=9, color=color, line=dict(width=0.5, color="#0a1628")),
                customdata=np.stack([sub["Z"].astype(int), sub["element"]], axis=-1),
                hovertemplate=(
                    "%{customdata[1]} (Z=%{customdata[0]})<br>"
                    "Exp μ: %{x:.2f} BM<br>"
                    "SOC μ: %{y:.2f} BM<br>"
                    "<i>Click to open in Flux Flywheel</i><extra></extra>"
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


def load_observations_trend_figures(
    z_max: int = 118,
    periods: list[int] | tuple[int, ...] | None = None,
) -> tuple[go.Figure, go.Figure, go.Figure, go.Figure]:
    """Return (fidelity trend, stability vs IE, stability vs EN, SOC μ) figures."""
    df = filter_trends_by_period(observations_trends_dataframe(z_max), periods)
    return (
        create_fidelity_trend_plot(df),
        create_stability_vs_ie_plot(df),
        create_stability_vs_en_plot(df),
        create_soc_mu_vs_experimental_plot(df),
    )