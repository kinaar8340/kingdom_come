"""Periodic table element data for Flux Flywheel explorer."""

from __future__ import annotations

from dataclasses import dataclass

# Noble gases + nuclear magic numbers (TOE stability anchors)
NOBLE_GAS_Z: frozenset[int] = frozenset({2, 10, 18, 36, 54, 86, 118})
MAGIC_NUMBER_Z: frozenset[int] = frozenset({2, 8, 20, 28, 50, 82})

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

# period, group (0 = f-block placeholder), category
_META: dict[int, tuple[int, int, str]] = {
    1: (1, 1, "nonmetal"),
    2: (1, 18, "noble gas"),
    10: (2, 18, "noble gas"),
    18: (3, 18, "noble gas"),
    36: (4, 18, "noble gas"),
    54: (5, 18, "noble gas"),
    86: (6, 18, "noble gas"),
    118: (7, 18, "noble gas"),
}


def _period_group_category(z: int) -> tuple[int, int, str]:
    if z in _META:
        return _META[z]
    if z in NOBLE_GAS_Z:
        return (1, 18, "noble gas")
    if z <= 2:
        return (1, z, "nonmetal")
    if z <= 10:
        return (2, z if z <= 2 else (z - 2 if z <= 4 else (z - 10 if z >= 13 else z)), "nonmetal")
    # simplified fallback
    if z <= 18:
        return (3, min(18, max(1, z - 10)), "nonmetal" if z < 13 else "halogen")
    if z <= 36:
        return (4, 1 if z == 19 else (2 if z == 20 else 0), "metal")
    if z <= 54:
        return (5, 1, "metal")
    if z <= 86:
        return (6, 0, "metal")
    if z <= 118:
        return (7, 0, "metal")
    return (0, 0, "synthetic")


def _aufbau_config(z: int) -> str:
    """Build electron configuration string via aufbau filling."""
    if z <= 0 or z > 118:
        return "—"
    subshells = [
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
    ]
    remaining = z
    parts: list[str] = []
    for label, cap in subshells:
        if remaining <= 0:
            break
        fill = min(remaining, cap)
        if fill:
            parts.append(f"{label}{fill if fill < 10 else fill}")
        remaining -= fill
    return " ".join(parts)


def shell_occupancies(z: int) -> list[tuple[int, int]]:
    """Electrons per principal shell n=1,2,3,... for cloud visualization."""
    if z <= 0 or z > 118:
        return []
    caps = {1: 2, 2: 8, 3: 18, 4: 32, 5: 32, 6: 18, 7: 8}
    order = [
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
    ]
    shells: dict[int, int] = {}
    rem = z
    for shell, cap in order:
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

    @property
    def toe_stability_note(self) -> str:
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
    if z < 1 or z > 118:
        return None
    period, group, category = _period_group_category(z)
    if z in NOBLE_GAS_Z:
        category = "noble gas"
    return Element(
        z=z,
        name=_NAMES[z],
        symbol=_SYMBOLS[z],
        period=period,
        group=group,
        category=category,
        electron_config=_aufbau_config(z),
        is_noble_gas=z in NOBLE_GAS_Z,
        is_magic_number=z in MAGIC_NUMBER_Z,
        is_known=True,
    )


def is_real_element(z: int) -> bool:
    return 1 <= z <= 118