"""Authoritative constants for portal demos (re-exported from flux_hopf_lib).

Prefer this module (or ``flux_hopf_lib`` directly) over hard-coded φ / R / κ
values in UI copy and simulations.
"""

from __future__ import annotations

from flux_hopf_lib.constants import (
    DEFAULT_GAUGE_STRENGTH,
    DEFAULT_KAPPA,
    DEFAULT_LAMBDA_T,
    DEFAULT_MAX_DEPTH,
    DEFAULT_TWIST_RATE,
    E,
    E_INV2,
    GOLDEN_ANGLE_DEG,
    GOLDEN_ANGLE_FRACTION,
    GOLDEN_ANGLE_RAD,
    PHI,
    PHI_INV2,
    PI,
    R_RESIDUAL,
    THETA_CRIT_BASE,
    W_G_LOCK,
    theta_crit,
)

# Common portal aliases
KAPPA_DOC = DEFAULT_KAPPA
WG_FROM_350_OVER_PI = 350.0 / PI  # ≈ 111.408 — topological clock / W_g lock

__all__ = [
    "PHI",
    "E",
    "PI",
    "R_RESIDUAL",
    "E_INV2",
    "GOLDEN_ANGLE_DEG",
    "GOLDEN_ANGLE_RAD",
    "GOLDEN_ANGLE_FRACTION",
    "PHI_INV2",
    "DEFAULT_KAPPA",
    "DEFAULT_GAUGE_STRENGTH",
    "DEFAULT_TWIST_RATE",
    "DEFAULT_MAX_DEPTH",
    "DEFAULT_LAMBDA_T",
    "THETA_CRIT_BASE",
    "W_G_LOCK",
    "KAPPA_DOC",
    "WG_FROM_350_OVER_PI",
    "theta_crit",
]
