"""Tests for two-gyro lattice simulation."""

from kingdom.simulations.lattice import (
    TwoGyroLattice,
    build_lattice_figure,
    run_lattice_comparison,
)
from kingdom.core.lattice import LatticeConfig


def test_lattice_run_produces_history():
    result = TwoGyroLattice(LatticeConfig(n_sites=24, frames=40), mode="stable").run(40)
    assert len(result.pointer_history) == 40
    assert len(result.mean_twist_history) == 40
    assert len(result.identity_preservation) == 40


def test_lattice_comparison_figure():
    stable, chaotic = run_lattice_comparison(frames=30, n_sites=24)
    fig = build_lattice_figure(stable, chaotic)
    assert len(fig.data) >= 4
    assert stable.total_bursts >= 0
    assert chaotic.total_bursts >= 0