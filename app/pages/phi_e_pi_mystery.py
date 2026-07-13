"""The φ-e-π Emergent Signature Mystery — Observations Investigation 6."""

from pathlib import Path

from kingdom.core.constants import DEFAULT_KAPPA, E, E_INV2, PHI, PI, R_RESIDUAL

MYSTERY_DIR = Path(__file__).resolve().parents[1] / "assets" / "mystery"
MYSTERY_REPO = "https://github.com/kinaar8340/mystery"
CORE_REPO = "https://github.com/kinaar8340/flux_hopf_lib"

PHI_TRIANGLE_IMAGE = MYSTERY_DIR / "phi_triangle.jpg"
PHI_VORTEX_IMAGE = MYSTERY_DIR / "phi_vortex_369.jpg"
PHI_BANNER_IMAGE = MYSTERY_DIR / "phi_overview_banner.jpg"

_R_FMT = f"{R_RESIDUAL:+.6f}"
_PHI_FMT = f"{PHI:.10f}"
_E_FMT = f"{E:.11f}"
_PI_FMT = f"{PI:.11f}"
_KAPPA_FMT = f"{DEFAULT_KAPPA:.2f}"
_E_OVER_PI = f"{(E / PI):.3f}"
_E_INV2_FMT = f"{E_INV2:.6f}"

PHI_E_PI_GALLERY: tuple[tuple[Path, str], ...] = (
    (
        PHI_TRIANGLE_IMAGE,
        f"Approximate φ-e-π right triangle — residual R ≈ {_R_FMT}",
    ),
    (
        PHI_VORTEX_IMAGE,
        "Vortex mathematics — 3-6-9 mapping (angles ÷ 10°)",
    ),
    (
        PHI_BANNER_IMAGE,
        "Emergent signature — gauged Hopf lattice field (φ, e, π fibers)",
    ),
)

INVESTIGATION_6_ACCORDION_TITLE = (
    "Investigation 6: The φ-e-π Emergent Signature Mystery"
)

INVESTIGATION_6_MD = rf"""
### Investigation 6: The φ-e-π Emergent Signature Mystery

**Source:** [github.com/kinaar8340/mystery](https://github.com/kinaar8340/mystery) ·
**Core constants:** [flux_hopf_lib]({CORE_REPO}) ·
**Status:** Active computational exploration (no claim of exact identity)

Three fundamental constants from different mathematical families exhibit a striking
near-alignment:

**$\phi^2 + e^2 \approx \pi^2$**

where $\phi$ (golden ratio) $\approx$ {_PHI_FMT}, $e$ (Euler's number) $\approx$ {_E_FMT}, and
$\pi \approx$ {_PI_FMT}.

High-precision computation yields a small residual **$R = \phi^2 + e^2 - \pi^2 \approx {_R_FMT}$**
(relative error ≈ 1.39%). This is **not** a forced mathematical identity, yet close
enough to be considered a *compatible emergent signature*.

#### Geometric resonance

Treating $\phi$ and $e$ as legs of a triangle with hypotenuse $\pi$ produces angles remarkably close
to a 30°-60°-90° triangle:

| Leg | Angle |
|-----|-------|
| $\phi$ | $\approx$ 31.0° |
| $e$ | $\approx$ 59.9° |
| $\pi$ (hypotenuse) | $\approx$ 89.1° |

This near-right triangle suggests emergent geometric harmony rather than pure coincidence.

#### Vortex mathematics & 3-6-9 connection

Scaling the angles by dividing by 10° maps them to ≈ **3.10**, **5.99**, **8.91** — sitting
extremely close to the sacred numbers **3, 6, 9** central to vortex math and Tesla-inspired
geometries. This hints at deeper harmonic or topological resonance.

#### Framework: gauged Hopf lattices & proposed TOE

The signature is explored within the **gauged Hopf lattice** model (broader TOE exploration):

| Observation | Detail |
|-------------|--------|
| Coupling κ | $\approx$ {_KAPPA_FMT} (very close to $e/\pi \approx$ {_E_OVER_PI}) |
| Survival analog | $e^{{-2}} \approx$ {_E_INV2_FMT} at $\lambda t = 2$ |
| PDE simulations | Relaxation preserves topology; non-random FFT content |
| Optimization sweeps | Residual proximity stable but not exact |
| Rodin mod-9 mapping | Doubling cycles on Hopf fiber phase advances — topological cipher candidate |

#### Computational probes performed

Multiple rigorous scripts in the mystery repo:

- Triangle & angle analysis
- Hopf constant bridging
- Vortex 369 clock geometry
- Residual bounding & κ sweeps
- PDE evolution with Hopfion/helical seeds
- Meta-optimization

All probes support the observation as **consistent and worthy of further study**.

#### Assessment & open questions

- The alignment is **quantified and reproducible** but not mathematically forced.
- It may reflect deeper structure through advanced geometric/topological lenses.
- **Next steps:** extended PDE runs, formal residual bounds, Rodin–Hopf mapping tests.

**References & full probes:** [kinaar8340/mystery](https://github.com/kinaar8340/mystery)

**Status:** Open, active investigation.
"""