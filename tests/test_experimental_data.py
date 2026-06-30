"""Tests for experimental observable lookups and model validation."""

from kingdom.core.experimental_data import (
    calculate_comparison_fidelity,
    compare_to_experiment,
    experimental_magnetic_moment,
    magnetic_moment_validation,
    observable_match_score,
)
from kingdom.core.flux_explorer import build_observables_table, build_observables_validation
from kingdom.core.flux_flywheel import map_z_to_flywheel_extended


def test_compare_to_experiment_iron_magnetic_moment():
    result = compare_to_experiment(26, 6.71, "magnetic_moment")
    assert result["available"] is True
    assert result["experimental_value"] == 6.71
    assert result["source"] == "NIST ASD / atomic beam"
    assert result["quality"] == "Direct measurement"
    assert result["delta"] == 0.0
    assert result["within_range"] is True


def test_compare_to_experiment_missing_data():
    result = compare_to_experiment(50, 3.0, "magnetic_moment")
    assert result["available"] is False
    assert result["experimental_value"] is None
    assert result["quality"] == "No experimental data"


def test_experimental_magnetic_moment_iron():
    entry = experimental_magnetic_moment(26)
    assert entry is not None
    assert entry["low"] == 6.0
    assert entry["high"] == 6.8


def test_fe_soc_matches_experimental_range():
    result = map_z_to_flywheel_extended(26)
    assert result["magnetic_moment_exp_available"] is True
    assert result["mu_within_exp_range"] is True
    assert result["mu_validation_score"] == 10.0
    assert abs(result["mu_delta_soc_vs_exp_BM"]) < 0.05


def test_fe_soc_closer_to_exp_than_spin_only():
    result = map_z_to_flywheel_extended(26)
    assert abs(result["mu_delta_soc_vs_exp_BM"]) < abs(result["mu_delta_spin_vs_exp_BM"])


def test_helium_experimental_zero():
    result = map_z_to_flywheel_extended(2)
    assert result["magnetic_moment_exp_available"] is True
    assert result["magnetic_moment_exp_BM"] == 0.0
    assert result["mu_validation_score"] == 10.0


def test_unknown_z_no_experimental_mu():
    result = magnetic_moment_validation(spin_only_bm=2.8, soc_bm=3.0, z=50)
    assert result["magnetic_moment_exp_available"] is False
    assert result["mu_validation_score"] is None


def test_observable_match_score_in_range():
    assert observable_match_score(6.71, 26, "magnetic_moment") == 10.0


def test_build_observables_validation_iron():
    extended = map_z_to_flywheel_extended(26)
    validation = build_observables_validation(26, extended)
    rows = validation["rows"]
    assert len(rows) == 3
    mu_row = rows[0]
    assert mu_row["category"] == "Magnetic Moment"
    assert mu_row["model_spin_only"] == "4.90 BM"
    assert "g_J=1.5" in mu_row["model_soc"]
    assert mu_row["delta"] == "+0.00 BM"
    assert rows[2]["category"] == "Electron Affinity"
    assert validation["fidelity_score"] is not None
    assert "magnetic_moment" in validation["fidelity_details"]


def test_build_observables_table_backward_compat():
    extended = map_z_to_flywheel_extended(26)
    assert len(build_observables_table(26, extended)) == 3


def test_calculate_comparison_fidelity_iron():
    extended = map_z_to_flywheel_extended(26)
    validation = build_observables_validation(26, extended)
    fidelity = calculate_comparison_fidelity(validation["comparisons"])
    assert fidelity["score"] is not None
    assert fidelity["details"]["magnetic_moment"] == 10.0
    assert fidelity["score"] >= 4.0