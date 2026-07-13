"""Hopf fibration S³ → S²: coordinates, fibers, and linking diagnostics.

Core maps re-export from flux_hopf_lib.hopf; stereographic sampling and
fiber families for the portal visualizer remain local.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from flux_hopf_lib.hopf.fibration import (
    hopf_coordinates,
    hopf_map,
    linking_number_pair,
)


def hopf_map_quaternion(w: float, x: float, y: float, z: float) -> tuple[float, float, float]:
    """Hopf map via unit quaternion (w, x, y, z) ≡ (x₁, x₂, x₃, x₄)."""
    y1, y2, y3 = hopf_map(
        np.array([w]), np.array([x]), np.array([y]), np.array([z])
    )
    return float(y1[0]), float(y2[0]), float(y3[0])


def stereographic_project(
    x1: NDArray[np.floating],
    x2: NDArray[np.floating],
    x3: NDArray[np.floating],
    x4: NDArray[np.floating],
    *,
    scale: float = 2.0,
) -> tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """Stereographic projection S³ → ℝ³ (pole at x₄ = −1, TOE-compatible convention)."""
    denom = 1.0 - x4 + 1e-12
    return scale * x2 / denom, scale * x3 / denom, scale * x1 / denom


def sample_fiber(
    eta: float,
    xi1: float,
    n_points: int = 200,
) -> dict[str, NDArray[np.floating]]:
    """Sample one Hopf fiber: fix base (η, ξ₁), sweep fiber phase ξ₂ ∈ [0, 2π)."""
    xi2 = np.linspace(0.0, 2.0 * np.pi, n_points, endpoint=False)
    x1, x2, x3, x4 = hopf_coordinates(np.full(n_points, eta), np.full(n_points, xi1), xi2)
    y1, y2, y3 = hopf_map(x1, x2, x3, x4)
    px, py, pz = stereographic_project(x1, x2, x3, x4)
    return {
        "xi2": xi2,
        "x1": x1,
        "x2": x2,
        "x3": x3,
        "x4": x4,
        "y1": y1,
        "y2": y2,
        "y3": y3,
        "px": px,
        "py": py,
        "pz": pz,
    }


def sample_fiber_family(
    n_fibers: int = 12,
    n_points: int = 160,
    eta_range: tuple[float, float] = (0.15, 1.35),
) -> list[dict[str, NDArray[np.floating] | float]]:
    """Sample a family of linked Hopf fibers over a spread of base points on S²."""
    eta_vals = np.linspace(eta_range[0], eta_range[1], int(np.sqrt(n_fibers)) + 1)
    xi1_vals = np.linspace(
        0.0, 2.0 * np.pi, int(np.ceil(n_fibers / max(len(eta_vals), 1))), endpoint=False
    )
    fibers: list[dict[str, NDArray[np.floating] | float]] = []
    for eta in eta_vals:
        for xi1 in xi1_vals:
            if len(fibers) >= n_fibers:
                break
            fiber = sample_fiber(float(eta), float(xi1), n_points=n_points)
            y1, y2, y3 = hopf_map(
                np.array([np.mean(fiber["x1"])]),
                np.array([np.mean(fiber["x2"])]),
                np.array([np.mean(fiber["x3"])]),
                np.array([np.mean(fiber["x4"])]),
            )
            fiber["eta"] = float(eta)
            fiber["xi1"] = float(xi1)
            fiber["base_y1"] = float(y1[0])
            fiber["base_y2"] = float(y2[0])
            fiber["base_y3"] = float(y3[0])
            fibers.append(fiber)
    return fibers


def base_sphere_mesh(
    n_theta: int = 24,
    n_phi: int = 48,
) -> tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """Unit S² mesh for the Hopf base space."""
    theta = np.linspace(0.0, np.pi, n_theta)
    phi = np.linspace(0.0, 2.0 * np.pi, n_phi)
    tt, pp = np.meshgrid(theta, phi, indexing="ij")
    return np.sin(tt) * np.cos(pp), np.sin(tt) * np.sin(pp), np.cos(tt)
