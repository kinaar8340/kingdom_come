"""Interactive Plotly Hopf fibration visualizer (kingdom portal).

Geometry and dashboard construction come from ``flux_hopf_lib.hopf`` /
``flux_hopf_lib.hopf.viz``. This module applies the Kingdom dark theme and
HF-safe view-mode policy.

Animation quality path
----------------------
Prefer **precomputed Plotly frames** + Gradio slider (instant scrub). Do **not**
rely on Matplotlib FuncAnimation or Plotly client-side Play under ``gr.Plot``.
"""

from __future__ import annotations

import hashlib
import os
from typing import Any, Literal

import numpy as np
import plotly.graph_objects as go

from flux_hopf_lib.hopf import sample_fiber, sample_fiber_family
from flux_hopf_lib.hopf.viz import (
    FIBER_COLORS,
    create_hopf_fiber_animation_frames,
    fiber_family_choices,
    plot_hopf_fibers_dashboard,
    plot_hopf_fibers_stereographic,
    plot_hopf_s2_fiber_explorer,
    s2_to_hopf_angles,
)

try:
    from flux_hopf_lib.hopf.viz import export_hopf_fiber_animation_mp4
except ImportError:  # pragma: no cover
    export_hopf_fiber_animation_mp4 = None  # type: ignore[assignment]

ViewMode = Literal["2d", "3d"]

ACCENT_GOLD = "#c9a227"
BG_DARK = "#0a1628"
GRID = "#1e3a5f"

# Process-local frame cache: bake once, scrub instantly (HF worker friendly).
_FRAME_CACHE: dict[str, list[go.Figure]] = {}
_FRAME_CACHE_MAX = 6


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
    """Local 3D WebGL view (not used on HF)."""
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


def _anim_cache_key(
    n_fibers: int,
    n_points: int,
    n_frames: int,
    mode: str,
    eta: float,
    xi1: float,
    scale: float,
    height: int,
) -> str:
    raw = f"{n_fibers}|{n_points}|{n_frames}|{mode}|{eta:.4f}|{xi1:.4f}|{scale:.3f}|{height}"
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def clear_animation_frame_cache() -> None:
    """Drop precomputed animation frames (tests / memory pressure)."""
    _FRAME_CACHE.clear()


def bake_hopf_animation_frames(
    n_fibers: int = 12,
    n_points: int = 100,
    n_frames: int = 60,
    *,
    mode: str = "twist",
    eta: float = 0.6,
    xi1: float = 1.2,
    projection_scale: float = 1.0,
    height: int = 600,
    opacity: float = 0.85,
    line_width: float = 2.5,
    force: bool = False,
) -> list[go.Figure]:
    """
    Precompute high-quality Plotly frames (process-cached).

    Scrubbing is ``frames[i]`` — no geometry re-sample per slider tick.
    Modes: ``twist``, ``gauge_evolution``, ``xi1_orbit``, ``eta_breath``, ``gauge_twist``.
    """
    key = _anim_cache_key(
        n_fibers, n_points, n_frames, mode, eta, xi1, projection_scale, height
    )
    if not force and key in _FRAME_CACHE:
        return _FRAME_CACHE[key]

    theme = kingdom_dark_theme()
    frames = create_hopf_fiber_animation_frames(
        n_fibers=int(n_fibers),
        n_points=min(int(n_points), 140),
        n_frames=max(1, int(n_frames)),
        mode=str(mode),
        eta=float(eta),
        xi1=float(xi1),
        projection_scale=float(projection_scale),
        height=int(height),
        theme=theme,
        color_by="index",
        opacity=float(opacity),
        line_width=float(line_width),
        fixed_axis_range=True,
        title=f"Hopf Fibers — {str(mode).replace('_', ' ').title()}",
    )
    for fig in frames:
        fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color="#8ecae6"))
        fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color="#8ecae6"))

    if len(_FRAME_CACHE) >= _FRAME_CACHE_MAX:
        _FRAME_CACHE.pop(next(iter(_FRAME_CACHE)))
    _FRAME_CACHE[key] = frames
    return frames


def frames_to_state_payload(frames: list[go.Figure]) -> list[dict[str, Any]]:
    """Serialize figures for ``gr.State`` (JSON-safe Plotly dicts)."""
    return [f.to_plotly_json() for f in frames]


def figure_from_state_payload(payload: dict[str, Any] | go.Figure) -> go.Figure:
    """Restore a Plotly figure from state or pass-through."""
    if isinstance(payload, go.Figure):
        return payload
    return go.Figure(payload)


def build_hopf_animation_frame(
    n_fibers: int = 12,
    n_points: int = 100,
    *,
    frame_idx: int = 0,
    n_frames: int = 60,
    mode: str = "twist",
    eta: float = 0.6,
    xi1: float = 1.2,
    projection_scale: float = 1.0,
    height: int = 600,
    bake: bool = True,
) -> go.Figure:
    """One animation frame for ``gr.Plot`` (uses bake cache by default)."""
    frames = bake_hopf_animation_frames(
        n_fibers=n_fibers,
        n_points=n_points,
        n_frames=n_frames,
        mode=mode,
        eta=eta,
        xi1=xi1,
        projection_scale=projection_scale,
        height=height,
        force=not bake,
    )
    return frames[int(frame_idx) % len(frames)]


def build_hopf_fiber_animation(
    n_fibers: int = 12,
    n_points: int = 100,
    n_frames: int = 60,
    *,
    mode: str = "twist",
    eta: float = 0.6,
    xi1: float = 1.2,
    projection_scale: float = 1.0,
    height: int = 600,
    frame_idx: int = 0,
    **_kwargs: Any,
) -> go.Figure:
    """Alias for :func:`build_hopf_animation_frame`."""
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
        bake=True,
    )


def export_kingdom_hopf_animation_mp4(
    n_fibers: int = 10,
    n_points: int = 90,
    n_frames: int = 48,
    *,
    mode: str = "xi1_orbit",
    eta: float = 0.6,
    xi1: float = 1.2,
    projection_scale: float = 1.0,
    path: str = "/tmp/kingdom_hopf_animation.mp4",
    fps: int = 18,
) -> str:
    """Bake frames and export MP4 for ``gr.Video`` (requires kaleido + imageio)."""
    if export_hopf_fiber_animation_mp4 is None:
        raise ImportError("export_hopf_fiber_animation_mp4 not available in flux-hopf-lib")
    frames = bake_hopf_animation_frames(
        n_fibers=n_fibers,
        n_points=n_points,
        n_frames=n_frames,
        mode=mode,
        eta=eta,
        xi1=xi1,
        projection_scale=projection_scale,
        height=560,
        force=False,
    )
    return export_hopf_fiber_animation_mp4(
        frames,
        path=path,
        fps=fps,
        width=960,
        height=640,
    )


def build_hopf_fibration_figure_auto(
    view_mode: ViewMode | str = "auto",
    **kwargs: Any,
) -> go.Figure:
    mode = resolve_view_mode(view_mode)
    if mode == "2d":
        return build_hopf_fibration_figure_2d(**kwargs)
    return build_hopf_fibration_figure(**kwargs)


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
    "bake_hopf_animation_frames",
    "clear_animation_frame_cache",
    "frames_to_state_payload",
    "figure_from_state_payload",
    "export_kingdom_hopf_animation_mp4",
    "fiber_family_choices",
    "s2_to_hopf_angles",
    "plot_hopf_fibers_stereographic",
    "FIBER_COLORS",
]
