"""Neon glow CSS plugin for Kingdom Come badges and highlights."""

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
  padding: 1.1rem 1.25rem;
  margin: 0.75rem 0;
}
.kc-element-card h2 {
  margin: 0 0 0.35rem;
  font-size: 1.6rem;
  color: #e8f4ff;
}
.kc-element-symbol {
  font-size: 2.4rem;
  font-weight: 700;
  color: #00c9b7;
  text-shadow: 0 0 12px rgba(0, 201, 183, 0.5);
  margin-right: 0.5rem;
}
.kc-element-meta {
  color: #8ecae6;
  font-size: 0.9rem;
  line-height: 1.5;
}
.kc-element-toe {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(26, 143, 227, 0.2);
  color: #d4e4f7;
  font-size: 0.88rem;
}
.kc-toe-narrative {
  color: #c9a227;
  font-style: italic;
  font-size: 0.95rem;
  line-height: 1.45;
}
.kc-synthetic-banner {
  color: #ef553b;
  font-weight: 600;
  font-size: 0.9rem;
}
@keyframes kc-neon-pulse {
  0%, 100% { box-shadow: 0 0 6px rgba(0,201,183,0.5), 0 0 14px rgba(26,143,227,0.3); }
  50% { box-shadow: 0 0 12px rgba(0,201,183,0.85), 0 0 22px rgba(26,143,227,0.5); }
}
"""


def element_card_html(element, flywheel: dict) -> str:
    """Render element info card with neon badges."""
    badges = []
    if element.is_noble_gas:
        badges.append('<span class="kc-neon-noble">✦ NOBLE GAS · FLUX FLYWHEEL LOCK</span>')
    if element.is_magic_number:
        badges.append('<span class="kc-neon-magic">Magic number</span>')
    badge_row = " ".join(badges)

    return f"""
<div class="kc-element-card">
  <div>
    <span class="kc-element-symbol">{element.symbol}</span>
    <h2>{element.name}</h2>
  </div>
  <div style="margin:0.5rem 0">{badge_row}</div>
  <div class="kc-element-meta">
    <strong>Z</strong> = {element.z} &nbsp;·&nbsp;
    Period {element.period} &nbsp;·&nbsp;
    Group {element.group if element.group else "—"} &nbsp;·&nbsp;
    {element.category.title()}<br/>
    <strong>e⁻ config:</strong> {element.electron_config}
  </div>
  <div class="kc-element-toe">
    <em class="kc-toe-narrative">{element.toe_narrative}</em><br/><br/>
    <strong>TOE interpretation:</strong> {element.toe_stability_note}<br/>
    <strong>Flywheel class:</strong> {flywheel["stability_class"]}
    (score {flywheel["stability_score"]})<br/>
    <strong>δω</strong> = {flywheel["delta_omega"]} &nbsp;·&nbsp;
    gauge = {flywheel["gauge_strength"]}
  </div>
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
            "<br/><strong>pseudo_Z = 129</strong> is the Magic Island sweep discovery ID "
            "(not a real element). Use Z = 2 for the physical noble-gas anchor."
        )
    return f"""
<div class="kc-element-card">
  <h2>Z = {z}</h2>
  <p class="kc-synthetic-banner">{label}</p>
  <div class="kc-element-meta">
    No standard periodic-table entry (Z &gt; 118 or &lt; 1).
    Flux flywheel model applies as a <em>theoretical</em> stability probe.{extra}
  </div>
  <div class="kc-element-toe">
    <strong>Flywheel class:</strong> {flywheel["stability_class"]}
    (score {flywheel["stability_score"]})
  </div>
</div>
"""