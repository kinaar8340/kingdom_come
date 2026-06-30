"""Tests for experimental observable lookups and model validation."""

from kingdom.core.experimental_data import (
    experimental_magnetic_moment,
    magnetic_moment_validation,
    observable_match_score,
)
from kingdom.core.flux_flywheel import map_z_to_flywheel_extended


def test_experimental_magnetic_moment_iron():
    obs = experimental_magnetic_moment(26)
    assert obs is not None
    assert obs.source == "NIST ASD"
    assert obs.low == 6.0
    assert obs.high == 6.8


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
    result = magnetic_moment_validation(spin_only_bm=2.8, soc_bm=3.0, z=44)
    assert result["magnetic_moment_exp_available"] is False
    assert result["mu_validation_score"] is None


def test_observable_match_score_in_range():
    obs = experimental_magnetic_moment(26)
    assert obs is not None
    assert observable_match_score(6.71, obs) == 10.0