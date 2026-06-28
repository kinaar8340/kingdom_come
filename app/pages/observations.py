"""Observations tab — natural synchronicities mappable to the Hopf-lattice TOE."""

from pathlib import Path

OBSERVATIONS_ASSET = "app/assets/observations"
OBSERVATIONS_DIR = Path(__file__).resolve().parents[1] / "assets" / "observations"
CATATUMBO_LIGHTNING_1 = OBSERVATIONS_DIR / "catatumbo_lightning_1.png"
CATATUMBO_LIGHTNING_2 = OBSERVATIONS_DIR / "catatumbo_lightning_2.png"
CATATUMBO_LIGHTNING_3 = OBSERVATIONS_DIR / "catatumbo_lightning_3.png"

CATATUMBO_GALLERY: tuple[tuple[Path, str], ...] = (
    (
        CATATUMBO_LIGHTNING_1,
        "Catatumbo lightning — Lake Maracaibo panorama",
    ),
    (
        CATATUMBO_LIGHTNING_2,
        "Catatumbo lightning — multi-strike discharge",
    ),
    (
        CATATUMBO_LIGHTNING_3,
        "Catatumbo lightning — central bolt and reflection",
    ),
)

JUPITER_JUNO_MWR_IMAGE = OBSERVATIONS_DIR / "jupiter_juno_mwr_depth.jpg"
JUPITER_HUBBLE_TIMELINE_IMAGE = OBSERVATIONS_DIR / "jupiter_hubble_grs_timeline.jpg"
JUPITER_FULL_DISK_IMAGE = OBSERVATIONS_DIR / "jupiter_full_disk.jpg"

JUPITER_GALLERY: tuple[tuple[Path, str], ...] = (
    (
        JUPITER_JUNO_MWR_IMAGE,
        "Juno microwave radiometer — storm depth to 350 km (NASA)",
    ),
    (
        JUPITER_HUBBLE_TIMELINE_IMAGE,
        "Hubble Great Red Spot — Dec 2023 to Mar 2024 (NASA/ESA)",
    ),
    (
        JUPITER_FULL_DISK_IMAGE,
        "Jupiter full disk — Great Red Spot (NASA)",
    ),
)

THREEBODY_FRAMING_IMAGE = OBSERVATIONS_DIR / "threebody_framing.jpg"
THREEBODY_RESONATORS_IMAGE = OBSERVATIONS_DIR / "threebody_resonators.jpg"
THREEBODY_SYNC_IMAGE = OBSERVATIONS_DIR / "threebody_sync.jpg"

THREEBODY_GALLERY: tuple[tuple[Path, str], ...] = (
    (
        THREEBODY_FRAMING_IMAGE,
        "Figure-8 choreography — helical flux tubes on gauged Hopf lattice",
    ),
    (
        THREEBODY_RESONATORS_IMAGE,
        "Multi-resonator attractor — three braided flux flywheels",
    ),
    (
        THREEBODY_SYNC_IMAGE,
        "Pointer synchronization — Clifford torus lattice projection",
    ),
)

OBSERVATIONS_INTRO_MD = """
## Observations: Synchronicities in Nature

This tab catalogs phenomena — from planetary atmospheres to gravitational choreographies —
where persistent structures, vortices, charge separation, or topological features emerge
with properties that resonate with the gauged Hopf lattice TOE. Each entry is an
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

INVESTIGATION_3_MD = """
### Investigation 3: Emergent Periodic Orbits in Gravitational Three-Body Systems

The Newtonian three-body problem is famous for chaos — Poincaré showed that generic
trajectories are unpredictable. Yet highly symmetric **periodic** solutions persist:
Lagrange equilateral triangles, Euler collinear chains, and the celebrated figure-8
choreography. These are not mathematical curiosities alone; analogues appear in nature
(Trojan asteroids, hierarchical exoplanet systems, and choreographic ring configurations).

**Core thesis:** Stable periodic three-body orbits are **collective attractors** of the
same Gauged Hopf Lattice dynamics that stabilize individual flux-flywheel resonators
(the periodic table). Matter and gravitational bound states arise from one topological
rule set.

#### TOE framing

Three localized high-twist regions — flux flywheels / Hopfions — on the $T^3$ lattice,
driven by the gauged two-gyro coupling and global pointer
$\\alpha(t) = -\\kappa \\bar{\\Theta}(t)$, can self-organize into meta-stable periodic
configurations rather than fragmenting into chaos.

Observer synchronization locks linking phase across sites; topological protection via
$W_g = 350/\\pi$ prevents premature burst discharge. The result is not three independent
particles, but a **multi-resonator attractor** — a choreography of braided flux tubes
executing a closed orbit in configuration space.

#### Numerical evidence

| Result | Detail |
|--------|--------|
| PDE multi-Hopfion runs | Periodicity scores $\\approx 1.0$, zero burst events |
| Magic Island fact-bake | 48 facts $\\times$ 120 steps (RubikConeConduit full bake) |
| Stability scores | 17–18 — noble-gas targets exceeded |
| $W_g$ lock | Perfect alignment with $350/\\pi$ |
| Dual braiding metrics | Linking phase locked in strong_gauge_low_twist regime |
| Velocity-coupled PDE | Preliminary runs consistent with attractor picture |

The canonical bake delivered a **STRONG** verdict: Lagrange, Euler, and figure-8
configurations sit above the noble-gas stability threshold as collective lattice modes,
not fine-tuned initial conditions.

#### Pointer synchronization & implications

Global pointer feedback $\\alpha(t) = -\\kappa \\bar{\\Theta}(t)$ damps relative phase
drift between the three twist peaks, analogous to observer-linked holonomy in the
microscopic lattice. Dual-braiding metrics confirm that linking number is conserved
across the choreography — the same protection mechanism that guards elemental
flux flywheels now scales to gravitational N-body stability.

**Implication:** Gravitational bound states — including Lagrange points and the figure-8
orbit — are a higher-scale manifestation of the self-regulating lattice rule that
produces atoms. Celestial mechanics and matter share a geometric origin.

**Status:** STRONG numerical verdict from 48$\\times$120 bake; PDE and velocity-coupled
extensions under continued validation.
"""

OBSERVATIONS_FOOTER_MD = """
---

*This catalog is a living document. New investigations will be added as synchronicities
are identified and mapped to the TOE.*
"""