"""Hopf fibration S³ → S²: coordinates, fibers, and linking diagnostics.

All geometry re-exports from flux_hopf_lib.hopf (v0.2+ fiber toolkit).
"""

from __future__ import annotations

from flux_hopf_lib.hopf import (
    base_sphere_mesh,
    fiber_linking_number,
    fiber_pair_diagnostics,
    holonomy_phase_proxy,
    hopf_coordinates,
    hopf_map,
    hopf_map_from_angles,
    hopf_map_quaternion,
    linking_number_pair,
    sample_fiber,
    sample_fiber_family,
    stereographic_project,
    wg_from_base,
)

__all__ = [
    "hopf_coordinates",
    "hopf_map",
    "hopf_map_from_angles",
    "hopf_map_quaternion",
    "linking_number_pair",
    "stereographic_project",
    "sample_fiber",
    "sample_fiber_family",
    "base_sphere_mesh",
    "fiber_linking_number",
    "fiber_pair_diagnostics",
    "holonomy_phase_proxy",
    "wg_from_base",
]
