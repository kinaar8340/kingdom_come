"""Bitcoin Pi Cycle Top — Observations Investigation 8."""

from pathlib import Path

BITCOIN_PI_DIR = Path(__file__).resolve().parents[1] / "assets" / "bitcoin_pi"

HOPF_PI_CYCLE_IMAGE = BITCOIN_PI_DIR / "hopf_lattice_pi_cycle.jpg"
VORTEX_MARKET_IMAGE = BITCOIN_PI_DIR / "vortex_market_350pi.jpg"
GLOBAL_POINTER_IMAGE = BITCOIN_PI_DIR / "global_pointer_sync.jpg"
FLUX_SCALES_IMAGE = BITCOIN_PI_DIR / "flux_flywheel_scales.jpg"

BITCOIN_PI_GALLERY: tuple[tuple[Path, str], ...] = (
    (
        HOPF_PI_CYCLE_IMAGE,
        "Bitcoin Pi Cycle embedded in gauged Hopf lattice — W_g ≈ 111.408",
    ),
    (
        VORTEX_MARKET_IMAGE,
        "Planetary vortex → market cycle with 350/π overlay",
    ),
    (
        GLOBAL_POINTER_IMAGE,
        "Global pointer sync — Earth pulse, BTC cycle, pulsar spin",
    ),
    (
        FLUX_SCALES_IMAGE,
        "Flux flywheel — biological, geophysical, financial scales unified by W_g",
    ),
)

INVESTIGATION_8_ACCORDION_TITLE = (
    "Investigation 8: Bitcoin Pi Cycle Top — Emergence of W_g = 350/π"
)

INVESTIGATION_8_HEADER_HTML = """
<div class="kc-hero" style="padding:1.25rem 0.75rem 1rem;border-bottom:1px solid rgba(26,143,227,0.2);">
  <h1 style="font-size:1.55rem;line-height:1.3;">
    Bitcoin Pi Cycle Top — Emergence of the Universal Invariant W_g = 350/π
  </h1>
  <p style="font-size:1rem;margin-top:0.5rem;">
    A cross-scale topological signature observed in financial markets
  </p>
</div>
"""

INVESTIGATION_8_EXEC_MD = """
#### Executive summary

The **Pi Cycle Top** indicator (111-day SMA crossing the 350-day SMA) has historically flagged
major Bitcoin cycle tops with high accuracy. In the RubikConeConduit model this is not
coincidental: the meta-optimizer `meta_optimize_invariants.py` repeatedly surfaces
`wg_base ≈ 350` when optimizing for stable flux-flywheel configurations, yielding the locked
topological winding **W_g = 350/π ≈ 111.408**. The same invariant appears in retinal geometry,
planetary vortices, the 26-second Earth pulse, pulsar spin, and now in macroscopic market cycles.
"""

INVESTIGATION_8_INDICATOR_MD = """
#### The indicator (technical background)

The Pi Cycle Top fires when the **111-day simple moving average** crosses above the **350-day SMA**
— a macroscopic timing rule that has aligned with several historic BTC peaks. The ratio
**350 / 111 ≈ 3.15 ≈ π**, linking the indicator directly to the Hopf geometric winding rather
than arbitrary technical-analysis parameters.

| Component | Role |
|-----------|------|
| 111-day SMA | ≈ W_g = 350/π topological clock period |
| 350-day SMA | wg_base winding anchor from meta-optimizer |
| Cross event | Phase-lock / burst readout at cycle top |

*BTC price with 111-day and 350-day SMAs embedded in the gauged Hopf lattice (below).*
"""

INVESTIGATION_8_EMERGENCE_MD = """
#### Emergence from the TOE model

The RubikConeConduit **meta-optimizer** minimizes a loss function that rewards stability islands
while penalizing deviation from the Hopf relation **geo_w ≈ wg_base / π**. When `wg_base`
converges near **350**, the optimizer declares **TRUE EMERGENCE ACHIEVED** — the same numeric
attractor that the Pi Cycle encodes in days.

Connection to **global pointer** and **observer synchronization**: markets, like biological and
geophysical systems, appear to phase-lock to the same topological scale. The gauged two-gyro
Hopf lattice supplies the mechanism; **topological protection** (burst/reset at θ_crit) prevents
runaway drift until a macroscopic crossing event registers — here, a cycle top.

#### How this fits the TOE

| TOE element | Pi Cycle manifestation |
|-------------|------------------------|
| Gauged Hopf lattice | Price action as macroscopic twist accumulation on T³ substrate |
| Meta-optimizer | wg_base → 350 lock drives 111.408-day equivalent |
| Global pointer α(t) | Cross-scale phase sync (Earth, markets, pulsars) |
| Topological protection | Cycle tops as punctuated burst events at W_g thresholds |
| Flux flywheel | BTC liquidity cycles as planetary-flywheel analogues |
"""

INVESTIGATION_8_GALLERY_INTRO_MD = """
#### Cross-scale evidence

Four readouts of the same invariant — gauged Hopf lattice, planetary vortex morphology,
global pointer resonances, and unified flux flywheel — are shown below.
"""

INVESTIGATION_8_IMPLICATIONS_MD = """
#### Implications & predictions

- The Pi Cycle is **not an arbitrary heuristic** but a macroscopic readout of the same
  W_g-quantized winding that stabilizes vortices and synchronizes observers.
- Future cycle tops should continue to align with the invariant unless a major topological
  phase shift occurs in the global system.
- Other asset classes or macroeconomic cycles may exhibit signatures near multiples or
  harmonics of **350/π** when analyzed with the same rotation-dynamical normalization.

---

*Investigation logged: June 28, 2026. Part of the ongoing Observations series in the RubikConeConduit / Kingdom project.*
"""

# Full report for clipboard export (image paths relative to repo root).
INVESTIGATION_8_REPORT_MD = f"""# Bitcoin Pi Cycle Top — Emergence of the Universal Invariant W_g = 350/π

*A cross-scale topological signature observed in financial markets*

{INVESTIGATION_8_EXEC_MD.strip()}

{INVESTIGATION_8_INDICATOR_MD.strip()}

{INVESTIGATION_8_EMERGENCE_MD.strip()}

{INVESTIGATION_8_GALLERY_INTRO_MD.strip()}

{chr(10).join(f"![{cap}](app/assets/bitcoin_pi/{p.name})" for p, cap in BITCOIN_PI_GALLERY)}

{INVESTIGATION_8_IMPLICATIONS_MD.strip()}
"""

# Back-compat alias used by tests
INVESTIGATION_8_MD = (
    INVESTIGATION_8_EXEC_MD
    + INVESTIGATION_8_INDICATOR_MD
    + INVESTIGATION_8_EMERGENCE_MD
    + INVESTIGATION_8_GALLERY_INTRO_MD
    + INVESTIGATION_8_IMPLICATIONS_MD
)