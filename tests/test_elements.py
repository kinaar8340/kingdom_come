"""Tests for periodic table element data."""

import plotly.graph_objects as go

from app.components.neon import element_card_html, toe_interpretation_html
from kingdom.core.elements import NOBLE_GAS_Z, get_element, shell_occupancies
from kingdom.core.flux_explorer import explore_flux_element, flux_metrics_table, noble_gas_art_path
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


def test_flux_metrics_table():
    payload = explore_flux_element(2)
    table = flux_metrics_table(payload["flywheel"])
    assert table[0] == ["Stability score", "8.0"]
    assert any(row[0] == "pseudo_Z (sweep ID)" for row in table)
    assert payload["metrics_table"] == table


def test_compact_element_card():
    payload = explore_flux_element(2)
    html = element_card_html(payload["element"], payload["flywheel"])
    assert "Helium" in html
    assert "TOE interpretation" not in html


def test_toe_interpretation_accordion_content():
    payload = explore_flux_element(2)
    html = toe_interpretation_html(payload["element"], payload["flywheel"])
    assert "Hopf fiber bundle" in html
    assert "TOE interpretation" in html


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