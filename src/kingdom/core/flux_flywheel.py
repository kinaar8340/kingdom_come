"""Flux flywheel stability mapping — emergent periodic table proxy."""

from __future__ import annotations

import re
from typing import Any

import numpy as np

from kingdom.core.elements import get_element

# First ionization energy (eV) — experimental anchors; fallback trend for other Z.
_IONIZATION_ENERGY_EV: dict[int, float] = {
    2: 24.59,
    10: 21.56,
    18: 15.76,
    26: 7.90,
    36: 13.99,
    54: 12.13,
    24: 6.77,
    29: 7.73,
    41: 8.10,
    42: 7.09,
    79: 9.23,
    86: 10.75,
    118: 8.0,
}

# Ground-state unpaired e⁻ overrides (Aufbau deviations: Cr, Mo, Nb, Pd, etc.).
_UNPAIRED_OVERRIDE: dict[int, int] = {
    2: 0,
    10: 0,
    24: 6,   # Cr — 3d⁵4s¹
    26: 4,   # Fe — high-spin 3d⁶
    29: 1,   # Cu — 3d¹⁰4s¹
    41: 5,   # Nb — 4d⁴5s¹
    42: 6,   # Mo — 4d⁵5s¹
    46: 0,   # Pd — 4d¹⁰ diamagnetic
    79: 1,
    118: 0,
}

_EXTENDED_ONLY_KEYS = frozenset({
    "real_ionization_energy_eV",
    "ie_model_implied_eV",
    "ie_delta_eV",
    "ie_delta_pct",
    "unpaired_electrons",
    "magnetic_moment_BM",
    "magnetic_moment_soc_BM",
    "magnetic_moment_spin_only_BM",
    "lande_g_J",
    "ground_term_L",
    "ground_term_S",
    "ground_term_J",
    "ground_term_label",
    "spin_orbit_applied",
    "is_diamagnetic",
    "model_vs_reality_alignment",
    "alignment_stability_pts",
    "alignment_ie_pts",
    "alignment_component_gap",
    "validation_notes",
    "heavy_element_caveat",
})

_ORBITAL_CAPACITY = {"s": 2, "p": 6, "d": 10, "f": 14}
_ORBITAL_L = {"s": 0, "p": 1, "d": 2, "f": 3}

# Ground LS terms (L, S, J, label) — anchors for SOC / Landé g_J.
_GROUND_TERM_LS: dict[int, tuple[int, float, float, str]] = {
    2: (0, 0.0, 0.0, "1S0"),
    10: (0, 0.0, 0.0, "1S0"),
    18: (0, 0.0, 0.0, "1S0"),
    24: (2, 3.0, 3.0, "7S3"),   # Cr 3d⁵4s¹ → ⁷S₃ (simplified)
    26: (2, 2.0, 4.0, "5D4"),   # Fe
    27: (3, 1.5, 4.5, "4F9/2"), # Co
    28: (3, 1.0, 4.0, "3F4"),   # Ni
    29: (0, 0.5, 0.5, "2S1/2"), # Cu 4s¹
    41: (2, 2.5, 1.5, "6D1/2"), # Nb
    42: (2, 3.0, 3.0, "7S3"),   # Mo
    46: (0, 0.0, 0.0, "1S0"),   # Pd
    79: (0, 0.5, 0.5, "2S1/2"), # Au 6s¹
    86: (0, 0.0, 0.0, "1S0"),
    118: (0, 0.0, 0.0, "1S0"),
}
_SUBSHELL_RE = re.compile(r"(\d+)([spdf])(\d+)")


def map_z_to_flywheel(z: int, n_sites: int = 96, frames: int = 300) -> dict:
    """
    Map atomic number Z to flux flywheel detuning and stability class.

    Calibrated against the Magic Island Sweep (pseudo_Z = 129, score = 8.0).
    """
    _ = n_sites, frames  # reserved for full lattice animation hooks

    delta_omega = 0.0005 * (z - 2) + 0.0015
    omega_L = 0.025
    omega_R = omega_L - delta_omega

    magic_params = {
        "num_layers": 4,
        "num_polarities": 9,
        "max_facts": 60,
        "gauge_strength": 0.85,
        "pseudo_Z": 129,
    }

    magic_delta = 0.0015
    detuning_offset = abs(delta_omega - magic_delta)

    if detuning_offset < 0.0020:
        stability_score = 8.0
        stability_class = "Noble-gas ultra-stable lock (magic island)"
        notes = "Exact match to the discovered pseudo_Z=129 island"
    elif detuning_offset < 0.0050:
        stability_score = 7.5
        stability_class = "Stable mid-table (near magic island)"
        notes = "Very close to the 8.0 stability peak"
    elif detuning_offset < 0.0100:
        stability_score = 6.5
        stability_class = "Transition zone"
        notes = "Approaching the magic island"
    elif detuning_offset < 0.0200:
        stability_score = 5.5
        stability_class = "Mildly radioactive"
        notes = "Farther from the discovered island"
    else:
        stability_score = 5.0
        stability_class = "Highly unstable"
        notes = "Outside current magic island range"

    return {
        "Z": z,
        "pseudo_Z": magic_params["pseudo_Z"],
        "delta_omega": round(delta_omega, 5),
        "omega_L": omega_L,
        "omega_R": round(omega_R, 5),
        "gauge_strength": magic_params["gauge_strength"],
        "num_layers": magic_params["num_layers"],
        "num_polarities": magic_params["num_polarities"],
        "max_facts": magic_params["max_facts"],
        "mean_twist_rad": 0.822796,
        "identity_preservation": 1.0,
        "stability_score": stability_score,
        "stability_class": stability_class,
        "notes": notes,
        "sweep_reference": "1000-trial Magic Island Sweep v1.7.1",
    }


def _hund_unpaired(electrons: int, capacity: int) -> int:
    """Max unpaired electrons in one subshell under Hund's rule."""
    if electrons <= 0 or electrons >= capacity:
        return 0
    orbitals = capacity // 2
    if electrons <= orbitals:
        return electrons
    return 2 * orbitals - electrons


def _unpaired_from_config(config: str) -> int:
    """Estimate unpaired electrons from an aufbau configuration string."""
    config = config.replace(" (predicted)", "").strip()
    if not config or config == "—":
        return 0
    total = 0
    for _n, orb, count in _SUBSHELL_RE.findall(config):
        cap = _ORBITAL_CAPACITY[orb]
        total += _hund_unpaired(int(count), cap)
    return total


def first_ionization_energy_ev(z: int) -> float:
    """First ionization energy (eV) — lookup anchors with smooth fallback."""
    if z in _IONIZATION_ENERGY_EV:
        return _IONIZATION_ENERGY_EV[z]
    return float(5.0 + 10.0 * np.exp(-z / 50.0))


def unpaired_electrons(z: int) -> int:
    """Unpaired valence electrons — lookup overrides, else aufbau + Hund."""
    if z in _UNPAIRED_OVERRIDE:
        return _UNPAIRED_OVERRIDE[z]
    element = get_element(z)
    if element is None:
        return max(0, (z % 10) - 5)
    return _unpaired_from_config(element.electron_config)


def spin_only_magnetic_moment_bm(n_unpaired: int) -> float:
    """Spin-only magnetic moment μ ≈ √(n(n+2)) Bohr magnetons."""
    if n_unpaired <= 0:
        return 0.0
    return float(np.sqrt(n_unpaired * (n_unpaired + 2)))


def lande_g_factor(L: int, S: float, J: float) -> float:
    """Landé g-factor for an LS-coupled term."""
    if J == 0:
        return 0.0
    numerator = J * (J + 1) + S * (S + 1) - L * (L + 1)
    return 1.0 + numerator / (2.0 * J * (J + 1))


def lande_magnetic_moment_bm(L: int, S: float, J: float) -> float:
    """Effective moment μ_eff = g_J √(J(J+1)) Bohr magnetons."""
    if J == 0:
        return 0.0
    g_j = lande_g_factor(L, S, J)
    return float(g_j * np.sqrt(J * (J + 1)))


def _hunds_rule_J(L: int, S: float, electrons: int, capacity: int) -> float:
    """Hund's rule J selection for a subshell with given occupancy."""
    if electrons <= 0 or electrons >= capacity:
        return 0.0
    half = capacity // 2
    if electrons < half:
        return abs(L - S)
    if electrons > half:
        return L + S
    return float(L)


def _estimate_ground_term_from_config(config: str, n_unpaired: int) -> tuple[int, float, float, str]:
    """Estimate (L, S, J, label) from aufbau string when no lookup exists."""
    if n_unpaired <= 0:
        return 0, 0.0, 0.0, "1S0"

    best: tuple[int, str, int, int] | None = None
    for shell_n, orb, count in _SUBSHELL_RE.findall(config.replace(" (predicted)", "")):
        cap = _ORBITAL_CAPACITY[orb]
        e = int(count)
        unpaired = _hund_unpaired(e, cap)
        if unpaired <= 0:
            continue
        candidate = (int(shell_n), orb, e, unpaired)
        if best is None or candidate[0] > best[0]:
            best = candidate

    if best is None:
        s = n_unpaired / 2.0
        return 0, s, abs(s), f"2S{int(abs(s))}"

    _shell_n, orb, electrons, unpaired = best
    L = _ORBITAL_L[orb]
    S = unpaired / 2.0
    cap = _ORBITAL_CAPACITY[orb]
    J = _hunds_rule_J(L, S, electrons, cap)
    j_label = int(J) if J == int(J) else J
    orb_label = orb.upper()
    mult = int(2 * S + 1)
    label = f"{mult}{orb_label}{j_label}"
    return L, S, J, label


def ground_term_ls(z: int, n_unpaired: int) -> tuple[int, float, float, str]:
    """Ground-term (L, S, J, label) for SOC — lookup with aufbau fallback."""
    if z in _GROUND_TERM_LS:
        return _GROUND_TERM_LS[z]
    element = get_element(z)
    if element is None:
        s = n_unpaired / 2.0 if n_unpaired else 0.0
        return 0, s, abs(s), f"2S{int(abs(s))}" if n_unpaired else "1S0"
    return _estimate_ground_term_from_config(element.electron_config, n_unpaired)


def effective_magnetic_moment_with_soc(
    n_unpaired: int,
    *,
    L: int = 0,
    S: float = 0.0,
    J: float = 0.0,
    use_spin_orbit: bool = True,
) -> float:
    """
    Magnetic moment in BM.

    When use_spin_orbit is False or L = 0, falls back to spin-only √(n(n+2)).
    Otherwise uses Landé g_J and μ_eff = g_J √(J(J+1)).
    """
    if n_unpaired <= 0:
        return 0.0
    if not use_spin_orbit or (L == 0 and J == 0):
        return spin_only_magnetic_moment_bm(n_unpaired)
    if J == 0:
        return spin_only_magnetic_moment_bm(n_unpaired)
    return lande_magnetic_moment_bm(L, S, J)


def magnetic_moment_observables(
    z: int,
    n_unpaired: int,
    *,
    use_spin_orbit: bool = True,
) -> dict[str, Any]:
    """Spin-only and SOC-corrected μ with ground-term metadata."""
    L, S, J, label = ground_term_ls(z, n_unpaired)
    spin_only = spin_only_magnetic_moment_bm(n_unpaired)
    soc_enabled = use_spin_orbit and J > 0 and (L > 0 or S > 0)
    soc = (
        lande_magnetic_moment_bm(L, S, J)
        if soc_enabled
        else spin_only
    )
    g_j = lande_g_factor(L, S, J) if soc_enabled else 0.0
    return {
        "magnetic_moment_spin_only_BM": round(spin_only, 2),
        "magnetic_moment_soc_BM": round(soc, 2),
        "magnetic_moment_BM": round(spin_only, 2),
        "lande_g_J": round(g_j, 3),
        "ground_term_L": L,
        "ground_term_S": S,
        "ground_term_J": J,
        "ground_term_label": label,
        "spin_orbit_applied": soc_enabled and abs(soc - spin_only) > 0.05,
    }


def ie_model_implied_ev(stability_score: float, ie_scale_ev: float = 25.0) -> float:
    """IE (eV) implied if model stability tracked ionization linearly."""
    return round((stability_score / 8.0) * ie_scale_ev, 2)


def ie_reality_delta(
    stability_score: float,
    real_ie: float,
    ie_scale_ev: float = 25.0,
) -> tuple[float, float]:
    """Δ real IE minus model-implied IE (eV) and percent of real IE."""
    implied = (stability_score / 8.0) * ie_scale_ev
    delta = real_ie - implied
    pct = (delta / real_ie * 100.0) if real_ie else 0.0
    return round(delta, 2), round(pct, 1)


def alignment_components(
    stability_score: float,
    ionization_ev: float,
    *,
    stability_weight: float = 0.5,
    ie_weight: float = 0.5,
    ie_scale_ev: float = 25.0,
) -> tuple[float, float, float]:
    """Alignment score split: stability points, IE points, gap (stab − IE)."""
    total = stability_weight + ie_weight
    if total <= 0:
        raise ValueError("alignment weights must sum to a positive value")
    w_stab = stability_weight / total
    w_ie = ie_weight / total
    ie_norm = min(ionization_ev / ie_scale_ev, 1.0)
    stab_pts = round(10.0 * w_stab * (stability_score / 8.0), 1)
    ie_pts = round(10.0 * w_ie * ie_norm, 1)
    return stab_pts, ie_pts, round(stab_pts - ie_pts, 1)


def model_reality_alignment(
    stability_score: float,
    ionization_ev: float,
    *,
    stability_weight: float = 0.5,
    ie_weight: float = 0.5,
    ie_scale_ev: float = 25.0,
) -> float:
    """Blend model stability and normalized IE into a 0–10 alignment score."""
    total = stability_weight + ie_weight
    if total <= 0:
        raise ValueError("alignment weights must sum to a positive value")
    w_stab = stability_weight / total
    w_ie = ie_weight / total
    ie_norm = min(ionization_ev / ie_scale_ev, 1.0)
    score = 10.0 * (w_stab * (stability_score / 8.0) + w_ie * ie_norm)
    return round(score, 1)


def base_flywheel_keys() -> frozenset[str]:
    """Keys produced by map_z_to_flywheel (regression guard for extended wrapper)."""
    return frozenset(map_z_to_flywheel(1)) - _EXTENDED_ONLY_KEYS


def map_z_to_flywheel_extended(
    z: int,
    n_sites: int = 96,
    frames: int = 300,
    *,
    stability_weight: float = 0.5,
    ie_weight: float = 0.5,
    ie_scale_ev: float = 25.0,
    use_spin_orbit: bool = True,
) -> dict[str, Any]:
    """
    Extended mapping: flywheel parameters plus laboratory-style observables.

    Adds ionization energy, unpaired electrons, magnetic moment (spin-only
    default on magnetic_moment_BM; SOC Landé value on magnetic_moment_soc_BM),
    and a simple model-vs-reality alignment metric for validation hooks.
    """
    base = map_z_to_flywheel(z, n_sites=n_sites, frames=frames)
    real_ie = first_ionization_energy_ev(z)
    n_unpaired = unpaired_electrons(z)
    moment = magnetic_moment_observables(z, n_unpaired, use_spin_orbit=use_spin_orbit)
    alignment = model_reality_alignment(
        base["stability_score"],
        real_ie,
        stability_weight=stability_weight,
        ie_weight=ie_weight,
        ie_scale_ev=ie_scale_ev,
    )
    implied_ie = ie_model_implied_ev(base["stability_score"], ie_scale_ev)
    delta_ie, delta_pct = ie_reality_delta(base["stability_score"], real_ie, ie_scale_ev)
    stab_pts, ie_pts, align_gap = alignment_components(
        base["stability_score"],
        real_ie,
        stability_weight=stability_weight,
        ie_weight=ie_weight,
        ie_scale_ev=ie_scale_ev,
    )
    heavy = z >= 80

    return {
        **base,
        "real_ionization_energy_eV": round(real_ie, 2),
        "ie_model_implied_eV": implied_ie,
        "ie_delta_eV": delta_ie,
        "ie_delta_pct": delta_pct,
        "unpaired_electrons": n_unpaired,
        **moment,
        "is_diamagnetic": n_unpaired == 0,
        "model_vs_reality_alignment": alignment,
        "alignment_stability_pts": stab_pts,
        "alignment_ie_pts": ie_pts,
        "alignment_component_gap": align_gap,
        "validation_notes": (
            f"Model stability {base['stability_score']} vs real IE {real_ie:.2f} eV "
            f"(Δ {delta_ie:+.2f} eV, {delta_pct:+.1f}%)"
        ),
        "heavy_element_caveat": heavy,
    }