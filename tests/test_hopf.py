"""Tests for Hopf fibration core."""

from __future__ import annotations

import numpy as np

from kingdom.core.hopf import (
    hopf_coordinates,
    hopf_map,
    linking_number_pair,
    sample_fiber,
    stereographic_project,
)
from kingdom.core.quaternion import Quaternion
from kingdom.viz.hopf_plotly import build_hopf_fibration_figure


def test_hopf_coordinates_on_unit_sphere():
    eta, xi1, xi2 = 0.5, 1.0, 2.0
    x1, x2, x3, x4 = hopf_coordinates(
        np.array([eta]), np.array([xi1]), np.array([xi2])
    )
    norm = np.sqrt(x1**2 + x2**2 + x3**2 + x4**2)[0]
    assert abs(norm - 1.0) < 1e-10


def test_hopf_map_lands_on_sphere():
    fiber = sample_fiber(0.4, 0.8, n_points=50)
    y1, y2, y3 = fiber["y1"], fiber["y2"], fiber["y3"]
    r = np.sqrt(y1**2 + y2**2 + y3**2)
    assert np.allclose(r, 1.0, atol=1e-6)


def test_fiber_is_closed_under_projection():
    fiber = sample_fiber(0.3, 1.5, n_points=200)
    px, py, pz = fiber["px"], fiber["py"], fiber["pz"]
    dist = np.sqrt((px[0] - px[-1]) ** 2 + (py[0] - py[-1]) ** 2 + (pz[0] - pz[-1]) ** 2)
    assert dist < 0.15  # stereographic closure is approximate at finite sampling


def test_quaternion_hopf_consistency():
    q = Quaternion.from_hopf_coords(0.5, 1.0, 2.0).normalize()
    y1, y2, y3 = q.hopf_image()
    y1m, y2m, y3m = hopf_map(*q.as_array())
    assert abs(y1 - y1m) < 1e-10
    assert abs(y2 - y2m) < 1e-10
    assert abs(y3 - y3m) < 1e-10


def test_linking_two_linked_rings():
    t = np.linspace(0, 2 * np.pi, 100, endpoint=False)
    ring_a = np.column_stack([np.cos(t), np.sin(t), np.zeros_like(t)])
    ring_b = np.column_stack([np.cos(t) + 2, np.sin(t), np.zeros_like(t)])
    lk = linking_number_pair(ring_a, ring_b)
    assert abs(lk) < 0.05


def test_plotly_figure_builds():
    fig = build_hopf_fibration_figure(n_fibers=4, n_points=80)
    assert len(fig.data) >= 4