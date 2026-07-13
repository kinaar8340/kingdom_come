"""Portal constants re-export from flux_hopf_lib."""

from __future__ import annotations

import math

from kingdom.core.constants import (
    DEFAULT_KAPPA,
    E,
    E_INV2,
    PHI,
    PI,
    R_RESIDUAL,
    WG_FROM_350_OVER_PI,
    W_G_LOCK,
)


def test_phi_matches_closed_form():
    assert abs(PHI - (1.0 + math.sqrt(5.0)) / 2.0) < 1e-15


def test_r_residual_definition():
    assert abs(R_RESIDUAL - (PHI**2 + E**2 - PI**2)) < 1e-15


def test_e_inv2():
    assert abs(E_INV2 - math.exp(-2.0)) < 1e-15


def test_kappa_doc_default():
    assert DEFAULT_KAPPA == 0.85


def test_wg_350_over_pi():
    assert abs(WG_FROM_350_OVER_PI - 350.0 / math.pi) < 1e-12
    assert abs(W_G_LOCK - 111.408) < 1e-3
