"""Tests for toroidal periodic × flux flywheel hybrid."""

from __future__ import annotations

from kingdom.core.elements import NOBLE_GAS_Z
from kingdom.viz.toroidal_periodic import (
    build_toroidal_periodic_figure,
    coil_uv,
    toroidal_element_positions_dataframe,
    torus_point,
)


def test_torus_point_on_surface():
    x, y, z = torus_point(0.0, 0.0, major_r=3.0, minor_r=1.0)
    assert abs((x**2 + y**2) ** 0.5 - 4.0) < 1e-9
    assert abs(z) < 1e-9


def test_coil_uv_maps_all_z():
    for z in range(1, 119):
        u, v = coil_uv(z)
        assert 0 <= u < 2 * 3.14159265
        assert 0 <= v < 2 * 3.14159265


def test_element_layout_dataframe_has_118_rows():
    df = toroidal_element_positions_dataframe()
    assert len(df) == 118
    assert set(df.columns) >= {"z", "symbol", "stability", "category", "is_noble"}


def test_noble_gas_count_in_layout():
    df = toroidal_element_positions_dataframe()
    assert int(df["is_noble"].sum()) == len(NOBLE_GAS_Z)


def test_plotly_3d_figure_builds():
    fig = build_toroidal_periodic_figure(view_mode="3d", z_highlight=54)
    assert len(fig.data) >= 3
    assert any(trace.type == "scatter3d" for trace in fig.data)


def test_plotly_2d_figure_builds_without_webgl():
    fig = build_toroidal_periodic_figure(view_mode="2d", z_highlight=54)
    assert len(fig.data) >= 1
    assert any(trace.type == "scatter" for trace in fig.data)


def test_focus_mode_and_period_bands():
    fig = build_toroidal_periodic_figure(
        view_mode="2d",
        z_highlight=54,
        focus_mode=True,
        show_period_bands=True,
    )
    assert len(fig.data) >= 3
    assert fig.layout.annotations


def test_xz_projection_builds():
    fig = build_toroidal_periodic_figure(view_mode="2d", projection_2d="xz")
    assert len(fig.data) >= 1
    assert "XZ" in str(fig.layout.title)


def test_toroidal_gallery_asset_exists():
    from app.pages.toroidal_periodic import TOROIDAL_GALLERY, TOROIDAL_HYBRID_IMAGE

    assert TOROIDAL_HYBRID_IMAGE.is_file()
    assert len(TOROIDAL_GALLERY) == 1