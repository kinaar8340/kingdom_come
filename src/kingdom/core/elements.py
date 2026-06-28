"""Periodic table element data for Flux Flywheel explorer (Z = 1–180)."""

from __future__ import annotations

from dataclasses import dataclass

from kingdom.core.periodic_meta import period_group_category
from kingdom.core.superheavy import superheavy_period_group, systematic_name_symbol

# Noble gases + nuclear magic numbers (TOE stability anchors)
NOBLE_GAS_Z: frozenset[int] = frozenset({2, 10, 18, 36, 54, 86, 118})
MAGIC_NUMBER_Z: frozenset[int] = frozenset({2, 8, 20, 28, 50, 82})
KNOWN_ELEMENT_MAX = 118
EXPLORER_Z_MAX = 180

_NAMES = (
    "",
    "Hydrogen",
    "Helium",
    "Lithium",
    "Beryllium",
    "Boron",
    "Carbon",
    "Nitrogen",
    "Oxygen",
    "Fluorine",
    "Neon",
    "Sodium",
    "Magnesium",
    "Aluminium",
    "Silicon",
    "Phosphorus",
    "Sulfur",
    "Chlorine",
    "Argon",
    "Potassium",
    "Calcium",
    "Scandium",
    "Titanium",
    "Vanadium",
    "Chromium",
    "Manganese",
    "Iron",
    "Cobalt",
    "Nickel",
    "Copper",
    "Zinc",
    "Gallium",
    "Germanium",
    "Arsenic",
    "Selenium",
    "Bromine",
    "Krypton",
    "Rubidium",
    "Strontium",
    "Yttrium",
    "Zirconium",
    "Niobium",
    "Molybdenum",
    "Technetium",
    "Ruthenium",
    "Rhodium",
    "Palladium",
    "Silver",
    "Cadmium",
    "Indium",
    "Tin",
    "Antimony",
    "Tellurium",
    "Iodine",
    "Xenon",
    "Caesium",
    "Barium",
    "Lanthanum",
    "Cerium",
    "Praseodymium",
    "Neodymium",
    "Promethium",
    "Samarium",
    "Europium",
    "Gadolinium",
    "Terbium",
    "Dysprosium",
    "Holmium",
    "Erbium",
    "Thulium",
    "Ytterbium",
    "Lutetium",
    "Hafnium",
    "Tantalum",
    "Tungsten",
    "Rhenium",
    "Osmium",
    "Iridium",
    "Platinum",
    "Gold",
    "Mercury",
    "Thallium",
    "Lead",
    "Bismuth",
    "Polonium",
    "Astatine",
    "Radon",
    "Francium",
    "Radium",
    "Actinium",
    "Thorium",
    "Protactinium",
    "Uranium",
    "Neptunium",
    "Plutonium",
    "Americium",
    "Curium",
    "Berkelium",
    "Californium",
    "Einsteinium",
    "Fermium",
    "Mendelevium",
    "Nobelium",
    "Lawrencium",
    "Rutherfordium",
    "Dubnium",
    "Seaborgium",
    "Bohrium",
    "Hassium",
    "Meitnerium",
    "Darmstadtium",
    "Roentgenium",
    "Copernicium",
    "Nihonium",
    "Flerovium",
    "Moscovium",
    "Livermorium",
    "Tennessine",
    "Oganesson",
)

_SYMBOLS = (
    "",
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Nh",
    "Fl",
    "Mc",
    "Lv",
    "Ts",
    "Og",
)

_SUBSHELLS: list[tuple[str, int]] = [
    ("1s", 2),
    ("2s", 2),
    ("2p", 6),
    ("3s", 2),
    ("3p", 6),
    ("4s", 2),
    ("3d", 10),
    ("4p", 6),
    ("5s", 2),
    ("4d", 10),
    ("5p", 6),
    ("6s", 2),
    ("4f", 14),
    ("5d", 10),
    ("6p", 6),
    ("7s", 2),
    ("5f", 14),
    ("6d", 10),
    ("7p", 6),
    # Theoretical superheavy extension (Z > 118)
    ("8s", 2),
    ("5g", 18),
    ("6f", 14),
    ("7d", 10),
    ("8p", 6),
    ("9s", 2),
    ("6g", 18),
    ("7f", 14),
    ("8d", 10),
    ("9p", 6),
]

_SHELL_ORDER: list[tuple[int, int]] = [
    (1, 2),
    (2, 8),
    (3, 8),
    (4, 2),
    (3, 10),
    (4, 6),
    (5, 2),
    (4, 10),
    (5, 6),
    (6, 2),
    (4, 14),
    (5, 10),
    (6, 6),
    (7, 2),
    (5, 14),
    (6, 10),
    (7, 6),
    (8, 2),
    (5, 18),
    (6, 14),
    (7, 10),
    (8, 6),
    (9, 2),
    (6, 18),
    (7, 14),
    (8, 10),
    (9, 6),
]


def _aufbau_config(z: int) -> str:
    """Build electron configuration via aufbau filling (extended for superheavy Z)."""
    if z <= 0 or z > EXPLORER_Z_MAX:
        return "—"
    remaining = z
    parts: list[str] = []
    for label, cap in _SUBSHELLS:
        if remaining <= 0:
            break
        fill = min(remaining, cap)
        if fill:
            parts.append(f"{label}{fill if fill < 10 else fill}")
        remaining -= fill
    suffix = " (predicted)" if z > KNOWN_ELEMENT_MAX else ""
    return " ".join(parts) + suffix


def shell_occupancies(z: int) -> list[tuple[int, int]]:
    """Electrons per principal shell n=1,2,3,... for cloud visualization."""
    if z <= 0 or z > EXPLORER_Z_MAX:
        return []
    shells: dict[int, int] = {}
    rem = z
    for shell, cap in _SHELL_ORDER:
        if rem <= 0:
            break
        fill = min(rem, cap)
        shells[shell] = shells.get(shell, 0) + fill
        rem -= fill
    return [(n, shells[n]) for n in sorted(shells) if shells[n] > 0]


@dataclass(frozen=True)
class Element:
    z: int
    name: str
    symbol: str
    period: int
    group: int
    category: str
    electron_config: str
    is_noble_gas: bool
    is_magic_number: bool
    is_known: bool
    is_synthetic: bool

    @property
    def toe_narrative(self) -> str:
        if self.is_synthetic:
            if self.z == 129:
                return (
                    "Magic Island sweep discovery ID (pseudo_Z = 129) — theoretical "
                    "ultra-stable detuning anchor on the Hopf flux lattice."
                )
            return (
                "Superheavy theoretical extension — extrapolated shell structure mapped "
                "onto the flux flywheel stability model beyond the known periodic table."
            )
        if self.is_noble_gas:
            return (
                "This configuration corresponds to a closed Hopf fiber bundle with "
                "maximal topological protection — a flux flywheel ultra-stable lock."
            )
        if self.is_magic_number:
            return (
                "Shell closure aligns with a nuclear magic number — enhanced flux "
                "coherence and identity preservation on the gauged lattice."
            )
        return (
            "Open or partially filled shells map to detuned flux flywheels — "
            "stability varies with distance from the Magic Island anchor."
        )

    @property
    def toe_stability_note(self) -> str:
        if self.is_synthetic:
            return (
                "IUPAC systematic / theoretical nomenclature. Electron configuration and "
                "shell clouds are predicted via extended aufbau — not experimentally confirmed."
            )
        if self.is_noble_gas:
            return (
                "Closed electron shell ↔ topologically protected flux flywheel lock. "
                "In the Hopf lattice, noble gases sit on ultra-stable detuning islands "
                "(Magic Island score ≈ 8.0 at Z = 2 anchor)."
            )
        if self.is_magic_number:
            return (
                "Nuclear magic number — enhanced flux coherence in the gauged lattice "
                "analogy (closed subshell / shell closure)."
            )
        return (
            "Standard flux flywheel detuning applies. Stability follows distance "
            "from the Magic Island anchor (pseudo_Z = 129 calibration)."
        )


def get_element(z: int) -> Element | None:
    """Return element record for Z = 1–180 (known + superheavy theoretical)."""
    if z < 1 or z > EXPLORER_Z_MAX:
        return None

    if z <= KNOWN_ELEMENT_MAX:
        period, group, category = period_group_category(z)
        if z in NOBLE_GAS_Z:
            category = "noble gas"
        name, symbol = _NAMES[z], _SYMBOLS[z]
        is_known = True
        is_synthetic = False
    else:
        period, group, category = superheavy_period_group(z)
        name, symbol = systematic_name_symbol(z)
        is_known = False
        is_synthetic = True

    return Element(
        z=z,
        name=name,
        symbol=symbol,
        period=period,
        group=group,
        category=category,
        electron_config=_aufbau_config(z),
        is_noble_gas=z in NOBLE_GAS_Z,
        is_magic_number=z in MAGIC_NUMBER_Z,
        is_known=is_known,
        is_synthetic=is_synthetic,
    )


def is_real_element(z: int) -> bool:
    return 1 <= z <= KNOWN_ELEMENT_MAX


def is_explorable_element(z: int) -> bool:
    return 1 <= z <= EXPLORER_Z_MAX