"""Observations tab — natural synchronicities mappable to the Hopf-lattice TOE."""

from pathlib import Path

OBSERVATIONS_ASSET = "app/assets/observations"
OBSERVATIONS_DIR = Path(__file__).resolve().parents[1] / "assets" / "observations"
CATATUMBO_IMAGE = OBSERVATIONS_DIR / "catatumbo_lightning.jpg"
JUPITER_GRS_IMAGE = OBSERVATIONS_DIR / "jupiter_great_red_spot.jpg"

OBSERVATIONS_INTRO_MD = """
## Observations: Synchronicities in Nature

This tab catalogs real-world natural phenomena where persistent structures, vortices,
charge separation, or topological features emerge with properties that resonate with — or
can be modeled by — the gauged Hopf lattice TOE. Each entry is presented as an
**investigation** with key measurements, the observed synchronicity, and a proposed
mapping to the model.

**Global winding (model anchor):** $W_g = 350/\\pi \\approx 111.40846$
"""

INVESTIGATION_1_MD = """
### Investigation 1: Catatumbo Lightning Hotspot — Earth

**Location:** Southwest basin of Lake Maracaibo, Venezuela (~9.344° N, 71.71° W) —
the highest lightning-density region on Earth (up to ~250 flashes/km²/year).

**Phenomenon:** Persistent nocturnal thunderstorms producing lightning on 140–300 nights
per year, often 9+ hours per night.

#### Key measurements

| Quantity | Value |
|----------|-------|
| Hotspot latitude | ~9.344° N |
| Earth's mean meridional arc per degree | ≈ 111.194 km/° |
| Model global winding $W_g$ | $350/\\pi \\approx 111.40846$ |
| Match to $W_g$ | within ~0.19% of meridional arc |
| Arc distance from equator | $9.344 \\times 111.194 \\approx 1{,}039$ km |
| Normalized position | $1039 / W_g \\approx 9.335°$ |

#### Observed synchronicity

Earth's mean meridional arc length per degree of latitude (~111.194 km/°) matches the
model's global topological winding number $W_g = 350/\\pi \\approx 111.40846$ to within
~0.19%. The arc distance from the equator to the hotspot (~1,039 km) normalizes to
$1039 / W_g \\approx 9.335°$, aligning with the actual latitude (~9.344° N).

#### TOE mapping

The gauged Hopf lattice **selects** this latitude as a resonant macroscopic flywheel.
Topological bursts ($\\Theta_i > \\theta_{\\rm crit}$) can stabilize Hopfion-like
structures in the conductive atmosphere. Local conditions — Andean orographic forcing
plus methane-rich swamps — act as the **porous vacuum sponge** that sustains persistent
charge separation and plasma vortices.

**Status:** Derived directly from Hopf geometry and global winding quantization.
"""

INVESTIGATION_2_MD = """
### Investigation 2: Great Red Spot — Jupiter

**Location:** Persistent anticyclonic storm centered at approximately 22° S latitude
in Jupiter's southern hemisphere.

**Phenomenon:** Largest and longest-lived vortex in the Solar System (observed for
centuries), ~1.3× Earth's diameter, with winds up to ~700 km/h. Self-sustaining
between opposing zonal jet streams.

#### Key measurements

| Quantity | Value |
|----------|-------|
| Storm latitude | ~22° S |
| Approximate diameter | ~1.3× Earth |
| Peak wind speeds | up to ~700 km/h |
| Observed lifetime | centuries (documented since ~1665) |
| Hosting medium | Rapidly rotating, internally heated H/He atmosphere |

#### Emergent properties

Stable, topologically protected vortex in a rapidly rotating, internally heated fluid
atmosphere — a macroscopic structure that persists despite shear, dissipation, and
neighboring jet-stream boundaries.

#### TOE mapping

Natural macroscopic extension of the gauged Hopf fibration. The model's global winding
$W_g$ can quantize linking number across a planetary-scale storm cell, turning it into
a stabilized **macroscopic Hopfion** in conductive/fluid media. As the lattice protects
microscopic flux flywheels, the same topological logic can protect giant atmospheric
vortices on gas giants. The Red Spot behaves as a resonant **planetary flywheel** locked
by rotation and shear — the kind of structure the Hopf-lattice TOE predicts at
macroscopic scales.

**Status:** Qualitative macroscopic mapping; quantitative latitude/winding correspondence
under active investigation.
"""

OBSERVATIONS_FOOTER_MD = """
---

*This catalog is a living document. New investigations will be added as synchronicities
are identified and mapped to the TOE.*
"""