"""Interactive Plotly Hopf fibration visualizer."""

from __future__ import annotations

import os
from typing import Any, Literal

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from kingdom.core.hopf import base_sphere_mesh, sample_fiber, sample_fiber_family

ViewMode = Literal["2d", "3d"]

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


def is_hf_space() -> bool:
    return bool(os.environ.get("SPACE_ID"))


def default_view_mode() -> ViewMode:
    return "2d" if is_hf_space() else "3d"


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


def _axis_style() -> dict[str, Any]:
    return dict(
        gridcolor=GRID,
        zerolinecolor=GRID,
        linecolor=GRID,
        tickfont=dict(color="#8ecae6"),
        title=dict(font=dict(color="#d4e4f7")),
    )


def build_hopf_fibration_figure_2d(
    n_fibers: int = 8,
    n_points: int = 160,
    eta: float = 0.6,
    xi1: float = 1.2,
    show_base_sphere: bool = True,
    show_single_fiber_highlight: bool = True,
    projection_scale: float = 1.0,
    height: int = 620,
) -> go.Figure:
    """
    WebGL-free Hopf visualizer using 2D Plotly scatter projections.

    HF Spaces iframes often block WebGL; this view works everywhere.
    """
    fibers = sample_fiber_family(n_fibers=n_fibers, n_points=n_points)
    highlight = sample_fiber(eta, xi1, n_points=n_points) if show_single_fiber_highlight else None
    theme = kingdom_dark_theme()

    panel_titles = (
        "① ℝ³ xy — linked Villarceau circles",
        "② ℝ³ xz — orthogonal projection",
        "③ S² base — fiber base points",
        "④ Highlight — fiber phase ξ₂",
    )
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=panel_titles,
        horizontal_spacing=0.08,
        vertical_spacing=0.11,
    )

    for i, fiber in enumerate(fibers):
        color = FIBER_COLORS[i % len(FIBER_COLORS)]
        px = np.asarray(fiber["px"]) * projection_scale
        py = np.asarray(fiber["py"]) * projection_scale
        pz = np.asarray(fiber["pz"]) * projection_scale

        fig.add_trace(
            go.Scatter(
                x=px,
                y=py,
                mode="lines",
                name=f"Fiber {i + 1}",
                legendgroup=f"fiber-{i}",
                line=dict(color=color, width=2.5),
                showlegend=i == 0,
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=px,
                y=pz,
                mode="lines",
                legendgroup=f"fiber-{i}",
                line=dict(color=color, width=2.5),
                showlegend=False,
            ),
            row=1,
            col=2,
        )

        if show_base_sphere:
            y1, y2, y3 = fiber["base_y1"], fiber["base_y2"], fiber["base_y3"]
            denom = max(1.0 - y3, 1e-6)
            fig.add_trace(
                go.Scatter(
                    x=[0.55 * y1 / denom],
                    y=[0.55 * y2 / denom],
                    mode="markers",
                    legendgroup=f"fiber-{i}",
                    marker=dict(color=color, size=7, line=dict(width=0.5, color="#0a1628")),
                    showlegend=False,
                ),
                row=2,
                col=1,
            )

    if show_base_sphere:
        theta = np.linspace(0.0, 2.0 * np.pi, 120)
        fig.add_trace(
            go.Scatter(
                x=0.55 * np.cos(theta),
                y=0.55 * np.sin(theta),
                mode="lines",
                line=dict(color="#1a8fe3", width=1, dash="dot"),
                showlegend=False,
                hoverinfo="skip",
            ),
            row=2,
            col=1,
        )

    if highlight is not None:
        hx = np.asarray(highlight["px"]) * projection_scale
        hy = np.asarray(highlight["py"]) * projection_scale
        hz = np.asarray(highlight["pz"]) * projection_scale
        xi2 = np.asarray(highlight["xi2"])

        fig.add_trace(
            go.Scatter(
                x=hx,
                y=hy,
                mode="lines",
                name=f"Highlight η={eta:.2f}",
                line=dict(color=ACCENT_GOLD, width=4),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=hx,
                y=hz,
                mode="lines",
                line=dict(color=ACCENT_GOLD, width=4),
                showlegend=False,
            ),
            row=1,
            col=2,
        )

        fig.add_trace(
            go.Scatter(
                x=hx,
                y=hy,
                mode="markers",
                marker=dict(
                    size=6,
                    color=xi2,
                    showscale=True,
                    colorbar=dict(
                        title=dict(text="ξ₂", font=dict(color="#d4e4f7")),
                        len=0.4,
                        y=0.18,
                        bgcolor="rgba(10,22,40,0.8)",
                        bordercolor="rgba(255,255,255,0.12)",
                        tickfont=dict(color="#8ecae6"),
                    ),
                    colorscale=[
                        [0.0, "#0d2137"],
                        [0.25, "#1a8fe3"],
                        [0.5, "#00c9b7"],
                        [0.75, "#c9a227"],
                        [1.0, "#ef553b"],
                    ],
                ),
                showlegend=False,
            ),
            row=2,
            col=2,
        )

        if show_base_sphere:
            hy1, hy2, hy3 = highlight["y1"][0], highlight["y2"][0], highlight["y3"][0]
            denom = max(1.0 - hy3, 1e-6)
            fig.add_trace(
                go.Scatter(
                    x=[0.55 * hy1 / denom],
                    y=[0.55 * hy2 / denom],
                    mode="markers",
                    marker=dict(size=12, color=ACCENT_GOLD, symbol="diamond"),
                    showlegend=False,
                ),
                row=2,
                col=1,
            )

    axis = _axis_style()
    for row in (1, 2):
        for col in (1, 2):
            fig.update_xaxes(**axis, row=row, col=col, showgrid=True)
            fig.update_yaxes(**axis, row=row, col=col, showgrid=True)
    for row, col in ((1, 1), (1, 2), (2, 1), (2, 2)):
        fig.update_xaxes(scaleanchor="y", scaleratio=1, row=row, col=col)

    fig.update_layout(
        **theme,
        height=height,
        title=dict(
            text="Hopf Fibration — S³ fibers → ℝ³ projections → S² base",
            x=0.5,
            xanchor="center",
            font=dict(size=15, color="#e8f4ff"),
        ),
        legend=dict(
            bgcolor="rgba(10, 22, 40, 0.7)",
            bordercolor="rgba(255,255,255,0.12)",
            borderwidth=1,
        ),
    )
    fig.add_annotation(
        text="Read left→right, top→bottom: stereographic views then Hopf base chart",
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.06,
        showarrow=False,
        font=dict(size=10, color="#5a7a9a"),
    )
    fig.update_annotations(font=dict(color="#8ecae6", size=10))
    return fig


def build_hopf_fibration_figure_auto(
    view_mode: ViewMode | str = "auto",
    **kwargs: Any,
) -> go.Figure:
    mode: ViewMode
    if view_mode == "auto":
        mode = default_view_mode()
    elif view_mode in ("2d", "3d"):
        mode = view_mode  # type: ignore[assignment]
    elif str(view_mode).lower().startswith("2"):
        mode = "2d"
    else:
        mode = "3d"

    if mode == "2d":
        return build_hopf_fibration_figure_2d(**kwargs)
    return build_hopf_fibration_figure(**kwargs)