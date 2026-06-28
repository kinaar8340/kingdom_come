"""Periodic table picker — dropdown, visual grid, quick-jump controls."""

from __future__ import annotations

from kingdom.core.elements import EXPLORER_Z_MAX, KNOWN_ELEMENT_MAX, MAGIC_NUMBER_Z, NOBLE_GAS_Z, get_element

PERIODIC_CSS = """
.kc-pt-wrap {
  margin: 0.35rem 0 0.5rem;
  overflow-x: auto;
}
.kc-pt-grid {
  display: grid;
  grid-template-columns: repeat(18, minmax(2.1rem, 1fr));
  gap: 3px;
  min-width: 36rem;
}
.kc-pt-cell {
  text-align: center;
  font-size: 0.68rem;
  font-weight: 600;
  padding: 0.22rem 0.1rem;
  border-radius: 5px;
  border: 1px solid rgba(26, 143, 227, 0.18);
  background: rgba(18, 36, 61, 0.75);
  color: #8ecae6;
  line-height: 1.1;
  cursor: pointer;
  font-family: inherit;
  width: 100%;
}
button.kc-pt-cell:hover {
  border-color: #1a8fe3;
  filter: brightness(1.12);
  box-shadow: 0 0 8px rgba(26, 143, 227, 0.35);
}
button.kc-pt-cell:focus-visible {
  outline: 2px solid #c9a227;
  outline-offset: 1px;
}
.kc-pt-cell sub {
  display: block;
  font-size: 0.52rem;
  font-weight: 400;
  color: #6a9bb8;
}
.kc-pt-cell.kc-pt-active {
  border-color: #c9a227;
  box-shadow: 0 0 10px rgba(201, 162, 39, 0.55);
  color: #ffe8a3;
  background: rgba(201, 162, 39, 0.18);
}
.kc-pt-cell.kc-pt-noble {
  color: #00f5ff;
  border-color: rgba(0, 201, 183, 0.45);
}
.kc-pt-cell.kc-pt-magic::after {
  content: "✦";
  font-size: 0.45rem;
  color: #c9a227;
  margin-left: 1px;
}
.kc-pt-gap { visibility: hidden; pointer-events: none; }
.kc-pt-legend {
  font-size: 0.72rem;
  color: #6a9bb8;
  margin-top: 0.35rem;
}
.kc-pt-superheavy {
  margin-top: 0.45rem;
  padding: 0.45rem 0.6rem;
  border-radius: 8px;
  border: 1px dashed rgba(239, 85, 59, 0.35);
  color: #ffb4a2;
  font-size: 0.78rem;
}
"""

_CATEGORY_COLORS = {
    "noble gas": "rgba(0,201,183,0.22)",
    "alkali metal": "rgba(239,85,59,0.15)",
    "alkaline earth metal": "rgba(255,180,100,0.12)",
    "transition metal": "rgba(26,143,227,0.15)",
    "post-transition metal": "rgba(100,160,220,0.12)",
    "metalloid": "rgba(150,120,200,0.12)",
    "nonmetal": "rgba(80,200,160,0.1)",
    "halogen": "rgba(0,200,180,0.14)",
    "lanthanide": "rgba(180,140,255,0.12)",
    "actinide": "rgba(200,100,180,0.12)",
}


def element_picker_choices() -> list[tuple[str, int]]:
    """Dropdown labels for Z = 1–180."""
    choices: list[tuple[str, int]] = []
    for z in range(1, EXPLORER_Z_MAX + 1):
        el = get_element(z)
        if el is None:
            continue
        tag = " ★" if el.is_noble_gas else (" ◆" if el.is_magic_number else "")
        synth = " [predicted]" if el.is_synthetic else ""
        label = f"Z={z:3d}  {el.symbol:3s}  {el.name}{tag}{synth}"
        choices.append((label, z))
    return choices


def picker_label_for_z(z: int) -> str:
    for label, val in element_picker_choices():
        if val == int(z):
            return label
    return f"Z={z:3d}"


def _grid_position(z: int) -> tuple[int, int]:
    el = get_element(z)
    if el is None:
        return (0, 0)
    if 57 <= z <= 71:
        return (9, z - 54)  # lanthanide row
    if 89 <= z <= 103:
        return (11, z - 86)  # actinide row
    group = el.group if el.group else 3
    return (el.period, group)


def periodic_table_html(current_z: int) -> str:
    """Render compact periodic table with active Z highlighted (Z = 1–118)."""
    grid: dict[tuple[int, int], int] = {}
    for z in range(1, KNOWN_ELEMENT_MAX + 1):
        pos = _grid_position(z)
        if pos[0] > 0:
            grid[pos] = z

    max_row = max((r for r, _ in grid), default=7)
    cells: list[str] = []
    for row in range(1, max_row + 1):
        for col in range(1, 19):
            z = grid.get((row, col))
            if z is None:
                cells.append('<div class="kc-pt-gap">·</div>')
                continue
            el = get_element(z)
            if el is None:
                continue
            classes = ["kc-pt-cell"]
            if z == current_z:
                classes.append("kc-pt-active")
            if z in NOBLE_GAS_Z:
                classes.append("kc-pt-noble")
            if z in MAGIC_NUMBER_Z:
                classes.append("kc-pt-magic")
            bg = _CATEGORY_COLORS.get(el.category, "rgba(18,36,61,0.75)")
            cells.append(
                f'<button type="button" class="{" ".join(classes)}" style="background:{bg}" '
                f'data-kc-z="{z}" title="{el.name} (Z={z})">'
                f"{el.symbol}<sub>{z}</sub></button>"
            )

    superheavy = ""
    if current_z > KNOWN_ELEMENT_MAX:
        el = get_element(current_z)
        if el:
            superheavy = (
                f'<div class="kc-pt-superheavy">Superheavy zone · Z={current_z} · '
                f"{el.name} ({el.symbol}) — theoretical / predicted</div>"
            )

    return f"""
<div class="kc-pt-wrap">
  <div class="kc-pt-grid">{"".join(cells)}</div>
  <div class="kc-pt-legend">Click any element · ★ noble gas · ◆ magic number · gold = current Z</div>
  {superheavy}
</div>
"""