"""Tests for Z ↔ Monster irrep toroidal overlay."""

from __future__ import annotations

from kingdom.core.elements import NOBLE_GAS_Z
from kingdom.viz.monster_toroidal_bridge import (
    irrep_for_z,
    irrep_toroidal_layout,
    z_to_irrep_map,
)
from kingdom.viz.toroidal_periodic import build_toroidal_periodic_figure


def test_z_to_irrep_linear_mapping():
    m = z_to_irrep_map("linear")
    assert m[1] == 0
    assert m[54] == 53
    assert m[118] == 117
    assert len(m) == 118


def test_noble_lock_maps_nobles_to_distinct_low_sum_irreps():
    m = z_to_irrep_map("noble_lock")
    noble_targets = [m[z] for z in sorted(NOBLE_GAS_Z)]
    assert len(set(noble_targets)) == len(NOBLE_GAS_Z)


def test_irrep_layout_has_194_nodes():
    rows = irrep_toroidal_layout()
    assert len(rows) == 194
    assert rows[0]["irrep_index"] == 0
    assert rows[0]["row_exponent_sum"] == 0


def test_dual_overlay_2d_builds():
    fig = build_toroidal_periodic_figure(
        view_mode="2d",
        z_highlight=54,
        manifold_mode="Dual overlay",
        z_irrep_scheme="Linear (Z−1 → irrep)",
        show_z_irrep_links=True,
    )
    assert len(fig.data) >= 4
    assert "dual" in str(fig.layout.title).lower()


def test_irreps_only_mode_builds():
    fig = build_toroidal_periodic_figure(
        view_mode="2d",
        z_highlight=1,
        manifold_mode="Monster irreps only",
        z_irrep_scheme="Stability rank",
    )
    assert len(fig.data) >= 1
    assert irrep_for_z(54, "linear") == 53