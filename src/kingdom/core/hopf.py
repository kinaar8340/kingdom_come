"""Hopf fibration S³ → S²: coordinates, fibers, and linking diagnostics."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def hopf_coordinates(
    eta: NDArray[np.floating],
    xi1: NDArray[np.floating],
    xi2: NDArray[np.floating],
) -> tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """S³ parametrization (η, ξ₁, ξ₂) → (x₁, x₂, x₃, x₄) with Σ xᵢ² = 1."""
    c1 = np.cos(xi1)
    s1 = np.sin(xi1)
    c2 = np.cos(xi2)
    s2 = np.sin(xi2)
    ce = np.cos(eta)
    se = np.sin(eta)
    x1 = ce * c1
    x2 = ce * s1
    x3 = se * c2
    x4 = se * s2
    return x1, x2, x3, x4


def hopf_map(
    x1: NDArray[np.floating],
    x2: NDArray[np.floating],
    x3: NDArray[np.floating],
    x4: NDArray[np.floating],
) -> tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """Standard Hopf fibration to S²: (x₁² − x₂², 2x₁x₂, 2(x₃x₄ + x₁x₂))."""
    y1 = x1**2 - x2**2
    y2 = 2.0 * x1 * x2
    y3 = 2.0 * (x3 * x4 + x1 * x2)
    norm = np.sqrt(y1**2 + y2**2 + y3**2) + 1e-12
    return y1 / norm, y2 / norm, y3 / norm


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
    xi1_vals = np.linspace(0.0, 2.0 * np.pi, int(np.ceil(n_fibers / max(len(eta_vals), 1))), endpoint=False)
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


def linking_number_pair(
    curve_a: NDArray[np.floating],
    curve_b: NDArray[np.floating],
) -> float:
    """Gauss linking integral for two closed 3D curves (discrete sum)."""
    n_a = curve_a.shape[0]
    n_b = curve_b.shape[0]
    total = 0.0
    for i in range(n_a):
        r1 = curve_a[i]
        r2 = curve_a[(i + 1) % n_a]
        dr1 = r2 - r1
        for j in range(n_b):
            s1 = curve_b[j]
            s2 = curve_b[(j + 1) % n_b]
            dr2 = s2 - s1
            r12 = s1 - r1
            denom = np.linalg.norm(r12) ** 3 + 1e-12
            total += np.dot(r12, np.cross(dr1, dr2)) / denom
    return total / (4.0 * np.pi)