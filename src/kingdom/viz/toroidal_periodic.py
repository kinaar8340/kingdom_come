"""Toroidal periodic table × Flux Flywheel hybrid (Kingdom Come + (1,7) coil)."""

from __future__ import annotations

from typing import Any, Literal

import numpy as np
import plotly.graph_objects as go

from kingdom.core.elements import NOBLE_GAS_Z, get_element
from kingdom.core.flux_flywheel import map_z_to_flywheel
from kingdom.core.periodic_meta import period_group_category
from kingdom.viz.hopf_plotly import ACCENT_GOLD, BG_DARK, GRID, kingdom_dark_theme

ToroidalViewMode = Literal["3d", "2d"]

BLOCK_COLORS: dict[str, str] = {
    "alkali metal": "#ef553b",
    "alkaline earth metal": "#ff8c42",
    "transition metal": "#ffd45a",
    "post-transition metal": "#c9a227",
    "metalloid": "#48bfe3",
    "nonmetal": "#00c9b7",
    "halogen": "#4cc9f0",
    "noble gas": "#00c9b7",
    "lanthanide": "#c77dff",
    "actinide": "#7b2cbf",
    "superheavy": "#ef553b",
}

FLUX_GOLD = "rgba(201, 162, 39, 0.55)"
FLUX_GOLD_SOLID = "#c9a227"
COIL_P = 1
COIL_Q = 7
Z_MAX = 118


def torus_point(
    u: float,
    v: float,
    *,
    major_r: float = 3.0,
    minor_r: float = 1.0,
) -> tuple[float, float, float]:
    """Parametric point on a standard torus."""
    return (
        (major_r + minor_r * np.cos(v)) * np.cos(u),
        (major_r + minor_r * np.cos(v)) * np.sin(u),
        minor_r * np.sin(v),
    )


def coil_uv(
    z: int,
    *,
    z_max: int = Z_MAX,
    p: int = COIL_P,
    q: int = COIL_Q,
) -> tuple[float, float]:
    """Map atomic number Z to (u, v) on a (p, q) torus coil."""
    z_clamped = max(1, min(z_max, int(z)))
    t = (z_clamped - 1) / z_max * 2 * np.pi * q
    u = p * t
    v = q * t
    return float(u % (2 * np.pi)), float(v % (2 * np.pi))


def _element_layout(
    *,
    z_max: int = Z_MAX,
    major_r: float = 3.0,
    minor_r: float = 1.0,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for z in range(1, z_max + 1):
        u, v = coil_uv(z, z_max=z_max)
        x, y, zc = torus_point(u, v, major_r=major_r, minor_r=minor_r)
        fw = map_z_to_flywheel(z)
        el = get_element(z)
        symbol = el.symbol if el else f"Z{z}"
        _, _, category = period_group_category(z)
        rows.append({
            "z": z,
            "symbol": symbol,
            "name": el.name if el else f"Z = {z}",
            "x": x,
            "y": y,
            "zc": zc,
            "u": u,
            "v": v,
            "category": category,
            "color": BLOCK_COLORS.get(category, "#8ecae6"),
            "stability": float(fw["stability_score"]),
            "stability_class": fw["stability_class"],
            "is_noble": z in NOBLE_GAS_Z,
            "flywheel_r": 0.08 + 0.018 * float(fw["stability_score"]),
        })
    return rows


def _torus_wireframe_traces(
    *,
    major_r: float,
    minor_r: float,
    nu: int = 40,
    nv: int = 20,
) -> list[go.Surface]:
    u_grid = np.linspace(0, 2 * np.pi, nu)
    v_grid = np.linspace(0, 2 * np.pi, nv)
    U, V = np.meshgrid(u_grid, v_grid)
    X = (major_r + minor_r * np.cos(V)) * np.cos(U)
    Y = (major_r + minor_r * np.cos(V)) * np.sin(U)
    Z = minor_r * np.sin(V)
    return [
        go.Surface(
            x=X,
            y=Y,
            z=Z,
            opacity=0.07,
            colorscale=[[0, GRID], [1, GRID]],
            showscale=False,
            hoverinfo="skip",
            name="Torus grid",
        )
    ]


def _coil_path_trace(layout: list[dict[str, Any]]) -> go.Scatter3d | go.Scatter:
    xs = [r["x"] for r in layout]
    ys = [r["y"] for r in layout]
    zs = [r["zc"] for r in layout]
    return go.Scatter3d(
        x=xs + [xs[0]],
        y=ys + [ys[0]],
        z=zs + [zs[0]],
        mode="lines",
        line=dict(color=ACCENT_GOLD, width=3),
        name=f"({COIL_P},{COIL_Q}) coil",
        hoverinfo="skip",
    )


def _coil_path_trace_2d(layout: list[dict[str, Any]]) -> go.Scatter:
    xs = [r["x"] for r in layout]
    ys = [r["y"] for r in layout]
    return go.Scatter(
        x=xs + [xs[0]],
        y=ys + [ys[0]],
        mode="lines",
        line=dict(color=ACCENT_GOLD, width=2),
        name=f"({COIL_P},{COIL_Q}) coil",
        hoverinfo="skip",
    )


def _noble_lock_traces_3d(layout: list[dict[str, Any]]) -> list[go.Scatter3d]:
    traces: list[go.Scatter3d] = []
    for row in layout:
        if not row["is_noble"]:
            continue
        traces.append(
            go.Scatter3d(
                x=[row["x"]],
                y=[row["y"]],
                z=[row["zc"]],
                mode="markers",
                marker=dict(
                    size=16,
                    color="rgba(201,162,39,0.28)",
                    line=dict(width=4, color=FLUX_GOLD_SOLID),
                    symbol="circle",
                ),
                name=f"Noble lock {row['symbol']}",
                showlegend=False,
                hoverinfo="skip",
            )
        )
    return traces


def _flux_ring_trace_3d(
    row: dict[str, Any],
    *,
    major_r: float = 3.0,
    minor_r: float = 1.0,
) -> go.Scatter3d:
    """Small gold ring in the tangent plane at the element site (flux flywheel metaphor)."""
    u, v = row["u"], row["v"]
    cx, cy, cz = row["x"], row["y"], row["zc"]
    tangent_u = np.linspace(0, 2 * np.pi, 24)
    ring_r = row["flywheel_r"]
    du = 0.04
    pts_x, pts_y, pts_z = [], [], []
    for t in tangent_u:
        uu = u + du * np.cos(t)
        vv = v + du * np.sin(t) * ring_r * 8
        x, y, z = torus_point(uu, vv, major_r=major_r, minor_r=minor_r)
        pts_x.append(cx + (x - cx) * ring_r * 3)
        pts_y.append(cy + (y - cy) * ring_r * 3)
        pts_z.append(cz + (z - cz) * ring_r * 3)
    dash = "solid" if row["is_noble"] or row["stability"] >= 7.5 else "dash"
    return go.Scatter3d(
        x=pts_x,
        y=pts_y,
        z=pts_z,
        mode="lines",
        line=dict(color=FLUX_GOLD, width=2 if row["is_noble"] else 1, dash=dash),
        showlegend=False,
        hoverinfo="skip",
    )


def build_toroidal_periodic_figure(
    *,
    z_highlight: int | None = None,
    major_r: float = 3.0,
    minor_r: float = 1.0,
    show_wireframe: bool = True,
    show_coil: bool = True,
    show_flux_rings: bool = True,
    show_noble_locks: bool = True,
    show_labels: bool = True,
    view_mode: ToroidalViewMode = "3d",
    height: int = 580,
) -> go.Figure:
    """
    Toroidal (1,7) coil of all 118 elements with Kingdom Come flux flywheel overlays.
    """
    layout = _element_layout(major_r=major_r, minor_r=minor_r)
    highlight = z_highlight if z_highlight is not None else None

    if view_mode == "2d":
        return _build_toroidal_2d(
            layout,
            z_highlight=highlight,
            show_coil=show_coil,
            show_labels=show_labels,
            height=height,
        )

    fig = go.Figure()
    if show_wireframe:
        for trace in _torus_wireframe_traces(major_r=major_r, minor_r=minor_r):
            fig.add_trace(trace)
    if show_coil:
        fig.add_trace(_coil_path_trace(layout))

    if show_flux_rings:
        ring_targets = layout
        if highlight is not None:
            ring_targets = [r for r in layout if r["z"] == highlight]
        elif len(layout) > 24:
            ring_targets = [r for r in layout if r["is_noble"] or r["stability"] >= 7.5]
        for row in ring_targets:
            fig.add_trace(
                _flux_ring_trace_3d(row, major_r=major_r, minor_r=minor_r)
            )

    if show_noble_locks:
        for trace in _noble_lock_traces_3d(layout):
            fig.add_trace(trace)

    sizes = []
    colors = []
    texts = []
    hover = []
    for row in layout:
        base = 5.5 + row["stability"] * 0.45
        if highlight is not None and row["z"] == highlight:
            base += 6
        sizes.append(base)
        colors.append(row["color"])
        texts.append(row["symbol"] if show_labels else "")
        hover.append(
            f"{row['name']} (Z={row['z']})<br>"
            f"{row['category']}<br>"
            f"Flux stability: {row['stability']:.1f}/10<br>"
            f"{row['stability_class']}"
            + ("<br>✦ noble gas lock" if row["is_noble"] else "")
        )

    fig.add_trace(
        go.Scatter3d(
            x=[r["x"] for r in layout],
            y=[r["y"] for r in layout],
            z=[r["zc"] for r in layout],
            mode="markers+text" if show_labels else "markers",
            text=texts,
            textfont=dict(size=8, color="#e8f4ff"),
            textposition="middle center",
            marker=dict(
                size=sizes,
                color=colors,
                line=dict(width=1, color=BG_DARK),
                opacity=0.92,
            ),
            name="Elements",
            hovertext=hover,
            hoverinfo="text",
        )
    )

    title_suffix = ""
    if highlight is not None:
        el = get_element(highlight)
        sym = el.symbol if el else str(highlight)
        title_suffix = f" — highlight {sym} (Z={highlight})"

    theme = kingdom_dark_theme()
    fig.update_layout(
        **theme,
        height=height,
        title=dict(
            text=(
                f"Toroidal Periodic Table × Flux Flywheel "
                f"({COIL_P},{COIL_Q}) coil{title_suffix}"
            ),
            x=0.5,
            font=dict(size=14, color="#e8f4ff"),
        ),
        scene=dict(
            bgcolor=BG_DARK,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data",
        ),
        legend=dict(
            bgcolor="rgba(10,22,40,0.75)",
            font=dict(size=10, color="#d4e4f7"),
        ),
    )
    return fig


def _build_toroidal_2d(
    layout: list[dict[str, Any]],
    *,
    z_highlight: int | None,
    show_coil: bool,
    show_labels: bool,
    height: int,
) -> go.Figure:
    """Orthographic xy projection — HF-safe (no WebGL)."""
    fig = go.Figure()
    if show_coil:
        fig.add_trace(_coil_path_trace_2d(layout))

    sizes, colors, texts, hover = [], [], [], []
    for row in layout:
        base = 7 + row["stability"] * 0.55
        if z_highlight is not None and row["z"] == z_highlight:
            base += 10
        sizes.append(base)
        colors.append(row["color"])
        texts.append(row["symbol"] if show_labels else "")
        hover.append(
            f"{row['name']} (Z={row['z']})<br>"
            f"Flux stability: {row['stability']:.1f}/10"
        )

    fig.add_trace(
        go.Scatter(
            x=[r["x"] for r in layout],
            y=[r["y"] for r in layout],
            mode="markers+text" if show_labels else "markers",
            text=texts,
            textfont=dict(size=9, color="#e8f4ff"),
            marker=dict(size=sizes, color=colors, line=dict(width=1, color=BG_DARK)),
            name="Elements",
            hovertext=hover,
            hoverinfo="text",
        )
    )

    if z_highlight is not None:
        row = next(r for r in layout if r["z"] == z_highlight)
        fig.add_trace(
            go.Scatter(
                x=[row["x"]],
                y=[row["y"]],
                mode="markers",
                marker=dict(
                    size=28,
                    color="rgba(201,162,39,0.35)",
                    line=dict(width=3, color=FLUX_GOLD_SOLID),
                ),
                name="Highlight",
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig.update_layout(
        **kingdom_dark_theme(),
        height=height,
        title="Toroidal Periodic × Flux Flywheel (2D projection)",
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x"),
    )
    return fig


def toroidal_element_positions_dataframe():
    """Tabular coil layout for tests and optional ScatterPlot export."""
    import pandas as pd

    rows = _element_layout()
    return pd.DataFrame(rows)