"""Tests for periodic table element data."""

import plotly.graph_objects as go

from kingdom.core.elements import NOBLE_GAS_Z, get_element, shell_occupancies
from app.components.neon import flux_metrics_accordion_html
from kingdom.core.flux_explorer import explore_flux_element, noble_gas_art_path
from kingdom.viz.electron_cloud import build_electron_cloud_figure
from kingdom.viz.magic_island import build_magic_island_heatmap


def test_noble_gases():
    for z in (2, 10, 18, 36, 54, 86, 118):
        el = get_element(z)
        assert el is not None
        assert el.is_noble_gas
        assert el.symbol in ("He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og")


def test_helium_magic_island():
    payload = explore_flux_element(2)
    assert payload["flywheel"]["stability_score"] == 8.0
    assert payload["element"].symbol == "He"
    assert isinstance(payload["cloud_fig"], go.Figure)
    assert isinstance(payload["magic_island"], go.Figure)


def test_electron_cloud_figure():
    el = get_element(10)
    fig = build_electron_cloud_figure(el, stability_score=7.0)
    assert len(fig.data) >= 3


def test_shell_occupancy_neon():
    shells = shell_occupancies(10)
    total = sum(c for _, c in shells)
    assert total == 10


def test_flux_metrics_accordion():
    payload = explore_flux_element(2)
    html = flux_metrics_accordion_html(2, payload["flywheel"])
    assert "<details" in html
    assert "Stability score" in html
    assert "pseudo_Z" in html


def test_toe_narrative_noble_gas():
    el = get_element(2)
    assert el is not None
    assert "Hopf fiber bundle" in el.toe_narrative


def test_magic_island_heatmap():
    fig = build_magic_island_heatmap(current_z=2)
    assert len(fig.data) >= 3


def test_explore_flux_magic_island_and_art():
    payload = explore_flux_element(2)
    assert payload["magic_island"] is not None
    assert payload["is_noble"] is True
    art = noble_gas_art_path(2)
    if art is not None:
        assert art.endswith(".png")


def test_synthetic_z_129():
    payload = explore_flux_element(129)
    assert payload["is_pseudo_z"] is True
    assert payload["element"] is None