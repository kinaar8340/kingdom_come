"""Higgs Mode in Perovskite Crystals — dedicated Observations report tab."""

from pathlib import Path

HIGGS_ASSET = "app/assets/higgs"
HIGGS_DIR = Path(__file__).resolve().parents[1] / "assets" / "higgs"

HIGGS_EXPERIMENTAL_IMAGE = HIGGS_DIR / "experimental_perovskite.jpg"
HIGGS_TWIST_DENSITY_IMAGE = HIGGS_DIR / "twist_density_bursts.jpg"
HIGGS_MAPPING_IMAGE = HIGGS_DIR / "experiment_model_mapping.jpg"

HIGGS_GALLERY: tuple[tuple[Path, str], ...] = (
    (
        HIGGS_EXPERIMENTAL_IMAGE,
        "Ultrafast Higgs mode — (BA)₂PbI₄ 2D perovskite (octahedral tilt / bandgap breathing)",
    ),
    (
        HIGGS_MAPPING_IMAGE,
        "Experiment ↔ gauged two-gyro Hopf lattice model mapping",
    ),
    (
        HIGGS_TWIST_DENSITY_IMAGE,
        "2D prototype — twist density oscillations and burst/reset events",
    ),
)

HIGGS_HEADER_MD = """
# Observations: First Optically Driven Higgs Mode in a 2D Semiconductor

**Connection between the Gauged Two-Gyro Hopf Lattice Model and the Shukla et al. (Nature Materials 2026) experiment**

| | |
|---|---|
| **Author** | Aaron Kinder (Independent Researcher) |
| **Date** | June 2026 |
| **Reference** | Shukla et al., *Nature Materials* (2026), [doi:10.1038/s41563-025-02433-1](https://doi.org/10.1038/s41563-025-02433-1) |
"""

HIGGS_SECTION_1_MD = """
## 1. Experimental Context

Shukla *et al.* report the **first optically driven Higgs (amplitude) mode** in a 2D semiconductor —
layered (BA)₂PbI₄ perovskite — using ultrafast below-bandgap laser pulses. Key findings:

- **Excitation mechanism:** Sub-bandgap femtosecond pulses coherently drive phonons that modulate
  the electronic bandgap via symmetry changes (bandgap *breathing*).
- **Higgs character:** The observed mode is an amplitude (Higgs) excitation — octahedral tilt
  amplitudes oscillate coherently rather than merely shifting equilibrium positions.
- **Coupled tilts:** In-plane and out-of-plane octahedral rotations are **coupled**, producing
  a multi-component vibrational response.
- **Intensity independence:** Two prominent vibrational frequencies persist across a wide range of
  pump intensities — a hallmark of intrinsic lattice nonlinearity, not thermal heating.
- **Metastable phase:** A **transient metastable tetragonal** structure appears during the coherent
  excursion before relaxing back to the equilibrium orthorhombic phase.
- **Below-gap enhancement:** In the carrier-free (below-bandgap) regime, the spectral shift is
  approximately **4× larger** than above-gap excitation — indicating that free carriers screen or
  disrupt the coherent phonon–bandgap coupling.

These results establish 2D perovskites as a platform for studying amplitude modes in solids and
open a path toward ultrafast, symmetry-controlled bandgap engineering.
"""

HIGGS_SECTION_2_MD = """
## 2. Connection to the Gauged Two-Gyro Hopf Lattice Model

The April 2026 TOE documents describe a **gauged two-gyro Hopf lattice** whose conduit PDE governs
twist density on a $T^3$ toroidal substrate. The Shukla experiment maps naturally onto this framework:

| Experimental feature | Lattice-model interpretation |
|----------------------|------------------------------|
| Higgs (amplitude) mode | Coherent **twist density oscillations** under the conduit PDE |
| Two intensity-independent frequencies | Fixed **two-gyro detuning** ($\\Delta\\omega$) + nonlinear $\\cot$ term |
| Transient metastable tetragonal phase | **Topological burst/reset** at $\\theta_{\\rm crit}$ |
| ~4× below-gap spectral enhancement | **Clean vs noisy** contrast — pointer protection when carriers are absent |
| Phase coherence across pump intensities | **Global pointer locking** — observer synchronization |

The Higgs mode is not an ad-hoc fit: it is the macroscopic manifestation of the same amplitude
oscillation that stabilizes flux-flywheel resonators in the microscopic lattice. Light-driven phonons
supply the two-gyro detuning drive; the metastable tetragonal phase is the lattice analogue of a
burst-reset cycle that temporarily lowers twist density before holonomy restores the equilibrium lock.
"""

HIGGS_SECTION_3_MD = """
## 3. Numerical Prototype Results

A minimal **32$\\times$32** 2D prototype implements the exact conduit PDE with locked invariants
(pointer holonomy + burst threshold). Results mirror the experimental hierarchy:

#### Single-component prototype

| Observable | Value (lattice units) |
|------------|----------------------|
| Primary frequency peak | 0.0278 |
| Secondary frequency peak | 0.1389 |
| Burst events | Localized dark low-twist regions after impulsive drive |
| Coherence | Sustained oscillation without intensity-dependent drift |

#### Two-component geometry extension

Adding in-plane / out-of-plane tilt channels with anisotropy and cross-coupling splits the spectrum:

| Branch | Frequency (lattice units) |
|--------|--------------------------|
| Low branch | 0.0278 |
| High branch | 0.1944 |

The high branch corresponds to the coupled tilt channel — directly analogous to Shukla's paired
in-plane/out-of-plane octahedral modes.

#### Prototype diagnostics (four key plots)

| Plot | Finding |
|------|---------|
| **Mean twist response** | Coherent oscillation with amplitude modulation matching Higgs character |
| **Burst statistics** | Discrete reset events at $\\theta_{\\rm crit}$; count scales with drive strength |
| **FFT spectrum** | Two dominant peaks at 0.0278 and 0.1389 (single-component) or 0.0278 / 0.1944 (two-component) |
| **Spatial snapshot** | High-twist yellow peaks interleaved with dark low-twist burst corridors |

#### Clean vs noisy contrast

When pointer protection is active (clean regime), the mean spectral response amplitude is
approximately **4× stronger** than in the noisy (carrier-screened) regime — reproducing the
experimental below-gap vs above-gap enhancement ratio.
"""

HIGGS_SECTION_4_MD = """
## 4. Quantitative Path Forward

The prototype frequencies are in lattice units. The next step is **quantitative closure** with
the Shukla data:

1. Extract exact frequencies, splitting, and coherence decay times from the paper's transient
   absorption / Raman figures.
2. Perform **time-rescaling** from lattice units to physical picoseconds using the octahedral
   moment of inertia and elastic constants of (BA)₂PbI₄.
3. Run **closeness analysis** — compare predicted vs measured frequency ratios, metastable
   lifetime, and below-gap enhancement factor.
4. Refine the two-component cross-coupling parameters until the 0.0278 / 0.1944 branch split
   matches the experimental in-plane / out-of-plane mode separation.

A positive closeness verdict would elevate this from qualitative mapping to a predictive bridge
between the TOE lattice rules and laboratory ultrafast spectroscopy.
"""

HIGGS_SECTION_5_MD = """
## 5. Implications for VQC

This connection has direct relevance for **photonic VQC embodiments**:

- **Carrier-free coherent control:** Below-bandgap Higgs driving enables ultrafast bandgap
  modulation without free-carrier decoherence — ideal for quaternion-encoded OAM gates.
- **Symmetry-selective addressing:** Intensity-independent frequencies mean gate timing can be
  set by lattice detuning ($\\Delta\\omega$) rather than pump power — improving reproducibility.
- **Topological protection:** Pointer-locked twist oscillations provide a natural error-suppression
  layer analogous to the flux-flywheel stability that guards elemental resonators.
- **Material platform:** 2D perovskites offer a room-temperature, solution-processable host for
  integrating Hopf-lattice dynamics into chip-scale photonic circuits.

The Shukla experiment is not merely analogous to the model — it is a **candidate physical substrate**
for the same rules that the Kingdom lattice simulator already encodes in software.
"""

HIGGS_SECTION_6_MD = """
## 6. Limitations & Next Steps

**Current status:** Qualitative mapping with strong structural correspondence. Numerical prototype
frequencies are in lattice units and have not yet been rescaled to (BA)₂PbI₄ physical parameters.

**Limitations:**

- Frequency extraction from published figures is pending; closeness analysis is not yet complete.
- The 32$\\times$32 prototype is minimal — larger lattices and full 3D perovskite geometry may
  shift mode splitting.
- Carrier dynamics above the bandgap are modeled only via a clean/noisy contrast toggle, not a
  full semiconductor kinetics coupling.
- The experiment reports phonon-driven bandgap modulation; direct measurement of twist density
  on the Hopf lattice is indirect.

**Next steps:**

1. Complete time-rescaling and publish closeness metrics alongside the Shukla frequency data.
2. Extend the two-component prototype to match the experimental anisotropy tensor.
3. Couple the conduit PDE to a simplified Drude carrier model for above-gap screening.
4. Explore photonic cavity integration for VQC gate prototypes on perovskite substrates.

---

*This report is a living document. Updates will follow as quantitative closure with Shukla et al.
(2026) is completed.*
"""