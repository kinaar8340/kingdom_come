"""Tests for flux flywheel mapping."""

from kingdom.core.flux_flywheel import (
    map_z_to_flywheel,
    map_z_to_flywheel_extended,
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


def test_extended_preserves_base_flywheel_keys():
    base = map_z_to_flywheel(10)
    ext = map_z_to_flywheel_extended(10)
    for key in ("Z", "delta_omega", "stability_score", "stability_class", "pseudo_Z"):
        assert ext[key] == base[key]


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
    assert result["real_ionization_energy_eV"] == 7.90


def test_unpaired_from_aufbau_neon():
    assert unpaired_electrons(10) == 0