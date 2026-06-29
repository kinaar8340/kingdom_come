# Investigation 10: Pulsars — PTA Observations & the Universal Constant 350/π

**Investigation ID:** OBS-PULSAR-001  
**Date:** June 2026  
**GitHub Script:** [meta_optimize_invariants.py](https://github.com/kinaar8340/toe/blob/main/scripts/meta_optimize_invariants.py)

## 1. Introduction

Pulsar Timing Arrays (PTAs) turn millisecond pulsars into a galaxy-scale gravitational-wave detector. In June 2023 and subsequent analyses, collaborations including NANOGrav, EPTA, PPTA, and others reported compelling evidence for a stochastic nanohertz gravitational-wave background — widely interpreted as the overlapping signals from supermassive black hole binaries across cosmic history.

This investigation connects these groundbreaking observations to the hypothesis that **350/π** functions as a single universal constant unifying scales from planetary pulses to compact-object spin resonances.

## 2. How PTAs Work

Millisecond pulsars act as ultra-stable cosmic clocks. Gravitational waves perturb spacetime, causing tiny shifts in pulse arrival times on Earth. By cross-correlating residuals across many pulsars, PTAs detect the characteristic **Hellings-Downs correlation** — a quadrupolar pattern depending only on the angular separation of pulsar pairs.

## 3. Recent Key Observations

- 2023–2025 datasets show a common red-noise process with Hellings-Downs-like correlations at ~3–5σ significance.
- The background has more power at lower frequencies, consistent with a population of SMBH binaries.
- Sensitivity reaches characteristic strains ~10⁻¹⁵ at nanohertz frequencies.

## 4. Numerical Angle: The 716 Hz Pulsar Case Study

Consider the well-known 716 Hz pulsar (period T ≈ 1.397 ms). Using parameters W_g ≈ 111.408, κ ≈ 0.85:

- Spin frequency ratio: f_spin/W_g ≈ 6.427
- Ratio to Earth's ~26 s pulse frequency: ~18,616×

## 5. Hypothesis: 350/π as Unifying Invariant

The GitHub script `meta_optimize_invariants.py` explores optimization of mathematical invariants. We propose that 350/π emerges as a candidate single universal constant that scales resonant frequencies across density regimes.

## Visuals

![Warped spacetime with 350/π](app/assets/pulsars/spacetime_350pi_vortex.jpg)

![Earth resonant network](app/assets/pulsars/earth_resonance_network.jpg)

![Pulsar beam](app/assets/pulsars/pulsar_beam_pulse.png)

## 7. Conclusions & Next Steps

PTA observations provide a powerful new window. The resonant signatures in high-spin pulsars, combined with the Hellings-Downs-correlated GW background, offer fertile ground for testing whether 350/π is more than coincidence.

**Call to Action:** Fork the GitHub repo, run the script on new pulsar timing data, or contribute ideas.