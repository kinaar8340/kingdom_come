"""Experimental atomic observables for model validation (hardcoded anchors + fallbacks)."""

from __future__ import annotations

from typing import Any, Literal

ObservableName = Literal["magnetic_moment", "ionization_energy", "electron_affinity"]

FIDELITY_WEIGHTS: dict[str, float] = {
    "magnetic_moment": 0.50,
    "ionization_energy": 0.30,
    "electron_affinity": 0.20,
}

# z → observable → {value, low?, high?, source, quality, note}
_EXPERIMENTAL_DATA: dict[int, dict[str, dict[str, Any]]] = {
    1: {
        "magnetic_moment": {
            "value": 1.000,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "²S₁/₂",
        },
    },
    2: {
        "magnetic_moment": {
            "value": 0.0,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "¹S₀ closed shell",
        },
        "ionization_energy": {
            "value": 24.59,
            "source": "NIST",
            "quality": "Excellent",
            "note": "First ionization, ground state",
        },
    },
    3: {
        "magnetic_moment": {
            "value": 1.60,
            "low": 1.5,
            "high": 1.7,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "²S₁/₂",
        },
    },
    6: {
        "magnetic_moment": {
            "value": 0.0,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "³P₀ (J=0)",
        },
        "electron_affinity": {
            "value": 1.26,
            "source": "NIST",
            "quality": "Excellent",
            "note": "Ground-state electron affinity",
        },
    },
    7: {
        "magnetic_moment": {
            "value": 1.41,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "⁴S₃/₂",
        },
        "electron_affinity": {
            "value": -0.07,
            "source": "NIST",
            "quality": "Excellent",
            "note": "Slightly negative — rare anion instability",
        },
    },
    8: {
        "magnetic_moment": {
            "value": 2.00,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "³P₂",
        },
        "electron_affinity": {
            "value": 1.46,
            "source": "NIST",
            "quality": "Excellent",
            "note": "Ground-state electron affinity",
        },
    },
    9: {
        "magnetic_moment": {
            "value": 1.36,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "²P₃/₂",
        },
        "electron_affinity": {
            "value": 3.40,
            "source": "NIST",
            "quality": "Excellent",
            "note": "Ground-state electron affinity",
        },
    },
    10: {
        "magnetic_moment": {
            "value": 0.0,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "¹S₀",
        },
        "ionization_energy": {
            "value": 21.56,
            "source": "NIST",
            "quality": "Excellent",
            "note": "First ionization, ground state",
        },
    },
    11: {
        "magnetic_moment": {
            "value": 2.22,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "²S₁/₂",
        },
    },
    12: {
        "magnetic_moment": {
            "value": 0.0,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "¹S₀",
        },
    },
    15: {
        "magnetic_moment": {
            "value": 1.41,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "⁴S₃/₂",
        },
    },
    16: {
        "magnetic_moment": {
            "value": 1.02,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "³P₂",
        },
        "electron_affinity": {
            "value": 2.08,
            "source": "NIST",
            "quality": "Excellent",
            "note": "Ground-state electron affinity",
        },
    },
    17: {
        "magnetic_moment": {
            "value": 1.14,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "²P₃/₂",
        },
        "electron_affinity": {
            "value": 3.61,
            "source": "NIST",
            "quality": "Excellent",
            "note": "Ground-state electron affinity",
        },
    },
    18: {
        "magnetic_moment": {
            "value": 0.0,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "¹S₀",
        },
        "ionization_energy": {
            "value": 15.76,
            "source": "NIST",
            "quality": "Excellent",
            "note": "First ionization, ground state",
        },
    },
    19: {
        "magnetic_moment": {
            "value": 2.22,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "²S₁/₂",
        },
    },
    20: {
        "magnetic_moment": {
            "value": 0.0,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "¹S₀",
        },
    },
    21: {
        "magnetic_moment": {
            "value": 2.82,
            "source": "NIST ASD",
            "quality": "Good",
            "note": "²D₃/₂",
        },
    },
    22: {
        "magnetic_moment": {
            "value": 2.82,
            "source": "NIST ASD",
            "quality": "Good",
            "note": "³F₂",
        },
    },
    23: {
        "magnetic_moment": {
            "value": 4.90,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "⁴F₃/₂",
        },
    },
    24: {
        "magnetic_moment": {
            "value": 5.92,
            "low": 5.5,
            "high": 6.2,
            "source": "NIST ASD / atomic beam",
            "quality": "Direct measurement",
            "note": "⁷S₃ (Cr 3d⁵4s¹)",
        },
        "ionization_energy": {
            "value": 6.77,
            "source": "NIST",
            "quality": "Excellent",
            "note": "First ionization, ground state",
        },
    },
    25: {
        "magnetic_moment": {
            "value": 5.92,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "⁶S₅/₂",
        },
    },
    26: {
        "magnetic_moment": {
            "value": 6.71,
            "low": 6.0,
            "high": 6.8,
            "source": "NIST ASD / atomic beam",
            "quality": "Direct measurement",
            "note": "⁵D₄; compilations sometimes quote 5.1–5.9 BM for alternate contexts",
        },
        "ionization_energy": {
            "value": 7.90,
            "source": "NIST",
            "quality": "Excellent",
            "note": "First ionization, ground state",
        },
        "electron_affinity": {
            "value": 0.16,
            "source": "NIST",
            "quality": "Good",
            "note": "Ground-state electron affinity",
        },
    },
    27: {
        "magnetic_moment": {
            "value": 5.29,
            "low": 4.8,
            "high": 5.6,
            "source": "NIST ASD",
            "quality": "Good",
            "note": "⁴F₉/₂",
        },
    },
    28: {
        "magnetic_moment": {
            "value": 3.55,
            "low": 3.0,
            "high": 4.0,
            "source": "NIST ASD",
            "quality": "Good",
            "note": "³F₄",
        },
    },
    29: {
        "magnetic_moment": {
            "value": 1.95,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "²S₁/₂ (4s¹)",
        },
        "ionization_energy": {
            "value": 7.73,
            "source": "NIST",
            "quality": "Excellent",
            "note": "First ionization, ground state",
        },
        "electron_affinity": {
            "value": 1.24,
            "source": "NIST",
            "quality": "Good",
            "note": "Ground-state electron affinity",
        },
    },
    30: {
        "magnetic_moment": {
            "value": 0.0,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "¹S₀",
        },
        "electron_affinity": {
            "value": -0.58,
            "source": "NIST",
            "quality": "Good",
            "note": "Ground-state electron affinity",
        },
    },
    43: {
        "magnetic_moment": {
            "value": 5.29,
            "low": 4.8,
            "high": 5.8,
            "source": "NIST ASD",
            "quality": "Estimated",
            "note": "⁶D₅/₂ — limited beam data",
        },
    },
    44: {
        "magnetic_moment": {
            "value": 2.82,
            "source": "NIST ASD",
            "quality": "Good",
            "note": "⁵F₅",
        },
    },
    45: {
        "magnetic_moment": {
            "value": 2.82,
            "low": 2.4,
            "high": 3.2,
            "source": "NIST ASD",
            "quality": "Good",
            "note": "⁴F₉/₂",
        },
    },
    47: {
        "magnetic_moment": {
            "value": 1.95,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "²S₁/₂ (5s¹)",
        },
    },
    48: {
        "magnetic_moment": {
            "value": 0.0,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "¹S₀ (4d¹⁰5s²)",
        },
    },
    36: {
        "ionization_energy": {
            "value": 13.99,
            "source": "NIST",
            "quality": "Excellent",
            "note": "First ionization, ground state",
        },
    },
    41: {
        "magnetic_moment": {
            "value": 5.29,
            "low": 4.5,
            "high": 5.8,
            "source": "NIST ASD",
            "quality": "Good",
            "note": "⁶D₁/₂",
        },
        "ionization_energy": {
            "value": 8.10,
            "source": "NIST",
            "quality": "Excellent",
            "note": "First ionization, ground state",
        },
    },
    42: {
        "magnetic_moment": {
            "value": 5.92,
            "source": "NIST ASD",
            "quality": "Good",
            "note": "⁷S₃",
        },
        "ionization_energy": {
            "value": 7.09,
            "source": "NIST",
            "quality": "Excellent",
            "note": "First ionization, ground state",
        },
    },
    46: {
        "magnetic_moment": {
            "value": 0.0,
            "source": "NIST ASD",
            "quality": "Direct measurement",
            "note": "¹S₀ (4d¹⁰)",
        },
    },
    54: {
        "ionization_energy": {
            "value": 12.13,
            "source": "NIST",
            "quality": "Excellent",
            "note": "First ionization, ground state",
        },
    },
    79: {
        "magnetic_moment": {
            "value": 1.95,
            "source": "Literature compilation",
            "quality": "Limited data",
            "note": "²S₁/₂ (6s¹); few direct atomic-beam measurements",
        },
        "ionization_energy": {
            "value": 9.23,
            "source": "NIST",
            "quality": "Excellent",
            "note": "First ionization, ground state",
        },
    },
    86: {
        "magnetic_moment": {
            "value": 0.0,
            "source": "NIST ASD",
            "quality": "Estimated",
            "note": "¹S₀; superheavy region — limited direct data",
        },
        "ionization_energy": {
            "value": 10.75,
            "source": "NIST",
            "quality": "Good",
            "note": "First ionization, ground state",
        },
    },
    118: {
        "ionization_energy": {
            "value": 8.0,
            "source": "Literature estimate",
            "quality": "Limited data",
            "note": "Og — predicted / sparse experimental confirmation",
        },
    },
}


def _reference_value(exp_entry: dict[str, Any]) -> float:
    value = float(exp_entry["value"])
    low = exp_entry.get("low")
    high = exp_entry.get("high")
    if low is not None and high is not None:
        if low <= value <= high:
            return value
        return (float(low) + float(high)) / 2.0
    return value


def _display_value(exp_entry: dict[str, Any]) -> str:
    low = exp_entry.get("low")
    high = exp_entry.get("high")
    if low is not None and high is not None:
        return f"{low:g}–{high:g}"
    return f"{exp_entry['value']:g}"


def compare_to_experiment(
    z: int,
    model_value: float,
    observable: ObservableName,
    experimental_data: dict[int, dict[str, dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """
    Compare a model value against experimental data.

    Returns structured comparison info (delta = model − experimental).
    """
    data = _EXPERIMENTAL_DATA if experimental_data is None else experimental_data
    exp_entry = data.get(z, {}).get(observable)

    if not exp_entry:
        return {
            "available": False,
            "experimental_value": None,
            "experimental_low": None,
            "experimental_high": None,
            "experimental_display": None,
            "delta": None,
            "percent_delta": None,
            "source": None,
            "quality": "No experimental data",
            "note": "Experimental value not available for this element",
            "within_range": None,
        }

    exp_value = float(exp_entry["value"])
    ref = _reference_value(exp_entry)
    delta = model_value - ref
    percent_delta = (delta / ref * 100.0) if ref != 0 else None

    within = None
    low = exp_entry.get("low")
    high = exp_entry.get("high")
    if low is not None and high is not None:
        within = float(low) <= model_value <= float(high)

    return {
        "available": True,
        "experimental_value": round(exp_value, 2),
        "experimental_low": low,
        "experimental_high": high,
        "experimental_display": _display_value(exp_entry),
        "delta": round(delta, 2),
        "percent_delta": round(percent_delta, 1) if percent_delta is not None else None,
        "source": exp_entry.get("source", "Unknown"),
        "quality": exp_entry.get("quality", "Standard"),
        "note": exp_entry.get("note", ""),
        "within_range": within,
    }


def experimental_entry(z: int, observable: ObservableName) -> dict[str, Any] | None:
    """Return raw experimental entry for Z and observable, if present."""
    return _EXPERIMENTAL_DATA.get(z, {}).get(observable)


def experimental_magnetic_moment(z: int) -> dict[str, Any] | None:
    """Experimental ground-state atomic μ entry, or None."""
    return experimental_entry(z, "magnetic_moment")


def first_electron_affinity_ev(z: int) -> float:
    """Electron affinity (eV) — NIST anchors with smooth fallback."""
    entry = experimental_entry(z, "electron_affinity")
    if entry is not None:
        return float(entry["value"])
    # Non-metals tend to bind electrons more strongly than metals.
    if z in {2, 10, 18, 36, 54, 86, 118}:
        return -0.5
    if z >= 17:
        return 2.5
    if z >= 11:
        return 0.8
    return 0.4


def ea_model_implied_ev(stability_score: float, ea_scale_ev: float = 3.5) -> float:
    """EA (eV) implied if less-stable flywheel states accept electrons more readily."""
    return round((8.0 - stability_score) / 8.0 * ea_scale_ev, 2)


def get_period(z: int) -> int:
    """IUPAC period for atomic number Z (1–118+)."""
    if z <= 118:
        from kingdom.core.periodic_meta import period_group_category

        return period_group_category(z)[0]
    from kingdom.core.superheavy import superheavy_period_group

    return superheavy_period_group(z)[0]


def elements_in_period(period: int, *, z_max: int = 118) -> list[int]:
    """Atomic numbers in the given period (default: known table Z ≤ 118)."""
    from kingdom.core.periodic_meta import _build

    meta = _build()
    return sorted(z for z, (p, _g, _c) in meta.items() if p == period and z <= z_max)


def _z_score(value: float, population: list[float]) -> float:
    if len(population) < 2:
        return 0.0
    mean = sum(population) / len(population)
    variance = sum((v - mean) ** 2 for v in population) / len(population)
    std = variance ** 0.5
    if std < 1e-9:
        return 0.0
    return (value - mean) / std


def compare_ionization_energy_relative(z: int, model_stability: float) -> dict[str, Any]:
    """
    Compare flywheel stability to real IE via period-relative z-scores.

    Answers: does this element's model stability rank appropriately vs its real IE
    within the same period? (Not an absolute IE prediction test.)
    """
    period = get_period(z)
    period_z = elements_in_period(period)
    if z not in period_z or len(period_z) < 3:
        return {
            "available": False,
            "experimental_value": None,
            "experimental_display": None,
            "delta": None,
            "percent_delta": None,
            "source": None,
            "quality": "No experimental data",
            "note": f"Insufficient period-{period} coverage for relative IE comparison",
            "within_range": None,
            "score": None,
            "comparison_mode": "period_relative",
        }

    from kingdom.core.flux_flywheel import first_ionization_energy_ev, map_z_to_flywheel

    stabilities = [map_z_to_flywheel(el)["stability_score"] for el in period_z]
    ionization_ev = [first_ionization_energy_ev(el) for el in period_z]
    real_ie = first_ionization_energy_ev(z)

    z_stab = _z_score(model_stability, stabilities)
    z_ie = _z_score(real_ie, ionization_ev)
    delta_z = z_stab - z_ie

    relative_error = min(abs(delta_z) / 2.0, 1.0)
    score = max(0.0, 10.0 * (1.0 - relative_error))
    if (z_stab >= 0) == (z_ie >= 0):
        score = min(10.0, score + 1.0)

    exp_entry = experimental_entry(z, "ionization_energy")
    source = exp_entry.get("source", "NIST / period trend") if exp_entry else "Lookup + period trend"
    quality = "Good" if exp_entry else "Estimated"

    return {
        "available": True,
        "experimental_value": round(real_ie, 2),
        "experimental_low": None,
        "experimental_high": None,
        "experimental_display": f"{real_ie:.2f}",
        "delta": round(delta_z, 3),
        "percent_delta": None,
        "source": source,
        "quality": quality,
        "note": (
            f"Period {period} z-score match: stability {z_stab:+.2f} vs IE {z_ie:+.2f} "
            f"(Δz = {delta_z:+.2f}). Relative ranking — not absolute IE prediction."
        ),
        "within_range": abs(delta_z) <= 0.5,
        "score": round(score, 1),
        "comparison_mode": "period_relative",
        "stability_z_score": round(z_stab, 3),
        "ie_z_score": round(z_ie, 3),
        "period": period,
    }


def calculate_comparison_fidelity(
    comparisons: dict[str, dict[str, Any]],
    *,
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """
    Composite 0–10 fidelity from compare_to_experiment() results.

    Weights default to FIDELITY_WEIGHTS (MM 50%, IE 30%, EA 20%).
    Renormalizes over observables that have experimental anchors.
    """
    w = FIDELITY_WEIGHTS if weights is None else weights
    total_weight = 0.0
    weighted_score = 0.0
    details: dict[str, float] = {}

    for key, comp in comparisons.items():
        if not comp.get("available") or comp.get("experimental_value") is None:
            continue

        weight = w.get(key, 0.0)
        if weight <= 0:
            continue

        if comp.get("score") is not None:
            score = float(comp["score"])
        else:
            delta = abs(comp.get("delta") or 0.0)
            exp_val = float(comp["experimental_value"])
            ref = abs(exp_val) if exp_val != 0 else 1.0

            if exp_val == 0.0:
                score = (
                    10.0
                    if delta < 0.05
                    else max(0.0, 10.0 * (1.0 - min(delta / ref, 1.0)))
                )
            else:
                relative_error = min(delta / ref, 1.0)
                score = max(0.0, 10.0 * (1.0 - relative_error))

            if comp.get("within_range"):
                score = min(10.0, score + 1.5)

        weighted_score += score * weight
        total_weight += weight
        details[key] = round(score, 1)

    if total_weight == 0:
        return {
            "score": None,
            "details": {},
            "note": "Insufficient experimental data",
            "weights_label": "MM 50%, IE 30%, EA 20%",
        }

    active = [k for k in w if k in details]
    parts = []
    labels = {
        "magnetic_moment": "MM",
        "ionization_energy": "IE",
        "electron_affinity": "EA",
    }
    for k in active:
        pct = int(w[k] * 100)
        parts.append(f"{labels.get(k, k)} {pct}%")

    return {
        "score": round(weighted_score / total_weight, 1),
        "details": details,
        "note": f"Weighted: {', '.join(parts)} (renormalized over available data)",
        "weights_label": "MM 50%, IE 30%, EA 20%",
    }


def observable_match_score(
    model: float,
    z: int,
    observable: ObservableName = "magnetic_moment",
    *,
    tolerance_bm: float = 1.0,
) -> float:
    """0–10 score: 10 when model matches experimental reference (or lies in range)."""
    entry = experimental_entry(z, observable)
    if entry is None:
        return 0.0

    ref = _reference_value(entry)
    if ref == 0.0 and model == 0.0:
        return 10.0
    if ref == 0.0:
        err = abs(model) / tolerance_bm
        return round(max(0.0, 10.0 * (1.0 - err)), 1)

    low = entry.get("low")
    high = entry.get("high")
    if low is not None and high is not None and float(low) <= model <= float(high):
        return 10.0

    rel_err = abs(model - ref) / abs(ref)
    return round(max(0.0, 10.0 * (1.0 - rel_err)), 1)


def magnetic_moment_validation(
    *,
    spin_only_bm: float,
    soc_bm: float,
    z: int,
    soc_preferred: bool = True,
) -> dict[str, Any]:
    """Compare spin-only and SOC μ against experimental anchors."""
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
            "magnetic_moment_exp_quality": None,
            "mu_delta_spin_vs_exp_BM": None,
            "mu_delta_soc_vs_exp_BM": None,
            "mu_delta_spin_vs_exp_pct": None,
            "mu_delta_soc_vs_exp_pct": None,
            "mu_within_exp_range": None,
            "mu_validation_score": None,
            "mu_validation_model": None,
        }

    spin_cmp = compare_to_experiment(z, spin_only_bm, "magnetic_moment")
    soc_cmp = compare_to_experiment(z, soc_bm, "magnetic_moment")
    model_mu = soc_bm if soc_preferred else spin_only_bm
    score = observable_match_score(model_mu, z, "magnetic_moment")

    return {
        "magnetic_moment_exp_available": True,
        "magnetic_moment_exp_BM": spin_cmp["experimental_value"],
        "magnetic_moment_exp_low_BM": spin_cmp["experimental_low"],
        "magnetic_moment_exp_high_BM": spin_cmp["experimental_high"],
        "magnetic_moment_exp_display": spin_cmp["experimental_display"],
        "magnetic_moment_exp_source": spin_cmp["source"],
        "magnetic_moment_exp_notes": spin_cmp["note"],
        "magnetic_moment_exp_quality": spin_cmp["quality"],
        "mu_delta_spin_vs_exp_BM": spin_cmp["delta"],
        "mu_delta_soc_vs_exp_BM": soc_cmp["delta"],
        "mu_delta_spin_vs_exp_pct": spin_cmp["percent_delta"],
        "mu_delta_soc_vs_exp_pct": soc_cmp["percent_delta"],
        "mu_within_exp_range": soc_cmp["within_range"] if soc_preferred else spin_cmp["within_range"],
        "mu_validation_score": score,
        "mu_validation_model": "soc" if soc_preferred else "spin-only",
    }