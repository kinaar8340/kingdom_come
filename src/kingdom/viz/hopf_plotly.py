"""Interactive Plotly Hopf fibration visualizer."""

from __future__ import annotations

from typing import Any

import numpy as np
import plotly.graph_objects as go

from kingdom.core.hopf import base_sphere_mesh, sample_fiber, sample_fiber_family

# Kingdom Come palette: deep blues/teals for topology, warm accents for flux
FIBER_COLORS = (
    "#1a8fe3",
    "#00c9b7",
    "#4cc9f0",
    "#2ec4b6",
    "#48bfe3",
    "#64dfdf",
    "#56cfe1",
    "#4ea8de",
    "#5390d9",
    "#5e60ce",
    "#7b2cbf",
    "#c77dff",
)
ACCENT_GOLD = "#c9a227"
BG_DARK = "#0a1628"
GRID = "#1e3a5f"


def kingdom_dark_theme() -> dict[str, Any]:
    return {
        "paper_bgcolor": BG_DARK,
        "plot_bgcolor": BG_DARK,
        "font": {"color": "#d4e4f7", "family": "Inter, system-ui, sans-serif"},
        "margin": {"l": 0, "r": 0, "t": 56, "b": 0},
    }


def build_hopf_fibration_figure(
    n_fibers: int = 8,
    n_points: int = 160,
    eta: float = 0.6,
    xi1: float = 1.2,
    show_base_sphere: bool = True,
    show_single_fiber_highlight: bool = True,
    projection_scale: float = 1.0,
    height: int = 560,
) -> go.Figure:
    """
    Build a dual-view Hopf fibration figure.

    Left scene: stereographic fibers in ℝ³ (linked Villarceau circles).
    Right scene: S² base with fiber base-point markers.
    """
    fibers = sample_fiber_family(n_fibers=n_fibers, n_points=n_points)
    theme = kingdom_dark_theme()
    fig = go.Figure()

    for i, fiber in enumerate(fibers):
        color = FIBER_COLORS[i % len(FIBER_COLORS)]
        px = np.asarray(fiber["px"]) * projection_scale
        py = np.asarray(fiber["py"]) * projection_scale
        pz = np.asarray(fiber["pz"]) * projection_scale
        xi2 = np.asarray(fiber["xi2"])
        hover = [
            f"η={fiber['eta']:.2f}  ξ₁={fiber['xi1']:.2f}<br>"
            f"ξ₂={t:.2f} rad<br>"
            f"base S²=({fiber['base_y1']:.2f}, {fiber['base_y2']:.2f}, {fiber['base_y3']:.2f})"
            for t in xi2
        ]
        fig.add_trace(
            go.Scatter3d(
                x=px,
                y=py,
                z=pz,
                mode="lines",
                name=f"Fiber {i + 1}",
                legendgroup=f"fiber-{i}",
                line=dict(color=color, width=4),
                text=hover,
                hoverinfo="text",
                hovertemplate="%{text}<extra></extra>",
                scene="scene",
            )
        )

    if show_single_fiber_highlight:
        highlight = sample_fiber(eta, xi1, n_points=n_points)
        hx = np.asarray(highlight["px"]) * projection_scale
        hy = np.asarray(highlight["py"]) * projection_scale
        hz = np.asarray(highlight["pz"]) * projection_scale
        fig.add_trace(
            go.Scatter3d(
                x=hx,
                y=hy,
                z=hz,
                mode="lines+markers",
                name=f"Highlight (η={eta:.2f}, ξ₁={xi1:.2f})",
                line=dict(color=ACCENT_GOLD, width=7),
                marker=dict(size=3, color=ACCENT_GOLD),
                scene="scene",
            )
        )

    if show_base_sphere:
        bx, by, bz = base_sphere_mesh()
        fig.add_trace(
            go.Surface(
                x=bx * 0.55,
                y=by * 0.55,
                z=bz * 0.55,
                opacity=0.12,
                colorscale=[[0, "#0d2137"], [1, "#1a8fe3"]],
                showscale=False,
                hoverinfo="skip",
                name="S² base",
                scene="scene2",
            )
        )

    for i, fiber in enumerate(fibers):
        color = FIBER_COLORS[i % len(FIBER_COLORS)]
        fig.add_trace(
            go.Scatter3d(
                x=[fiber["base_y1"]],
                y=[fiber["base_y2"]],
                z=[fiber["base_y3"]],
                mode="markers",
                name=f"Base {i + 1}",
                legendgroup=f"fiber-{i}",
                showlegend=False,
                marker=dict(size=5, color=color, symbol="circle"),
                scene="scene2",
            )
        )

    if show_single_fiber_highlight:
        hy1, hy2, hy3 = highlight["y1"][0], highlight["y2"][0], highlight["y3"][0]
        fig.add_trace(
            go.Scatter3d(
                x=[hy1],
                y=[hy2],
                z=[hy3],
                mode="markers",
                name="Highlight base",
                marker=dict(size=9, color=ACCENT_GOLD, symbol="diamond"),
                scene="scene2",
            )
        )

    scene_axes = dict(
        backgroundcolor=BG_DARK,
        gridcolor=GRID,
        zerolinecolor=GRID,
        showbackground=True,
    )

    fig.update_layout(
        **theme,
        height=height,
        title=dict(
            text="Hopf Fibration — S³ fibers stereographically projected to ℝ³",
            x=0.5,
            xanchor="center",
            font=dict(size=15, color="#e8f4ff"),
        ),
        legend=dict(
            bgcolor="rgba(10, 22, 40, 0.7)",
            bordercolor="rgba(255,255,255,0.12)",
            borderwidth=1,
        ),
        scene=dict(
            xaxis=dict(title="x", **scene_axes),
            yaxis=dict(title="y", **scene_axes),
            zaxis=dict(title="z", **scene_axes),
            aspectmode="cube",
            domain=dict(x=[0.0, 0.52], y=[0.0, 1.0]),
            camera=dict(eye=dict(x=1.6, y=1.4, z=1.1)),
        ),
        scene2=dict(
            xaxis=dict(title="y₁", **scene_axes),
            yaxis=dict(title="y₂", **scene_axes),
            zaxis=dict(title="y₃", **scene_axes),
            aspectmode="cube",
            domain=dict(x=[0.55, 1.0], y=[0.0, 1.0]),
            camera=dict(eye=dict(x=1.8, y=0.8, z=1.2)),
            annotations=[
                dict(
                    showarrow=False,
                    x=0,
                    y=0,
                    z=1.15,
                    text="S² base space",
                    font=dict(size=11, color="#8ecae6"),
                )
            ],
        ),
    )
    return fig