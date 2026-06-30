"""Toroidal manifold modes with Monster irrep overlay (elements / irreps / dual)."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go

from kingdom.core.elements import get_element
from kingdom.viz.hopf_plotly import ACCENT_GOLD, BG_DARK, kingdom_dark_theme
from kingdom.viz.monster_toroidal_bridge import (
    ManifoldMode,
    ZIrrepScheme,
    irrep_for_z,
    irrep_hover,
    irrep_toroidal_layout,
    z_to_irrep_map,
)
from kingdom.viz.toroidal_periodic import (
    COIL_P,
    COIL_Q,
    FLUX_GOLD_SOLID,
    Projection2D,
    ToroidalViewMode,
    _STABILITY_LEGEND_ANNOTATION,
    _build_toroidal_2d,
    _coil_backbone_trace_3d,
    _coil_path_trace_2d,
    _element_layout,
    _element_marker_trace_2d,
    _element_marker_trace_3d,
    _flux_ring_trace_2d,
    _flux_ring_trace_3d,
    _marker_glow_trace_2d,
    _marker_glow_trace_3d,
    _noble_lock_traces_3d,
    _partition_layout,
    _project_2d,
    _stability_colorbar_trace,
    _torus_wireframe_traces,
)

IRREP_COIL_COLOR = "#9b5de5"
LINK_COLOR = "rgba(199, 125, 255, 0.75)"

_SCHEME_LABELS = {
    "linear": "linear Z−1",
    "stability_rank": "stability rank",
    "noble_lock": "noble lock",
    "period_group": "period×group",
}

_MODE_LABELS = {
    "elements": "elements",
    "irreps": "Monster irreps",
    "dual": "dual overlay",
}


def _parse_scheme(scheme: str) -> ZIrrepScheme:
    key = str(scheme).lower().replace(" ", "_").replace("×", "_")
    if "stability" in key:
        return "stability_rank"
    if "noble" in key:
        return "noble_lock"
    if "period" in key:
        return "period_group"
    return "linear"


def _parse_mode(mode: str) -> ManifoldMode:
    m = str(mode).lower()
    if m.startswith("irrep"):
        return "irreps"
    if "dual" in m:
        return "dual"
    return "elements"


def _irrep_by_index(irrep_layout: list[dict], irrep_index: int) -> dict | None:
    for row in irrep_layout:
        if int(row["irrep_index"]) == int(irrep_index):
            return row
    return None


def _partition_irreps(
    irrep_layout: list[dict],
    *,
    highlight_irrep: int | None,
    focus_mode: bool,
) -> tuple[list[dict], list[dict]]:
    if not focus_mode or highlight_irrep is None:
        return irrep_layout, []
    bg = [r for r in irrep_layout if r["irrep_index"] != highlight_irrep]
    fg = [r for r in irrep_layout if r["irrep_index"] == highlight_irrep]
    return bg, fg


def _irrep_size(row: dict, *, emphasized: bool) -> float:
    base = 5.0 + row["row_exponent_sum"] * 0.22
    return base + (8 if emphasized else 0)


def _irrep_marker_3d(
    rows: list[dict],
    *,
    show_labels: bool,
    opacity: float,
    emphasize_index: int | None,
    name: str,
) -> go.Scatter3d:
    texts = [r["label"] if show_labels else "" for r in rows]
    hover = [irrep_hover(r) for r in rows]
    sizes = [
        _irrep_size(r, emphasized=emphasize_index == r["irrep_index"])
        for r in rows
    ]
    return go.Scatter3d(
        x=[r["x"] for r in rows],
        y=[r["y"] for r in rows],
        z=[r["zc"] for r in rows],
        mode="markers+text" if show_labels else "markers",
        text=texts,
        textfont=dict(size=7, color="#e8d4ff"),
        textposition="middle center",
        marker=dict(
            size=sizes,
            color=[r["color"] for r in rows],
            line=dict(width=2, color=IRREP_COIL_COLOR),
            opacity=opacity,
        ),
        name=name,
        hovertext=hover,
        hoverinfo="text",
    )


def _irrep_marker_2d(
    rows: list[dict],
    *,
    projection: Projection2D,
    show_labels: bool,
    opacity: float,
    emphasize_index: int | None,
    name: str,
) -> go.Scatter:
    texts = [r["label"] if show_labels else "" for r in rows]
    hover = [irrep_hover(r) for r in rows]
    sizes = [
        _irrep_size(r, emphasized=emphasize_index == r["irrep_index"])
        for r in rows
    ]
    return go.Scatter(
        x=[_project_2d(r, projection)[0] for r in rows],
        y=[_project_2d(r, projection)[1] for r in rows],
        mode="markers+text" if show_labels else "markers",
        text=texts,
        textfont=dict(size=7, color="#e8d4ff"),
        marker=dict(
            size=sizes,
            color=[r["color"] for r in rows],
            line=dict(width=2, color=IRREP_COIL_COLOR),
            opacity=opacity,
        ),
        name=name,
        hovertext=hover,
        hoverinfo="text",
    )


def _irrep_coil_3d(irrep_layout: list[dict]) -> go.Scatter3d:
    xs = [r["x"] for r in irrep_layout]
    ys = [r["y"] for r in irrep_layout]
    zs = [r["zc"] for r in irrep_layout]
    return go.Scatter3d(
        x=xs + [xs[0]],
        y=ys + [ys[0]],
        z=zs + [zs[0]],
        mode="lines",
        line=dict(color=IRREP_COIL_COLOR, width=2, dash="dot"),
        name=f"Monster ({COIL_P},{COIL_Q}) coil",
        hoverinfo="skip",
    )


def _irrep_coil_2d(irrep_layout: list[dict], *, projection: Projection2D) -> go.Scatter:
    xs = [_project_2d(r, projection)[0] for r in irrep_layout]
    ys = [_project_2d(r, projection)[1] for r in irrep_layout]
    return go.Scatter(
        x=xs + [xs[0]],
        y=ys + [ys[0]],
        mode="lines",
        line=dict(color=IRREP_COIL_COLOR, width=1.5, dash="dot"),
        name=f"Monster ({COIL_P},{COIL_Q}) coil",
        hoverinfo="skip",
    )


def _link_pairs(
    element_layout: list[dict],
    irrep_layout: list[dict],
    scheme: ZIrrepScheme,
    *,
    z_highlight: int | None,
    show_all: bool,
) -> list[tuple[dict, dict]]:
    mapping = z_to_irrep_map(scheme)
    if show_all:
        zs = range(1, len(element_layout) + 1)
    elif z_highlight is not None:
        zs = [z_highlight]
    else:
        return []
    pairs: list[tuple[dict, dict]] = []
    el_by_z = {int(r["z"]): r for r in element_layout}
    for z in zs:
        el = el_by_z.get(int(z))
        ir = _irrep_by_index(irrep_layout, mapping[int(z)])
        if el and ir:
            pairs.append((el, ir))
    return pairs


def _link_trace_3d(pairs: list[tuple[dict, dict]]) -> list[go.Scatter3d]:
    traces: list[go.Scatter3d] = []
    for el, ir in pairs:
        traces.append(
            go.Scatter3d(
                x=[el["x"], ir["x"]],
                y=[el["y"], ir["y"]],
                z=[el["zc"], ir["zc"]],
                mode="lines",
                line=dict(color=LINK_COLOR, width=3, dash="dash"),
                showlegend=False,
                hoverinfo="skip",
            )
        )
    return traces


def _link_trace_2d(
    pairs: list[tuple[dict, dict]],
    *,
    projection: Projection2D,
) -> list[go.Scatter]:
    traces: list[go.Scatter] = []
    for el, ir in pairs:
        ex, ey = _project_2d(el, projection)
        ix, iy = _project_2d(ir, projection)
        traces.append(
            go.Scatter(
                x=[ex, ix],
                y=[ey, iy],
                mode="lines",
                line=dict(color=LINK_COLOR, width=2, dash="dash"),
                showlegend=False,
                hoverinfo="skip",
            )
        )
    return traces


def _title_suffix(
    *,
    z_highlight: int | None,
    highlight_irrep: int | None,
    scheme: ZIrrepScheme,
    mode: ManifoldMode,
    focus_mode: bool,
) -> str:
    parts: list[str] = []
    if z_highlight is not None:
        el = get_element(z_highlight)
        sym = el.symbol if el else str(z_highlight)
        parts.append(f"{sym} Z={z_highlight}")
    if highlight_irrep is not None and mode != "elements":
        parts.append(f"irrep {highlight_irrep}")
    if mode == "dual":
        parts.append(f"map: {_SCHEME_LABELS[scheme]}")
    if focus_mode:
        parts.append("focus")
    return (" — " + " · ".join(parts)) if parts else ""


def _dual_annotation(mode: ManifoldMode, scheme: ZIrrepScheme) -> dict:
    if mode == "elements":
        return _STABILITY_LEGEND_ANNOTATION
    text = "<b>Gold coil</b> = elements (118)<br><b>Purple coil</b> = Monster irreps (194)"
    if mode == "dual":
        text += f"<br><b>Dashed links</b> = exploratory Z↔irrep ({_SCHEME_LABELS[scheme]})"
    else:
        text += "<br><b>Marker size</b> ∝ exponent sum"
    ann = dict(_STABILITY_LEGEND_ANNOTATION)
    ann["text"] = text
    return ann


def build_toroidal_monster_manifold_figure(
    *,
    z_highlight: int | None,
    major_r: float,
    minor_r: float,
    show_wireframe: bool,
    show_coil: bool,
    show_flux_rings: bool,
    show_noble_locks: bool,
    show_labels: bool,
    show_period_bands: bool,
    focus_mode: bool,
    projection_2d: Projection2D,
    view_mode: ToroidalViewMode,
    manifold_mode: ManifoldMode,
    z_irrep_scheme: ZIrrepScheme,
    show_z_irrep_links: bool,
    show_all_z_irrep_links: bool,
    height: int = 580,
) -> go.Figure:
    """Build toroidal figure for irreps-only or dual element×Monster modes."""
    scheme = z_irrep_scheme
    mode = manifold_mode
    highlight = z_highlight if z_highlight is not None else None
    highlight_irrep = irrep_for_z(highlight, scheme) if highlight is not None else None

    element_layout = _element_layout(major_r=major_r, minor_r=minor_r)
    irrep_layout = irrep_toroidal_layout(
        major_r=major_r * 0.72,
        minor_r=minor_r * 0.52,
    )

    if mode == "irreps" and view_mode == "2d":
        return _build_irrep_2d(
            irrep_layout,
            z_highlight=highlight,
            highlight_irrep=highlight_irrep,
            show_coil=show_coil,
            show_labels=show_labels,
            focus_mode=focus_mode,
            projection=projection_2d,
            scheme=scheme,
            mode=mode,
            height=height,
        )

    if view_mode == "2d":
        return _build_dual_2d(
            element_layout,
            irrep_layout,
            z_highlight=highlight,
            highlight_irrep=highlight_irrep,
            show_coil=show_coil,
            show_labels=show_labels,
            show_period_bands=show_period_bands,
            show_flux_rings=show_flux_rings,
            focus_mode=focus_mode,
            projection=projection_2d,
            scheme=scheme,
            mode=mode,
            show_z_irrep_links=show_z_irrep_links,
            show_all_z_irrep_links=show_all_z_irrep_links,
            height=height,
        )

    return _build_dual_3d(
        element_layout,
        irrep_layout,
        z_highlight=highlight,
        highlight_irrep=highlight_irrep,
        major_r=major_r,
        minor_r=minor_r,
        show_wireframe=show_wireframe,
        show_coil=show_coil,
        show_flux_rings=show_flux_rings,
        show_noble_locks=show_noble_locks,
        show_labels=show_labels,
        show_period_bands=show_period_bands,
        focus_mode=focus_mode,
        scheme=scheme,
        mode=mode,
        show_z_irrep_links=show_z_irrep_links,
        show_all_z_irrep_links=show_all_z_irrep_links,
        height=height,
    )


def _build_irrep_2d(
    irrep_layout: list[dict],
    *,
    z_highlight: int | None,
    highlight_irrep: int | None,
    show_coil: bool,
    show_labels: bool,
    focus_mode: bool,
    projection: Projection2D,
    scheme: ZIrrepScheme,
    mode: ManifoldMode,
    height: int,
) -> go.Figure:
    proj_label = {"xy": "XY", "xz": "XZ", "yz": "YZ"}[projection]
    fig = go.Figure()
    if show_coil:
        fig.add_trace(_irrep_coil_2d(irrep_layout, projection=projection))

    bg, fg = _partition_irreps(
        irrep_layout,
        highlight_irrep=highlight_irrep if focus_mode else None,
        focus_mode=focus_mode,
    )
    if bg:
        fig.add_trace(
            _irrep_marker_2d(
                bg,
                projection=projection,
                show_labels=show_labels,
                opacity=0.14 if focus_mode and highlight_irrep is not None else 0.88,
                emphasize_index=highlight_irrep,
                name="Monster irreps",
            )
        )
    if fg:
        fig.add_trace(
            _irrep_marker_2d(
                fg,
                projection=projection,
                show_labels=show_labels,
                opacity=1.0,
                emphasize_index=highlight_irrep,
                name="Highlight irrep",
            )
        )
    elif not bg:
        fig.add_trace(
            _irrep_marker_2d(
                irrep_layout,
                projection=projection,
                show_labels=show_labels,
                opacity=0.88,
                emphasize_index=highlight_irrep,
                name="Monster irreps",
            )
        )

    theme = kingdom_dark_theme()
    theme.pop("margin", None)
    fig.update_layout(
        **theme,
        height=height,
        title=(
            f"Monster irrep toroidal coil ({proj_label})"
            + _title_suffix(
                z_highlight=z_highlight,
                highlight_irrep=highlight_irrep,
                scheme=scheme,
                mode=mode,
                focus_mode=focus_mode,
            )
        ),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x"),
        annotations=[_dual_annotation(mode, scheme)],
        margin=dict(l=0, r=48, t=56, b=0),
    )
    return fig


def _build_dual_2d(
    element_layout: list[dict],
    irrep_layout: list[dict],
    *,
    z_highlight: int | None,
    highlight_irrep: int | None,
    show_coil: bool,
    show_labels: bool,
    show_period_bands: bool,
    show_flux_rings: bool,
    focus_mode: bool,
    projection: Projection2D,
    scheme: ZIrrepScheme,
    mode: ManifoldMode,
    show_z_irrep_links: bool,
    show_all_z_irrep_links: bool,
    height: int,
) -> go.Figure:
    if mode == "elements":
        return _build_toroidal_2d(
            element_layout,
            z_highlight=z_highlight,
            show_coil=show_coil,
            show_labels=show_labels,
            show_period_bands=show_period_bands,
            show_flux_rings=show_flux_rings,
            focus_mode=focus_mode,
            projection=projection,
            height=height,
        )

    proj_label = {"xy": "XY", "xz": "XZ", "yz": "YZ"}[projection]
    fig = go.Figure()

    if show_coil:
        if mode == "dual":
            for trace in _coil_path_trace_2d(
                element_layout,
                projection=projection,
                show_period_bands=show_period_bands,
            ):
                fig.add_trace(trace)
            fig.add_trace(_irrep_coil_2d(irrep_layout, projection=projection))
        else:
            fig.add_trace(_irrep_coil_2d(irrep_layout, projection=projection))

    if mode == "dual" and show_z_irrep_links:
        pairs = _link_pairs(
            element_layout,
            irrep_layout,
            scheme,
            z_highlight=z_highlight,
            show_all=show_all_z_irrep_links,
        )
        for trace in _link_trace_2d(pairs, projection=projection):
            fig.add_trace(trace)

    if mode == "dual":
        size_by_z = {
            row["z"]: 7 + row["stability"] * 0.55 + (10 if z_highlight == row["z"] else 0)
            for row in element_layout
        }
        el_bg, el_fg = _partition_layout(
            element_layout, z_highlight=z_highlight, focus_mode=focus_mode
        )
        if el_bg:
            fig.add_trace(
                _element_marker_trace_2d(
                    el_bg,
                    projection=projection,
                    sizes=[size_by_z[r["z"]] for r in el_bg],
                    show_labels=show_labels,
                    opacity=0.14 if focus_mode and z_highlight else 0.92,
                    name="Elements",
                )
            )
        if el_fg:
            fig.add_trace(
                _element_marker_trace_2d(
                    el_fg,
                    projection=projection,
                    sizes=[size_by_z[r["z"]] for r in el_fg],
                    show_labels=show_labels,
                    opacity=1.0,
                    name="Highlight element",
                )
            )
        elif not el_bg:
            fig.add_trace(
                _element_marker_trace_2d(
                    element_layout,
                    projection=projection,
                    sizes=[size_by_z[r["z"]] for r in element_layout],
                    show_labels=show_labels,
                    opacity=0.92,
                )
            )

        if show_flux_rings and z_highlight is not None:
            row = next(r for r in element_layout if r["z"] == z_highlight)
            for trace in _flux_ring_trace_2d(
                row, projection=projection, emphasized=True
            ):
                fig.add_trace(trace)

    ir_bg, ir_fg = _partition_irreps(
        irrep_layout,
        highlight_irrep=highlight_irrep if focus_mode else None,
        focus_mode=focus_mode and mode == "dual",
    )
    if ir_bg:
        fig.add_trace(
            _irrep_marker_2d(
                ir_bg,
                projection=projection,
                show_labels=show_labels and mode == "irreps",
                opacity=0.35 if mode == "dual" else 0.88,
                emphasize_index=highlight_irrep,
                name="Monster irreps",
            )
        )
    if ir_fg:
        fig.add_trace(
            _irrep_marker_2d(
                ir_fg,
                projection=projection,
                show_labels=True,
                opacity=1.0,
                emphasize_index=highlight_irrep,
                name="Highlight irrep",
            )
        )
    elif mode == "irreps" and not ir_bg:
        fig.add_trace(
            _irrep_marker_2d(
                irrep_layout,
                projection=projection,
                show_labels=show_labels,
                opacity=0.88,
                emphasize_index=highlight_irrep,
                name="Monster irreps",
            )
        )

    if mode == "dual":
        fig.add_trace(_stability_colorbar_trace())

    theme = kingdom_dark_theme()
    theme.pop("margin", None)
    fig.update_layout(
        **theme,
        height=height,
        title=(
            f"Toroidal × Monster ({_MODE_LABELS[mode]}, {proj_label})"
            + _title_suffix(
                z_highlight=z_highlight,
                highlight_irrep=highlight_irrep,
                scheme=scheme,
                mode=mode,
                focus_mode=focus_mode,
            )
        ),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x"),
        annotations=[_dual_annotation(mode, scheme)],
        margin=dict(l=0, r=72 if mode == "dual" else 48, t=56, b=0),
    )
    return fig


def _build_dual_3d(
    element_layout: list[dict],
    irrep_layout: list[dict],
    *,
    z_highlight: int | None,
    highlight_irrep: int | None,
    major_r: float,
    minor_r: float,
    show_wireframe: bool,
    show_coil: bool,
    show_flux_rings: bool,
    show_noble_locks: bool,
    show_labels: bool,
    show_period_bands: bool,
    focus_mode: bool,
    scheme: ZIrrepScheme,
    mode: ManifoldMode,
    show_z_irrep_links: bool,
    show_all_z_irrep_links: bool,
    height: int,
) -> go.Figure:
    fig = go.Figure()
    wire_opacity = 0.03 if focus_mode and z_highlight else 0.07
    if show_wireframe:
        for trace in _torus_wireframe_traces(major_r=major_r, minor_r=minor_r):
            trace.opacity = wire_opacity
            fig.add_trace(trace)

    if show_coil and mode == "dual":
        fig.add_trace(_coil_backbone_trace_3d(element_layout))
        fig.add_trace(_irrep_coil_3d(irrep_layout))
    elif show_coil:
        fig.add_trace(_irrep_coil_3d(irrep_layout))

    if mode == "dual" and show_z_irrep_links:
        for trace in _link_trace_3d(
            _link_pairs(
                element_layout,
                irrep_layout,
                scheme,
                z_highlight=z_highlight,
                show_all=show_all_z_irrep_links,
            )
        ):
            fig.add_trace(trace)

    if mode == "dual":
        if show_flux_rings and z_highlight is not None:
            row = next(r for r in element_layout if r["z"] == z_highlight)
            for trace in _flux_ring_trace_3d(
                row, major_r=major_r, minor_r=minor_r, emphasized=True
            ):
                fig.add_trace(trace)
        if show_noble_locks and not focus_mode:
            for trace in _noble_lock_traces_3d(element_layout):
                fig.add_trace(trace)

        size_by_z = {
            row["z"]: 5.5 + row["stability"] * 0.45 + (6 if z_highlight == row["z"] else 0)
            for row in element_layout
        }
        el_bg, el_fg = _partition_layout(
            element_layout, z_highlight=z_highlight, focus_mode=focus_mode
        )
        if el_bg:
            fig.add_trace(
                _element_marker_trace_3d(
                    el_bg,
                    sizes=[size_by_z[r["z"]] for r in el_bg],
                    show_labels=show_labels,
                    opacity=0.14 if focus_mode and z_highlight else 0.92,
                    name="Elements",
                )
            )
        if el_fg:
            fig.add_trace(
                _element_marker_trace_3d(
                    el_fg,
                    sizes=[size_by_z[r["z"]] for r in el_fg],
                    show_labels=show_labels,
                    opacity=1.0,
                    name="Highlight element",
                )
            )
        elif not el_bg:
            fig.add_trace(
                _element_marker_trace_3d(
                    element_layout,
                    sizes=[size_by_z[r["z"]] for r in element_layout],
                    show_labels=show_labels,
                    opacity=0.92,
                )
            )

    ir_bg, ir_fg = _partition_irreps(
        irrep_layout,
        highlight_irrep=highlight_irrep if focus_mode else None,
        focus_mode=focus_mode and mode == "dual",
    )
    if ir_bg:
        fig.add_trace(
            _irrep_marker_3d(
                ir_bg,
                show_labels=show_labels and mode == "irreps",
                opacity=0.35 if mode == "dual" else 0.88,
                emphasize_index=highlight_irrep,
                name="Monster irreps",
            )
        )
    if ir_fg:
        fig.add_trace(
            _irrep_marker_3d(
                ir_fg,
                show_labels=True,
                opacity=1.0,
                emphasize_index=highlight_irrep,
                name="Highlight irrep",
            )
        )
    elif mode == "irreps":
        fig.add_trace(
            _irrep_marker_3d(
                irrep_layout,
                show_labels=show_labels,
                opacity=0.88,
                emphasize_index=highlight_irrep,
                name="Monster irreps",
            )
        )

    if mode == "dual":
        fig.add_trace(_stability_colorbar_trace())

    theme = kingdom_dark_theme()
    theme.pop("margin", None)
    fig.update_layout(
        **theme,
        height=height,
        title=dict(
            text=(
                f"Toroidal × Monster ({_MODE_LABELS[mode]}, ({COIL_P},{COIL_Q}) coil)"
                + _title_suffix(
                    z_highlight=z_highlight,
                    highlight_irrep=highlight_irrep,
                    scheme=scheme,
                    mode=mode,
                    focus_mode=focus_mode,
                )
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
        annotations=[_dual_annotation(mode, scheme)],
        margin=dict(l=0, r=72 if mode == "dual" else 48, t=56, b=0),
    )
    return fig