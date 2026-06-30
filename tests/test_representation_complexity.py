"""Tests for Monster irrep representation complexity on Flux Flywheel."""

from app.components.neon import (
    element_card_html,
    flux_metrics_cards_html,
    flux_observables_right_html,
    synthetic_z_html,
)
from kingdom.core.flux_explorer import explore_flux_element, explore_flux_element_extended
from kingdom.core.flux_flywheel import map_z_to_flywheel, map_z_to_flywheel_extended
from kingdom.core.representation_complexity import (
    irrep_index_for_z,
    representation_complexity_payload,
)
from kingdom.core.elements import get_element
from kingdom.viz.electron_cloud import (
    build_chemistry_vs_toe_figure,
    build_electron_cloud_figure,
)


def test_irrep_index_linear_for_known_elements():
    assert irrep_index_for_z(1) == (0, False)
    assert irrep_index_for_z(54) == (53, False)
    assert irrep_index_for_z(118) == (117, False)


def test_irrep_index_modular_for_superheavy():
    idx, extrap = irrep_index_for_z(150)
    assert extrap is True
    assert idx == (150 - 1) % 194


def test_xenon_representation_complexity_payload():
    payload = representation_complexity_payload(54, stability_score=8.5)
    assert payload["rep_irrep_index"] == 53
    assert 0 <= payload["rep_complexity_score"] <= 10
    assert payload["rep_exponent_sum"] > 0
    assert "Monster irrep 53" in payload["rep_complexity_tooltip"]
    assert payload["rep_flux_delta"] is not None


def test_base_and_extended_flywheel_include_rep_fields():
    for mapper in (map_z_to_flywheel, map_z_to_flywheel_extended):
        record = mapper(54)
        assert record["rep_irrep_index"] == 53
        assert "rep_complexity_score" in record
        assert "rep_complexity_tooltip" in record


def test_explore_flux_figures_carry_rep_tooltips():
    payload = explore_flux_element_extended(54)
    fly = payload["flywheel"]
    cloud = payload["cloud_fig"]
    compare = payload["compare_fig"]
    ring_trace = next(
        t for t in cloud.data
        if (t.name or "").startswith("Flux flywheel")
    )
    assert "Rep complexity" in ring_trace.hovertemplate
    assert str(fly["rep_complexity_score"]) in ring_trace.hovertemplate
    assert len(compare.data[0].x) == 3
    assert "Monster" in compare.data[0].x[-1]


def test_rep_complexity_in_flux_html_xenon():
    payload = explore_flux_element_extended(54)
    fly = payload["flywheel"]
    el = get_element(54)

    card = element_card_html(el, fly)
    assert "Rep complexity" in card
    assert "irrep 53" in card
    assert fly["rep_complexity_tooltip"][:40] in card

    metrics = flux_metrics_cards_html(fly)
    assert "Rep complexity" in metrics

    right = flux_observables_right_html(fly)
    assert "Rep complexity" in right
    assert "kc-obs-tip" in right
    assert "Δ flux−rep" in right


def test_superheavy_synthetic_card_shows_extrapolated_rep():
    payload = explore_flux_element(150)
    fly = payload["flywheel"]
    html = synthetic_z_html(150, fly)
    assert "Rep complexity" in html
    assert "extrapolated map" in html


def test_flux_metrics_table_includes_rep_rows():
    payload = explore_flux_element(54)
    labels = [row[0] for row in payload["metrics_table"]]
    assert "Rep complexity (/10)" in labels
    assert "Monster irrep index" in labels


def test_electron_cloud_accepts_rep_kwargs():
    el = get_element(54)
    tip = representation_complexity_payload(54, stability_score=8.5)["rep_complexity_tooltip"]
    fig = build_electron_cloud_figure(
        el,
        stability_score=8.5,
        rep_complexity_score=5.0,
        rep_flux_delta=3.5,
        rep_complexity_tooltip=tip,
    )
    ring = next(t for t in fig.data if (t.name or "").startswith("Flux flywheel"))
    assert "Rep complexity" in ring.hovertemplate

    bar_fig = build_chemistry_vs_toe_figure(
        el,
        8.5,
        rep_complexity_score=5.0,
        rep_flux_delta=3.5,
        rep_complexity_tooltip=tip,
    )
    assert len(bar_fig.data[0].x) == 3