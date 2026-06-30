"""Home / landing page — intro + sub-tabs: The Model, Clock, W_g, Papers, Explore."""

from pathlib import Path

HOME_ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets" / "home"

HOME_INTRO_MD = """
# Kingdom Come

A topological foundation for emergent physics via the Hopf Fibration and gauged flux lattices —  
**Aaron Michael Kinder's Theory of Everything.**

**Start here:** Hopf Visualizer → *Classic Hopf* preset → Update visualization
"""

HOME_INTRO_GALLERY: tuple[tuple[Path, str], ...] = (
    (
        HOME_ASSETS_DIR / "hopf_linked_fibers.png",
        "Linked Villarceau circles — stereographic Hopf fiber projection",
    ),
    (
        HOME_ASSETS_DIR / "hopf_ribbon_torus.jpg",
        "Rainbow Hopf ribbon torus — Classic Hopf preset",
    ),
    (
        HOME_ASSETS_DIR / "hopf_fibration_bundle.png",
        "Hopf fibration fiber bundle with S² base sphere projection",
    ),
)

HOME_THE_MODEL_MD = """
### Emergent Reality

Aaron's Theory of Everything models fundamental reality as **stable topological configurations** of rotating, braided **flux flywheels** inside a **gauged Hopf lattice**, embedded in a porous vacuum *sponge*. Particles, forces, and physical phenomena emerge from the geometric and dynamic constraints of this system.

The framework is implemented in the RubikConeConduit simulation and explored across seven Hugging Face Spaces.

### Core Substrate

| Concept | Role |
|--------------------------|------|
| Hopf fibration | $S^3 \\to S^2$ backbone — linked circular fibers supply the lattice geometry |
| Flux flywheels | Stable rotating flux configurations — emergent particles and periodic-table proxy |
| Gauged Hopf lattice | Porous vacuum sponge with twist, braiding, and gauge dynamics |
| Observer synchronization | Embedded observers share the lattice — bursts may not appear as external signals |

### Vision

Physics emerges from **topologically protected flux structures** on a gauged Hopf lattice embedded in a porous vacuum. The Hopf fibration $S^3 \\to S^2$ supplies the geometric backbone. Quaternions provide the algebra, while stable **flux flywheels** anchor emergent matter and the periodic table.

### Mathematical Backbone

The Hopf map sends a unit 4-vector $(x_1, x_2, x_3, x_4) \\in S^3$ to a point on $S^2$:

$$
y_1 = x_1^2 - x_2^2, \\quad
y_2 = 2x_2x_3, \\quad
y_3 = 2(x_3x_4 + x_1x_2)
$$

Each point on $S^2$ has a **fiber** — a circle in $S^3$. Distinct fibers are **linked** with Hopf invariant $Q_H = 1$. Stereographic projection reveals these as linked Villarceau circles (nested tori) in $\\mathbb{R}^3$.

### Flux Flywheels & Emergent Structure

Detuning parameters $(\\Delta\\omega,\\ \\text{gauge strength},\\ \\text{layers})$ select **stability islands** on the lattice. The Magic Island Sweep identified a noble-gas-like ultra-stable lock — a template for emergent element mapping.

The constant $W_{g} \\approx 350/\\pi \\approx 111.408$ emerges as a universal invariant, acting as a critical threshold in the underlying clock-like accumulation mechanism (see **The Clock** tab).

### Observer Synchronization

Phase holonomy between linked fibers damps as $\\Delta\\theta(t) = \\Delta\\theta(0) \\cdot e^{-\\kappa t}$, providing a topological mechanism for observer-linked non-locality. This explains why certain burst events remain synchronized and difficult to detect externally.

### Monstrous Moonshine (finite symmetry companion)

The **Monster group** $\\mathbb{M}$ has exactly **194** irreducible representations (OEIS [A001379](https://oeis.org/A001379)).
The first non-trivial degree is **196883**; moonshine identifies **196884 = 196883 + 1** as the
coefficient of $q$ in the modular **$j$-invariant** — a bridge between finite sporadic symmetry
and complex analysis.

Kingdom Come treats this as a **second periodic manifold**: each irrep carries a
**15-dimensional fingerprint** (exponents of the supersingular primes in its degree). Explore it
in the **Monster Fingerprints** tab alongside the 118-element toroidal coil. This is interpretive
topology, not a substitute for flux-flywheel physics — but the structural rhyme (closed labels,
quantized classes, harmonic anchors) is deliberate.

*Fingerprint data: [meta-introspector/monster](https://github.com/meta-introspector/monster)*
"""

HOME_CLOCK_MD = """
### The Clock

The underlying process is an **accumulation-and-release cycle** — a relaxation oscillator
(integrate-and-fire in topological terms).

Let $S(t)$ represent accumulated stress, twist, pressure, or gauged weight in the flux lattice.

#### Build-up (the tick)

$$
\\frac{dS}{dt} = r
$$

(or discrete recurrence $S_{n+1} = S_n + \\Delta$), where $r$ is a roughly constant drive rate
set by lattice dynamics, `twist_rate`, braiding, or external gauging fields.

#### Trigger / alarm

When $S(t)$ reaches the critical threshold:

$$
S_{\\text{crit}} = W_{g} = \\frac{350}{\\pi} \\approx 111.4085
$$

a topological instability occurs. Simulations reproducibly lock $W_{g}$ at $111.4080 \\pm 0.0000$.

#### Burst + reset (the chime)

A punctuated release follows — energy/momentum reconfiguration, braiding phase shift, or burst
(modeled in *GW_Burst_Threshold* and related papers). Then $S$ resets (subtract $W_{g}$ or
drop to baseline), and the cycle repeats.

This produces a **sawtooth waveform**: slow linear rise → sudden drop → repeat.

#### Why it acts like a clock

| Phase | Clock analog |
|-------|--------------|
| Constant-rate accumulation | Steady tick / spring-winding |
| Fixed threshold $W_{g}$ | Alarm setting |
| Sudden release + reset | Chime and mechanism reset |
| Repetition | Quasi-periodic rhythm — period set by rate and threshold |

The braiding phase $\\phi_b$ also locks tightly ($\\phi_b \\approx 0.814$) alongside $W_{g}$,
reinforcing topological invariance. Full dynamics derive from the effective Lagrangian of the
gauged Hopf lattice (*Lagrangian_Derivation.pdf* in **The Papers** tab).
"""

HOME_WG_MD = """
### $W_{g}$ Constant

The constant $W_{g}$ emerges as a robust invariant from the gauged Hopf lattice dynamics.

**Approximate Value:**  
$W_{g} = 350/\\pi \\approx 111.408$

This value acts as the critical threshold in the clock-like accumulation mechanism. When accumulated
stress or twist reaches $W_{g}$, the system undergoes a punctuated burst and reset.

The subscript $g$ stands for **gauged**, reflecting the gauged nature of the Hopf lattice.
"""

HOME_EXPLORE_MD = """
### Explore

#### GitHub (pinned repos)

| Repo | Focus |
|------|-------|
| [toe](https://github.com/kinaar8340/toe) | RubikConeConduit — $W_{g}$ lock, stability islands, braiding phase |
| [kingdom_come](https://github.com/kinaar8340/kingdom_come) | This portal — visualizers and investigations |
| [qvpic](https://github.com/kinaar8340/qvpic) | Quaternion vortex persistent identity |
| [pic](https://github.com/kinaar8340/pic) | Persistent identity conduit (RubikCone-first) |
| [vqc_proto](https://github.com/kinaar8340/vqc_proto) | Orbital Braille VQC prototype |
| [vqc_sims_public](https://github.com/kinaar8340/vqc_sims_public) | Full VQC OAM simulation pipeline |
| [hfb](https://github.com/kinaar8340/hfb) | Hopf Flux Bubble — analog gravity & hopfions |
| [6-string-optimizer](https://github.com/kinaar8340/6-string-optimizer) | $S^3$ burst optimizer |
| [mystery](https://github.com/kinaar8340/mystery) | $\\phi$, $e$, $\\pi$ emergent signature probes |

Papers in the repo (*GW_Burst_Threshold*, *GW_Echo*, *Lagrangian_Derivation*,
*Observer_Synchronization*, *Aaron's_TOE_Complete*) reproduce the locked invariants and
document burst, echo, and observer effects.

#### Where to go next in Kingdom Come

| Tab | What you'll find |
|-----|------------------|
| **Hopf Visualizer** | Linked $S^3 \\to S^2$ fibers — geometric intuition |
| **Lattice Simulator** | Two-gyro gauged quaternion lattice (stable vs chaotic) |
| **Flux Flywheel** | Periodic table as flux flywheel stability proxy |
| **Monster Fingerprints** | 15×194 supersingular-prime heatmap for Monster irreps |
| **The Papers** (sub-tab) | Accordion summaries + inline page previews |
| **Observations** | $W_{g} = 350/\\pi$ signatures in nature and markets |
| **Showcase** | All seven HF Spaces in the ecosystem |
| **Help** | Site navigation, controls, and acronym glossary |

The seven projects collectively explore accumulated twist evolving until the $350/\\pi$ alarm
triggers the reset — a self-consistent, testable topological framework.
"""