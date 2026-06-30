"""Tests for periodic table element data."""

import plotly.graph_objects as go

from app.components.neon import (
    NEON_CSS,
    element_card_html,
    flux_metrics_cards_html,
    flux_observables_cards_html,
    install_neon_plugin,
    toe_strip_html,
)


def test_install_neon_plugin_returns_css():
    assert install_neon_plugin() == NEON_CSS
    assert ".kc-neon-noble" in install_neon_plugin()
    assert ".kc-obs-fidelity-panel" in install_neon_plugin()
from app.components.periodic_picker import (
    element_picker_choices,
    known_periodic_table_html,
    periodic_table_html,
    picker_label_for_z,
    superheavy_periodic_table_html,
)
from kingdom.core.elements import EXPLORER_Z_MAX, get_element, shell_occupancies
from kingdom.core.flux_explorer import (
    element_art_path,
    explore_flux_element,
    explore_flux_element_extended,
    flux_metrics_table,
)
from kingdom.core.superheavy import systematic_name_symbol
from kingdom.viz.electron_cloud import build_electron_cloud_figure
from kingdom.viz.magic_island import build_magic_island_heatmap


def test_noble_gases():
    for z in (2, 10, 18, 36, 54, 86, 118):
        el = get_element(z)
        assert el is not None
        assert el.is_noble_gas
        assert el.symbol in ("He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og")


def test_iupac_groups_transition_and_f_block():
    fe = get_element(26)
    assert fe.period == 4 and fe.group == 8 and fe.category == "transition metal"
    la = get_element(57)
    assert la.period == 6 and la.group == 3 and la.category == "lanthanide"
    u = get_element(92)
    assert u.period == 7 and u.group == 3 and u.category == "actinide"
    og = get_element(118)
    assert og.period == 7 and og.group == 18


def test_superheavy_systematic_names():
    name, sym = systematic_name_symbol(119)
    assert name == "Ununennium"
    assert sym == "Uue"
    name, sym = systematic_name_symbol(120)
    assert name == "Unbinilium"
    assert sym == "Ubn"
    el = get_element(129)
    assert el is not None
    assert el.is_synthetic
    assert el.name == "Unbiennium"
    assert el.z == 129


def test_superheavy_zone_populates():
    for z in (119, 150, 180):
        payload = explore_flux_element(z)
        el = payload["element"]
        assert el is not None
        assert el.is_synthetic
        assert len(payload["cloud_fig"].data) >= 3
        assert "(predicted)" in el.electron_config


def test_helium_magic_island():
    payload = explore_flux_element(2)
    assert payload["flywheel"]["stability_score"] == 8.5
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
    assert table[0] == ["Stability score", "8.5"]


def test_flux_metrics_cards_html():
    payload = explore_flux_element(2)
    html = flux_metrics_cards_html(payload["flywheel"])
    assert "kc-metrics-grid" in html


def test_flux_observables_cards_html():
    payload = explore_flux_element_extended(26)
    html = flux_observables_cards_html(payload["flywheel"])
    assert "kc-observables-grid" in html
    assert "7.9" in html
    assert "4" in html
    assert "Alignment" in html
    assert "Δ" in html
    assert "/ 10" in html
    assert "SOC μ" in html or "spin-only" in html.lower()
    assert "μ exp" in html
    assert "Δ SOC vs exp" in html
    assert "kc-obs-val-table" in html
    assert "model-vs-experiment-table" in html
    assert "kc-obs-val-delta-col" in html
    assert "Magnetic Moment" in html
    assert "Direct measurement" in html
    assert "Overall Comparison Fidelity" in html
    assert "Core Model Fidelity" in html
    assert "kc-obs-fidelity-header" in html
    assert "kc-neon-plugin" in html
    assert "Proxy Quality" in html
    assert "Electron Affinity" in html
    assert "Δz" in html or "stab z" in html
    assert "Atomic Radius" in html
    assert "132 pm" in html
    assert "pm" in html  # model radius proxy line


def test_flux_observables_heavy_element_caveat():
    payload = explore_flux_element_extended(86)
    assert payload["flywheel"]["heavy_element_caveat"] is True
    html = flux_observables_cards_html(payload["flywheel"])
    assert "kc-obs-heavy" in html
    assert "Z ≥ 80" in html


def test_compact_element_card_with_art_inset():
    payload = explore_flux_element(2)
    art = element_art_path(2)
    html = element_card_html(payload["element"], payload["flywheel"], art_path=art)
    assert "Helium" in html
    if art:
        assert "kc-card-art" in html


def test_toe_strip_visible():
    payload = explore_flux_element(2)
    html = toe_strip_html(payload["element"], payload["flywheel"])
    assert "Hopf fiber bundle" in html


def test_magic_island_heatmap():
    fig = build_magic_island_heatmap(current_z=2)
    assert len(fig.data) >= 3


def test_all_elements_z_1_to_118_populate():
    for z in range(1, 119):
        payload = explore_flux_element(z)
        el = payload["element"]
        assert el is not None and not el.is_synthetic
        assert el.z == z
        assert len(payload["cloud_fig"].data) >= 3


def test_explorer_z_range():
    assert get_element(0) is None
    assert get_element(EXPLORER_Z_MAX) is not None
    assert get_element(EXPLORER_Z_MAX + 1) is None


def test_element_picker_choices_count():
    choices = element_picker_choices()
    assert len(choices) == EXPLORER_Z_MAX
    assert picker_label_for_z(79).startswith("Z= 79")
    assert "Au" in picker_label_for_z(79)


def test_periodic_table_html_highlights():
    html = known_periodic_table_html(26)
    assert "kc-pt-active" in html
    assert "Fe" in html
    assert 'data-kc-z="26"' in html
    assert "<button" in html
    assert 'data-kc-z="129"' not in html
    html_sh = superheavy_periodic_table_html(129)
    assert "kc-pt-active" in html_sh
    assert 'data-kc-z="129"' in html_sh
    assert 'data-kc-z="180"' in html_sh
    assert known_periodic_table_html(26) + superheavy_periodic_table_html(26) == periodic_table_html(26)


def test_periodic_table_js_wires_pick_event():
    from app.components.periodic_picker import PERIODIC_TABLE_JS

    assert "trigger('pick'" in PERIODIC_TABLE_JS
    assert "data-kc-z" in PERIODIC_TABLE_JS
    assert "watch('value'" in PERIODIC_TABLE_JS


def test_magic_number_toe_narrative():
    el = get_element(28)
    assert el is not None
    assert "magic number" in el.toe_narrative.lower()
    assert "28" in el.toe_narrative


def test_imagine_inbox_complete():
    from pathlib import Path

    manifest = Path(__file__).resolve().parents[1] / "app/assets/elements_imagine/batch_manifest.json"
    if manifest.is_file():
        import json

        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data["inbox_ready"] == data["total"] == EXPLORER_Z_MAX


def test_superheavy_art_paths_exist_after_generation():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    sh = root / "app" / "assets" / "superheavy"
    if sh.is_dir():
        assert any(sh.glob("*.png"))