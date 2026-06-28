"""Gauged Hopf lattice model (stub — integrate from toe repo)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LatticeConfig:
    """Parameters for a porous-vacuum gauged lattice simulation."""

    n_sites: int = 96
    num_layers: int = 4
    num_polarities: int = 9
    max_facts: int = 60
    gauge_strength: float = 0.85
    omega_L: float = 0.025
    delta_omega: float = 0.0015
    frames: int = 300
    tags: list[str] = field(default_factory=lambda: ["hopf", "flux-flywheel"])

    def summary(self) -> str:
        return (
            f"Lattice({self.n_sites} sites, L={self.num_layers}, "
            f"pol={self.num_polarities}, gauge={self.gauge_strength:.2f})"
        )