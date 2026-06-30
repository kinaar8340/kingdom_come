"""Stylized electron cloud / flux flywheel shell visualizations (2D, WebGL-free)."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from kingdom.core.elements import Element, shell_occupancies
from kingdom.viz.hopf_plotly import ACCENT_GOLD, BG_DARK, FIBER_COLORS, GRID, kingdom_dark_theme

SHELL_COLORS = ("#1a8fe3", "#00c9b7", "#4cc9f0", "#48bfe3", "#c9a227", "#7b2cbf", "#ef553b")
FLUX_RING_COLOR = "rgba(201, 162, 39, 0.5)"
FLUX_RING_GLOW_COLOR = "rgba(201, 162, 39, 0.25)"


def build_electron_cloud_figure(
    element: Element,
    *,
    n_cloud_points: int = 400,
    stability_score: float = 5.0,
    rep_complexity_score: float | None = None,
    rep_flux_delta: float | None = None,
    rep_complexity_tooltip: str | None = None,
    height: int = 340,
) -> go.Figure:
    """2D stylized electron density cross-section with optional flux flywheel ring."""
    shells = shell_occupancies(element.z)
    theme = kingdom_dark_theme()
    fig = go.Figure()

    # Nucleus
    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker=dict(size=14, color="#ef553b", line=dict(width=1, color="#fff")),
            name="Nucleus",
            hovertemplate=f"Nucleus<br>{element.name} ({element.symbol})<extra></extra>",
        )
    )

    max_r = 1.0
    for i, (shell_n, count) in enumerate(shells):
        radius = 0.35 + 0.22 * shell_n
        max_r = max(max_r, radius + 0.15)
        color = SHELL_COLORS[i % len(SHELL_COLORS)]
        alpha = min(0.85, 0.25 + count / 18.0)

        theta = np.linspace(0, 2 * np.pi, 80)
        fig.add_trace(
            go.Scatter(
                x=radius * np.cos(theta),
                y=radius * np.sin(theta),
                mode="lines",
                line=dict(color=color, width=2, dash="dot"),
                opacity=alpha,
                showlegend=False,
                hoverinfo="skip",
            )
        )

        rng = np.random.default_rng(element.z * 1000 + shell_n)
        angles = rng.uniform(0, 2 * np.pi, n_cloud_points // max(len(shells), 1))
        radii = rng.normal(radius, 0.06 + 0.02 * shell_n, size=angles.size)
        fig.add_trace(
            go.Scatter(
                x=radii * np.cos(angles),
                y=radii * np.sin(angles),
                mode="markers",
                name=f"Shell n={shell_n} ({count} e⁻)",
                marker=dict(size=4, color=color, opacity=min(0.85, 0.35 + 0.04 * count)),
            )
        )

    # Flux flywheel stability ring (TOE overlay) — thin 50% transparent gold
    flywheel_r = max_r * (0.52 + 0.045 * stability_score)
    ring_t = np.linspace(0, 2 * np.pi, 160)
    high_lock = stability_score >= 7.5 or element.is_noble_gas
    ring_width = 1.5 if high_lock else (1.25 if stability_score >= 6.5 else 1.0)
    if high_lock:
        glow_r = flywheel_r * 1.04
        fig.add_trace(
            go.Scatter(
                x=glow_r * np.cos(ring_t),
                y=glow_r * np.sin(ring_t),
                mode="lines",
                line=dict(color=FLUX_RING_GLOW_COLOR, width=ring_width + 0.75),
                showlegend=False,
                hoverinfo="skip",
            )
        )
    ring_hover = (
        f"Flux stability: {stability_score:.1f}/10"
        f"<br>{element.name} ({element.symbol})"
    )
    if rep_complexity_score is not None:
        ring_hover += f"<br>Rep complexity: {rep_complexity_score:.1f}/10"
        if rep_flux_delta is not None:
            ring_hover += f"<br>Δ flux−rep: {rep_flux_delta:+.1f}"
    if rep_complexity_tooltip:
        ring_hover += f"<br><br>{rep_complexity_tooltip}"
    ring_hover += "<extra></extra>"

    fig.add_trace(
        go.Scatter(
            x=flywheel_r * np.cos(ring_t),
            y=flywheel_r * np.sin(ring_t),
            mode="lines",
            name=f"Flux flywheel (score {stability_score:.1f})",
            line=dict(
                color=FLUX_RING_COLOR,
                width=ring_width,
                dash="solid" if high_lock else "dash",
            ),
            hovertemplate=ring_hover,
        )
    )

    notes: list[str] = []
    if element.is_noble_gas:
        notes.append("noble gas lock")
    if element.is_synthetic:
        notes.append("predicted superheavy")
    note = f" — {' · '.join(notes)}" if notes else ""
    fig.update_layout(
        **theme,
        height=height,
        title=dict(
            text=f"{element.name} ({element.symbol}) — electron shells + flux flywheel{note}",
            x=0.5,
            font=dict(size=13, color="#e8f4ff"),
        ),
        showlegend=True,
        legend=dict(bgcolor="rgba(10,22,40,0.75)", font=dict(size=9)),
    )
    axis = dict(
        scaleanchor="y",
        scaleratio=1,
        range=[-max_r - 0.3, max_r + 0.3],
        gridcolor=GRID,
        zerolinecolor=GRID,
        tickfont=dict(color="#8ecae6"),
        title=dict(font=dict(color="#d4e4f7")),
    )
    fig.update_xaxes(**axis)
    fig.update_yaxes(**axis)
    return fig


def build_chemistry_vs_toe_figure(
    element: Element,
    stability_score: float,
    *,
    rep_complexity_score: float | None = None,
    rep_flux_delta: float | None = None,
    rep_complexity_tooltip: str | None = None,
) -> go.Figure:
    """Shell-closure chemistry vs flux stability vs Monster rep complexity."""
    labels = [
        "Shell closure\n(chemistry)",
        "Flux flywheel\n(model)",
    ]
    chem = 10.0 if element.is_noble_gas else (7.0 if element.is_magic_number else 5.0)
    toe = float(stability_score)
    values = [chem, toe]
    colors = [FIBER_COLORS[0], ACCENT_GOLD]
    hover_texts = [
        f"Shell closure expectation: {chem:.1f}/10",
        f"Flux flywheel stability: {toe:.1f}/10",
    ]
    if rep_complexity_score is not None:
        labels.append("Rep complexity\n(Monster)")
        values.append(float(rep_complexity_score))
        colors = list(colors) + ["#7b2cbf"]
        rep_hover = f"Representation complexity: {rep_complexity_score:.1f}/10"
        if rep_flux_delta is not None:
            rep_hover += f"<br>Δ flux−rep: {rep_flux_delta:+.1f}"
        if rep_complexity_tooltip:
            rep_hover += f"<br><br>{rep_complexity_tooltip}"
        hover_texts.append(rep_hover)

    gap = toe - chem
    fig = go.Figure(
        go.Bar(
            x=labels,
            y=values,
            marker_color=colors,
            text=[f"{v:.1f}" for v in values],
            textposition="outside",
            hovertemplate="%{customdata}<extra></extra>",
            customdata=hover_texts,
        )
    )
    if element.is_noble_gas:
        subtitle = "Noble gas: chemistry expects maximal shell closure"
    elif element.is_magic_number:
        subtitle = "Magic number: enhanced closure vs open-shell baseline"
    else:
        subtitle = "Open / reactive shell: lower closure expectation"
    gap_note = f"Δ model − chemistry = {gap:+.1f}"
    if rep_complexity_score is not None and rep_flux_delta is not None:
        gap_note += f" · Δ flux−rep = {rep_flux_delta:+.1f}"
    if abs(gap) > 2.0:
        gap_note += " (large gap — check validation panel)"
    theme = {k: v for k, v in kingdom_dark_theme().items() if k != "margin"}
    fig.update_layout(
        **theme,
        height=200,
        title=dict(
            text="Shell closure strength vs model stability",
            font=dict(size=12, color="#e8f4ff"),
        ),
        annotations=[
            dict(
                text=subtitle,
                xref="paper",
                yref="paper",
                x=0.5,
                y=1.12,
                showarrow=False,
                font=dict(size=9, color="#8ecae6"),
                xanchor="center",
            ),
            dict(
                text=gap_note,
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.22,
                showarrow=False,
                font=dict(
                    size=9,
                    color="#00c9b7" if abs(gap) <= 1.5 else "#ffb4a2",
                ),
                xanchor="center",
            ),
        ],
        margin=dict(t=55, b=45),
        yaxis=dict(
            range=[0, 10.5],
            title=dict(text="Stability score (0–10)", font=dict(size=10, color="#8ecae6")),
            gridcolor=GRID,
            tickfont=dict(color="#8ecae6"),
        ),
    )
    return fig