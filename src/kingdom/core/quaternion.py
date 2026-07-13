"""Quaternion algebra and rotation utilities.

Base type and Rodrigues helpers re-export from flux_hopf_lib; portal helpers
(``hopf_image``, ``from_hopf_coords``) stay on a thin subclass. Methods that
construct new quaternions return ``type(self)`` so portal methods survive
``normalize()`` / ``multiply()``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from flux_hopf_lib.quaternion.core import Quaternion as _CoreQuaternion
from flux_hopf_lib.quaternion.core import rodrigues_rotation


@dataclass
class Quaternion(_CoreQuaternion):
    """Unit quaternion with Hopf-fibration helpers for the portal demos."""

    def normalize(self) -> Quaternion:
        n = self.norm()
        if n < 1e-12:
            return type(self)(1.0, 0.0, 0.0, 0.0)
        return type(self)(self.w / n, self.x / n, self.y / n, self.z / n)

    def conjugate(self) -> Quaternion:
        return type(self)(self.w, -self.x, -self.y, -self.z)

    def inverse(self) -> Quaternion:
        n2 = self.norm() ** 2
        if n2 < 1e-16:
            raise ZeroDivisionError("cannot invert near-zero quaternion")
        return type(self)(self.w / n2, -self.x / n2, -self.y / n2, -self.z / n2)

    def multiply(self, other: _CoreQuaternion) -> Quaternion:
        return type(self)(
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def hopf_image(self) -> tuple[float, float, float]:
        from .hopf import hopf_map_quaternion

        return hopf_map_quaternion(self.w, self.x, self.y, self.z)

    @classmethod
    def from_axis_angle(cls, axis: np.ndarray, theta: float) -> Quaternion:
        axis = np.asarray(axis, dtype=float)
        n = np.linalg.norm(axis)
        if n < 1e-12:
            return cls(1.0, 0.0, 0.0, 0.0)
        axis = axis / n
        half = theta / 2.0
        s = np.sin(half)
        return cls(
            float(np.cos(half)),
            float(axis[0] * s),
            float(axis[1] * s),
            float(axis[2] * s),
        )

    @classmethod
    def from_hopf_coords(cls, eta: float, xi1: float, xi2: float) -> Quaternion:
        from .hopf import hopf_coordinates

        x1, x2, x3, x4 = hopf_coordinates(
            np.array([eta]), np.array([xi1]), np.array([xi2])
        )
        return cls(float(x1[0]), float(x2[0]), float(x3[0]), float(x4[0]))


__all__ = [
    "Quaternion",
    "rodrigues_rotation",
]
