"""IUPAC period, group, and category for Z = 1–118."""

from __future__ import annotations

# (period, group, category) indexed by atomic number Z
_PERIOD_GROUP_CATEGORY: dict[int, tuple[int, int, str]] = {}


def _set(z: int, period: int, group: int, category: str) -> None:
    _PERIOD_GROUP_CATEGORY[z] = (period, group, category)


def _build() -> dict[int, tuple[int, int, str]]:
    if _PERIOD_GROUP_CATEGORY:
        return _PERIOD_GROUP_CATEGORY

    _set(1, 1, 1, "nonmetal")
    _set(2, 1, 18, "noble gas")

    p2 = [
        (3, 1, "alkali metal"),
        (4, 2, "alkaline earth metal"),
        (5, 13, "metalloid"),
        (6, 14, "nonmetal"),
        (7, 15, "nonmetal"),
        (8, 16, "nonmetal"),
        (9, 17, "halogen"),
        (10, 18, "noble gas"),
    ]
    for z, (_, g, c) in enumerate(p2, start=3):
        _set(z, 2, g, c)

    p3 = [
        (11, 1, "alkali metal"),
        (12, 2, "alkaline earth metal"),
        (13, 13, "post-transition metal"),
        (14, 14, "metalloid"),
        (15, 15, "nonmetal"),
        (16, 16, "nonmetal"),
        (17, 17, "halogen"),
        (18, 18, "noble gas"),
    ]
    for z, (_, g, c) in enumerate(p3, start=11):
        _set(z, 3, g, c)

    for z, g in enumerate(range(1, 19), start=19):
        if g == 1:
            cat = "alkali metal"
        elif g == 2:
            cat = "alkaline earth metal"
        elif 3 <= g <= 12:
            cat = "transition metal"
        elif g == 13:
            cat = "post-transition metal"
        elif g == 14:
            cat = "metalloid"
        elif g == 15:
            cat = "metalloid" if z == 33 else "nonmetal"
        elif g == 16:
            cat = "nonmetal"
        elif g == 17:
            cat = "halogen"
        else:
            cat = "noble gas"
        _set(z, 4, g, cat)

    for z, g in enumerate(range(1, 19), start=37):
        if g == 1:
            cat = "alkali metal"
        elif g == 2:
            cat = "alkaline earth metal"
        elif 3 <= g <= 12:
            cat = "transition metal"
        elif g == 13:
            cat = "post-transition metal"
        elif g == 14:
            cat = "metalloid"
        elif g == 15:
            cat = "metalloid"
        elif g == 16:
            cat = "nonmetal"
        elif g == 17:
            cat = "halogen"
        else:
            cat = "noble gas"
        _set(z, 5, g, cat)

    _set(55, 6, 1, "alkali metal")
    _set(56, 6, 2, "alkaline earth metal")
    for z in range(57, 72):
        _set(z, 6, 3, "lanthanide")
    for z, g in enumerate(range(4, 19), start=72):
        if g <= 12:
            cat = "transition metal"
        elif g == 13:
            cat = "post-transition metal"
        elif g == 14:
            cat = "post-transition metal"
        elif g == 15:
            cat = "metalloid"
        elif g == 16:
            cat = "post-transition metal"
        elif g == 17:
            cat = "halogen"
        else:
            cat = "noble gas"
        _set(z, 6, g, cat)

    _set(87, 7, 1, "alkali metal")
    _set(88, 7, 2, "alkaline earth metal")
    for z in range(89, 104):
        _set(z, 7, 3, "actinide")
    for z, g in enumerate(range(4, 19), start=104):
        if g <= 12:
            cat = "transition metal"
        elif g == 13:
            cat = "post-transition metal"
        elif g == 14:
            cat = "post-transition metal"
        elif g == 15:
            cat = "post-transition metal"
        elif g == 16:
            cat = "post-transition metal"
        elif g == 17:
            cat = "halogen"
        else:
            cat = "noble gas"
        _set(z, 7, g, cat)

    return _PERIOD_GROUP_CATEGORY


def period_group_category(z: int) -> tuple[int, int, str]:
    meta = _build()
    if z in meta:
        return meta[z]
    return (0, 0, "unknown")