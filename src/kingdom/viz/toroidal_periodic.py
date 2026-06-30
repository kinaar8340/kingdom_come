"""Toroidal periodic table × Flux Flywheel hybrid (Kingdom Come + (1,7) coil)."""

from __future__ import annotations

from typing import Any, Literal

import numpy as np
import plotly.graph_objects as go

from kingdom.core.elements import NOBLE_GAS_Z, get_element
from kingdom.core.flux_flywheel import map_z_to_flywheel
from kingdom.core.periodic_meta import period_group_category
from kingdom.viz.hopf_plotly import ACCENT_GOLD, BG_DARK, GRID, kingdom_dark_theme

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

ToroidalViewMode = Literal["3d", "2d"]
Projection2D = Literal["xy", "xz", "yz"]

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
FLUX_GOLD_BRIGHT = "rgba(255, 214, 90, 0.95)"
COIL_P = 1
COIL_Q = 7
Z_MAX = 118

_STABILITY_LEGEND_ANNOTATION = dict(
    text=(
        "<b>Marker size</b> ∝ flux stability (5–10)<br>"
        "<b>Color wash</b> low → high stability"
    ),
    xref="paper",
    yref="paper",
    x=0.01,
    y=0.99,
    xanchor="left",
    yanchor="top",
    showarrow=False,
    font=dict(size=10, color="#a8c4e0"),
    bgcolor="rgba(10,22,40,0.82)",
    bordercolor="rgba(30,58,95,0.9)",
    borderwidth=1,
    borderpad=6,
)


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
        period, group, category = period_group_category(z)
        config = el.electron_config if el else "—"
        rows.append({
            "z": z,
            "symbol": symbol,
            "name": el.name if el else f"Z = {z}",
            "x": x,
            "y": y,
            "zc": zc,
            "u": u,
            "v": v,
            "period": period,
            "group": group,
            "category": category,
            "electron_config": config,
            "color": BLOCK_COLORS.get(category, "#8ecae6"),
            "stability": float(fw["stability_score"]),
            "stability_class": fw["stability_class"],
            "flux_notes": fw["notes"],
            "is_noble": z in NOBLE_GAS_Z,
            "flywheel_r": 0.08 + 0.018 * float(fw["stability_score"]),
        })
    return rows


def _stability_fill_color(score: float) -> str:
    """Continuous stability tint for marker faces (5–10 scale)."""
    t = max(0.0, min(1.0, (score - 5.0) / 3.5))
    # deep navy → teal → gold
    stops = [(0.0, (26, 58, 95)), (0.55, (0, 201, 183)), (1.0, (201, 162, 39))]
    if t <= 0.55:
        u = t / 0.55
        r = int(stops[0][1][0] + u * (stops[1][1][0] - stops[0][1][0]))
        g = int(stops[0][1][1] + u * (stops[1][1][1] - stops[0][1][1]))
        b = int(stops[0][1][2] + u * (stops[1][1][2] - stops[0][1][2]))
    else:
        u = (t - 0.55) / 0.45
        r = int(stops[1][1][0] + u * (stops[2][1][0] - stops[1][1][0]))
        g = int(stops[1][1][1] + u * (stops[2][1][1] - stops[1][1][1]))
        b = int(stops[1][1][2] + u * (stops[2][1][2] - stops[1][1][2]))
    return f"rgb({r},{g},{b})"


def _blend_block_and_stability(block_hex: str, score: float, *, weight: float = 0.35) -> str:
    """Tint block color with stability gradient so markers read on dark backgrounds."""
    block = block_hex.lstrip("#")
    br, bg, bb = int(block[0:2], 16), int(block[2:4], 16), int(block[4:6], 16)
    stab = _stability_fill_color(score).removeprefix("rgb(").removesuffix(")").split(",")
    sr, sg, sb = int(stab[0]), int(stab[1]), int(stab[2])
    w = weight
    r = int((1 - w) * br + w * sr)
    g = int((1 - w) * bg + w * sg)
    b = int((1 - w) * bb + w * sb)
    return f"rgb({r},{g},{b})"


def _rich_hover(row: dict[str, Any]) -> str:
    chem_line = (
        "Chemistry ↔ flux: closed-shell lock aligns with high stability"
        if row["is_noble"]
        else f"Chemistry ↔ flux: {row['flux_notes']}"
    )
    return (
        f"<b>{row['name']}</b> ({row['symbol']}, Z={row['z']})<br>"
        f"Period {row['period']}, group {row['group']} · {row['category']}<br>"
        f"Config: {row['electron_config']}<br>"
        f"Flux stability: <b>{row['stability']:.1f}</b>/10 — {row['stability_class']}<br>"
        f"{chem_line}"
        + ("<br>✦ noble gas lock" if row["is_noble"] else "")
    )


def _project_2d(row: dict[str, Any], projection: Projection2D) -> tuple[float, float]:
    if projection == "xz":
        return row["x"], row["zc"]
    if projection == "yz":
        return row["y"], row["zc"]
    return row["x"], row["y"]


def _partition_layout(
    layout: list[dict[str, Any]],
    *,
    z_highlight: int | None,
    focus_mode: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split layout into background + foreground when focus mode is active."""
    if not focus_mode or z_highlight is None:
        return layout, []
    bg = [r for r in layout if r["z"] != z_highlight]
    fg = [r for r in layout if r["z"] == z_highlight]
    return bg, fg


def _element_marker_trace_3d(
    rows: list[dict[str, Any]],
    *,
    sizes: list[float],
    show_labels: bool,
    opacity: float,
    name: str = "Elements",
) -> go.Scatter3d:
    colors = [_blend_block_and_stability(r["color"], r["stability"]) for r in rows]
    line_colors = [r["color"] for r in rows]
    texts = [r["symbol"] if show_labels else "" for r in rows]
    hover = [_rich_hover(r) for r in rows]
    return go.Scatter3d(
        x=[r["x"] for r in rows],
        y=[r["y"] for r in rows],
        z=[r["zc"] for r in rows],
        mode="markers+text" if show_labels else "markers",
        text=texts,
        textfont=dict(size=8, color="#e8f4ff"),
        textposition="middle center",
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(width=2.5, color=line_colors),
            opacity=opacity,
        ),
        name=name,
        hovertext=hover,
        hoverinfo="text",
    )


def _element_marker_trace_2d(
    rows: list[dict[str, Any]],
    *,
    projection: Projection2D,
    sizes: list[float],
    show_labels: bool,
    opacity: float,
    name: str = "Elements",
) -> go.Scatter:
    colors = [_blend_block_and_stability(r["color"], r["stability"]) for r in rows]
    line_colors = [r["color"] for r in rows]
    texts = [r["symbol"] if show_labels else "" for r in rows]
    hover = [_rich_hover(r) for r in rows]
    xs = [_project_2d(r, projection)[0] for r in rows]
    ys = [_project_2d(r, projection)[1] for r in rows]
    return go.Scatter(
        x=xs,
        y=ys,
        mode="markers+text" if show_labels else "markers",
        text=texts,
        textfont=dict(size=9, color="#e8f4ff"),
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(width=2.5, color=line_colors),
            opacity=opacity,
        ),
        name=name,
        hovertext=hover,
        hoverinfo="text",
    )


def _period_color(period: int, *, alpha: float = 0.55) -> str:
    hex_color = _PERIOD_COLORS[(period - 1) % len(_PERIOD_COLORS)]
    rgb = tuple(int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    return f"rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha})"


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


def _coil_backbone_trace_3d(layout: list[dict[str, Any]]) -> go.Scatter3d:
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


def _coil_period_band_traces_3d(layout: list[dict[str, Any]]) -> list[go.Scatter3d]:
    """Faint period-colored segments along the sequential coil."""
    traces: list[go.Scatter3d] = []
    for idx in range(len(layout)):
        row = layout[idx]
        nxt = layout[(idx + 1) % len(layout)]
        traces.append(
            go.Scatter3d(
                x=[row["x"], nxt["x"]],
                y=[row["y"], nxt["y"]],
                z=[row["zc"], nxt["zc"]],
                mode="lines",
                line=dict(color=_period_color(row["period"], alpha=0.42), width=5),
                showlegend=False,
                hoverinfo="skip",
            )
        )
    return traces


def _coil_path_trace_2d(
    layout: list[dict[str, Any]],
    *,
    projection: Projection2D = "xy",
    show_period_bands: bool = True,
) -> list[go.Scatter]:
    traces: list[go.Scatter] = []
    if show_period_bands:
        for idx in range(len(layout)):
            row = layout[idx]
            nxt = layout[(idx + 1) % len(layout)]
            x0, y0 = _project_2d(row, projection)
            x1, y1 = _project_2d(nxt, projection)
            traces.append(
                go.Scatter(
                    x=[x0, x1],
                    y=[y0, y1],
                    mode="lines",
                    line=dict(
                        color=_period_color(row["period"], alpha=0.38),
                        width=6,
                    ),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )
    xs = [_project_2d(r, projection)[0] for r in layout]
    ys = [_project_2d(r, projection)[1] for r in layout]
    traces.append(
        go.Scatter(
            x=xs + [xs[0]],
            y=ys + [ys[0]],
            mode="lines",
            line=dict(color=ACCENT_GOLD, width=2),
            name=f"({COIL_P},{COIL_Q}) coil",
            hoverinfo="skip",
        )
    )
    return traces


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


def _flux_ring_points_3d(
    row: dict[str, Any],
    *,
    major_r: float,
    minor_r: float,
    scale: float = 1.0,
) -> tuple[list[float], list[float], list[float]]:
    u, v = row["u"], row["v"]
    cx, cy, cz = row["x"], row["y"], row["zc"]
    tangent_u = np.linspace(0, 2 * np.pi, 28)
    ring_r = row["flywheel_r"] * scale
    du = 0.04
    pts_x, pts_y, pts_z = [], [], []
    for t in tangent_u:
        uu = u + du * np.cos(t)
        vv = v + du * np.sin(t) * ring_r * 8
        x, y, z = torus_point(uu, vv, major_r=major_r, minor_r=minor_r)
        pts_x.append(cx + (x - cx) * ring_r * 3)
        pts_y.append(cy + (y - cy) * ring_r * 3)
        pts_z.append(cz + (z - cz) * ring_r * 3)
    return pts_x, pts_y, pts_z


def _flux_ring_trace_3d(
    row: dict[str, Any],
    *,
    major_r: float = 3.0,
    minor_r: float = 1.0,
    emphasized: bool = False,
) -> list[go.Scatter3d]:
    """Small gold ring in the tangent plane at the element site (flux flywheel metaphor)."""
    scale = 1.55 if emphasized else 1.0
    pts_x, pts_y, pts_z = _flux_ring_points_3d(
        row, major_r=major_r, minor_r=minor_r, scale=scale
    )
    dash = "solid" if emphasized or row["is_noble"] or row["stability"] >= 7.5 else "dash"
    color = FLUX_GOLD_BRIGHT if emphasized else FLUX_GOLD
    width = 5 if emphasized else (2 if row["is_noble"] else 1)
    traces = [
        go.Scatter3d(
            x=pts_x,
            y=pts_y,
            z=pts_z,
            mode="lines",
            line=dict(color=color, width=width, dash=dash),
            showlegend=False,
            hoverinfo="skip",
        )
    ]
    if emphasized:
        glow_x, glow_y, glow_z = _flux_ring_points_3d(
            row, major_r=major_r, minor_r=minor_r, scale=scale * 1.25
        )
        traces.append(
            go.Scatter3d(
                x=glow_x,
                y=glow_y,
                z=glow_z,
                mode="lines",
                line=dict(color="rgba(255,214,90,0.22)", width=9),
                showlegend=False,
                hoverinfo="skip",
            )
        )
    return traces


def _flux_ring_trace_2d(
    row: dict[str, Any],
    *,
    projection: Projection2D,
    emphasized: bool = False,
) -> list[go.Scatter]:
    cx, cy = _project_2d(row, projection)
    theta = np.linspace(0, 2 * np.pi, 32)
    radius = 0.09 + row["flywheel_r"] * (1.7 if emphasized else 1.0)
    xs = cx + radius * np.cos(theta)
    ys = cy + radius * np.sin(theta)
    color = FLUX_GOLD_BRIGHT if emphasized else FLUX_GOLD
    width = 3.5 if emphasized else 1.5
    traces = [
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            line=dict(color=color, width=width, dash="solid" if emphasized else "dash"),
            showlegend=False,
            hoverinfo="skip",
        )
    ]
    if emphasized:
        traces.insert(
            0,
            go.Scatter(
                x=cx + radius * 1.2 * np.cos(theta),
                y=cy + radius * 1.2 * np.sin(theta),
                mode="lines",
                line=dict(color="rgba(255,214,90,0.18)", width=8),
                showlegend=False,
                hoverinfo="skip",
            ),
        )
    return traces


def _marker_glow_trace_3d(
    layout: list[dict[str, Any]],
    *,
    sizes: list[float],
    z_highlight: int | None,
    focus_mode: bool,
) -> go.Scatter3d | None:
    glow_x, glow_y, glow_z, glow_c, glow_s = [], [], [], [], []
    for row, size in zip(layout, sizes):
        if focus_mode and z_highlight is not None and row["z"] != z_highlight:
            continue
        glow_x.append(row["x"])
        glow_y.append(row["y"])
        glow_z.append(row["zc"])
        glow_c.append(row["color"])
        glow_s.append(size + 5)
    if not glow_x:
        return None
    return go.Scatter3d(
        x=glow_x,
        y=glow_y,
        z=glow_z,
        mode="markers",
        marker=dict(
            size=glow_s,
            color=glow_c,
            opacity=0.22,
            line=dict(width=0),
        ),
        showlegend=False,
        hoverinfo="skip",
    )


def _marker_glow_trace_2d(
    layout: list[dict[str, Any]],
    *,
    projection: Projection2D,
    sizes: list[float],
    z_highlight: int | None,
    focus_mode: bool,
) -> go.Scatter | None:
    glow_x, glow_y, glow_c, glow_s = [], [], [], []
    for row, size in zip(layout, sizes):
        if focus_mode and z_highlight is not None and row["z"] != z_highlight:
            continue
        px, py = _project_2d(row, projection)
        glow_x.append(px)
        glow_y.append(py)
        glow_c.append(row["color"])
        glow_s.append(size + 6)
    if not glow_x:
        return None
    return go.Scatter(
        x=glow_x,
        y=glow_y,
        mode="markers",
        marker=dict(
            size=glow_s,
            color=glow_c,
            opacity=0.24,
            line=dict(width=0),
        ),
        showlegend=False,
        hoverinfo="skip",
    )


def _stability_colorbar_trace() -> go.Scatter:
    """Invisible stability gradient used only for the colorbar legend."""
    return go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(
            size=0.1,
            color=[5, 6.5, 8, 9.5, 10],
            colorscale=[
                [0.0, "#1a3a5f"],
                [0.45, "#00c9b7"],
                [1.0, "#c9a227"],
            ],
            cmin=5,
            cmax=10,
            colorbar=dict(
                title=dict(text="Flux stability", side="right", font=dict(size=10)),
                thickness=12,
                len=0.35,
                x=1.02,
                tickvals=[5, 6.5, 8, 9.5, 10],
                ticktext=["5", "6.5", "8", "9.5", "10"],
                bgcolor="rgba(10,22,40,0.75)",
                bordercolor="rgba(30,58,95,0.9)",
                borderwidth=1,
                tickfont=dict(size=9, color="#a8c4e0"),
            ),
            showscale=True,
        ),
        hoverinfo="skip",
        showlegend=False,
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
    show_period_bands: bool = True,
    focus_mode: bool = False,
    projection_2d: Projection2D = "xy",
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
            show_period_bands=show_period_bands,
            show_flux_rings=show_flux_rings,
            focus_mode=focus_mode,
            projection=projection_2d,
            height=height,
        )

    fig = go.Figure()
    wire_opacity = 0.03 if focus_mode and highlight is not None else 0.07
    if show_wireframe:
        for trace in _torus_wireframe_traces(major_r=major_r, minor_r=minor_r):
            trace.opacity = wire_opacity
            fig.add_trace(trace)
    if show_coil:
        if show_period_bands:
            for trace in _coil_period_band_traces_3d(layout):
                fig.add_trace(trace)
        fig.add_trace(_coil_backbone_trace_3d(layout))

    if show_flux_rings:
        ring_targets = layout
        if focus_mode and highlight is not None:
            ring_targets = [r for r in layout if r["z"] == highlight]
        elif highlight is not None:
            ring_targets = [r for r in layout if r["z"] == highlight]
        elif len(layout) > 24:
            ring_targets = [r for r in layout if r["is_noble"] or r["stability"] >= 7.5]
        for row in ring_targets:
            emphasized = highlight is not None and row["z"] == highlight
            for trace in _flux_ring_trace_3d(
                row,
                major_r=major_r,
                minor_r=minor_r,
                emphasized=emphasized,
            ):
                fig.add_trace(trace)

    if show_noble_locks and not (focus_mode and highlight is not None):
        for trace in _noble_lock_traces_3d(layout):
            fig.add_trace(trace)

    size_by_z = {
        row["z"]: 5.5 + row["stability"] * 0.45 + (6 if highlight == row["z"] else 0)
        for row in layout
    }
    bg_rows, fg_rows = _partition_layout(
        layout, z_highlight=highlight, focus_mode=focus_mode
    )
    glow_rows = fg_rows if fg_rows else layout
    glow_sizes = [size_by_z[r["z"]] for r in glow_rows]
    glow = _marker_glow_trace_3d(
        glow_rows, sizes=glow_sizes, z_highlight=highlight, focus_mode=focus_mode
    )
    if glow is not None:
        fig.add_trace(glow)

    if bg_rows:
        fig.add_trace(
            _element_marker_trace_3d(
                bg_rows,
                sizes=[size_by_z[r["z"]] for r in bg_rows],
                show_labels=show_labels,
                opacity=0.14 if focus_mode and highlight is not None else 0.92,
                name="Elements",
            )
        )
    if fg_rows:
        fig.add_trace(
            _element_marker_trace_3d(
                fg_rows,
                sizes=[size_by_z[r["z"]] for r in fg_rows],
                show_labels=show_labels,
                opacity=1.0,
                name="Highlight element",
            )
        )
    elif not bg_rows:
        fig.add_trace(
            _element_marker_trace_3d(
                layout,
                sizes=[size_by_z[r["z"]] for r in layout],
                show_labels=show_labels,
                opacity=0.92,
            )
        )

    fig.add_trace(_stability_colorbar_trace())

    title_suffix = ""
    if highlight is not None:
        el = get_element(highlight)
        sym = el.symbol if el else str(highlight)
        title_suffix = f" — highlight {sym} (Z={highlight})"
    if focus_mode and highlight is not None:
        title_suffix += " · focus mode"

    theme = kingdom_dark_theme()
    theme.pop("margin", None)
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
        annotations=[_STABILITY_LEGEND_ANNOTATION],
        margin=dict(l=0, r=72, t=56, b=0),
    )
    return fig


def _build_toroidal_2d(
    layout: list[dict[str, Any]],
    *,
    z_highlight: int | None,
    show_coil: bool,
    show_labels: bool,
    show_period_bands: bool,
    show_flux_rings: bool,
    focus_mode: bool,
    projection: Projection2D,
    height: int,
) -> go.Figure:
    """Orthographic 2D projection — HF-safe (no WebGL)."""
    proj_label = {"xy": "XY", "xz": "XZ", "yz": "YZ"}[projection]
    fig = go.Figure()
    if show_coil:
        for trace in _coil_path_trace_2d(
            layout,
            projection=projection,
            show_period_bands=show_period_bands,
        ):
            fig.add_trace(trace)

    if show_flux_rings:
        ring_targets = layout
        if focus_mode and z_highlight is not None:
            ring_targets = [r for r in layout if r["z"] == z_highlight]
        elif z_highlight is not None:
            ring_targets = [r for r in layout if r["z"] == z_highlight]
        elif len(layout) > 24:
            ring_targets = [r for r in layout if r["is_noble"] or r["stability"] >= 7.5]
        for row in ring_targets:
            emphasized = z_highlight is not None and row["z"] == z_highlight
            for trace in _flux_ring_trace_2d(
                row, projection=projection, emphasized=emphasized
            ):
                fig.add_trace(trace)

    size_by_z = {
        row["z"]: 7 + row["stability"] * 0.55 + (10 if z_highlight == row["z"] else 0)
        for row in layout
    }
    bg_rows, fg_rows = _partition_layout(
        layout, z_highlight=z_highlight, focus_mode=focus_mode
    )
    glow_rows = fg_rows if fg_rows else layout
    glow_sizes = [size_by_z[r["z"]] for r in glow_rows]
    glow = _marker_glow_trace_2d(
        glow_rows,
        projection=projection,
        sizes=glow_sizes,
        z_highlight=z_highlight,
        focus_mode=focus_mode,
    )
    if glow is not None:
        fig.add_trace(glow)

    if bg_rows:
        fig.add_trace(
            _element_marker_trace_2d(
                bg_rows,
                projection=projection,
                sizes=[size_by_z[r["z"]] for r in bg_rows],
                show_labels=show_labels,
                opacity=0.14 if focus_mode and z_highlight is not None else 0.92,
            )
        )
    if fg_rows:
        fig.add_trace(
            _element_marker_trace_2d(
                fg_rows,
                projection=projection,
                sizes=[size_by_z[r["z"]] for r in fg_rows],
                show_labels=show_labels,
                opacity=1.0,
                name="Highlight element",
            )
        )
    elif not bg_rows:
        fig.add_trace(
            _element_marker_trace_2d(
                layout,
                projection=projection,
                sizes=[size_by_z[r["z"]] for r in layout],
                show_labels=show_labels,
                opacity=0.92,
            )
        )

    if z_highlight is not None:
        row = next(r for r in layout if r["z"] == z_highlight)
        hx, hy = _project_2d(row, projection)
        fig.add_trace(
            go.Scatter(
                x=[hx],
                y=[hy],
                mode="markers",
                marker=dict(
                    size=32,
                    color="rgba(201,162,39,0.35)",
                    line=dict(width=4, color=FLUX_GOLD_SOLID),
                ),
                name="Highlight",
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig.add_trace(_stability_colorbar_trace())

    title_suffix = ""
    if z_highlight is not None:
        el = get_element(z_highlight)
        sym = el.symbol if el else str(z_highlight)
        title_suffix = f" — {sym} (Z={z_highlight})"
    if focus_mode and z_highlight is not None:
        title_suffix += " · focus"

    theme = kingdom_dark_theme()
    theme.pop("margin", None)
    fig.update_layout(
        **theme,
        height=height,
        title=f"Toroidal Periodic × Flux Flywheel ({proj_label} projection){title_suffix}",
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x"),
        annotations=[_STABILITY_LEGEND_ANNOTATION],
        margin=dict(l=0, r=72, t=56, b=0),
    )
    return fig


def toroidal_element_positions_dataframe():
    """Tabular coil layout for tests and optional ScatterPlot export."""
    import pandas as pd

    rows = _element_layout()
    return pd.DataFrame(rows)