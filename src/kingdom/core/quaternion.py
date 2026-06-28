"""Quaternion algebra and rotation utilities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Quaternion:
    w: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def norm(self) -> float:
        return float(np.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2))

    def normalize(self) -> Quaternion:
        n = self.norm() + 1e-12
        return Quaternion(self.w / n, self.x / n, self.y / n, self.z / n)

    def conjugate(self) -> Quaternion:
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self) -> Quaternion:
        n = self.norm() ** 2
        return Quaternion(self.w / n, -self.x / n, -self.y / n, -self.z / n)

    def multiply(self, other: Quaternion) -> Quaternion:
        return Quaternion(
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def as_array(self) -> np.ndarray:
        return np.array([self.w, self.x, self.y, self.z], dtype=float)

    def hopf_image(self) -> tuple[float, float, float]:
        from .hopf import hopf_map_quaternion

        return hopf_map_quaternion(self.w, self.x, self.y, self.z)

    @classmethod
    def from_axis_angle(cls, axis: np.ndarray, theta: float) -> Quaternion:
        axis = axis / (np.linalg.norm(axis) + 1e-12)
        half = theta / 2.0
        return cls(
            np.cos(half),
            axis[0] * np.sin(half),
            axis[1] * np.sin(half),
            axis[2] * np.sin(half),
        )

    @classmethod
    def from_hopf_coords(cls, eta: float, xi1: float, xi2: float) -> Quaternion:
        from .hopf import hopf_coordinates

        x1, x2, x3, x4 = hopf_coordinates(
            np.array([eta]), np.array([xi1]), np.array([xi2])
        )
        return cls(float(x1[0]), float(x2[0]), float(x3[0]), float(x4[0]))


def rodrigues_rotation(v: np.ndarray, k: np.ndarray, theta: float) -> np.ndarray:
    k = k / (np.linalg.norm(k) + 1e-12)
    return v * np.cos(theta) + np.cross(k, v) * np.sin(theta) + k * np.dot(k, v) * (1 - np.cos(theta))