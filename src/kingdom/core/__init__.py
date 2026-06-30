"""Core mathematical and physical models."""

from .experimental_data import (
    allen_electronegativity,
    calculate_comparison_fidelity,
    compare_atomic_radius,
    compare_electronegativity,
    get_proxy_quality_tags,
    compare_ionization_energy_relative,
    compare_to_experiment,
    covalent_radius_pm,
    estimate_model_covalent_radius_pm,
    estimate_model_electronegativity_allen,
)
from .flux_flywheel import (
    effective_magnetic_moment_with_soc,
    lande_g_factor,
    map_z_to_flywheel,
    map_z_to_flywheel_extended,
)
from .hopf import (
    hopf_coordinates,
    hopf_map,
    hopf_map_quaternion,
    linking_number_pair,
    sample_fiber,
    sample_fiber_family,
    stereographic_project,
)
from .quaternion import Quaternion, rodrigues_rotation

__all__ = [
    "Quaternion",
    "hopf_coordinates",
    "hopf_map",
    "hopf_map_quaternion",
    "linking_number_pair",
    "allen_electronegativity",
    "calculate_comparison_fidelity",
    "compare_atomic_radius",
    "compare_electronegativity",
    "get_proxy_quality_tags",
    "compare_ionization_energy_relative",
    "estimate_model_electronegativity_allen",
    "compare_to_experiment",
    "covalent_radius_pm",
    "estimate_model_covalent_radius_pm",
    "effective_magnetic_moment_with_soc",
    "lande_g_factor",
    "map_z_to_flywheel",
    "map_z_to_flywheel_extended",
    "rodrigues_rotation",
    "sample_fiber",
    "sample_fiber_family",
    "stereographic_project",
]