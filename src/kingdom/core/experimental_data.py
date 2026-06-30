"""Experimental atomic observables for model validation (hardcoded anchors + fallbacks)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExperimentalObservation:
    """Single experimental observable with optional uncertainty range."""

    value: float
    low: float | None = None
    high: float | None = None
    source: str = "literature"
    notes: str = ""

    @property
    def midpoint(self) -> float:
        if self.low is not None and self.high is not None:
            if self.low <= self.value <= self.high:
                return self.value
            return (self.low + self.high) / 2.0
        return self.value

    @property
    def has_range(self) -> bool:
        return self.low is not None and self.high is not None

    def display_value(self) -> str:
        if self.has_range:
            return f"{self.low:g}–{self.high:g}"
        return f"{self.value:g}"


# Ground-state atomic magnetic moment (Bohr magnetons) — NIST ASD / CRC anchors.
_MAGNETIC_MOMENT_EXP: dict[int, ExperimentalObservation] = {
    1: ExperimentalObservation(1.000, source="NIST ASD", notes="²S₁/₂"),
    2: ExperimentalObservation(0.0, source="NIST ASD", notes="¹S₀"),
    3: ExperimentalObservation(1.60, low=1.5, high=1.7, source="NIST ASD", notes="²S₁/₂"),
    6: ExperimentalObservation(0.0, source="NIST ASD", notes="³P₀ (J=0)"),
    7: ExperimentalObservation(1.41, source="NIST ASD", notes="⁴S₃/₂"),
    8: ExperimentalObservation(2.00, source="NIST ASD", notes="³P₂"),
    9: ExperimentalObservation(1.36, source="NIST ASD", notes="²P₃/₂"),
    10: ExperimentalObservation(0.0, source="NIST ASD", notes="¹S₀"),
    11: ExperimentalObservation(2.22, source="NIST ASD", notes="²S₁/₂"),
    12: ExperimentalObservation(0.0, source="NIST ASD", notes="¹S₀"),
    15: ExperimentalObservation(1.41, source="NIST ASD", notes="⁴S₃/₂"),
    16: ExperimentalObservation(1.02, source="NIST ASD", notes="³P₂"),
    17: ExperimentalObservation(1.14, source="NIST ASD", notes="²P₃/₂"),
    18: ExperimentalObservation(0.0, source="NIST ASD", notes="¹S₀"),
    19: ExperimentalObservation(2.22, source="NIST ASD", notes="²S₁/₂"),
    20: ExperimentalObservation(0.0, source="NIST ASD", notes="¹S₀"),
    22: ExperimentalObservation(2.82, source="NIST ASD", notes="³F₂"),
    23: ExperimentalObservation(4.90, source="NIST ASD", notes="⁴F₃/₂"),
    24: ExperimentalObservation(5.92, low=5.5, high=6.2, source="NIST ASD", notes="⁷S₃ (Cr 3d⁵4s¹)"),
    25: ExperimentalObservation(5.92, source="NIST ASD", notes="⁶S₅/₂"),
    26: ExperimentalObservation(6.71, low=6.0, high=6.8, source="NIST ASD", notes="⁵D₄ atomic beam"),
    27: ExperimentalObservation(5.29, low=4.8, high=5.6, source="NIST ASD", notes="⁴F₉/₂"),
    28: ExperimentalObservation(3.55, low=3.0, high=4.0, source="NIST ASD", notes="³F₄"),
    29: ExperimentalObservation(1.95, source="NIST ASD", notes="²S₁/₂ (4s¹)"),
    30: ExperimentalObservation(0.0, source="NIST ASD", notes="¹S₀"),
    41: ExperimentalObservation(5.29, low=4.5, high=5.8, source="NIST ASD", notes="⁶D₁/₂"),
    42: ExperimentalObservation(5.92, source="NIST ASD", notes="⁷S₃"),
    46: ExperimentalObservation(0.0, source="NIST ASD", notes="¹S₀ (4d¹⁰)"),
    79: ExperimentalObservation(1.95, source="NIST ASD", notes="²S₁/₂ (6s¹)"),
    86: ExperimentalObservation(0.0, source="NIST ASD", notes="¹S₀"),
}


def experimental_magnetic_moment(z: int) -> ExperimentalObservation | None:
    """Experimental ground-state atomic μ (BM), or None if no anchor."""
    return _MAGNETIC_MOMENT_EXP.get(z)


def observable_match_score(
    model: float,
    experimental: ExperimentalObservation,
    *,
    tolerance_bm: float = 1.0,
) -> float:
    """
    0–10 score: 10 when model matches experimental midpoint (or lies in range).

    Uses relative error vs |exp| when nonzero; absolute BM tolerance when exp ≈ 0.
    """
    exp_ref = experimental.midpoint
    if exp_ref == 0.0 and model == 0.0:
        return 10.0
    if exp_ref == 0.0:
        err = abs(model) / tolerance_bm
        return round(max(0.0, 10.0 * (1.0 - err)), 1)

    if experimental.has_range and experimental.low is not None and experimental.high is not None:
        if experimental.low <= model <= experimental.high:
            return 10.0

    rel_err = abs(model - exp_ref) / abs(exp_ref)
    return round(max(0.0, 10.0 * (1.0 - rel_err)), 1)


def magnetic_moment_validation(
    *,
    spin_only_bm: float,
    soc_bm: float,
    z: int,
    soc_preferred: bool = True,
) -> dict[str, Any]:
    """
    Compare model μ (spin-only and SOC) against experimental anchors.

    Returns empty-ish dict when no experimental data exists for Z.
    """
    exp = experimental_magnetic_moment(z)
    if exp is None:
        return {
            "magnetic_moment_exp_available": False,
            "magnetic_moment_exp_BM": None,
            "magnetic_moment_exp_low_BM": None,
            "magnetic_moment_exp_high_BM": None,
            "magnetic_moment_exp_display": None,
            "magnetic_moment_exp_source": None,
            "magnetic_moment_exp_notes": None,
            "mu_delta_spin_vs_exp_BM": None,
            "mu_delta_soc_vs_exp_BM": None,
            "mu_delta_spin_vs_exp_pct": None,
            "mu_delta_soc_vs_exp_pct": None,
            "mu_within_exp_range": None,
            "mu_validation_score": None,
            "mu_validation_model": None,
        }

    ref = exp.midpoint
    delta_spin = round(spin_only_bm - ref, 2)
    delta_soc = round(soc_bm - ref, 2)
    pct_spin = round((delta_spin / ref * 100.0), 1) if ref else None
    pct_soc = round((delta_soc / ref * 100.0), 1) if ref else None

    within = None
    if exp.has_range and exp.low is not None and exp.high is not None:
        model_mu = soc_bm if soc_preferred else spin_only_bm
        within = exp.low <= model_mu <= exp.high

    model_mu = soc_bm if soc_preferred else spin_only_bm
    score = observable_match_score(model_mu, exp)

    return {
        "magnetic_moment_exp_available": True,
        "magnetic_moment_exp_BM": round(exp.value, 2) if not exp.has_range else round(ref, 2),
        "magnetic_moment_exp_low_BM": exp.low,
        "magnetic_moment_exp_high_BM": exp.high,
        "magnetic_moment_exp_display": exp.display_value(),
        "magnetic_moment_exp_source": exp.source,
        "magnetic_moment_exp_notes": exp.notes,
        "mu_delta_spin_vs_exp_BM": delta_spin,
        "mu_delta_soc_vs_exp_BM": delta_soc,
        "mu_delta_spin_vs_exp_pct": pct_spin,
        "mu_delta_soc_vs_exp_pct": pct_soc,
        "mu_within_exp_range": within,
        "mu_validation_score": score,
        "mu_validation_model": "soc" if soc_preferred else "spin-only",
    }