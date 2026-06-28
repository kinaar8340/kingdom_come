"""Two-gyro gauged quaternion lattice — ported from toe/scripts/two_gyro_lattice_demo.py."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from kingdom.core.lattice import LatticeConfig
from kingdom.viz.hopf_plotly import ACCENT_GOLD, BG_DARK, FIBER_COLORS, GRID, kingdom_dark_theme


def _q_mult(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array(
        [
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        ]
    )


def _q_conj(q: np.ndarray) -> np.ndarray:
    return np.array([q[0], -q[1], -q[2], -q[3]])


def _q_normalize(q: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(q)
    return q / n if n > 1e-8 else q


def _small_rotor(theta: float, axis: np.ndarray | None = None) -> np.ndarray:
    axis = np.array([0.0, 0.0, 1.0]) if axis is None else axis
    axis = axis / (np.linalg.norm(axis) + 1e-8)
    half = theta / 2.0
    return np.array([np.cos(half), *(np.sin(half) * axis)])


@dataclass
class LatticeRunResult:
    mode: str
    frames: int
    pointer_history: list[float] = field(default_factory=list)
    mean_twist_history: list[float] = field(default_factory=list)
    identity_preservation: list[float] = field(default_factory=list)
    burst_events: list[tuple[int, int]] = field(default_factory=list)
    total_bursts: int = 0
    config: LatticeConfig | None = None

    @property
    def stability_score(self) -> float:
        if not self.identity_preservation:
            return 0.0
        return float(np.mean(self.identity_preservation[-max(10, len(self.identity_preservation) // 10) :]))


class TwoGyroLattice:
    """Gauged two-gyro quaternion lattice on n sites."""

    def __init__(self, config: LatticeConfig | None = None, mode: str = "stable"):
        self.config = config or LatticeConfig()
        self.mode = mode
        self.n = self.config.n_sites
        self.gauge_strength = self.config.gauge_strength

        rng = np.random.default_rng(42 if mode == "stable" else 7)
        self.q = np.array([_q_normalize(rng.standard_normal(4)) for _ in range(self.n)])
        self.identity = np.array([_q_normalize(rng.standard_normal(4)) for _ in range(self.n)])
        self.initial_identity = self.identity.copy()
        self.twist = np.zeros(self.n)

        self.omega_L = self.config.omega_L
        self.omega_R = self.config.omega_L - self.config.delta_omega
        if mode == "chaotic":
            self.omega_R = 0.018
            self.gauge_strength = 0.08

        self.pointer_history: list[float] = []
        self.mean_twist_history: list[float] = []
        self.identity_preservation: list[float] = []
        self.burst_events: list[tuple[int, int]] = []
        self.total_bursts = 0

    def step_frame(self) -> None:
        delta_L = _small_rotor(self.omega_L)
        delta_R = _small_rotor(self.omega_R)

        for i in range(self.n):
            q_temp = _q_mult(delta_L, self.q[i])
            self.q[i] = _q_normalize(_q_mult(q_temp, _q_conj(delta_R)))
            self.twist[i] = 2.0 * np.arccos(np.clip(self.q[i][0], -1.0, 1.0))

        avg_imbalance = np.mean(self.twist) % (2.0 * np.pi)
        gauge_alpha = -self.gauge_strength * avg_imbalance
        gauge_rot = np.array([np.cos(gauge_alpha), 0.0, 0.0, np.sin(gauge_alpha)])

        for i in range(self.n):
            self.q[i] = _q_normalize(_q_mult(self.q[i], gauge_rot))
            self.identity[i] = _q_normalize(_q_mult(self.identity[i], gauge_rot))

        bursts_this_step = 0
        for i in range(self.n):
            if self.twist[i] > 5.8:
                self.q[i] = _q_normalize(0.3 * np.array([1.0, 0.0, 0.0, 0.0]) + 0.7 * self.q[i])
                self.twist[i] *= 0.15
                bursts_this_step += 1

        if bursts_this_step > 0:
            self.burst_events.append((len(self.pointer_history), bursts_this_step))
            self.total_bursts += bursts_this_step

        pointer = float(np.tanh(gauge_alpha * 6.0))
        self.pointer_history.append(pointer)
        self.mean_twist_history.append(float(np.mean(self.twist)))
        cosines = np.sum(self.identity * self.initial_identity, axis=1)
        self.identity_preservation.append(float(np.mean(cosines)))

    def run(self, frames: int | None = None) -> LatticeRunResult:
        n_frames = frames or self.config.frames
        for _ in range(n_frames):
            self.step_frame()
        return LatticeRunResult(
            mode=self.mode,
            frames=n_frames,
            pointer_history=self.pointer_history.copy(),
            mean_twist_history=self.mean_twist_history.copy(),
            identity_preservation=self.identity_preservation.copy(),
            burst_events=self.burst_events.copy(),
            total_bursts=self.total_bursts,
            config=self.config,
        )


def run_lattice_comparison(
    frames: int = 150,
    n_sites: int = 96,
    gauge_stable: float = 0.85,
) -> tuple[LatticeRunResult, LatticeRunResult]:
    stable_cfg = LatticeConfig(n_sites=n_sites, gauge_strength=gauge_stable, frames=frames)
    chaotic_cfg = LatticeConfig(n_sites=n_sites, gauge_strength=0.08, frames=frames, delta_omega=0.007)
    stable = TwoGyroLattice(config=stable_cfg, mode="stable").run(frames)
    chaotic = TwoGyroLattice(config=chaotic_cfg, mode="chaotic").run(frames)
    return stable, chaotic


def build_lattice_figure(
    stable: LatticeRunResult,
    chaotic: LatticeRunResult,
    height: int = 520,
) -> go.Figure:
    """WebGL-free lattice metrics dashboard (stable vs chaotic)."""
    theme = kingdom_dark_theme()
    t_s = np.arange(len(stable.pointer_history))
    t_c = np.arange(len(chaotic.pointer_history))

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Gauge pointer — stable",
            "Gauge pointer — chaotic",
            "Mean twist & identity — stable",
            "Mean twist & identity — chaotic",
        ),
        vertical_spacing=0.14,
        horizontal_spacing=0.1,
    )

    fig.add_trace(
        go.Scatter(x=t_s, y=stable.pointer_history, mode="lines", name="pointer (stable)",
                   line=dict(color=FIBER_COLORS[1], width=2)),
        row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(x=t_c, y=chaotic.pointer_history, mode="lines", name="pointer (chaotic)",
                   line=dict(color="#ef553b", width=2)),
        row=1, col=2,
    )
    fig.add_trace(
        go.Scatter(x=t_s, y=stable.mean_twist_history, mode="lines", name="mean twist",
                   line=dict(color=FIBER_COLORS[0], width=2)),
        row=2, col=1,
    )
    fig.add_trace(
        go.Scatter(x=t_s, y=stable.identity_preservation, mode="lines", name="identity",
                   line=dict(color=ACCENT_GOLD, width=2)),
        row=2, col=1,
    )
    fig.add_trace(
        go.Scatter(x=t_c, y=chaotic.mean_twist_history, mode="lines", name="mean twist",
                   line=dict(color=FIBER_COLORS[0], width=2), showlegend=False),
        row=2, col=2,
    )
    fig.add_trace(
        go.Scatter(x=t_c, y=chaotic.identity_preservation, mode="lines", name="identity",
                   line=dict(color=ACCENT_GOLD, width=2), showlegend=False),
        row=2, col=2,
    )

    axis = dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color="#8ecae6"))
    fig.update_xaxes(**axis)
    fig.update_yaxes(**axis)

    fig.update_layout(
        **theme,
        height=height,
        title=dict(
            text=(
                f"Two-Gyro Gauged Lattice — stable ({stable.total_bursts} bursts) "
                f"vs chaotic ({chaotic.total_bursts} bursts)"
            ),
            x=0.5,
            font=dict(size=14, color="#e8f4ff"),
        ),
        legend=dict(bgcolor="rgba(10,22,40,0.7)"),
    )
    fig.update_annotations(font=dict(color="#8ecae6", size=10))
    return fig