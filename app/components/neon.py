"""Neon glow CSS plugin for Kingdom Come badges and highlights."""

from __future__ import annotations

import base64
from pathlib import Path

from kingdom.core.experimental_data import interpret_comparison_fidelity
from kingdom.core.flux_explorer import build_observables_validation

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
  background: rgba(18, 36, 61, 0.40);
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
  background: rgba(18, 36, 61, 0.40);
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
.kc-observables-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.35rem;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}
.kc-observables-grid .kc-metric-card strong {
  color: #00c9b7;
}
.kc-obs-align {
  grid-column: 1 / -1;
}
.kc-align-track {
  margin-top: 0.35rem;
  height: 6px;
  border-radius: 999px;
  background: rgba(26, 143, 227, 0.18);
  overflow: hidden;
}
.kc-align-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #1a8fe3, #00c9b7);
}
.kc-align-fill.kc-align-mid {
  background: linear-gradient(90deg, #c9a227, #ffd45a);
}
.kc-align-fill.kc-align-low {
  background: linear-gradient(90deg, #ef553b, #ffb4a2);
}
.kc-obs-caption {
  display: block;
  margin-top: 0.25rem;
  color: #6a9bb8;
  font-size: 0.68rem;
  line-height: 1.35;
}
.kc-obs-tip {
  cursor: help;
  border-bottom: 1px dotted rgba(142, 202, 230, 0.45);
}
.kc-obs-delta {
  display: block;
  margin-top: 0.2rem;
  font-size: 0.68rem;
  color: #8ecae6;
  line-height: 1.3;
}
.kc-obs-delta.kc-obs-delta-pos { color: #00c9b7; }
.kc-obs-delta.kc-obs-delta-neg { color: #ffb4a2; }
.kc-obs-align-score {
  display: flex;
  align-items: baseline;
  gap: 0.35rem;
}
.kc-obs-align-score small {
  color: #6a9bb8;
  font-size: 0.72rem;
  font-weight: 400;
}
.kc-observables-grid.kc-obs-heavy .kc-metric-card:nth-child(3) strong,
.kc-observables-grid.kc-obs-heavy .kc-metric-card:nth-child(4) strong {
  color: #9ec8e8;
  opacity: 0.88;
}
.kc-obs-heavy-note {
  grid-column: 1 / -1;
  padding: 0.35rem 0.45rem;
  border-radius: 6px;
  background: rgba(18, 36, 61, 0.45);
  border: 1px dashed rgba(142, 202, 230, 0.25);
  color: #6a9bb8;
  font-size: 0.67rem;
  line-height: 1.35;
  font-style: italic;
}
.kc-obs-mu-stack {
  display: flex;
  flex-direction: column;
  gap: 0.12rem;
  margin-top: 0.15rem;
}
.kc-obs-mu-stack .kc-obs-delta {
  margin-top: 0;
}
.kc-obs-exp-tag {
  color: #8ecae6;
  font-size: 0.62rem;
  font-style: italic;
}
.kc-obs-val-wrap {
  grid-column: 1 / -1;
  margin-top: 0.25rem;
}
.kc-obs-val-title {
  display: block;
  color: #6a9bb8;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.3rem;
}
.kc-obs-val-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.68rem;
  line-height: 1.35;
}
.kc-obs-val-table th {
  color: #6a9bb8;
  font-weight: 600;
  text-align: left;
  padding: 0.28rem 0.35rem;
  border-bottom: 1px solid rgba(26, 143, 227, 0.22);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  font-size: 0.62rem;
}
.kc-obs-val-table td {
  color: #e8f4ff;
  padding: 0.3rem 0.35rem;
  border-bottom: 1px solid rgba(26, 143, 227, 0.1);
  vertical-align: top;
}
.kc-obs-val-table tr:last-child td {
  border-bottom: none;
}
.kc-obs-val-table .kc-obs-val-cat {
  color: #00c9b7;
  font-weight: 600;
  white-space: nowrap;
}
.kc-obs-val-table .kc-obs-val-delta-pos { color: #00c9b7; }
.kc-obs-val-table .kc-obs-val-delta-neg { color: #ffb4a2; }
.kc-obs-val-table .kc-obs-val-quality {
  color: #8ecae6;
  font-style: italic;
  white-space: nowrap;
}
.kc-obs-val-info {
  cursor: help;
  border-bottom: 1px dotted rgba(142, 202, 230, 0.45);
}
.kc-obs-fidelity {
  grid-column: 1 / -1;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.35rem 0.6rem;
  padding: 0.55rem 0.65rem;
  background: rgba(10, 22, 40, 0.55);
  border-radius: 8px;
}
.kc-obs-fidelity-headline strong {
  font-size: 1.65rem;
  line-height: 1;
}
.kc-obs-fidelity strong {
  font-size: 1.15rem;
}
.kc-obs-fidelity small {
  color: #6a9bb8;
  font-size: 0.78rem;
}
.kc-obs-fidelity .kc-obs-caption {
  flex: 1 1 100%;
  margin-top: 0;
}
.kc-obs-fidelity.kc-fidelity-high {
  border-color: rgba(0, 201, 183, 0.45);
}
.kc-obs-fidelity.kc-fidelity-mid {
  border-color: rgba(255, 212, 90, 0.5);
  box-shadow: 0 0 10px rgba(255, 212, 90, 0.12);
}
.kc-obs-fidelity.kc-fidelity-low {
  border-color: rgba(255, 180, 162, 0.4);
}
.kc-obs-fidelity.kc-fidelity-high strong { color: #00c9b7; }
.kc-obs-fidelity.kc-fidelity-mid strong { color: #ffd45a; }
.kc-obs-fidelity.kc-fidelity-low strong { color: #ffb4a2; }
.kc-fidelity-tier {
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 0.08rem 0.4rem;
  border-radius: 4px;
}
.kc-tier-high {
  color: #00c9b7;
  background: rgba(0, 201, 183, 0.12);
}
.kc-tier-mid {
  color: #ffd45a;
  background: rgba(255, 212, 90, 0.14);
}
.kc-tier-low {
  color: #ffb4a2;
  background: rgba(255, 180, 162, 0.12);
}
.kc-obs-fidelity-panel {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}
.kc-obs-fidelity-header {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  width: 100%;
  align-items: stretch;
}
.kc-obs-fidelity-header .kc-obs-fidelity-headline {
  flex: 1 1 260px;
  min-width: 0;
}
.kc-obs-fidelity-core-card {
  flex: 1 1 200px;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.15rem;
  padding: 0.55rem 0.65rem;
  background: rgba(26, 143, 227, 0.1);
  border: 1px solid rgba(26, 143, 227, 0.28);
  border-radius: 8px;
}
.kc-obs-fidelity-core-card strong {
  font-size: 1.35rem;
  line-height: 1;
  color: #4cc9f0;
}
.kc-obs-fidelity-core-card small {
  color: #6a9bb8;
  font-size: 0.78rem;
}
.kc-obs-fidelity-core-card .kc-obs-fidelity-core-note {
  font-size: 0.62rem;
  color: #8ecae6;
  line-height: 1.35;
}
.kc-obs-fidelity-core {
  font-size: 0.74rem;
  color: #8ecae6;
  padding: 0.3rem 0.45rem;
  background: rgba(26, 143, 227, 0.08);
  border-radius: 6px;
  border: 1px solid rgba(26, 143, 227, 0.2);
  width: 100%;
  box-sizing: border-box;
}
.kc-obs-fidelity-core strong {
  color: #4cc9f0;
}
.kc-obs-fidelity-cats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.25rem 0.5rem;
  font-size: 0.68rem;
  padding: 0.4rem 0.45rem;
  background: rgba(18, 36, 61, 0.45);
  border: 1px solid rgba(26, 143, 227, 0.18);
  border-radius: 6px;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}
.kc-obs-fidelity-cat-breakdown {
  color: #6a9bb8;
  font-size: 0.58rem;
}
.kc-obs-fidelity-cat {
  color: #d4e4f7;
  padding: 0.2rem 0.35rem;
  background: rgba(18, 36, 61, 0.35);
  border-radius: 4px;
}
.kc-obs-fidelity-cat span {
  color: #6a9bb8;
  display: block;
  font-size: 0.6rem;
}
.kc-obs-fidelity-cat strong {
  color: #00c9b7;
}
.kc-obs-fidelity-cat-na strong {
  color: #6a9bb8;
}
.kc-obs-fidelity-proxy {
  font-size: 0.62rem;
  color: #8ecae6;
  line-height: 1.5;
  width: 100%;
  box-sizing: border-box;
}
.kc-obs-fidelity-proxy-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem 0.35rem;
  margin-top: 0.2rem;
}
.kc-proxy-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.1rem 0.4rem;
  border-radius: 999px;
  font-size: 0.58rem;
  font-weight: 600;
  border: 1px solid transparent;
  cursor: help;
}
.kc-proxy-pill-label {
  color: #6a9bb8;
  font-weight: 500;
}
.kc-proxy-pill.kc-proxy-high {
  color: #00c9b7;
  background: rgba(0, 201, 183, 0.12);
  border-color: rgba(0, 201, 183, 0.35);
}
.kc-proxy-pill.kc-proxy-medium {
  color: #ffd45a;
  background: rgba(255, 212, 90, 0.12);
  border-color: rgba(255, 212, 90, 0.35);
}
.kc-proxy-pill.kc-proxy-low {
  color: #ffb4a2;
  background: rgba(255, 180, 162, 0.12);
  border-color: rgba(255, 180, 162, 0.35);
}
.kc-proxy-pill.kc-proxy-none {
  color: #6a9bb8;
  background: rgba(106, 155, 184, 0.1);
  border-color: rgba(106, 155, 184, 0.28);
}
.kc-obs-fidelity-breakdown {
  font-size: 0.65rem;
  color: #8ecae6;
}
.kc-obs-coverage-pill {
  display: inline-block;
  padding: 0.1rem 0.45rem;
  border-radius: 999px;
  font-size: 0.62rem;
  font-weight: 600;
  color: #8ecae6;
  background: rgba(26, 143, 227, 0.12);
  border: 1px solid rgba(26, 143, 227, 0.28);
}
.kc-obs-interpret {
  grid-column: 1 / -1;
  background: rgba(18, 36, 61, 0.55);
  border: 1px solid rgba(255, 180, 162, 0.25);
  border-radius: 8px;
  padding: 0.35rem 0.55rem;
  font-size: 0.74rem;
  color: #d4e4f7;
  line-height: 1.45;
}
.kc-obs-interpret summary {
  cursor: pointer;
  color: #ffd45a;
  font-weight: 600;
  font-size: 0.76rem;
}
.kc-obs-interpret ul {
  margin: 0.35rem 0 0 1rem;
  padding: 0;
  color: #8ecae6;
}
.kc-obs-interpret-note {
  margin: 0.35rem 0 0;
  color: #8ecae6;
  font-style: italic;
}
.kc-obs-noble-banner {
  grid-column: 1 / -1;
  padding: 0.4rem 0.6rem;
  border-radius: 8px;
  font-size: 0.74rem;
  color: #e0ffff;
  background: rgba(0, 201, 183, 0.12);
  border: 1px solid rgba(0, 201, 183, 0.55);
  box-shadow: 0 0 14px rgba(0, 201, 183, 0.18);
}
.kc-obs-noble-banner summary {
  cursor: pointer;
  font-weight: 700;
  color: #00c9b7;
  list-style: none;
}
.kc-obs-noble-banner summary::-webkit-details-marker { display: none; }
.kc-obs-noble-banner[open] summary { margin-bottom: 0.3rem; }
.kc-obs-noble-banner-body {
  color: #b8e8e3;
  line-height: 1.45;
  font-size: 0.72rem;
}
.kc-obs-interpret.kc-interpret-solid {
  border-color: rgba(255, 212, 90, 0.35);
}
.kc-obs-val-wrap details summary {
  cursor: pointer;
  color: #1a8fe3;
  font-size: 0.76rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}
.kc-obs-val-delta-strong {
  font-weight: 700;
}
.kc-obs-val-delta-icon {
  opacity: 0.85;
  margin-right: 0.15rem;
}
.kc-toe-strip {
  background: rgba(18, 36, 61, 0.40);
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
.kc-neon-synthetic {
  display: inline-block;
  padding: 0.18rem 0.5rem;
  border-radius: 6px;
  font-size: 0.72rem;
  color: #ffb4a2;
  border: 1px solid rgba(239, 85, 59, 0.45);
  background: rgba(239, 85, 59, 0.12);
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


def install_neon_plugin() -> str:
    """Return Kingdom Come neon plugin CSS for Gradio ``css=`` injection."""
    return NEON_CSS


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
    if element.is_synthetic:
        badges.append('<span class="kc-neon-synthetic">Theoretical superheavy</span>')
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
        {("Predicted" if element.is_synthetic else "Known")} &nbsp;·&nbsp;
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


def _delta_cell_class(delta_str: str) -> str:
    if delta_str == "—" or delta_str.startswith("+0.00") or delta_str.startswith("+0.0 "):
        return "kc-obs-val-delta-pos"
    if delta_str.startswith("+"):
        return "kc-obs-val-delta-pos"
    if delta_str.startswith("-"):
        return "kc-obs-val-delta-neg"
    return ""


def _delta_display(delta_str: str) -> str:
    """Add scan-friendly icon and emphasis for large mismatches."""
    if delta_str == "—":
        return delta_str
    icon = "↔"
    strong = False
    if delta_str.startswith("+"):
        icon = "↑"
    elif delta_str.startswith("-"):
        icon = "↓"
    if "Δz" in delta_str:
        try:
            val = float(delta_str.replace("Δz", "").strip())
            strong = abs(val) >= 1.5
        except ValueError:
            pass
    elif "pm" in delta_str or "eV" in delta_str or "BM" in delta_str:
        try:
            num = delta_str.split()[0].replace("+", "")
            strong = abs(float(num)) >= 15.0
        except ValueError:
            pass
    cls = "kc-obs-val-delta-strong" if strong else ""
    return (
        f'<span class="{cls}">'
        f'<span class="kc-obs-val-delta-icon">{icon}</span>{delta_str}</span>'
    )


def _fidelity_tier_html(tier: str | None) -> str:
    if tier == "excellent":
        return '<span class="kc-fidelity-tier kc-tier-high">Excellent</span>'
    if tier == "solid":
        return '<span class="kc-fidelity-tier kc-tier-mid">Solid</span>'
    if tier == "low":
        return '<span class="kc-fidelity-tier kc-tier-low">Low</span>'
    return ""


def _fidelity_class(score: float) -> str:
    if score >= 8.5:
        return "kc-fidelity-high"
    if score >= 7.0:
        return "kc-fidelity-mid"
    return "kc-fidelity-low"


def _category_score_html(
    category_scores: dict[str, float | None],
    category_details: dict[str, list[str]] | None = None,
) -> str:
    cat_meta = {
        "Magnetic": ("Magnetic Properties", "Magnetic moment"),
        "Electronic": ("Electronic Properties", "Ionization Energy + Electronegativity"),
        "Structural": ("Structural Properties", "Atomic Radius"),
        "Chemical": ("Chemical Reactivity", "Electron Affinity"),
    }
    breakdowns = category_details or {}
    rows: list[str] = []
    for key, (title, subtitle) in cat_meta.items():
        val = category_scores.get(key)
        parts = breakdowns.get(key, [])
        breakdown_html = ""
        if parts:
            breakdown_html = (
                f'<span class="kc-obs-fidelity-cat-breakdown">'
                f"({' + '.join(parts)})</span>"
            )
        if val is None:
            rows.append(
                f'<div class="kc-obs-fidelity-cat kc-obs-fidelity-cat-na">'
                f'<strong>N/A</strong> {title}<span>{subtitle}</span></div>'
            )
        else:
            rows.append(
                f'<div class="kc-obs-fidelity-cat">'
                f'<strong>{val:.1f}</strong> / 10 · {title}'
                f'{breakdown_html}<span>{subtitle}</span></div>'
            )
    return f'<div class="kc-obs-fidelity-cats">{"".join(rows)}</div>'


_PROXY_QUALITY_TIPS: dict[str, str] = {
    "high": "Direct measurement or period-relative ranking — high trust.",
    "medium": "Stability-based proxy — useful but less direct.",
    "low": "Weak proxy for this element — down-weighted in category scores.",
    "none": "No experimental anchor — excluded from scoring.",
}


def _proxy_quality_html(proxy_quality: dict[str, dict[str, str]]) -> str:
    if not proxy_quality:
        return ""
    labels = {
        "magnetic_moment": "MM",
        "ionization_energy": "IE",
        "atomic_radius": "Radius",
        "electron_affinity": "EA",
        "electronegativity": "EN",
    }
    items: list[str] = []
    for key in labels:
        tag = proxy_quality.get(key, {})
        level = tag.get("level", "medium")
        label = tag.get("label", "Medium")
        note = tag.get("note", "")
        tip = f"{_PROXY_QUALITY_TIPS.get(level, '')} {note}".strip()
        items.append(
            f'<span class="kc-proxy-pill kc-proxy-{level}" title="{tip}">'
            f'<span class="kc-proxy-pill-label">{labels[key]}</span>{label}</span>'
        )
    return (
        '<div class="kc-obs-fidelity-proxy"><strong>Proxy Quality</strong> '
        f'<div class="kc-obs-fidelity-proxy-pills">{"".join(items)}</div></div>'
    )


def flux_observables_fidelity_html(extended: dict, *, interpretation: dict | None = None) -> str:
    """Layered comparison fidelity panel (overall, core, categories, proxy tags)."""
    score = extended.get("comparison_fidelity_score")
    if score is None:
        return ""

    details = extended.get("comparison_fidelity_details") or {}
    note = extended.get("comparison_fidelity_note", "")
    core = extended.get("comparison_fidelity_core_score")
    category_scores = extended.get("comparison_fidelity_category_scores") or {}
    category_details = extended.get("comparison_fidelity_category_details") or {}
    proxy_quality = extended.get("comparison_fidelity_proxy_quality") or {}
    interp = interpretation or {}
    coverage = interp.get("coverage", {})
    coverage_html = ""
    if coverage.get("label"):
        missing_tip = ", ".join(coverage.get("missing", [])) or "all present"
        coverage_html = (
            f'<span class="kc-obs-coverage-pill" title="Missing: {missing_tip}">'
            f'{coverage["label"]}</span>'
        )

    fidelity_class = _fidelity_class(float(score))
    tier_html = _fidelity_tier_html(interp.get("fidelity_tier"))

    short_labels = {
        "magnetic_moment": "μ",
        "ionization_energy": "IE",
        "electron_affinity": "EA",
        "atomic_radius": "radius",
        "electronegativity": "EN",
    }
    breakdown = " · ".join(
        f"{short_labels.get(k, k)} {v}/10" for k, v in details.items()
    )
    tip = note
    if breakdown:
        tip += f" Observable breakdown: {breakdown}."

    breakdown_html = ""
    if breakdown:
        breakdown_html = f'<span class="kc-obs-fidelity-breakdown">{breakdown}</span>'

    core_card_html = ""
    core_gap_note = ""
    if core is not None:
        if float(score) < core - 1.0:
            core_gap_note = (
                "Core exceeds overall — gaps are mainly in weaker proxy translations, "
                "not the underlying stability ranking."
            )
        core_card_html = (
            f'<div class="kc-metric-card kc-obs-fidelity-core-card">'
            f'<span class="kc-obs-tip" title="IE & EN period-relative trends (high-trust proxies)">'
            f"Core Model Fidelity</span>"
            f"<strong>{core}</strong><small>/ 10</small>"
            f'<span class="kc-obs-fidelity-core-note">{core_gap_note or "Stability → IE & EN (high-trust proxies)"}</span>'
            f"</div>"
        )

    header_html = (
        f'<div class="kc-obs-fidelity-header">'
        f'<div class="kc-metric-card kc-obs-fidelity kc-obs-fidelity-headline {fidelity_class}">'
        f'<span class="kc-obs-tip" title="{tip}">Overall Comparison Fidelity</span>'
        f"<strong>{score}</strong><small>/ 10</small>{tier_html}{coverage_html}{breakdown_html}"
        f'<span class="kc-obs-caption">{note}</span>'
        f"</div>"
        f"{core_card_html}"
        f"</div>"
    )

    return f"""
  <div class="kc-obs-fidelity-panel kc-neon-plugin">
    {header_html}
    {_category_score_html(category_scores, category_details)}
    {_proxy_quality_html(proxy_quality)}
  </div>"""


def flux_observables_interpretation_html(interpretation: dict) -> str:
    """Collapsible fidelity interpretation panel."""
    if not interpretation.get("show_interpretation"):
        return ""
    score = interpretation.get("fidelity_score", "—")
    tier = interpretation.get("fidelity_tier")
    if tier in ("solid", "excellent"):
        heading = f"Fidelity interpretation ({score}/10 — {tier})"
        panel_class = "kc-obs-interpret kc-interpret-solid"
    else:
        heading = f"Why is fidelity {score}/10?"
        panel_class = "kc-obs-interpret"
    drivers = interpretation.get("drivers") or []
    driver_items = "".join(f"<li>{d}</li>" for d in drivers[:4])
    drivers_block = f"<ul>{driver_items}</ul>" if driver_items else ""
    notes = interpretation.get("notes") or []
    notes_block = "".join(f'<p class="kc-obs-interpret-note">{n}</p>' for n in notes)
    return f"""
<details class="{panel_class}" open>
  <summary>{heading}</summary>
  <p>{interpretation.get('summary', '')}</p>{notes_block}{drivers_block}
</details>"""


def flux_observables_validation_table_html(rows: list[dict]) -> str:
    """HTML table: spin-only → SOC → experimental comparison."""
    if not rows:
        return ""

    body_rows: list[str] = []
    for row in rows:
        delta_class = _delta_cell_class(row["delta"])
        quality_tip = f"{row['quality']}: {row['note']}" if row.get("note") else row["quality"]
        source_tip = row.get("note", "")
        body_rows.append(
            f"""<tr>
  <td class="kc-obs-val-cat">{row["category"]}</td>
  <td>{row["model_spin_only"]}</td>
  <td>{row["model_soc"]}</td>
  <td>{row["experimental"]}</td>
  <td class="{delta_class}">{_delta_display(row["delta"])}</td>
  <td><span class="kc-obs-val-info" title="{source_tip}">{row["source"]}</span></td>
  <td class="kc-obs-val-quality"><span class="kc-obs-val-info" title="{quality_tip}">{row["quality"]}</span></td>
</tr>"""
        )

    return f"""
<div class="kc-obs-val-wrap">
  <details open>
  <summary>Model vs experiment ({len(rows)} observables)</summary>
  <table class="kc-obs-val-table">
    <thead><tr>
      <th>Category</th>
      <th>Spin-only / Model</th>
      <th>SOC</th>
      <th>Experimental</th>
      <th>Δ (model − exp)</th>
      <th>Source</th>
      <th>Quality</th>
    </tr></thead>
    <tbody>{"".join(body_rows)}</tbody>
  </table>
  </details>
</div>"""


def flux_observables_cards_html(extended: dict) -> str:
    """Laboratory observables + model alignment (Flux Flywheel secondary row)."""
    alignment = float(extended["model_vs_reality_alignment"])
    align_pct = max(0.0, min(100.0, alignment * 10.0))
    if alignment >= 8.0:
        fill_class = "kc-align-fill"
    elif alignment >= 6.0:
        fill_class = "kc-align-fill kc-align-mid"
    else:
        fill_class = "kc-align-fill kc-align-low"
    diamagnetic = extended["is_diamagnetic"]
    spin_label = "Diamagnetic" if diamagnetic else "Paramagnetic"
    delta_ie = float(extended.get("ie_delta_eV", 0.0))
    delta_pct = float(extended.get("ie_delta_pct", 0.0))
    delta_class = "kc-obs-delta-pos" if delta_ie >= 0 else "kc-obs-delta-neg"
    align_gap = float(extended.get("alignment_component_gap", 0.0))
    gap_class = "kc-obs-delta-pos" if align_gap >= 0 else "kc-obs-delta-neg"
    stab_pts = extended.get("alignment_stability_pts", "—")
    ie_pts = extended.get("alignment_ie_pts", "—")
    implied_ie = extended.get("ie_model_implied_eV", "—")
    heavy = extended.get("heavy_element_caveat", False)
    grid_class = "kc-observables-grid kc-obs-heavy" if heavy else "kc-observables-grid"
    heavy_note = ""
    if heavy:
        heavy_note = """
  <div class="kc-obs-heavy-note" title="Relativistic and many-body effects grow for heavy Z">
    Z ≥ 80: LS spin-only / Landé μ are illustrative — jj coupling and
    relativistic core contraction dominate; values are exploratory only.
  </div>"""

    align_tip = (
        "50% model stability (÷8) + 50% normalized real IE (÷25 eV). "
        f"Stability contributes {stab_pts} pts · IE contributes {ie_pts} pts."
    )
    mu_spin = extended.get("magnetic_moment_spin_only_BM", extended["magnetic_moment_BM"])
    mu_soc = extended.get("magnetic_moment_soc_BM", mu_spin)
    soc_applied = extended.get("spin_orbit_applied", False)
    g_j = extended.get("lande_g_J", 0)
    term = extended.get("ground_term_label", "")
    term_j = extended.get("ground_term_J", 0)
    mu_exp_available = extended.get("magnetic_moment_exp_available", False)
    mu_exp_display = extended.get("magnetic_moment_exp_display")
    mu_exp_source = extended.get("magnetic_moment_exp_source", "")
    mu_exp_notes = extended.get("magnetic_moment_exp_notes", "")
    mu_exp_quality = extended.get("magnetic_moment_exp_quality", "")
    mu_delta_soc = extended.get("mu_delta_soc_vs_exp_BM")
    mu_delta_spin = extended.get("mu_delta_spin_vs_exp_BM")
    mu_fidelity = extended.get("mu_validation_score")
    mu_in_range = extended.get("mu_within_exp_range")

    mu_stack_lines: list[str] = []
    if soc_applied and mu_soc != mu_spin:
        mu_stack_lines.append(
            f'<span class="kc-obs-delta kc-obs-delta-pos" '
            f'title="Landé g_J √(J(J+1)) with ground term {term}">'
            f"SOC μ = {mu_soc} BM (g_J={g_j}, J={term_j})</span>"
        )
    if mu_exp_available and mu_exp_display is not None:
        range_note = ""
        if mu_in_range is True:
            range_note = " · within experimental range"
        elif mu_in_range is False:
            range_note = " · outside quoted range"
        quality_tag = f" · {mu_exp_quality}" if mu_exp_quality else ""
        mu_stack_lines.append(
            f'<span class="kc-obs-delta" title="{mu_exp_notes} ({mu_exp_source})">'
            f"μ exp = {mu_exp_display} BM"
            f'<span class="kc-obs-exp-tag"> · {mu_exp_source}{quality_tag}</span></span>'
        )
        if mu_delta_soc is not None:
            soc_delta_class = (
                "kc-obs-delta-pos" if abs(mu_delta_soc) <= 0.5 else "kc-obs-delta-neg"
            )
            mu_stack_lines.append(
                f'<span class="kc-obs-delta {soc_delta_class}" '
                f'title="SOC model minus experimental midpoint{range_note}">'
                f"Δ SOC vs exp = {mu_delta_soc:+.2f} BM"
                f"{f' · fidelity {mu_fidelity}/10' if mu_fidelity is not None else ''}"
                f"</span>"
            )
        if mu_delta_spin is not None and mu_delta_spin != mu_delta_soc:
            mu_stack_lines.append(
                f'<span class="kc-obs-delta" title="Spin-only model minus experimental midpoint">'
                f"Δ spin-only vs exp = {mu_delta_spin:+.2f} BM</span>"
            )

    mu_stack = ""
    if mu_stack_lines:
        mu_stack = f"""
    <div class="kc-obs-mu-stack">{''.join(mu_stack_lines)}
    </div>"""

    exp_tip = ""
    if mu_exp_available:
        exp_tip = (
            f" Experimental μ = {mu_exp_display} BM ({mu_exp_source}; {mu_exp_notes})."
            f" Typical atomic-beam / Zeeman uncertainties are ±0.1–0.5 BM for 3d metals."
        )
    mu_tip = (
        f"Spin-only μ ≈ √(n(n+2)) = {mu_spin} BM. "
        + (
            f"SOC-corrected (LS): μ_eff = {mu_soc} BM via {term}, g_J={g_j}. "
            if soc_applied
            else "L=0 or closed shell — spin-only equals SOC. "
        )
        + exp_tip
        + " Free-atom LS coupling; jj coupling dominates for Z ≳ 80."
    )
    ie_tip = (
        f"Experimental first ionization energy ({extended['real_ionization_energy_eV']} eV). "
        f"Fidelity uses period-relative z-score ranking (stability vs IE within period), "
        f"not the absolute stability-derived proxy ({implied_ie} eV)."
    )

    z = int(extended.get("Z", 1))
    validation = build_observables_validation(z, extended)
    interpretation = interpret_comparison_fidelity(
        z,
        fidelity_score=validation["fidelity_score"],
        fidelity_details=validation["fidelity_details"],
        comparisons=validation["comparisons"],
        stability_score=float(extended["stability_score"]),
        is_noble_gas=bool(extended.get("is_noble_gas")),
        core_model_fidelity=validation.get("fidelity_core_score"),
        category_scores=validation.get("fidelity_category_scores"),
        category_details=validation.get("fidelity_category_details"),
    )
    interpretation["fidelity_score"] = validation["fidelity_score"]
    fidelity_card = flux_observables_fidelity_html({
        **extended,
        "comparison_fidelity_score": validation["fidelity_score"],
        "comparison_fidelity_core_score": validation.get("fidelity_core_score"),
        "comparison_fidelity_category_scores": validation.get("fidelity_category_scores", {}),
        "comparison_fidelity_category_details": validation.get("fidelity_category_details", {}),
        "comparison_fidelity_proxy_quality": validation.get("fidelity_proxy_quality", {}),
        "comparison_fidelity_details": validation["fidelity_details"],
        "comparison_fidelity_note": validation["fidelity_note"],
    }, interpretation=interpretation)
    interpretation_card = flux_observables_interpretation_html(interpretation)
    validation_table = flux_observables_validation_table_html(validation["rows"])
    noble_banner = ""
    if extended.get("is_noble_gas"):
        bonus = extended.get("noble_gas_stability_bonus", 0)
        _bonus_hint = (
            f" (+{bonus:.1f} stability bonus applied)"
            if bonus
            else ""
        )
        noble_banner = f"""
  <details class="kc-obs-noble-banner" data-kc-noble-z="{z}" open
    title="Closed-shell noble gas — stability bonus{_bonus_hint}">
    <summary>Noble Gas — Closed Shell Detected</summary>
    <div class="kc-obs-noble-banner-body">
      This element has a closed electron shell, which the model recognizes through a
      stability bonus{_bonus_hint}. However, alignment on Electronegativity and some
      other properties can still be modest for heavier noble gases (period 5+). This
      reflects a known limitation of stability-based proxies in this region.
    </div>
  </details>"""

    return f"""
<div class="{grid_class} kc-neon-plugin">{fidelity_card}{interpretation_card}{noble_banner}
  <div class="kc-metric-card">
    <span class="kc-obs-tip" title="Flux flywheel stability score (magic-island calibrated)">Model score</span>
    <strong>{extended["stability_score"]}</strong>
  </div>
  <div class="kc-metric-card">
    <span class="kc-obs-tip" title="{ie_tip}">Real IE (eV)</span>
    <strong>{extended["real_ionization_energy_eV"]}</strong>
    <span class="kc-obs-delta {delta_class}" title="Real IE minus model-implied IE from stability score">
      Δ {delta_ie:+.2f} eV ({delta_pct:+.1f}%)
    </span>
  </div>
  <div class="kc-metric-card">
    <span class="kc-obs-tip" title="Ground-state unpaired electrons (Aufbau + Hund, with known overrides)">Unpaired e⁻</span>
    <strong>{extended["unpaired_electrons"]}</strong>
  </div>
  <div class="kc-metric-card kc-obs-mu">
    <span class="kc-obs-tip" title="{mu_tip}">Magnetic moment (BM)</span>
    <strong>{mu_spin}</strong>
    <span class="kc-obs-caption">spin-only</span>{mu_stack}
  </div>
  <div class="kc-metric-card kc-obs-align">
    <span class="kc-obs-tip" title="{align_tip}">Alignment · {spin_label}</span>
    <div class="kc-obs-align-score">
      <strong>{alignment:.1f}</strong><small>/ 10</small>
    </div>
    <div class="kc-align-track" title="Alignment score: {alignment:.1f} / 10">
      <div class="{fill_class}" style="width:{align_pct:.0f}%"></div>
    </div>
    <span class="kc-obs-delta {gap_class}" title="Stability contribution minus IE contribution (alignment points)">
      Δ model vs IE: {align_gap:+.1f} pts
    </span>
    <span class="kc-obs-caption">{extended["validation_notes"]}</span>
  </div>{heavy_note}{validation_table}
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