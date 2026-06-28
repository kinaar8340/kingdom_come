"""IUPAC systematic names and symbols for Z > 118 (superheavy / theoretical zone)."""

from __future__ import annotations

_DIGIT_ROOTS = (
    "nil",
    "un",
    "bi",
    "tri",
    "quad",
    "pent",
    "hex",
    "sept",
    "oct",
    "enn",
)

# Special cases where proposed names differ from strict concatenation
_OVERRIDES: dict[int, tuple[str, str]] = {
    129: ("Unbiennium", "Ube"),  # Magic Island sweep anchor ID
}


def systematic_name_symbol(z: int) -> tuple[str, str]:
    """Return (name, symbol) using IUPAC provisional nomenclature."""
    if z in _OVERRIDES:
        return _OVERRIDES[z]
    digits = [int(ch) for ch in str(z)]
    roots = [_DIGIT_ROOTS[d] for d in digits]
    name = "".join(roots) + "ium"
    name = name[0].upper() + name[1:]
    symbol = roots[0][0].upper() + "".join(root[0].lower() for root in roots[1:])
    if len(symbol) > 3:
        symbol = symbol[:3]
    return name, symbol


def superheavy_period_group(z: int) -> tuple[int, int, str]:
    """Assign period 8 block placement for theoretical Z = 119–180."""
    offset = z - 119
    if offset < 2:
        return (8, 1 + offset, "superheavy alkali metal" if offset == 0 else "superheavy alkaline earth")
    if offset < 12:
        return (8, 3 + (offset - 2), "superheavy transition metal")
    if offset < 18:
        return (8, 13 + (offset - 12), "superheavy post-transition metal")
    return (8, 18, "superheavy noble gas candidate")