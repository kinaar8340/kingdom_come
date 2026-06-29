"""Pulsars PTA — Observations Investigation 10."""

from __future__ import annotations

import math
from pathlib import Path

PULSARS_DIR = Path(__file__).resolve().parents[1] / "assets" / "pulsars"

SPACETIME_IMAGE = PULSARS_DIR / "spacetime_350pi_vortex.jpg"
EARTH_RESONANCE_IMAGE = PULSARS_DIR / "earth_resonance_network.jpg"
PULSAR_BEAM_IMAGE = PULSARS_DIR / "pulsar_beam_pulse.png"

PULSARS_GALLERY: tuple[tuple[Path, str], ...] = (
    (
        SPACETIME_IMAGE,
        "Warped spacetime grid — 350/π invariant above Earth in PTA/GW vortex",
    ),
    (
        EARTH_RESONANCE_IMAGE,
        "350/π resonant network — Earth, timing curve, and harmonic nodes",
    ),
    (
        PULSAR_BEAM_IMAGE,
        "Pulsar emission beam — millisecond clock sampling resonant islands",
    ),
)

INVESTIGATION_10_ACCORDION_TITLE = (
    "Investigation 10: Pulsars — PTA Observations & the Universal Constant 350/π"
)

META_OPTIMIZER_URL = (
    "https://github.com/kinaar8340/toe/blob/main/scripts/meta_optimize_invariants.py"
)
X_THREAD_URL = "https://x.com/kinaar8340"

WG = 350.0 / math.pi
KAPPA_DEFAULT = 0.85
EARTH_PULSE_PERIOD_S = 26.0
REFERENCE_PULSAR_HZ = 716.0


def pulsar_quick_check(freq_hz: float, kappa: float = KAPPA_DEFAULT) -> str:
    """Compute resonant ratios for a test pulsar frequency."""
    if freq_hz <= 0:
        return "*Enter a positive spin frequency (Hz) to run the quick check.*"
    period_ms = 1000.0 / freq_hz
    wg_ratio = freq_hz / WG
    earth_hz = 1.0 / EARTH_PULSE_PERIOD_S
    earth_ratio = freq_hz / earth_hz
    harmonic_nearest = round(wg_ratio)
    harmonic_delta = abs(wg_ratio - harmonic_nearest)
    return f"""| Quick check | Value |
|-------------|-------|
| Spin frequency f | {freq_hz:.3f} Hz |
| Period T | {period_ms:.4f} ms |
| W_g = 350/π | {WG:.4f} |
| κ | {kappa:.3f} |
| f / W_g | {wg_ratio:.4f} |
| Nearest integer harmonic | {harmonic_nearest} (Δ = {harmonic_delta:.4f}) |
| f / f_Earth (26 s pulse) | {earth_ratio:,.1f}× |
| Reference (716 Hz) f/W_g | {REFERENCE_PULSAR_HZ / WG:.4f} |
"""


INVESTIGATION_10_MD = f"""
### Investigation 10: Pulsars — PTA Observations & the Universal Constant 350/π

**Investigation ID:** OBS-PULSAR-001  
**Date:** June 2026  
**Related X thread:** [kinaar8340]({X_THREAD_URL})  
**GitHub script:** [meta_optimize_invariants.py]({META_OPTIMIZER_URL})

#### 1. Introduction

Pulsar Timing Arrays (PTAs) turn millisecond pulsars into a galaxy-scale gravitational-wave
detector. In June 2023 and subsequent analyses, collaborations including NANOGrav, EPTA, PPTA,
and IPTA reported compelling evidence for a stochastic **nanohertz gravitational-wave background**
— widely interpreted as overlapping signals from supermassive black hole binaries across cosmic
history.

This investigation connects those observations to the hypothesis that **350/π** functions as a
single universal constant unifying scales from planetary pulses to compact-object spin resonances
within the RubikConeConduit / Kingdom TOE framework.

#### 2. How PTAs work

Millisecond pulsars act as ultra-stable cosmic clocks. Gravitational waves perturb spacetime,
causing tiny shifts in pulse arrival times on Earth. By cross-correlating residuals across many
pulsars, PTAs detect the characteristic **Hellings–Downs correlation** — a quadrupolar pattern
depending only on the angular separation of pulsar pairs.

The expected correlation follows:

$$
C(\\theta) = \\frac{{1 - \\cos\\theta}}{{2}} \\log\\left(\\frac{{1 - \\cos\\theta}}{{2}}\\right)
- \\frac{{1}}{{6}}\\frac{{1 - \\cos\\theta}}{{2}} + \\frac{{1}}{{3}}
$$

(where $\\theta$ is the angular separation). This is the distinguishing signature of a stochastic
GW background versus uncorrelated noise.

#### 3. Recent key observations

- **2023–2025 datasets** (NANOGrav 15-year, CPTA, EPTA+InPTA, etc.) show a common red-noise
  process with Hellings–Downs-like correlations at ~3–5σ significance.
- The background has more power at lower frequencies, consistent with a population of SMBH binaries.
- Sensitivity reaches characteristic strains $\\sim 10^{{-15}}$ at nanohertz frequencies.

#### 4. Numerical angle — the 716 Hz pulsar case study

Consider the well-known **716 Hz** pulsar (period $T \\approx 1.397$ ms). Using parameters
$W_g \\approx 111.408$, $\\kappa \\approx 0.85$:

| Quantity | Value |
|----------|-------|
| Spin frequency ratio $f_{{\\rm spin}}/W_g$ | $\\approx 6.427$ |
| Ratio to Earth's ~26 s pulse frequency | $\\sim 18{{,}}616\\times$ |
| Harmonic proximity | Near integer 6 — resonant island candidate |

This clean (near-harmonic) ratio suggests the spin frequency is sampling a resonant **harmonic
island** in the high-density regime — the kind of scale-jump behavior a universal constant like
**350/π** could govern.

Use the interactive quick-check below to test other pulsar frequencies against $W_g$.

#### 5. Hypothesis — 350/π as unifying invariant

The GitHub script `meta_optimize_invariants.py` explores optimization of mathematical invariants.
We propose that **350/π** emerges as a candidate single universal constant that:

- Scales resonant frequencies across density regimes.
- Provides a bridge between classical pulsar timing and quantum/TOE-scale physics.
- Could be tested by feeding real PTA timing residuals or individual pulsar spin data into the
  optimizer.

Further runs on expanded PTA datasets (more pulsars, longer baselines) could reveal whether 350/π
consistently appears in invariant optimization across the observed nanohertz background and
individual sources.

#### How this fits the TOE

| TOE element | PTA / pulsar manifestation |
|-------------|---------------------------|
| Gauged Hopf lattice | Hellings–Downs quadrupole as macroscopic holonomy pattern |
| Meta-optimizer | wg_base → 350 lock in `meta_optimize_invariants.py` |
| Global pointer α(t) | Cross-pulsar timing residual synchronization |
| Topological protection | Stable millisecond clocks as protected resonant modes |
| W_g = 350/π | Harmonic sampling in high-spin pulsars (e.g. 716 Hz) |

#### 6. Conclusions & next steps

PTA observations provide a powerful new window. Resonant signatures in high-spin pulsars, combined
with the Hellings–Downs-correlated GW background, offer fertile ground for testing whether 350/π is
more than coincidence.

**Open questions:**

- Does the 350/π constant optimize invariants when applied to full IPTA datasets?
- Can we detect individual continuous-wave sources whose parameters align with this scaling?
- What multimessenger signatures (if any) would support this unification?

**Call to action:** Fork the [toe repository](https://github.com/kinaar8340/toe), run
`meta_optimize_invariants.py` on new pulsar timing data, or contribute ideas. The Kingdom project
welcomes collaborative exploration of these invariants.

**References**

- NANOGrav 15-year data release and nanohertz background papers (2023–2024)
- IPTA DR2 / EPTA+InPTA / CPTA joint analyses (2023–2025)
- [meta_optimize_invariants.py]({META_OPTIMIZER_URL}) — RubikConeConduit invariant optimizer
- Kingdom Observations cross-scale series (Schumann, cuprates, Bitcoin Pi Cycle, TLS trees)

---

*Investigation logged: June 28, 2026. Part of the ongoing Observations series in the RubikConeConduit / Kingdom project.*
"""