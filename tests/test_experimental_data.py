"""Tests for experimental observable lookups and model validation."""

from kingdom.core.experimental_data import (
    calculate_comparison_fidelity,
    compare_atomic_radius,
    estimate_model_covalent_radius_pm,
    compare_ionization_energy_relative,
    compare_to_experiment,
    covalent_radius_pm,
    experimental_magnetic_moment,
    magnetic_moment_validation,
    observable_match_score,
)
from kingdom.core.flux_explorer import explore_flux_element_extended
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
    assert len(rows) == 4
    mu_row = rows[0]
    assert mu_row["category"] == "Magnetic Moment"
    assert mu_row["model_spin_only"] == "4.90 BM"
    assert "g_J=1.5" in mu_row["model_soc"]
    assert mu_row["delta"] == "+0.00 BM"
    assert rows[2]["category"] == "Electron Affinity"
    assert rows[3]["category"] == "Atomic Radius (Covalent)"
    assert "132 pm" in rows[3]["experimental"]
    assert "pm" in rows[3]["model_spin_only"]
    assert rows[3]["delta"].endswith("pm")
    assert validation["fidelity_score"] is not None
    assert "magnetic_moment" in validation["fidelity_details"]


def test_build_observables_table_backward_compat():
    extended = map_z_to_flywheel_extended(26)
    assert len(build_observables_table(26, extended)) == 4


def test_compare_atomic_radius_iron():
    result = compare_atomic_radius(26, 5.5)
    assert result["available"] is True
    assert result["experimental_value"] == 132
    assert result["model_value"] == estimate_model_covalent_radius_pm(5.5, 26)
    assert result["delta"] == round(result["model_value"] - 132, 1)
    assert "Cordero" in result["source"]


def test_estimate_model_covalent_radius_pm_bounds():
    r = estimate_model_covalent_radius_pm(8.0, 2)
    assert 38 <= r <= 225
    assert estimate_model_covalent_radius_pm(5.0, 29) > 0


def test_covalent_radius_fallback():
    assert covalent_radius_pm(26) == 132.0
    assert covalent_radius_pm(50) > 0


def test_calculate_comparison_fidelity_iron():
    extended = map_z_to_flywheel_extended(26)
    validation = build_observables_validation(26, extended)
    fidelity = calculate_comparison_fidelity(validation["comparisons"])
    assert fidelity["score"] is not None
    assert fidelity["details"]["magnetic_moment"] == 10.0
    assert fidelity["score"] >= 4.0


def test_compare_ionization_energy_relative_iron():
    result = compare_ionization_energy_relative(26, 5.5)
    assert result["available"] is True
    assert result["comparison_mode"] == "period_relative"
    assert result["experimental_value"] == 7.90
    assert result["score"] is not None
    assert result["score"] >= 4.0
    assert abs(result["delta"]) < 2.0


def test_iron_fidelity_improved_with_relative_ie():
    payload = explore_flux_element_extended(26)
    score = payload["flywheel"]["comparison_fidelity_score"]
    ie_detail = payload["flywheel"]["comparison_fidelity_details"]["ionization_energy"]
    assert score is not None
    assert ie_detail >= 4.0
    assert score > 5.0


def test_build_observables_ie_row_uses_period_relative():
    extended = map_z_to_flywheel_extended(26)
    ie_row = build_observables_validation(26, extended)["rows"][1]
    assert ie_row["category"] == "Ionization Energy"
    assert "stab z" in ie_row["model_spin_only"]
    assert "Δz" in ie_row["delta"]
    assert "Period-relative" in ie_row["source"]