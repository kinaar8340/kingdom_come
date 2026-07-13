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
    fiber_family_choices,
    plot_hopf_fibers_dashboard,
    plot_hopf_fibers_stereographic,
    plot_hopf_s2_fiber_explorer,
    s2_to_hopf_angles,
)

try:
    from flux_hopf_lib.hopf import lod_n_points, sample_fiber_family_cached
except ImportError:  # pragma: no cover — older core
    lod_n_points = None  # type: ignore[assignment]
    sample_fiber_family_cached = None  # type: ignore[assignment]

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


def _resolve_anim_mode(mode: str) -> str:
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
        "hopfion_spin": "eta_breath",  # 2D-safe
        "hopfion": "eta_breath",
    }
    return aliases.get(mode_key, "xi1_orbit")


def _anim_eta_xi1(
    mode: str,
    frame_idx: int,
    n_frames: int,
    *,
    eta0: float,
    xi1_0: float,
) -> tuple[float, float]:
    """Map frame index → (η, ξ₁) for the gold highlight fiber."""
    t = float(frame_idx) / max(int(n_frames), 1)
    mode = _resolve_anim_mode(mode)
    if mode == "xi1_orbit":
        return float(eta0), float((xi1_0 + 2.0 * np.pi * t) % (2.0 * np.pi))
    if mode == "eta_breath":
        eta = 0.25 + 0.95 * (0.5 + 0.5 * np.sin(2.0 * np.pi * t))
        return float(eta), float(xi1_0)
    # gauge_twist keeps base fixed
    return float(eta0), float(xi1_0)


def build_hopf_animation_frame(
    n_fibers: int = 8,
    n_points: int = 80,
    *,
    frame_idx: int = 0,
    n_frames: int = 36,
    mode: str = "xi1_orbit",
    eta: float = 0.6,
    xi1: float = 1.2,
    projection_scale: float = 1.0,
    height: int = 560,
) -> go.Figure:
    """
    Single-frame Hopf animation snapshot for Gradio ``gr.Plot``.

    Gradio cannot run Plotly's client-side Play (``gr.Plot``) and strips scripts
    from ``gr.HTML``. Drive playback with a Gradio frame slider + Timer instead.
    """
    resolved = _resolve_anim_mode(mode)
    n_frames = max(1, int(n_frames))
    frame_idx = int(frame_idx) % n_frames
    pts = int(n_points)
    if lod_n_points is not None:
        pts = int(lod_n_points(n_fibers, base_points=n_points))

    if sample_fiber_family_cached is not None:
        fibers = sample_fiber_family_cached(n_fibers=n_fibers, n_points=pts, scale=2.0)
    else:
        fibers = sample_fiber_family(n_fibers=n_fibers, n_points=pts, scale=2.0)

    e, x = _anim_eta_xi1(resolved, frame_idx, n_frames, eta0=eta, xi1_0=xi1)
    highlight = sample_fiber(e, x, n_points=pts, scale=2.0)
    hx = np.asarray(highlight["px"]) * projection_scale
    hy = np.asarray(highlight["py"]) * projection_scale
    k = (
        int((frame_idx / max(n_frames, 1)) * (len(hx) - 1))
        if resolved == "gauge_twist"
        else 0
    )

    fig = go.Figure()
    for i, fiber in enumerate(fibers):
        color = FIBER_COLORS[i % len(FIBER_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=np.asarray(fiber["px"]) * projection_scale,
                y=np.asarray(fiber["py"]) * projection_scale,
                mode="lines",
                line=dict(color=color, width=2.0),
                opacity=0.4,
                showlegend=False,
                hoverinfo="skip",
            )
        )
    fig.add_trace(
        go.Scatter(
            x=hx,
            y=hy,
            mode="lines",
            line=dict(color=ACCENT_GOLD, width=4.5),
            name="highlight",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[float(hx[k])],
            y=[float(hy[k])],
            mode="markers",
            marker=dict(size=11, color=ACCENT_GOLD),
            name="phase",
            showlegend=False,
        )
    )

    theme = kingdom_dark_theme()
    layout = {
        **theme,
        "height": height,
        "title": dict(
            text=(
                f"Hopf animation — {resolved}  · frame {frame_idx}/{n_frames - 1}  "
                f"· η={e:.2f} ξ₁={x:.2f}"
            ),
            x=0.5,
            xanchor="center",
            font=dict(size=14, color="#e8f4ff"),
        ),
        "margin": dict(l=40, r=20, t=56, b=40),
        "xaxis": dict(
            scaleanchor="y",
            scaleratio=1,
            showgrid=True,
            gridcolor=GRID,
            zerolinecolor=GRID,
            tickfont=dict(color="#8ecae6"),
        ),
        "yaxis": dict(
            showgrid=True,
            gridcolor=GRID,
            zerolinecolor=GRID,
            tickfont=dict(color="#8ecae6"),
        ),
        "showlegend": True,
        "legend": dict(orientation="h", y=1.08, font=dict(color="#d4e4f7")),
    }
    fig.update_layout(**layout)
    return fig


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
    frame_idx: int = 0,
    as_html: bool = False,  # kept for API compat; ignored (use Gradio Timer instead)
) -> go.Figure:
    """
    Animation snapshot for portals.

    Prefer :func:`build_hopf_animation_frame` + Gradio frame slider / Timer.
    Plotly client-side Play does not work under ``gr.Plot`` on HF Spaces.
    """
    _ = as_html  # deprecated path
    return build_hopf_animation_frame(
        n_fibers=n_fibers,
        n_points=n_points,
        frame_idx=frame_idx,
        n_frames=n_frames,
        mode=mode,
        eta=eta,
        xi1=xi1,
        projection_scale=projection_scale,
        height=height,
    )


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
    "build_hopf_animation_frame",
    "fiber_family_choices",
    "s2_to_hopf_angles",
    "plot_hopf_fibers_stereographic",
    "FIBER_COLORS",
]

