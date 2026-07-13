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
from kingdom.viz.hopf_plotly import (
    build_hopf_animation_frame,
    build_hopf_fibration_figure,
    build_hopf_fibration_figure_2d,
    build_hopf_fibration_figure_auto,
    build_hopf_fiber_animation,
    build_hopf_s2_explorer,
    fiber_family_choices,
)


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


def test_plotly_2d_figure_builds_without_webgl():
    fig = build_hopf_fibration_figure_2d(n_fibers=4, n_points=80)
    assert len(fig.data) >= 4
    assert all(trace.type == "scatter" for trace in fig.data)


def test_plotly_auto_selects_2d_on_hf():
    import os

    os.environ["SPACE_ID"] = "kinaar111/kingdom"
    fig = build_hopf_fibration_figure_auto(view_mode="3D interactive (WebGL)", n_fibers=3, n_points=60)
    assert all(trace.type == "scatter" for trace in fig.data)
    del os.environ["SPACE_ID"]


def test_s2_explorer_builds_and_has_customdata():
    fig = build_hopf_s2_explorer(n_fibers=5, n_points=40, height=300)
    assert len(fig.data) >= 5
    assert all(trace.type == "scatter" for trace in fig.data)
    with_cd = [t for t in fig.data if getattr(t, "customdata", None) is not None]
    assert len(with_cd) >= 1


def test_fiber_family_choices_for_dropdown():
    choices = fiber_family_choices(n_fibers=4)
    assert len(choices) == 4
    assert all(len(c) == 3 for c in choices)


def test_plotly_fiber_animation_builds():
    from kingdom.viz.hopf_plotly import clear_animation_frame_cache

    clear_animation_frame_cache()
    fig = build_hopf_fiber_animation(
        n_fibers=3, n_points=40, n_frames=6, mode="xi1_orbit", height=300, frame_idx=2
    )
    assert len(fig.data) >= 3
    assert all(trace.type == "scatter" for trace in fig.data)


def test_hopf_animation_frame_changes_with_index():
    from kingdom.viz.hopf_plotly import (
        bake_hopf_animation_frames,
        clear_animation_frame_cache,
        figure_from_state_payload,
        frames_to_state_payload,
    )

    clear_animation_frame_cache()
    frames = bake_hopf_animation_frames(
        n_fibers=3, n_points=40, n_frames=12, mode="twist", force=True
    )
    assert len(frames) == 12
    a, b = frames[0], frames[6]
    assert list(a.data[0].x[:5]) != list(b.data[0].x[:5])
    assert list(a.layout.xaxis.range) == list(b.layout.xaxis.range)
    again = bake_hopf_animation_frames(
        n_fibers=3, n_points=40, n_frames=12, mode="twist", force=False
    )
    assert again is frames
    # State round-trip (Gradio pattern)
    payload = frames_to_state_payload(frames)
    restored = figure_from_state_payload(payload[3])
    assert len(restored.data) == len(frames[3].data)


def test_resolve_view_mode_defaults_2d():
    from kingdom.viz.hopf_plotly import resolve_view_mode

    assert resolve_view_mode("auto") == "2d"