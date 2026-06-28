"""Neon glow CSS plugin for Kingdom Come badges and highlights."""

from __future__ import annotations

import base64
from pathlib import Path

NEON_CSS = """
/* Kingdom Come neon plugin — noble gas / magic island badges */
.kc-neon-noble {
  display: inline-block;
  padding: 0.2rem 0.65rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: #e0ffff;
  background: rgba(0, 201, 183, 0.15);
  border: 1px solid rgba(0, 201, 183, 0.55);
  box-shadow:
    0 0 6px rgba(0, 201, 183, 0.6),
    0 0 14px rgba(26, 143, 227, 0.35),
    inset 0 0 8px rgba(0, 201, 183, 0.12);
  text-shadow: 0 0 8px rgba(0, 245, 255, 0.9);
  animation: kc-neon-pulse 2.8s ease-in-out infinite;
}
.kc-neon-magic {
  display: inline-block;
  padding: 0.2rem 0.55rem;
  border-radius: 6px;
  font-size: 0.75rem;
  color: #ffe8a3;
  border: 1px solid rgba(201, 162, 39, 0.5);
  box-shadow: 0 0 10px rgba(201, 162, 39, 0.35);
  text-shadow: 0 0 6px rgba(201, 162, 39, 0.8);
}
.kc-element-card {
  background: rgba(18, 36, 61, 0.92);
  border: 1px solid rgba(26, 143, 227, 0.3);
  border-radius: 14px;
  padding: 0.75rem 0.9rem;
  margin: 0;
}
.kc-card-inner {
  display: flex;
  gap: 0.6rem;
  align-items: flex-start;
}
.kc-card-body { flex: 1; min-width: 0; }
.kc-card-art {
  width: 68px;
  height: 68px;
  border-radius: 8px;
  border: 1px solid rgba(0, 201, 183, 0.35);
  object-fit: cover;
  flex-shrink: 0;
  box-shadow: 0 0 10px rgba(0, 201, 183, 0.2);
}
.kc-element-card h2 {
  margin: 0 0 0.2rem;
  font-size: 1.35rem;
  color: #e8f4ff;
}
.kc-element-symbol {
  font-size: 1.85rem;
  font-weight: 700;
  color: #00c9b7;
  text-shadow: 0 0 12px rgba(0, 201, 183, 0.5);
  margin-right: 0.4rem;
}
.kc-element-meta {
  color: #8ecae6;
  font-size: 0.82rem;
  line-height: 1.4;
}
.kc-element-summary {
  margin-top: 0.45rem;
  color: #d4e4f7;
  font-size: 0.8rem;
}
.kc-metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.35rem;
}
.kc-metric-card {
  background: rgba(18, 36, 61, 0.88);
  border: 1px solid rgba(26, 143, 227, 0.22);
  border-radius: 8px;
  padding: 0.4rem 0.5rem;
}
.kc-metric-card span {
  display: block;
  color: #6a9bb8;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.kc-metric-card strong {
  color: #e8f4ff;
  font-size: 0.88rem;
  font-weight: 600;
}
.kc-metric-wide { grid-column: 1 / -1; }
.kc-toe-strip {
  background: rgba(18, 36, 61, 0.78);
  border: 1px solid rgba(201, 162, 39, 0.22);
  border-radius: 10px;
  padding: 0.55rem 0.8rem;
  margin: 0;
}
.kc-toe-narrative {
  color: #c9a227;
  font-style: italic;
  font-size: 0.86rem;
  line-height: 1.4;
}
.kc-toe-details {
  margin-top: 0.35rem;
  color: #8ecae6;
  font-size: 0.8rem;
}
.kc-toe-details summary {
  cursor: pointer;
  color: #1a8fe3;
  font-size: 0.78rem;
}
.kc-synthetic-banner {
  color: #ef553b;
  font-weight: 600;
  font-size: 0.88rem;
}
@keyframes kc-neon-pulse {
  0%, 100% { box-shadow: 0 0 6px rgba(0,201,183,0.5), 0 0 14px rgba(26,143,227,0.3); }
  50% { box-shadow: 0 0 12px rgba(0,201,183,0.85), 0 0 22px rgba(26,143,227,0.5); }
}
"""


def _art_inset_html(art_path: str | None) -> str:
    """Inline noble-gas thumbnail inside the element card (HF-safe data URI)."""
    if not art_path:
        return ""
    path = Path(art_path)
    if not path.is_file():
        return ""
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return (
        f'<img class="kc-card-art" src="data:image/png;base64,{b64}" '
        f'alt="Noble gas electron cloud" title="Noble gas artwork"/>'
    )


def element_card_html(element, flywheel: dict, *, art_path: str | None = None) -> str:
    """Compact element card with optional noble-gas art inset."""
    badges = []
    if element.is_noble_gas:
        badges.append('<span class="kc-neon-noble">✦ NOBLE GAS · FLUX FLYWHEEL LOCK</span>')
    if element.is_magic_number:
        badges.append('<span class="kc-neon-magic">Magic number</span>')
    badge_row = " ".join(badges)
    art = _art_inset_html(art_path)

    return f"""
<div class="kc-element-card">
  <div class="kc-card-inner">
    <div class="kc-card-body">
      <div>
        <span class="kc-element-symbol">{element.symbol}</span>
        <h2>{element.name}</h2>
      </div>
      <div style="margin:0.35rem 0">{badge_row}</div>
      <div class="kc-element-meta">
        <strong>Z</strong> = {element.z} &nbsp;·&nbsp;
        Period {element.period} &nbsp;·&nbsp;
        Group {element.group if element.group else "—"} &nbsp;·&nbsp;
        {element.category.title()}<br/>
        <strong>e⁻ config:</strong> {element.electron_config}
      </div>
      <div class="kc-element-summary">
        <strong>Flywheel:</strong> {flywheel["stability_class"]}
        (score {flywheel["stability_score"]}) &nbsp;·&nbsp;
        δω = {flywheel["delta_omega"]}
      </div>
    </div>
    {art}
  </div>
</div>
"""


def flux_metrics_cards_html(flywheel: dict) -> str:
    """Compact metric cards for the secondary row."""
    stability_class = flywheel["stability_class"]
    if len(stability_class) > 38:
        stability_class = stability_class[:36] + "…"
    return f"""
<div class="kc-metrics-grid">
  <div class="kc-metric-card">
    <span>Stability</span><strong>{flywheel["stability_score"]}</strong>
  </div>
  <div class="kc-metric-card">
    <span>δω</span><strong>{flywheel["delta_omega"]}</strong>
  </div>
  <div class="kc-metric-card">
    <span>Gauge</span><strong>{flywheel["gauge_strength"]}</strong>
  </div>
  <div class="kc-metric-card">
    <span>pseudo_Z</span><strong>{flywheel["pseudo_Z"]}</strong>
  </div>
  <div class="kc-metric-card kc-metric-wide">
    <span>Class</span><strong>{stability_class}</strong>
  </div>
</div>
"""


def toe_strip_html(element, flywheel: dict) -> str:
    """Always-visible TOE strip with optional expanded detail."""
    return f"""
<div class="kc-toe-strip">
  <em class="kc-toe-narrative">{element.toe_narrative}</em>
  <details class="kc-toe-details">
    <summary>Full TOE interpretation</summary>
    {element.toe_stability_note}<br/>
    δω = {flywheel["delta_omega"]} · gauge = {flywheel["gauge_strength"]} ·
    ω_L = {flywheel["omega_L"]} · ω_R = {flywheel["omega_R"]}
  </details>
</div>
"""


def synthetic_z_html(z: int, flywheel: dict) -> str:
    label = (
        "Beyond known elements — theoretical TOE extension"
        if z > 118
        else "Synthetic probe — outside periodic table"
    )
    extra = ""
    if z == 129:
        extra = (
            " · <strong>pseudo_Z=129</strong> sweep ID (use Z=2 for physical anchor)"
        )
    return f"""
<div class="kc-element-card">
  <h2>Z = {z}</h2>
  <p class="kc-synthetic-banner">{label}</p>
  <div class="kc-element-meta">
    Theoretical flux probe — no periodic-table entry.{extra}
  </div>
  <div class="kc-element-summary">
    <strong>Flywheel:</strong> {flywheel["stability_class"]}
    (score {flywheel["stability_score"]})
  </div>
</div>
"""


def synthetic_toe_strip_html(z: int, flywheel: dict) -> str:
    extra = ""
    if z == 129:
        extra = (
            " pseudo_Z=129 is the Magic Island sweep anchor; Z=2 (He) is the physical reference."
        )
    return f"""
<div class="kc-toe-strip">
  <em class="kc-toe-narrative">Theoretical flux flywheel probe at Z = {z} — mapped onto the
  Hopf lattice stability model beyond known elements.{extra}</em>
  <details class="kc-toe-details">
    <summary>Full notes</summary>
    {flywheel["stability_class"]} (score {flywheel["stability_score"]}) ·
    δω = {flywheel["delta_omega"]} · gauge = {flywheel["gauge_strength"]}
  </details>
</div>
"""