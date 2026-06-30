"""Tests for flux flywheel mapping."""

from kingdom.core.flux_flywheel import (
    base_flywheel_keys,
    lande_g_factor,
    lande_magnetic_moment_bm,
    map_z_to_flywheel,
    map_z_to_flywheel_extended,
    model_reality_alignment,
    spin_only_magnetic_moment_bm,
    unpaired_electrons,
)


def test_magic_island_peak():
    # detuning anchor: delta_omega = 0.0015 when Z = 2
    result = map_z_to_flywheel(2)
    assert result["stability_score"] == 8.0
    assert "magic island" in result["stability_class"].lower()
    assert result["pseudo_Z"] == 129  # sweep discovery ID (separate from input Z)


def test_z_returns_required_keys():
    result = map_z_to_flywheel(6)
    assert result["Z"] == 6
    assert "delta_omega" in result
    assert "gauge_strength" in result


def test_extended_preserves_entire_base_flywheel_output():
    """Extended wrapper must not alter any map_z_to_flywheel() field."""
    keys = base_flywheel_keys()
    for z in (1, 2, 10, 24, 26, 41, 79, 118, 129):
        if z > 180:
            continue
        base = map_z_to_flywheel(z)
        ext = map_z_to_flywheel_extended(z)
        assert keys == base_flywheel_keys()
        for key in keys:
            assert ext[key] == base[key], f"Z={z} key={key}"


def test_extended_helium_observables():
    result = map_z_to_flywheel_extended(2)
    assert result["stability_score"] == 8.0
    assert result["real_ionization_energy_eV"] == 24.59
    assert result["unpaired_electrons"] == 0
    assert result["magnetic_moment_BM"] == 0.0
    assert result["is_diamagnetic"] is True
    assert result["model_vs_reality_alignment"] >= 9.5


def test_extended_iron_magnetism():
    result = map_z_to_flywheel_extended(26)
    assert result["unpaired_electrons"] == 4
    assert result["magnetic_moment_BM"] == round(spin_only_magnetic_moment_bm(4), 2)
    assert result["magnetic_moment_soc_BM"] > result["magnetic_moment_BM"]
    assert result["ground_term_label"] == "5D4"
    assert result["spin_orbit_applied"] is True
    assert result["real_ionization_energy_eV"] == 7.90


def test_lande_g_factor_iron():
    g_j = lande_g_factor(L=2, S=2.0, J=4.0)
    assert abs(g_j - 1.5) < 0.01
    mu = lande_magnetic_moment_bm(2, 2.0, 4.0)
    assert mu > spin_only_magnetic_moment_bm(4)


def test_helium_soc_matches_spin_only():
    result = map_z_to_flywheel_extended(2)
    assert result["magnetic_moment_soc_BM"] == result["magnetic_moment_BM"] == 0.0
    assert result["spin_orbit_applied"] is False


def test_unpaired_from_aufbau_neon():
    assert unpaired_electrons(10) == 0


def test_unpaired_transition_metal_overrides():
    assert unpaired_electrons(24) == 6  # Cr
    assert unpaired_electrons(29) == 1  # Cu
    assert unpaired_electrons(41) == 5  # Nb
    assert unpaired_electrons(42) == 6  # Mo
    assert unpaired_electrons(46) == 0  # Pd


def test_extended_ie_delta_fields():
    result = map_z_to_flywheel_extended(2)
    assert result["ie_model_implied_eV"] == 25.0
    assert result["ie_delta_eV"] == round(24.59 - 25.0, 2)
    assert "alignment_stability_pts" in result
    assert result["heavy_element_caveat"] is False


def test_alignment_weights_are_tunable():
    default = model_reality_alignment(5.5, 7.90)
    ie_heavy = model_reality_alignment(5.5, 7.90, stability_weight=0.2, ie_weight=0.8)
    stab_heavy = model_reality_alignment(5.5, 7.90, stability_weight=0.8, ie_weight=0.2)
    assert ie_heavy < default < stab_heavy