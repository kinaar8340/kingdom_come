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
  padding: 0.24rem 0.1rem;
  border-radius: 5px;
  border: 1px solid rgba(90, 170, 255, 0.55);
  background: rgba(40, 75, 130, 0.85);
  color: #ffffff;
  line-height: 1.1;
  cursor: pointer;
  font-family: inherit;
  width: 100%;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.08);
}
.kc-pt-symbol {
  display: block;
  font-size: 0.78rem;
  font-weight: 800;
  color: #ffffff !important;
  letter-spacing: 0.02em;
  line-height: 1.15;
}
button.kc-pt-cell .kc-pt-symbol {
  color: #ffffff !important;
}
button.kc-pt-cell:hover {
  border-color: #5eb8ff;
  filter: brightness(1.18) saturate(1.15);
  box-shadow: 0 0 10px rgba(26, 143, 227, 0.45);
}
button.kc-pt-cell:focus-visible {
  outline: 2px solid #c9a227;
  outline-offset: 1px;
}
.kc-pt-cell sub {
  display: block;
  font-size: 0.52rem;
  font-weight: 400;
  color: #8ecae6;
}
.kc-pt-cell.kc-pt-active {
  border-color: #ffd45a;
  box-shadow: 0 0 12px rgba(255, 210, 80, 0.65);
  color: #ffffff;
  background: rgba(220, 170, 40, 0.82) !important;
}
.kc-pt-cell.kc-pt-active .kc-pt-symbol {
  color: #ffffff !important;
}
.kc-pt-cell.kc-pt-noble {
  color: #ffffff;
  border-color: rgba(0, 245, 255, 0.72);
}
.kc-pt-cell.kc-pt-noble .kc-pt-symbol {
  color: #ffffff !important;
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
  color: #8ecae6;
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

# Flux Flywheel tab only — periodic tables need higher contrast on black.
FLUX_PERIODIC_CSS = """
.kc-flux-page .accordion {
  background: rgba(18, 36, 61, 0.58) !important;
}
.kc-flux-page .kc-pt-wrap {
  padding: 0.55rem 0.65rem;
  background: rgba(18, 36, 61, 0.72);
  border: 1px solid rgba(26, 143, 227, 0.35);
  border-radius: 10px;
}
.kc-flux-page .html-container,
.kc-flux-page .html-container .prose {
  background: transparent !important;
}
.kc-flux-page .kc-pt-cell {
  border-color: rgba(110, 185, 255, 0.62) !important;
  color: #ffffff !important;
  filter: saturate(1.12);
}
.kc-flux-page .kc-pt-symbol,
.kc-flux-page .kc-pt-cell.kc-pt-active .kc-pt-symbol,
.kc-flux-page .kc-pt-cell.kc-pt-noble .kc-pt-symbol {
  color: #ffffff !important;
  font-weight: 800 !important;
}
.kc-flux-page .kc-pt-cell sub {
  color: #b8ddf5 !important;
}
.kc-flux-page .kc-pt-legend {
  color: #a8cce8 !important;
}
"""

PERIODIC_TABLE_JS = """
function wirePtClicks() {
  element.querySelectorAll('[data-kc-z]').forEach((btn) => {
    if (btn.dataset.kcWired === '1') return;
    btn.dataset.kcWired = '1';
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const z = parseInt(btn.getAttribute('data-kc-z'), 10);
      if (!Number.isNaN(z)) trigger('pick', { z });
    });
  });
}
wirePtClicks();
watch('value', wirePtClicks);
"""

_CATEGORY_COLORS = {
    "noble gas": "rgba(0, 235, 215, 0.84)",
    "alkali metal": "rgba(255, 88, 72, 0.82)",
    "alkaline earth metal": "rgba(255, 188, 95, 0.82)",
    "transition metal": "rgba(45, 155, 255, 0.82)",
    "post-transition metal": "rgba(115, 175, 255, 0.80)",
    "metalloid": "rgba(175, 135, 255, 0.80)",
    "nonmetal": "rgba(75, 225, 165, 0.78)",
    "halogen": "rgba(0, 225, 195, 0.82)",
    "lanthanide": "rgba(190, 145, 255, 0.80)",
    "actinide": "rgba(225, 105, 195, 0.80)",
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


def _known_grid_position(z: int) -> tuple[int, int]:
    el = get_element(z)
    if el is None:
        return (0, 0)
    if 57 <= z <= 71:
        return (9, z - 54)  # lanthanide row
    if 89 <= z <= 103:
        return (11, z - 86)  # actinide row
    group = el.group if el.group else 3
    return (el.period, group)


def _superheavy_grid_position(z: int) -> tuple[int, int]:
    """18-column extension grid for Z = 119–180 (period-8 block + overflow rows)."""
    offset = z - (KNOWN_ELEMENT_MAX + 1)
    if offset < 0:
        return (0, 0)
    return (1 + offset // 18, offset % 18 + 1)


def _periodic_cell_html(z: int, current_z: int) -> str:
    el = get_element(z)
    if el is None:
        return '<div class="kc-pt-gap">·</div>'
    classes = ["kc-pt-cell"]
    if z == current_z:
        classes.append("kc-pt-active")
    if z in NOBLE_GAS_Z:
        classes.append("kc-pt-noble")
    if z in MAGIC_NUMBER_Z:
        classes.append("kc-pt-magic")
    bg = _CATEGORY_COLORS.get(el.category, "rgba(40,75,130,0.85)")
    synth = " — predicted" if el.is_synthetic else ""
    return (
        f'<button type="button" class="{" ".join(classes)}" style="background:{bg}" '
        f'data-kc-z="{z}" title="{el.name} (Z={z}){synth}">'
        f'<span class="kc-pt-symbol">{el.symbol}</span><sub>{z}</sub></button>'
    )


def _periodic_grid_html(
    z_min: int,
    z_max: int,
    current_z: int,
    position_fn,
    legend: str,
) -> str:
    grid: dict[tuple[int, int], int] = {}
    for z in range(z_min, z_max + 1):
        pos = position_fn(z)
        if pos[0] > 0:
            grid[pos] = z

    if not grid:
        return ""

    max_row = max(row for row, _ in grid)
    cells: list[str] = []
    for row in range(1, max_row + 1):
        for col in range(1, 19):
            z = grid.get((row, col))
            if z is None:
                cells.append('<div class="kc-pt-gap">·</div>')
                continue
            cells.append(_periodic_cell_html(z, current_z))

    return f"""
<div class="kc-pt-wrap kc-flux-pt">
  <div class="kc-pt-grid">{"".join(cells)}</div>
  <div class="kc-pt-legend">{legend}</div>
</div>
"""


def known_periodic_table_html(current_z: int) -> str:
    """Render known elements Z = 1–118."""
    return _periodic_grid_html(
        1,
        KNOWN_ELEMENT_MAX,
        current_z,
        _known_grid_position,
        "Click any element · ★ noble gas · ◆ magic number · gold = current Z",
    )


def superheavy_periodic_table_html(current_z: int) -> str:
    """Render predicted superheavy elements Z = 119–180."""
    return _periodic_grid_html(
        KNOWN_ELEMENT_MAX + 1,
        EXPLORER_Z_MAX,
        current_z,
        _superheavy_grid_position,
        "Click any superheavy element · ◆ magic number (Z=129) · gold = current Z · all predicted",
    )


def periodic_table_html(current_z: int) -> str:
    """Both tables — kept for backward compatibility in tests."""
    return known_periodic_table_html(current_z) + superheavy_periodic_table_html(current_z)