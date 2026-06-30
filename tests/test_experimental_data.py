"""Tests for experimental observable lookups and model validation."""

from kingdom.core.experimental_data import (
    allen_electronegativity,
    calculate_comparison_fidelity,
    compare_atomic_radius,
    compare_electronegativity,
    estimate_model_covalent_radius_pm,
    estimate_model_electronegativity_allen,
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
    assert len(rows) == 5
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
    assert rows[4]["category"] == "Electronegativity (Allen)"
    assert "Δz" in rows[4]["delta"]
    assert "Period-relative" in rows[4]["source"]
    assert validation["fidelity_score"] is not None
    assert "magnetic_moment" in validation["fidelity_details"]
    assert "electronegativity" in validation["fidelity_details"]


def test_build_observables_table_backward_compat():
    extended = map_z_to_flywheel_extended(26)
    assert len(build_observables_table(26, extended)) == 5


def test_compare_atomic_radius_iron():
    result = compare_atomic_radius(26, 5.5)
    assert result["available"] is True
    assert result["experimental_value"] == 132
    assert result["model_value"] == estimate_model_covalent_radius_pm(5.5, 26)
    assert result["delta"] == round(result["model_value"] - 132, 1)
    assert "Cordero" in result["source"]


def test_estimate_model_covalent_radius_pm_bounds():
    r = estimate_model_covalent_radius_pm(8.0, 2)
    assert 40 <= r <= 220
    assert estimate_model_covalent_radius_pm(5.0, 29) > 0


def test_estimate_model_covalent_radius_pm_iron_closer_to_experiment():
    model = estimate_model_covalent_radius_pm(5.5, 26)
    assert 110 <= model <= 140
    assert abs(model - 132) < 20


def test_covalent_radius_fallback():
    assert covalent_radius_pm(26) == 132.0
    assert covalent_radius_pm(50) > 0


def test_calculate_comparison_fidelity_iron():
    extended = map_z_to_flywheel_extended(26)
    validation = build_observables_validation(26, extended)
    fidelity = calculate_comparison_fidelity(validation["comparisons"], z=26)
    assert fidelity["score"] is not None
    assert fidelity["overall_fidelity"] == fidelity["score"]
    assert fidelity["details"]["magnetic_moment"] == 10.0
    assert fidelity["core_model_fidelity"] is not None
    assert "Electronic" in fidelity["category_scores"]
    assert fidelity["proxy_quality"]["ionization_energy"]["level"] == "high"
    assert fidelity["score"] >= 4.0


def test_layered_fidelity_xenon():
    extended = map_z_to_flywheel_extended(54)
    validation = build_observables_validation(54, extended)
    fidelity = calculate_comparison_fidelity(validation["comparisons"], z=54)
    assert fidelity["score"] is not None
    assert fidelity["score"] >= 7.5
    assert fidelity["core_model_fidelity"] == 8.7
    assert fidelity["category_scores"]["Structural"] == 10.0
    assert fidelity["category_scores"]["Electronic"] >= 7.0
    assert fidelity["category_scores"]["Magnetic"] is None
    en_detail = fidelity["details"]["electronegativity"]
    assert en_detail >= 4.0
    assert "EN" in " ".join(fidelity["category_details"]["Electronic"])
    assert fidelity["proxy_quality"]["electronegativity"]["level"] == "low"
    assert fidelity["proxy_quality"]["magnetic_moment"]["level"] == "none"


def test_build_key_takeaways_xenon():
    from kingdom.core.experimental_data import build_key_takeaways

    extended = map_z_to_flywheel_extended(54)
    validation = build_observables_validation(54, extended)
    takeaways = build_key_takeaways(
        54,
        comparisons=validation["comparisons"],
        fidelity_details=validation["fidelity_details"],
        category_scores=validation.get("fidelity_category_scores"),
        proxy_quality=validation.get("fidelity_proxy_quality"),
        core_model_fidelity=validation.get("fidelity_core_score"),
        overall_fidelity=validation.get("fidelity_score"),
        is_noble_gas=True,
        noble_gas_stability_bonus=float(extended.get("noble_gas_stability_bonus") or 0),
    )
    assert len(takeaways) >= 3
    texts = " ".join(t["text"] for t in takeaways).lower()
    assert any(t["kind"] == "positive" for t in takeaways)
    assert any(t["kind"] == "caveat" for t in takeaways)
    assert "structural" in texts or "electronic" in texts
    assert "electronegativity" in texts or "magnetic" in texts


def test_build_model_insights_xenon():
    from kingdom.core.experimental_data import build_model_insights

    extended = map_z_to_flywheel_extended(54)
    validation = build_observables_validation(54, extended)
    insights = build_model_insights(
        54,
        comparisons=validation["comparisons"],
        fidelity_details=validation["fidelity_details"],
        category_scores=validation.get("fidelity_category_scores"),
        proxy_quality=validation.get("fidelity_proxy_quality"),
        core_model_fidelity=validation.get("fidelity_core_score"),
        overall_fidelity=validation.get("fidelity_score"),
        is_noble_gas=True,
        noble_gas_stability_bonus=float(extended.get("noble_gas_stability_bonus") or 0),
    )
    assert len(insights["strengths"]) >= 2
    assert len(insights["limitations"]) >= 1
    assert any("structural" in s.lower() or "radius" in s.lower() for s in insights["strengths"])
    assert any("electronegativity" in lim.lower() for lim in insights["limitations"])


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


def test_allen_electronegativity_noble_gas_neon():
    assert allen_electronegativity(10) == 4.787
    assert allen_electronegativity(2) == 4.16


def test_estimate_model_electronegativity_allen_bounds():
    en = estimate_model_electronegativity_allen(5.5, 26)
    assert 0.8 <= en <= 4.8
    xe_en = estimate_model_electronegativity_allen(6.0, 54)
    assert 2.4 <= xe_en <= 2.6


def test_compare_electronegativity_iron():
    result = compare_electronegativity(26, 5.5)
    assert result["available"] is True
    assert result["comparison_mode"] == "period_relative"
    assert result["experimental_value"] == 1.628
    assert result["model_value"] is not None
    assert result["score"] is not None
    assert result["delta"] is not None


def test_fidelity_data_coverage():
    from kingdom.core.experimental_data import fidelity_data_coverage

    extended = map_z_to_flywheel_extended(54)
    validation = build_observables_validation(54, extended)
    cov = fidelity_data_coverage(validation["comparisons"])
    assert cov["total"] == 5
    assert cov["available"] >= 3
    assert "Magnetic Moment" in cov["missing"]


def test_interpret_comparison_fidelity_xenon():
    from kingdom.core.experimental_data import interpret_comparison_fidelity

    extended = map_z_to_flywheel_extended(54)
    validation = build_observables_validation(54, extended)
    interp = interpret_comparison_fidelity(
        54,
        fidelity_score=validation["fidelity_score"],
        fidelity_details=validation["fidelity_details"],
        comparisons=validation["comparisons"],
        stability_score=extended["stability_score"],
        is_noble_gas=True,
        core_model_fidelity=validation.get("fidelity_core_score"),
        category_scores=validation.get("fidelity_category_scores"),
    )
    assert interp["coverage"]["label"].startswith("3/")
    assert interp["model_limitation"] == "noble_gas"
    assert interp["fidelity_tier"] in ("solid", "excellent")
    assert "agreement" in interp["summary"].lower()
    assert any("Electronegativity" in n for n in interp.get("notes", []))
    assert validation.get("fidelity_core_score") == 8.7
    assert validation["fidelity_category_scores"]["Structural"] == 10.0


def test_compare_electronegativity_neon_high_allen():
    extended = map_z_to_flywheel_extended(10)
    result = compare_electronegativity(10, extended["stability_score"])
    assert result["available"] is True
    assert result["experimental_value"] == 4.787
    assert result["score"] is not None