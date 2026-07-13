"""Interactive Plotly Hopf fibration visualizer (kingdom portal).

Geometry and dashboard construction come from ``flux_hopf_lib.hopf`` /
``flux_hopf_lib.hopf.viz``. This module applies the Kingdom dark theme and
HF-safe view-mode policy.
"""

from __future__ import annotations

import os
from typing import Any, Literal

import numpy as np
import plotly.graph_objects as go

from flux_hopf_lib.hopf import sample_fiber, sample_fiber_family
from flux_hopf_lib.hopf.viz import (
    FIBER_COLORS,
    create_plotly_fiber_animation,
    fiber_family_choices,
    plot_hopf_fibers_dashboard,
    plot_hopf_fibers_stereographic,
    plot_hopf_s2_fiber_explorer,
    s2_to_hopf_angles,
)

try:
    # flux-hopf-lib >= 0.2.3
    from flux_hopf_lib.hopf.viz import plotly_fig_to_html as _core_plotly_to_html
except ImportError:  # pragma: no cover
    _core_plotly_to_html = None  # type: ignore[assignment]

ViewMode = Literal["2d", "3d"]

ACCENT_GOLD = "#c9a227"
BG_DARK = "#0a1628"
GRID = "#1e3a5f"


def is_hf_space() -> bool:
    """Detect Hugging Face Spaces runtime (env var or /app root)."""
    if os.environ.get("SPACE_ID"):
        return True
    cwd = os.getcwd()
    return cwd == "/app" or cwd.startswith("/app/")


def default_view_mode() -> ViewMode:
    """Always prefer 2D — WebGL is unreliable in HF iframes and many browsers."""
    return "2d"


def resolve_view_mode(view_mode: ViewMode | str) -> ViewMode:
    """Force 2D on Hugging Face regardless of UI selection."""
    if is_hf_space():
        return "2d"
    if view_mode == "auto":
        return default_view_mode()
    if view_mode in ("2d", "3d"):
        return view_mode  # type: ignore[return-value]
    if str(view_mode).lower().startswith("2"):
        return "2d"
    return "3d"


def kingdom_dark_theme() -> dict[str, Any]:
    return {
        "paper_bgcolor": BG_DARK,
        "plot_bgcolor": BG_DARK,
        "font": {"color": "#d4e4f7", "family": "Inter, system-ui, sans-serif"},
        "margin": {"l": 0, "r": 0, "t": 56, "b": 0},
    }


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
    """HF-safe 2×2 dashboard via flux_hopf_lib.hopf.viz.plot_hopf_fibers_dashboard."""
    theme = kingdom_dark_theme()
    fig = plot_hopf_fibers_dashboard(
        n_fibers=n_fibers,
        n_points=n_points,
        eta=eta,
        xi1=xi1,
        projection_scale=projection_scale,
        show_base=show_base_sphere,
        show_highlight=show_single_fiber_highlight,
        title="Hopf Fibration — S³ fibers → ℝ³ projections → S² base",
        height=height,
        theme=theme,
    )
    # Kingdom-specific axis colors
    for row in (1, 2):
        for col in (1, 2):
            fig.update_xaxes(
                gridcolor=GRID,
                zerolinecolor=GRID,
                linecolor=GRID,
                tickfont=dict(color="#8ecae6"),
                row=row,
                col=col,
            )
            fig.update_yaxes(
                gridcolor=GRID,
                zerolinecolor=GRID,
                linecolor=GRID,
                tickfont=dict(color="#8ecae6"),
                row=row,
                col=col,
            )
    fig.update_annotations(font=dict(color="#8ecae6", size=10))
    return fig


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
    Local 3D WebGL view (not used on HF).

    Built from core stereographic sampling with kingdom theming.
    """
    fibers = sample_fiber_family(n_fibers=n_fibers, n_points=n_points, scale=2.0)
    theme = kingdom_dark_theme()
    fig = go.Figure()

    for i, fiber in enumerate(fibers):
        color = FIBER_COLORS[i % len(FIBER_COLORS)]
        px = np.asarray(fiber["px"]) * projection_scale
        py = np.asarray(fiber["py"]) * projection_scale
        pz = np.asarray(fiber["pz"]) * projection_scale
        fig.add_trace(
            go.Scatter3d(
                x=px,
                y=py,
                z=pz,
                mode="lines",
                name=f"Fiber {i + 1}",
                line=dict(color=color, width=4),
                scene="scene",
            )
        )

    if show_single_fiber_highlight:
        h = sample_fiber(eta, xi1, n_points=n_points, scale=2.0)
        fig.add_trace(
            go.Scatter3d(
                x=np.asarray(h["px"]) * projection_scale,
                y=np.asarray(h["py"]) * projection_scale,
                z=np.asarray(h["pz"]) * projection_scale,
                mode="lines",
                name=f"Highlight (η={eta:.2f}, ξ₁={xi1:.2f})",
                line=dict(color=ACCENT_GOLD, width=7),
                scene="scene",
            )
        )

    if show_base_sphere:
        for i, fiber in enumerate(fibers):
            color = FIBER_COLORS[i % len(FIBER_COLORS)]
            fig.add_trace(
                go.Scatter3d(
                    x=[fiber["base_y1"]],
                    y=[fiber["base_y2"]],
                    z=[fiber["base_y3"]],
                    mode="markers",
                    marker=dict(size=5, color=color),
                    showlegend=False,
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
        scene=dict(
            xaxis=dict(title="x", **scene_axes),
            yaxis=dict(title="y", **scene_axes),
            zaxis=dict(title="z", **scene_axes),
            aspectmode="cube",
            domain=dict(x=[0.0, 0.55], y=[0.0, 1.0]),
            camera=dict(eye=dict(x=1.6, y=1.4, z=1.1)),
        ),
        scene2=dict(
            xaxis=dict(title="y₁", **scene_axes),
            yaxis=dict(title="y₂", **scene_axes),
            zaxis=dict(title="y₃", **scene_axes),
            aspectmode="cube",
            domain=dict(x=[0.58, 1.0], y=[0.0, 1.0]),
            camera=dict(eye=dict(x=1.8, y=0.8, z=1.2)),
        ),
    )
    return fig


def build_hopf_s2_explorer(
    n_fibers: int = 12,
    n_points: int = 140,
    eta: float = 0.6,
    xi1: float = 1.2,
    projection_scale: float = 1.0,
    height: int = 560,
) -> go.Figure:
    """S² explorer with hover customdata; HF-safe (no WebGL)."""
    theme = kingdom_dark_theme()
    fig = plot_hopf_s2_fiber_explorer(
        n_fibers=n_fibers,
        n_points=n_points,
        selected_eta=eta,
        selected_xi1=xi1,
        projection_scale=projection_scale,
        height=height,
        theme=theme,
        title="S² base explorer — pick a fiber (dropdown) or hover base points",
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color="#8ecae6"))
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color="#8ecae6"))
    return fig


def plotly_fig_to_html(fig: go.Figure, *, height: int | None = None) -> str:
    """Embed Plotly figure as HTML so client-side animate (Play) works in Gradio/HF."""
    if _core_plotly_to_html is not None:
        return _core_plotly_to_html(fig, height=height)
    if height is not None:
        fig.update_layout(height=int(height))
    inner = fig.to_html(
        include_plotlyjs="cdn",
        full_html=False,
        config={"responsive": True, "displayModeBar": True, "displaylogo": False},
    )
    return (
        '<div class="hopf-plotly-embed" style="width:100%;min-height:480px;">'
        f"{inner}</div>"
    )


def build_hopf_fiber_animation(
    n_fibers: int = 8,
    n_points: int = 80,
    n_frames: int = 36,
    *,
    mode: str = "xi1_orbit",
    eta: float = 0.6,
    xi1: float = 1.2,
    projection_scale: float = 1.0,
    height: int = 560,
    as_html: bool = False,
) -> go.Figure | str:
    """
    HF-safe Plotly frame animation (2D stereographic xy).

    Modes: ``xi1_orbit``, ``eta_breath``, ``gauge_twist``
    (``hopfion_spin`` falls back inside core to a 2D-safe mode).

    Set ``as_html=True`` for Gradio/HF — ``gr.Plot`` breaks Plotly Play;
    embed the returned HTML string in ``gr.HTML`` instead.
    """
    theme = kingdom_dark_theme()
    # Map UI labels → core mode keys
    mode_key = str(mode).strip().lower().replace(" ", "_").replace("–", "-")
    aliases = {
        "xi1_orbit": "xi1_orbit",
        "ξ₁_orbit": "xi1_orbit",
        "orbit": "xi1_orbit",
        "eta_breath": "eta_breath",
        "η_breath": "eta_breath",
        "breath": "eta_breath",
        "gauge_twist": "gauge_twist",
        "twist": "gauge_twist",
        "hopfion_spin": "hopfion_spin",
        "hopfion": "hopfion_spin",
    }
    resolved = aliases.get(mode_key, mode_key if mode_key in aliases.values() else "xi1_orbit")
    fig = create_plotly_fiber_animation(
        n_fibers=n_fibers,
        n_points=n_points,
        n_frames=n_frames,
        mode=resolved,  # type: ignore[arg-type]
        eta=eta,
        xi1=xi1,
        projection_scale=projection_scale,
        height=height,
        theme=theme,
        title=f"Hopf fiber animation — {resolved} (HF-safe 2D frames)",
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color="#8ecae6"))
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color="#8ecae6"))
    if as_html:
        return plotly_fig_to_html(fig, height=height)
    return fig


def build_hopf_fibration_figure_auto(
    view_mode: ViewMode | str = "auto",
    **kwargs: Any,
) -> go.Figure:
    mode = resolve_view_mode(view_mode)
    if mode == "2d":
        return build_hopf_fibration_figure_2d(**kwargs)
    return build_hopf_fibration_figure(**kwargs)


# re-exports for portal UI
__all__ = [
    "is_hf_space",
    "default_view_mode",
    "resolve_view_mode",
    "kingdom_dark_theme",
    "build_hopf_fibration_figure",
    "build_hopf_fibration_figure_2d",
    "build_hopf_fibration_figure_auto",
    "build_hopf_s2_explorer",
    "build_hopf_fiber_animation",
    "plotly_fig_to_html",
    "fiber_family_choices",
    "s2_to_hopf_angles",
    "plot_hopf_fibers_stereographic",
    "FIBER_COLORS",
]

