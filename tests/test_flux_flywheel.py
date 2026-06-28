"""Tests for flux flywheel mapping."""

from kingdom.core.flux_flywheel import map_z_to_flywheel


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