"""Tests for periodic table element data."""

from kingdom.core.elements import NOBLE_GAS_Z, get_element, shell_occupancies
from kingdom.core.flux_explorer import explore_flux_element
from kingdom.viz.electron_cloud import build_electron_cloud_figure


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
    assert payload["cloud_fig"] is not None


def test_electron_cloud_figure():
    el = get_element(10)
    fig = build_electron_cloud_figure(el, stability_score=7.0)
    assert len(fig.data) >= 3


def test_shell_occupancy_neon():
    shells = shell_occupancies(10)
    total = sum(c for _, c in shells)
    assert total == 10