"""Experimental atomic observables for model validation (hardcoded anchors + fallbacks)."""

from __future__ import annotations

from typing import Any, Literal

from kingdom.core.elements import NOBLE_GAS_Z

ObservableName = Literal["magnetic_moment", "ionization_energy", "electron_affinity"]
DataObservable = Literal[
    "magnetic_moment",
    "ionization_energy",
    "electron_affinity",
    "atomic_radius",
    "electronegativity",
]

FIDELITY_WEIGHTS: dict[str, float] = {
    "magnetic_moment": 0.28,
    "ionization_energy": 0.22,
    "atomic_radius": 0.18,
    "electron_affinity": 0.16,
    "electronegativity": 0.16,
}

_FIDELITY_WEIGHTS_LABEL = "MM 28%, IE 22%, radius 18%, EA 16%, EN 16%"

CORE_MODEL_OBSERVABLES: tuple[str, ...] = ("ionization_energy", "electronegativity")
MIN_CORE_OBSERVABLES = 2
LOW_PROXY_CATEGORY_WEIGHT = 0.5

FIDELITY_CATEGORIES: dict[str, tuple[str, ...]] = {
    "Magnetic": ("magnetic_moment",),
    "Electronic": ("ionization_energy", "electronegativity"),
    "Structural": ("atomic_radius",),
    "Chemical": ("electron_affinity",),
}

_CATEGORY_LABELS: dict[str, str] = {
    "Magnetic": "Magnetic Properties",
    "Electronic": "Electronic Properties",
    "Structural": "Structural Properties",
    "Chemical": "Chemical Reactivity",
}

_PROXY_OBSERVABLE_LABELS: dict[str, str] = {
    "magnetic_moment": "Magnetic Moment",
    "ionization_energy": "Ionization Energy",
    "atomic_radius": "Atomic Radius",
    "electron_affinity": "Electron Affinity",
    "electronegativity": "Electronegativity (Allen)",
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

# Covalent radii (pm) — Cordero et al. (2008) / CRC; merged into _EXPERIMENTAL_DATA.
_COVALENT_RADIUS_PM: dict[int, dict[str, Any]] = {
    1: {"value": 31, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    2: {"value": 28, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    3: {"value": 128, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    4: {"value": 96, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    5: {"value": 84, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    6: {"value": 76, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    7: {"value": 71, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    8: {"value": 66, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    9: {"value": 57, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    10: {"value": 58, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    11: {"value": 166, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    12: {"value": 141, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    13: {"value": 121, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    14: {"value": 111, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    15: {"value": 107, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    16: {"value": 105, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    17: {"value": 102, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    18: {"value": 106, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    19: {"value": 203, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    20: {"value": 176, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    21: {"value": 170, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    22: {"value": 160, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    23: {"value": 153, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    24: {"value": 139, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    25: {"value": 139, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    26: {"value": 132, "source": "Cordero et al. (2008) / CRC", "quality": "Good", "note": "Covalent radius"},
    27: {"value": 132, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    28: {"value": 135, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    29: {"value": 138, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    30: {"value": 131, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    31: {"value": 126, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    32: {"value": 122, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    33: {"value": 119, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    34: {"value": 120, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    35: {"value": 120, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    36: {"value": 116, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    37: {"value": 220, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    38: {"value": 195, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    39: {"value": 190, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    40: {"value": 175, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    41: {"value": 164, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    42: {"value": 154, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    43: {"value": 147, "source": "Cordero et al. (2008)", "quality": "Estimated", "note": "Covalent radius"},
    44: {"value": 146, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    45: {"value": 142, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    46: {"value": 139, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    47: {"value": 145, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    48: {"value": 144, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    50: {"value": 139, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    53: {"value": 139, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    54: {"value": 140, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    55: {"value": 244, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    56: {"value": 215, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    72: {"value": 175, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    74: {"value": 162, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    79: {"value": 136, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    80: {"value": 132, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    82: {"value": 146, "source": "Cordero et al. (2008)", "quality": "Good", "note": "Covalent radius"},
    86: {"value": 116, "source": "Cordero et al. (2008)", "quality": "Estimated", "note": "Covalent radius"},
}

for _z_radius, _radius_entry in _COVALENT_RADIUS_PM.items():
    _EXPERIMENTAL_DATA.setdefault(_z_radius, {})["atomic_radius"] = _radius_entry

# Allen electronegativity (dimensionless) — Allen (1989) / L. C. Allen compilation.
# Noble gases included (high Allen EN from average IE).
_ALLEN_ELECTRONEGATIVITY: dict[int, dict[str, Any]] = {
    1: {"value": 2.300, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    2: {"value": 4.160, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    3: {"value": 0.912, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    4: {"value": 1.576, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    5: {"value": 2.051, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    6: {"value": 2.544, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    7: {"value": 2.686, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    8: {"value": 3.610, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    9: {"value": 4.193, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    10: {"value": 4.787, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    11: {"value": 0.869, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    12: {"value": 1.293, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    13: {"value": 1.613, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    14: {"value": 1.916, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    15: {"value": 2.253, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    16: {"value": 2.589, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    17: {"value": 2.869, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    18: {"value": 3.242, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    19: {"value": 0.734, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    20: {"value": 1.034, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    21: {"value": 1.190, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    22: {"value": 1.378, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    23: {"value": 1.468, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    24: {"value": 1.565, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    25: {"value": 1.589, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    26: {"value": 1.628, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    27: {"value": 1.667, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    28: {"value": 1.681, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    29: {"value": 1.675, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    30: {"value": 1.588, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    31: {"value": 1.758, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    32: {"value": 1.824, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    33: {"value": 1.933, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    34: {"value": 2.045, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    35: {"value": 2.263, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    36: {"value": 2.406, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    37: {"value": 0.706, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    38: {"value": 0.963, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    39: {"value": 1.143, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    40: {"value": 1.241, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    41: {"value": 1.339, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    42: {"value": 1.417, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    43: {"value": 1.473, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    44: {"value": 1.567, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    45: {"value": 1.638, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    46: {"value": 1.679, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    47: {"value": 1.560, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    48: {"value": 1.521, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    49: {"value": 1.656, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    50: {"value": 1.707, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    51: {"value": 1.787, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    52: {"value": 1.852, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    53: {"value": 1.958, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    54: {"value": 2.058, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    55: {"value": 0.659, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    56: {"value": 0.881, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    57: {"value": 1.085, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    58: {"value": 1.092, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    59: {"value": 1.108, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    60: {"value": 1.118, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    61: {"value": 1.124, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    62: {"value": 1.134, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    63: {"value": 1.137, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    64: {"value": 1.141, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    65: {"value": 1.148, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    66: {"value": 1.154, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    67: {"value": 1.158, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    68: {"value": 1.166, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    69: {"value": 1.170, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    70: {"value": 1.176, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    71: {"value": 1.181, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    72: {"value": 1.269, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    73: {"value": 1.345, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    74: {"value": 1.418, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    75: {"value": 1.492, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    76: {"value": 1.571, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    77: {"value": 1.637, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    78: {"value": 1.705, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    79: {"value": 1.758, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    80: {"value": 1.770, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    81: {"value": 1.715, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    82: {"value": 1.750, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    83: {"value": 1.797, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    84: {"value": 1.855, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    85: {"value": 1.920, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    86: {"value": 1.985, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    87: {"value": 0.670, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    88: {"value": 0.881, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    89: {"value": 1.085, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    90: {"value": 1.308, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    91: {"value": 1.428, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    92: {"value": 1.447, "source": "Allen (1989)", "quality": "Good", "note": "Allen scale"},
    93: {"value": 1.472, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    94: {"value": 1.488, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    95: {"value": 1.502, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    96: {"value": 1.513, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    97: {"value": 1.525, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    98: {"value": 1.536, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    99: {"value": 1.545, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    100: {"value": 1.553, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    101: {"value": 1.559, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    102: {"value": 1.564, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
    103: {"value": 1.568, "source": "Allen (1989)", "quality": "Estimated", "note": "Allen scale"},
}

for _z_en, _en_entry in _ALLEN_ELECTRONEGATIVITY.items():
    _EXPERIMENTAL_DATA.setdefault(_z_en, {})["electronegativity"] = _en_entry


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


def experimental_entry(z: int, observable: DataObservable) -> dict[str, Any] | None:
    """Return raw experimental entry for Z and observable, if present."""
    return _EXPERIMENTAL_DATA.get(z, {}).get(observable)


_PERIOD_FIRST_Z: dict[int, int] = {
    1: 1,
    2: 3,
    3: 11,
    4: 19,
    5: 37,
    6: 55,
    7: 87,
    8: 119,
}

# Noble-gas covalent radii are larger than stability-shrink proxy predicts (period 3+).
_NOBLE_GAS_RADIUS_OFFSET_PM: dict[int, float] = {
    2: -5.0,
    10: 0.0,
    18: 12.0,
    36: 22.0,
    54: 35.0,
    86: 48.0,
    118: 52.0,
}

_PERIOD_BASE_RADIUS_PM: dict[int, float] = {
    1: 50.0,
    2: 90.0,
    3: 135.0,
    4: 145.0,
    5: 155.0,
    6: 160.0,
    7: 165.0,
    8: 170.0,
}


def estimate_model_covalent_radius_pm(stability_score: float, z: int) -> float:
    """
    Period-aware stability-based covalent radius proxy (pm).

    Higher stability → smaller radius. d-block periods use a softer stability term.
    """
    period = get_period(z)
    period_base = _PERIOD_BASE_RADIUS_PM.get(period, 150.0)
    start_z = _PERIOD_FIRST_Z.get(period, 1)
    position = max(0, z - start_z)
    base = period_base - (position * 2.8)

    stability_multiplier = 3.0 if period in (4, 5) else 3.5
    stability_adjust = (stability_score - 5.0) * stability_multiplier
    radius = base - stability_adjust

    if 57 <= z <= 71 or 89 <= z <= 103:
        radius += 3.0
    if z in NOBLE_GAS_Z:
        radius += _NOBLE_GAS_RADIUS_OFFSET_PM.get(z, 30.0)

    return round(max(40.0, min(radius, 220.0)), 1)


def compare_atomic_radius(
    z: int,
    stability_score: float | None = None,
) -> dict[str, Any]:
    """Experimental covalent radius (pm) with optional stability-based model comparison."""
    entry = experimental_entry(z, "atomic_radius")
    if entry is None:
        return {
            "available": False,
            "experimental_value": None,
            "experimental_display": None,
            "model_value": None,
            "delta": None,
            "percent_delta": None,
            "source": None,
            "quality": "No data",
            "note": "Covalent radius data not available for this element",
            "within_range": None,
        }

    value = int(entry["value"])
    result: dict[str, Any] = {
        "available": True,
        "experimental_value": value,
        "experimental_display": f"{value} pm",
        "model_value": None,
        "delta": None,
        "percent_delta": None,
        "source": entry.get("source", "Unknown"),
        "quality": entry.get("quality", "Good"),
        "note": entry.get("note", "Covalent radius"),
        "within_range": None,
    }

    if stability_score is not None:
        model_radius = estimate_model_covalent_radius_pm(stability_score, z)
        delta = round(model_radius - value, 1)
        result["model_value"] = model_radius
        result["delta"] = delta
        if value != 0:
            result["percent_delta"] = round(delta / value * 100.0, 1)
        result["note"] = (
            f"{entry.get('note', 'Covalent radius')}. "
            f"Model proxy: stability + Z trend (higher stability → smaller radius)."
        )

    return result


def covalent_radius_pm(z: int) -> float:
    """Covalent radius (pm) — Cordero anchors with smooth period trend fallback."""
    entry = experimental_entry(z, "atomic_radius")
    if entry is not None:
        return float(entry["value"])
    period = get_period(z)
    group_offset = (z % 18) or 18
    return float(round(260 - 6.5 * group_offset + 8.0 * (period - 4), 0))


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


_PERIOD_BASE_ALLEN_EN: dict[int, float] = {
    1: 3.0,
    2: 3.3,
    3: 2.7,
    4: 2.4,
    5: 2.3,
    6: 2.2,
    7: 2.1,
    8: 2.1,
}


def allen_electronegativity(z: int) -> float | None:
    """Allen-scale electronegativity for Z, or None if no tabulated value."""
    entry = experimental_entry(z, "electronegativity")
    if entry is None:
        return None
    return float(entry["value"])


def estimate_model_electronegativity_allen(stability_score: float, z: int) -> float:
    """
    Stability-based proxy for Allen electronegativity.

    Higher stability → higher electronegativity (tighter electron holding).
    Period 5+ noble gases get a refined closed-shell correction: modest stability
    credit plus period-scaled dampening so period-relative Allen ranking improves.
    """
    period = get_period(z)
    period_base = _PERIOD_BASE_ALLEN_EN.get(period, 2.1)
    first_z = _PERIOD_FIRST_Z.get(period, 1)
    position = max(0, z - first_z)
    base = period_base + (position * 0.085)
    stability_effect = (stability_score - 5.0) * 0.20

    if z in NOBLE_GAS_Z and period >= 5:
        stability_effect *= 1.35
        en = base + stability_effect
        en -= 1.52 + max(0, period - 5) * 1.10
    elif z in NOBLE_GAS_Z:
        en = base + (stability_score - 5.0) * 0.22
        en -= 0.65 + max(0, period - 3) * 0.30
    else:
        base = period_base + (position * 0.09)
        en = base + (stability_score - 5.0) * 0.22

    return round(max(0.8, min(en, 4.8)), 2)


def compare_electronegativity(z: int, stability_score: float) -> dict[str, Any]:
    """
    Period-relative Allen electronegativity comparison.

    Compares model-implied EN z-score to experimental Allen EN z-score within
    the same period (noble gases included).
    """
    period = get_period(z)
    period_z = elements_in_period(period)
    exp_values: dict[int, float] = {}
    for el in period_z:
        val = allen_electronegativity(el)
        if val is not None:
            exp_values[el] = val

    if z not in exp_values or len(exp_values) < 3:
        return {
            "available": False,
            "experimental_value": None,
            "experimental_display": None,
            "model_value": None,
            "delta": None,
            "percent_delta": None,
            "source": None,
            "quality": "No data",
            "note": f"Insufficient period-{period} Allen EN coverage",
            "within_range": None,
            "score": None,
            "comparison_mode": "period_relative",
        }

    population = list(exp_values.values())
    exp_en = exp_values[z]
    model_en = estimate_model_electronegativity_allen(stability_score, z)
    exp_z = _z_score(exp_en, population)
    model_z = _z_score(model_en, population)
    delta_z = model_z - exp_z

    relative_error = min(abs(delta_z) / 2.0, 1.0)
    score = max(0.0, 10.0 * (1.0 - relative_error))
    if (model_z >= 0) == (exp_z >= 0):
        score = min(10.0, score + 1.0)

    entry = experimental_entry(z, "electronegativity")
    return {
        "available": True,
        "experimental_value": round(exp_en, 3),
        "experimental_low": None,
        "experimental_high": None,
        "experimental_display": f"{exp_en:.3f}",
        "model_value": model_en,
        "delta": round(delta_z, 3),
        "percent_delta": None,
        "source": entry.get("source", "Allen (1989)") if entry else "Allen (1989)",
        "quality": entry.get("quality", "Good") if entry else "Good",
        "note": (
            f"Period {period} Allen z-score match: model {model_z:+.2f} vs exp {exp_z:+.2f} "
            f"(Δz = {delta_z:+.2f}). Relative ranking — not absolute EN prediction."
        ),
        "within_range": abs(delta_z) <= 0.5,
        "score": round(score, 1),
        "comparison_mode": "period_relative",
        "model_z_score": round(model_z, 3),
        "en_z_score": round(exp_z, 3),
        "period": period,
    }


def _fidelity_component_score(comp: dict[str, Any]) -> float | None:
    """Derive a 0–10 component score from a comparison result."""
    if not comp.get("available") or comp.get("experimental_value") is None:
        return None
    if comp.get("score") is not None:
        return float(comp["score"])
    if comp.get("delta") is None:
        return None

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
    return score


def _average_fidelity_scores(scores: list[float | None]) -> float | None:
    valid = [s for s in scores if s is not None]
    if not valid:
        return None
    return round(sum(valid) / len(valid), 1)


def _weighted_average_fidelity(
    scores_weights: list[tuple[float, float]],
) -> float | None:
    if not scores_weights:
        return None
    total_weight = sum(weight for _, weight in scores_weights)
    if total_weight <= 0:
        return None
    weighted_sum = sum(score * weight for score, weight in scores_weights)
    return round(weighted_sum / total_weight, 1)


_FIDELITY_SHORT_LABELS: dict[str, str] = {
    "magnetic_moment": "MM",
    "ionization_energy": "IE",
    "electron_affinity": "EA",
    "atomic_radius": "radius",
    "electronegativity": "EN",
}


def get_proxy_quality_tags(
    z: int,
    comparisons: dict[str, dict[str, Any]],
) -> dict[str, dict[str, str]]:
    """Per-observable proxy trust level (High / Medium / Low / No data)."""
    period = get_period(z)
    tags: dict[str, dict[str, str]] = {}
    for key in _FIDELITY_OBSERVABLE_ORDER:
        comp = comparisons.get(key, {})
        if key == "magnetic_moment":
            if not comp.get("available"):
                tags[key] = {
                    "level": "none",
                    "label": "No data",
                    "note": "No experimental anchor for this element",
                }
            else:
                tags[key] = {
                    "level": "high",
                    "label": "High",
                    "note": "Direct NIST / SOC comparison",
                }
        elif key == "ionization_energy":
            tags[key] = {
                "level": "high",
                "label": "High",
                "note": "Period-relative z-score ranking",
            }
        elif key == "atomic_radius":
            tags[key] = {
                "level": "medium",
                "label": "Medium",
                "note": "Stability-based covalent radius proxy",
            }
        elif key == "electron_affinity":
            tags[key] = {
                "level": "medium",
                "label": "Medium",
                "note": "Stability-implied electron affinity proxy",
            }
        elif key == "electronegativity":
            if z in NOBLE_GAS_Z and period >= 5:
                tags[key] = {
                    "level": "low",
                    "label": "Low",
                    "note": "Allen proxy weaker for period 5+ noble gases",
                }
            else:
                tags[key] = {
                    "level": "medium",
                    "label": "Medium",
                    "note": "Allen period-relative proxy",
                }
        else:
            tags[key] = {"level": "medium", "label": "Medium", "note": ""}
    return tags


def _category_scores(
    comparisons: dict[str, dict[str, Any]],
    details: dict[str, float],
    proxy_quality: dict[str, dict[str, str]],
) -> tuple[dict[str, float | None], dict[str, list[str]]]:
    """Domain-level fidelity averages with low-proxy down-weighting."""
    out: dict[str, float | None] = {}
    breakdown: dict[str, list[str]] = {}
    for cat, keys in FIDELITY_CATEGORIES.items():
        weighted: list[tuple[float, float]] = []
        components: list[str] = []
        for key in keys:
            if key in details:
                score = details[key]
            else:
                score = _fidelity_component_score(comparisons.get(key, {}))
            if score is None:
                continue
            pq = proxy_quality.get(key, {})
            weight = (
                LOW_PROXY_CATEGORY_WEIGHT
                if pq.get("level") == "low"
                else 1.0
            )
            weighted.append((score, weight))
            components.append(
                f"{_FIDELITY_SHORT_LABELS.get(key, key)} {score:.1f}"
            )
        out[cat] = _weighted_average_fidelity(weighted)
        breakdown[cat] = components
    return out, breakdown


def calculate_comparison_fidelity(
    comparisons: dict[str, dict[str, Any]],
    *,
    z: int | None = None,
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """
    Layered fidelity: overall composite, core model, categories, and proxy tags.

    Overall weights default to FIDELITY_WEIGHTS and renormalize over available data.
    Core model fidelity averages IE and EN (period-relative stability proxies),
    excluding Low-proxy tags. Requires at least MIN_CORE_OBSERVABLES scored core
    observables before reporting. Category scores down-weight Low-proxy observables.
    """
    w = FIDELITY_WEIGHTS if weights is None else weights
    details: dict[str, float] = {}
    for key in _FIDELITY_OBSERVABLE_ORDER:
        comp = comparisons.get(key, {})
        score = _fidelity_component_score(comp)
        if score is not None:
            details[key] = round(score, 1)

    proxy_quality = get_proxy_quality_tags(z or 0, comparisons) if z is not None else {}

    total_weight = 0.0
    weighted_score = 0.0
    for key, weight in w.items():
        if key not in details or weight <= 0:
            continue
        pq = proxy_quality.get(key, {})
        effective_weight = (
            weight * LOW_PROXY_CATEGORY_WEIGHT
            if pq.get("level") == "low"
            else weight
        )
        weighted_score += details[key] * effective_weight
        total_weight += effective_weight

    if total_weight == 0:
        return {
            "score": None,
            "overall_fidelity": None,
            "core_model_fidelity": None,
            "category_scores": {},
            "category_details": {},
            "details": {},
            "proxy_quality": proxy_quality,
            "note": "Insufficient experimental data",
            "weights_label": _FIDELITY_WEIGHTS_LABEL,
        }

    overall = round(weighted_score / total_weight, 1)

    core_available = sum(
        1 for key in CORE_MODEL_OBSERVABLES if key in details
    )
    core_scores: list[float] = []
    for key in CORE_MODEL_OBSERVABLES:
        if key not in details:
            continue
        pq = proxy_quality.get(key, {})
        if pq.get("level") == "low":
            continue
        core_scores.append(details[key])
    core_model = (
        _average_fidelity_scores(core_scores)
        if core_available >= MIN_CORE_OBSERVABLES and core_scores
        else None
    )

    category_scores, category_details = _category_scores(
        comparisons, details, proxy_quality
    )

    active = [k for k in w if k in details]
    parts = []
    for k in active:
        pct = int(w[k] * 100)
        parts.append(f"{_FIDELITY_SHORT_LABELS.get(k, k)} {pct}%")

    note = f"Overall weighted: {', '.join(parts)} (renormalized over available data)"
    if core_model is not None:
        note += f" · Core model (IE+EN, high-trust proxies): {core_model}/10"

    return {
        "score": overall,
        "overall_fidelity": overall,
        "core_model_fidelity": core_model,
        "category_scores": category_scores,
        "category_details": category_details,
        "details": details,
        "proxy_quality": proxy_quality,
        "note": note,
        "weights_label": _FIDELITY_WEIGHTS_LABEL,
    }


_FIDELITY_OBSERVABLE_LABELS: dict[str, str] = {
    "magnetic_moment": "Magnetic Moment",
    "ionization_energy": "Ionization Energy",
    "electron_affinity": "Electron Affinity",
    "atomic_radius": "Atomic Radius",
    "electronegativity": "Electronegativity",
}

_FIDELITY_OBSERVABLE_ORDER: tuple[str, ...] = (
    "magnetic_moment",
    "ionization_energy",
    "electron_affinity",
    "atomic_radius",
    "electronegativity",
)


def fidelity_data_coverage(comparisons: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Count observables with experimental anchors used in fidelity scoring."""
    total = len(_FIDELITY_OBSERVABLE_ORDER)
    available = 0
    scored = 0
    missing: list[str] = []
    for key in _FIDELITY_OBSERVABLE_ORDER:
        comp = comparisons.get(key, {})
        if comp.get("available") and comp.get("experimental_value") is not None:
            available += 1
            if comp.get("score") is not None:
                scored += 1
            else:
                missing.append(_FIDELITY_OBSERVABLE_LABELS[key])
        else:
            missing.append(_FIDELITY_OBSERVABLE_LABELS[key])
    return {
        "total": total,
        "available": available,
        "scored": scored,
        "missing": missing,
        "label": f"{available}/{total} observables",
    }


def build_model_insights(
    z: int,
    *,
    comparisons: dict[str, dict[str, Any]],
    fidelity_details: dict[str, float],
    category_scores: dict[str, float | None] | None = None,
    proxy_quality: dict[str, dict[str, str]] | None = None,
    core_model_fidelity: float | None = None,
    overall_fidelity: float | None = None,
    is_noble_gas: bool = False,
    noble_gas_stability_bonus: float = 0.0,
) -> dict[str, list[str]]:
    """Balanced strengths and limitations for the chemistry analysis column."""
    strengths: list[str] = []
    limitations: list[str] = []
    cats = category_scores or {}
    proxies = proxy_quality or {}

    for cat, score in cats.items():
        if score is None:
            continue
        label = _CATEGORY_LABELS.get(cat, cat)
        if score >= 8.5:
            strengths.append(f"Strong alignment on {label.lower()} ({score}/10)")
        elif score < 6.0:
            limitations.append(f"{label} below target ({score}/10)")

    ie_score = fidelity_details.get("ionization_energy")
    if ie_score is not None and ie_score >= 7.0:
        strengths.append(
            f"Period-relative ionization energy ranking is solid (component {ie_score}/10)"
        )
    elif ie_score is not None and ie_score < 6.0:
        limitations.append(
            f"Ionization energy period-relative mismatch (component {ie_score}/10)"
        )

    radius_score = fidelity_details.get("atomic_radius")
    if radius_score is not None and radius_score >= 9.0:
        strengths.append("Structural radius proxy tracks experiment closely")

    if is_noble_gas and noble_gas_stability_bonus > 0:
        strengths.append(
            f"Shell-closure stability bonus applied (+{noble_gas_stability_bonus:.1f})"
        )

    if core_model_fidelity is not None and overall_fidelity is not None:
        if core_model_fidelity - overall_fidelity >= 1.0:
            strengths.append(
                f"Core model fidelity ({core_model_fidelity}/10) exceeds overall — "
                "stability ranking is sound"
            )

    en_pq = proxies.get("electronegativity", {})
    en_score = fidelity_details.get("electronegativity")
    if en_pq.get("level") == "low" or (
        en_score is not None and en_score < 5.0 and is_noble_gas and get_period(z) >= 5
    ):
        limitations.append(
            "Electronegativity (Allen) proxy has limited predictive power for "
            "heavy noble gases"
        )
    elif en_score is not None and en_score < 5.0:
        limitations.append(
            f"Electronegativity alignment is modest (component {en_score}/10)"
        )

    ea_cmp = comparisons.get("electron_affinity", {})
    ea_score = fidelity_details.get("electron_affinity")
    if ea_cmp.get("available") and ea_score is not None and ea_score < 6.0:
        limitations.append(
            "Chemical reactivity metrics (e.g. electron affinity) show larger divergence"
        )
    elif not ea_cmp.get("available"):
        limitations.append(
            "Electron affinity often unavailable — chemical reactivity category incomplete"
        )

    mm_cmp = comparisons.get("magnetic_moment", {})
    if not mm_cmp.get("available") and is_noble_gas:
        limitations.append(
            "Magnetic moment anchors are usually absent for closed-shell noble gases"
        )

    if not strengths:
        strengths.append("Model stability score is within the calibrated flywheel range")
    if not limitations and overall_fidelity is not None and overall_fidelity < 8.5:
        limitations.append(
            "Some proxy translations remain weaker than direct measurements"
        )

    return {"strengths": strengths[:4], "limitations": limitations[:4]}


def build_key_takeaways(
    z: int,
    *,
    comparisons: dict[str, dict[str, Any]],
    fidelity_details: dict[str, float],
    category_scores: dict[str, float | None] | None = None,
    proxy_quality: dict[str, dict[str, str]] | None = None,
    core_model_fidelity: float | None = None,
    overall_fidelity: float | None = None,
    is_noble_gas: bool = False,
    noble_gas_stability_bonus: float = 0.0,
) -> list[dict[str, str]]:
    """Short scannable bullets for the left-column summary card."""
    items: list[dict[str, str]] = []
    cats = category_scores or {}
    proxies = proxy_quality or {}

    structural = cats.get("Structural")
    electronic = cats.get("Electronic")
    ie_score = fidelity_details.get("ionization_energy")
    if (
        (structural is not None and structural >= 8.0)
        and (electronic is not None and electronic >= 7.0 or ie_score is not None and ie_score >= 7.0)
    ):
        items.append({
            "kind": "positive",
            "text": "Strong structural and period-relative electronic alignment",
        })
    elif structural is not None and structural >= 8.0:
        items.append({
            "kind": "positive",
            "text": "Structural properties align well with experiment",
        })
    elif ie_score is not None and ie_score >= 7.0:
        items.append({
            "kind": "positive",
            "text": "Period-relative ionization energy ranking is solid",
        })

    if is_noble_gas and noble_gas_stability_bonus > 0:
        items.append({
            "kind": "positive",
            "text": "Shell-closure bonus improves stability as expected",
        })

    if overall_fidelity is not None and overall_fidelity >= 8.5:
        items.append({
            "kind": "positive",
            "text": f"Overall comparison fidelity is strong ({overall_fidelity}/10)",
        })
    elif core_model_fidelity is not None and overall_fidelity is not None:
        if core_model_fidelity - overall_fidelity >= 1.0:
            items.append({
                "kind": "positive",
                "text": "Core stability ranking outperforms weaker proxy translations",
            })

    en_pq = proxies.get("electronegativity", {})
    en_score = fidelity_details.get("electronegativity")
    if en_pq.get("level") == "low" or (
        is_noble_gas and get_period(z) >= 5 and en_score is not None and en_score < 7.0
    ):
        items.append({
            "kind": "caveat",
            "text": "Electronegativity proxy needs refinement for heavy nobles",
        })
    elif en_score is not None and en_score < 5.0:
        items.append({
            "kind": "caveat",
            "text": "Electronegativity alignment remains modest for this element",
        })

    mm_cmp = comparisons.get("magnetic_moment", {})
    ea_cmp = comparisons.get("electron_affinity", {})
    mm_missing = not mm_cmp.get("available")
    ea_missing = not ea_cmp.get("available")
    if mm_missing and ea_missing:
        items.append({
            "kind": "caveat",
            "text": "Limited data for magnetic and reactivity metrics",
        })
    elif mm_missing:
        items.append({
            "kind": "caveat",
            "text": "Magnetic moment anchors are sparse for this configuration",
        })
    elif ea_missing:
        items.append({
            "kind": "caveat",
            "text": "Electron affinity data limits chemical reactivity scoring",
        })

    chemical = cats.get("Chemical")
    if chemical is not None and chemical < 6.0:
        items.append({
            "kind": "caveat",
            "text": "Chemical reactivity proxies show larger divergence",
        })

    if not items:
        items.append({
            "kind": "positive",
            "text": "Model stability score is within the calibrated flywheel range",
        })

    positives = [i for i in items if i["kind"] == "positive"][:3]
    caveats = [i for i in items if i["kind"] == "caveat"][:2]
    return positives + caveats


def interpret_comparison_fidelity(
    z: int,
    *,
    fidelity_score: float | None,
    fidelity_details: dict[str, float],
    comparisons: dict[str, dict[str, Any]],
    stability_score: float,
    is_noble_gas: bool = False,
    core_model_fidelity: float | None = None,
    category_scores: dict[str, float | None] | None = None,
    category_details: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    """
    Human-readable drivers for composite fidelity (esp. low scores).
    """
    coverage = fidelity_data_coverage(comparisons)
    drivers: list[str] = []
    cats = category_scores or {}
    cat_breakdown = category_details or {}

    if cats:
        for cat, cat_score in sorted(cats.items(), key=lambda kv: kv[1] if kv[1] is not None else 11):
            label = _CATEGORY_LABELS.get(cat, cat)
            parts = cat_breakdown.get(cat, [])
            parts_suffix = f" ({' + '.join(parts)})" if parts else ""
            if cat_score is None:
                drivers.append(f"{label}: N/A (no scored data)")
            elif cat_score < 7.0:
                drivers.append(f"{label}: {cat_score}/10{parts_suffix}")

    if fidelity_score is not None and fidelity_details:
        weakest = sorted(fidelity_details.items(), key=lambda kv: kv[1])
        for key, comp_score in weakest[:2]:
            if comp_score >= 7.0:
                continue
            if any(_FIDELITY_OBSERVABLE_LABELS.get(key, key) in d for d in drivers):
                continue
            label = _FIDELITY_OBSERVABLE_LABELS.get(key, key)
            comp = comparisons.get(key, {})
            if key == "ionization_energy" and comp.get("comparison_mode") == "period_relative":
                drivers.append(
                    f"{label} period-relative mismatch (component {comp_score}/10; "
                    f"Δz {comp.get('delta', '—')})"
                )
            elif comp.get("delta") is not None:
                drivers.append(f"{label} gap (component {comp_score}/10; Δ {comp['delta']})")
            else:
                drivers.append(f"{label} weak match (component {comp_score}/10)")

    notes: list[str] = []
    en_score = fidelity_details.get("electronegativity")
    period = get_period(z)
    if en_score is not None and en_score < 7.0 and (
        (is_noble_gas and period >= 5) or en_score < 5.0
    ):
        notes.append(
            "Electronegativity alignment is modest for heavy noble gases. Stability-based "
            "proxies generally have weaker predictive power for closed-shell configurations "
            "in period 5 and beyond."
            if is_noble_gas and period >= 5
            else "Electronegativity (Allen) is a weaker component here — stability-based "
            "proxies are less predictive for this configuration."
        )

    core_gap_note = ""
    if (
        fidelity_score is not None
        and core_model_fidelity is not None
        and core_model_fidelity - fidelity_score >= 1.5
    ):
        core_gap_note = (
            f" Core model fidelity ({core_model_fidelity}/10) is stronger than the "
            f"overall score — gaps are mainly in weaker proxy translations, not the "
            "underlying stability ranking."
        )

    if is_noble_gas:
        if fidelity_score is not None and fidelity_score >= 7.0:
            summary = (
                f"Solid agreement ({fidelity_score}/10) for this noble gas after "
                "shell-closure bonus. Period-relative rankings drive the score; "
                "μ is usually absent for closed shells."
                + core_gap_note
            )
        else:
            summary = (
                f"Noble gas Z={z}: closed-shell stability bonus applied (+shell closure). "
                "Fidelity uses period-relative rankings; μ is usually absent for closed shells."
            )
            if fidelity_score is not None and fidelity_score < 5.0:
                summary += (
                    " Remaining gaps often reflect heavier noble gases where the detuning map "
                    "still diverges from experimental IE / radius trends."
                )
    elif fidelity_score is not None and fidelity_score < 5.0:
        summary = (
            f"Low fidelity ({fidelity_score}/10) — largest gaps in "
            + (drivers[0].split("(")[0].strip() if drivers else "multiple observables")
            + "."
        )
    elif fidelity_score is not None and fidelity_score < 7.0:
        summary = f"Moderate fidelity ({fidelity_score}/10); see component breakdown."
    elif fidelity_score is not None and fidelity_score < 8.5:
        summary = f"Solid agreement ({fidelity_score}/10) across available observables." + core_gap_note
    else:
        summary = f"Excellent agreement ({fidelity_score}/10) across available observables." + core_gap_note

    limitation = None
    if is_noble_gas:
        limitation = "noble_gas"
    elif z >= 80:
        limitation = "heavy_element"
    elif 21 <= z <= 30 or 39 <= z <= 48:
        limitation = "transition_metal"

    fidelity_tier = None
    if fidelity_score is not None:
        if fidelity_score >= 8.5:
            fidelity_tier = "excellent"
        elif fidelity_score >= 7.0:
            fidelity_tier = "solid"
        elif fidelity_score >= 5.0:
            fidelity_tier = "moderate"
        else:
            fidelity_tier = "low"

    return {
        "summary": summary,
        "drivers": drivers,
        "notes": notes,
        "coverage": coverage,
        "category_scores": cats,
        "core_model_fidelity": core_model_fidelity,
        "model_limitation": limitation,
        "fidelity_tier": fidelity_tier,
        "show_interpretation": fidelity_score is not None and (
            fidelity_score < 7.0
            or is_noble_gas
            or coverage["available"] < coverage["total"]
            or bool(notes)
        ),
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