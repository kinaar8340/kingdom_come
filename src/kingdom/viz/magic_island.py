"""Magic Island stability heatmap — Z vs flux flywheel score."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from kingdom.core.elements import MAGIC_NUMBER_Z, NOBLE_GAS_Z
from kingdom.core.flux_flywheel import map_z_to_flywheel
from kingdom.viz.hopf_plotly import ACCENT_GOLD, BG_DARK, FIBER_COLORS, GRID, kingdom_dark_theme

# Precompute stability landscape once at import
_Z_RANGE = np.arange(1, 181)
_SCORES = np.array([map_z_to_flywheel(int(z))["stability_score"] for z in _Z_RANGE])
_DETUNING = np.array([map_z_to_flywheel(int(z))["delta_omega"] for z in _Z_RANGE])


def build_magic_island_heatmap(current_z: int = 2, height: int = 260) -> go.Figure:
    """2D stability landscape with noble gas and magic number markers."""
    theme = kingdom_dark_theme()
    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(
            z=_SCORES.reshape(1, -1),
            x=_Z_RANGE,
            y=["stability"],
            colorscale=[
                [0.0, "#0d2137"],
                [0.35, "#1a8fe3"],
                [0.55, "#00c9b7"],
                [0.75, "#c9a227"],
                [1.0, "#ffe8a3"],
            ],
            zmin=5.0,
            zmax=8.0,
            colorbar=dict(
                title=dict(text="score", font=dict(color="#d4e4f7")),
                tickfont=dict(color="#8ecae6"),
            ),
            hovertemplate="Z=%{x}<br>score=%{z:.1f}<extra></extra>",
        )
    )

    noble_x = sorted(NOBLE_GAS_Z)
    noble_y = [_SCORES[z - 1] for z in noble_x]
    fig.add_trace(
        go.Scatter(
            x=noble_x,
            y=[0.0] * len(noble_x),
            mode="markers+text",
            text=[f"Ng" for _ in noble_x],
            textposition="top center",
            marker=dict(size=12, color=ACCENT_GOLD, symbol="diamond", line=dict(width=1, color="#fff")),
            name="Noble gases",
            customdata=noble_y,
            hovertemplate="Noble gas Z=%{x}<br>score=%{customdata:.1f}<extra></extra>",
        )
    )

    magic_x = sorted(MAGIC_NUMBER_Z)
    fig.add_trace(
        go.Scatter(
            x=magic_x,
            y=[0.0] * len(magic_x),
            mode="markers",
            marker=dict(size=8, color=FIBER_COLORS[4], symbol="circle-open", line=dict(width=2)),
            name="Magic numbers",
            hovertemplate="Magic Z=%{x}<extra></extra>",
        )
    )

    cz = int(np.clip(current_z, 1, 180))
    fig.add_vline(x=cz, line=dict(color="#ef553b", width=2, dash="dot"))
    fig.add_annotation(
        x=cz,
        y=0.35,
        text=f"Z={cz}",
        showarrow=False,
        font=dict(color="#ef553b", size=11),
    )

    fig.update_layout(
        **theme,
        height=height,
        title=dict(
            text="Magic Island — flux stability vs atomic number Z",
            x=0.5,
            font=dict(size=12, color="#e8f4ff"),
        ),
        xaxis=dict(title="Z", gridcolor=GRID, tickfont=dict(color="#8ecae6"), dtick=20),
        yaxis=dict(visible=False, range=[-0.5, 0.6]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=9)),
    )
    return fig