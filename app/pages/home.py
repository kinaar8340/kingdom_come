"""Home / landing page — intro + sub-tabs: The Model, Clock, W_g, Papers, Explore."""

HOME_INTRO_MD = """
# Kingdom Come

A topological foundation for emergent physics via the Hopf Fibration and gauged flux lattices —  
**Aaron Michael Kinder's Theory of Everything.**

**Start here:** Hopf Visualizer → *Classic Hopf* preset → Update visualization
"""

HOME_THE_MODEL_MD = r"""
## Emergent Reality

Aaron's Theory of Everything models fundamental reality as **stable topological configurations**
of rotating, braided **flux flywheels** inside a **gauged Hopf lattice**, embedded in a porous
vacuum *sponge*. Particles, forces, and physical phenomena emerge from the geometric and dynamic
constraints of this system.

The framework is implemented in the [RubikConeConduit](https://github.com/kinaar8340/toe) simulation
and explored across [seven Hugging Face Spaces](https://huggingface.co/kinaar111/spaces).

### Core Substrate

| Concept | Role |
|---------|------|
| **Hopf fibration** | \(S^3 \to S^2\) backbone — linked circular fibers supply the lattice geometry |
| **Flux flywheels** | Stable rotating flux configurations — emergent particles and periodic-table proxy |
| **Gauged Hopf lattice** | Porous vacuum sponge with twist, braiding, and gauge dynamics |
| **Observer synchronization** | Embedded observers share the lattice — bursts may not appear as external signals |

---

## Vision

Physics emerges from **topologically protected flux structures** on a gauged Hopf lattice embedded
in a porous vacuum. The Hopf fibration \(S^3 \to S^2\) supplies the geometric backbone. Quaternions
provide the algebra, while stable **flux flywheels** anchor emergent matter and the periodic table.

---

## Mathematical Backbone

The Hopf map sends a unit 4-vector \((x_1, x_2, x_3, x_4) \in S^3\) to a point on \(S^2\):

\[
y_1 = x_1^2 - x_2^2, \quad y_2 = 2 x_1 x_2, \quad y_3 = 2(x_3 x_4 + x_1 x_2)
\]

Each point on \(S^2\) has a **fiber** — a circle in \(S^3\). Distinct fibers are **linked** with
Hopf invariant \(Q_H = 1\). Stereographic projection reveals these as linked Villarceau circles
(nested tori) in \(\mathbb{R}^3\).

---

## Flux Flywheels & Emergent Structure

Detuning parameters \((\Delta\omega, \text{gauge strength}, \text{layers})\) select **stability islands**
on the lattice. The *Magic Island Sweep* identified a noble-gas-like ultra-stable lock — a template
for emergent element mapping.

The **\(W_g\)** constant (\(\approx 350/\pi \approx 111.408\)) emerges as a universal invariant,
acting as a critical threshold in the underlying clock-like accumulation mechanism (see **The Clock**
sub-tab).

---

## Observer Synchronization

Phase holonomy between linked fibers damps as \(\Delta\theta(t) = \Delta\theta(0) \cdot e^{-\kappa t}\),
providing a topological mechanism for observer-linked non-locality. This explains why certain burst
events remain synchronized and difficult to detect externally.

"""

HOME_CLOCK_MD = r"""
## The Clock Equation

The underlying process is an **accumulation-and-release cycle** — a relaxation oscillator
(integrate-and-fire in topological terms):

Let **S(t)** represent accumulated stress, twist, pressure, or gauged weight in the flux lattice.

### Build-up (the tick)

\[
\frac{dS}{dt} = r
\]

(or discrete recurrence \(S_{n+1} = S_n + \Delta\)), where **r** is a roughly constant drive rate
set by lattice dynamics, `twist_rate`, braiding, or external gauging fields.

### Trigger / alarm

When **S(t)** reaches the critical threshold:

\[
S_{\text{crit}} = W_g = \frac{350}{\pi} \approx 111.4085
\]

a topological instability occurs. Simulations reproducibly lock **W_g** at **111.4080 ± 0.0000**.

### Burst + reset (the chime)

A punctuated release follows — energy/momentum reconfiguration, braiding phase shift, or burst
(modeled in *GW_Burst_Threshold* and related papers). Then **S** resets (subtract \(W_g\) or
drop to baseline), and the cycle repeats.

This produces a **sawtooth waveform**: slow linear rise → sudden drop → repeat.

### Why it acts like a clock

| Phase | Clock analog |
|-------|--------------|
| Constant-rate accumulation | Steady tick / spring-winding |
| Fixed threshold \(W_g\) | Alarm setting |
| Sudden release + reset | Chime and mechanism reset |
| Repetition | Quasi-periodic rhythm — period set by rate and threshold |

The braiding phase also locks tightly (~0.814) alongside \(W_g\), reinforcing topological invariance.
Full dynamics derive from the effective Lagrangian of the gauged Hopf lattice
(*Lagrangian_Derivation.pdf* in **The Papers** sub-tab).
"""

HOME_WG_MD = r"""
## The Key Emergent Constant: \(W_g \approx 350/\pi\)

**\(W_g\)** is the universal alarm threshold — the critical accumulated gauged weight, twist,
stress, or pressure at which the system becomes unstable.

\[
\frac{350}{\pi} \approx 111.40846 \quad\text{(simulation rounds to 111.4080)}
\]

This value **emerges** as a robust invariant across simulation runs — it is **not** an input parameter.

### Why exactly 350/π?

| Factor | Origin |
|--------|--------|
| **π** | Hopf fibration S¹ fibers — phases, linking numbers, and angular integrations |
| **350** | Lattice discretization, total flux quanta, embedding parameters, ~12 active elements |
| **Division by π** | Normalizes rotational/circular contributions from flywheels and braiding |

Because the model is proposed as a fundamental TOE substrate, the same
**pressure-build → burst → reset** mechanism applies universally:

- Quantum-scale flux configurations (particles as stable flywheels)
- Macroscopic domains (tectonic stress, neuronal integrate-and-fire, volcanic instabilities,
  biological punctuated rhythms, cosmic events)

The **Observations** tab visualizes macro/micro examples of this pattern across nature.
"""

HOME_EXPLORE_MD = """
## Supporting Resources

### GitHub (pinned repos)

| Repo | Focus |
|------|-------|
| [toe](https://github.com/kinaar8340/toe) | RubikConeConduit — W_g lock, stability islands, braiding phase |
| [kingdom_come](https://github.com/kinaar8340/kingdom_come) | This portal — visualizers and investigations |
| [qvpic](https://github.com/kinaar8340/qvpic) | Quaternion vortex persistent identity |
| [pic](https://github.com/kinaar8340/pic) | Persistent identity conduit (RubikCone-first) |
| [vqc_proto](https://github.com/kinaar8340/vqc_proto) | Orbital Braille VQC prototype |
| [vqc_sims_public](https://github.com/kinaar8340/vqc_sims_public) | Full VQC OAM simulation pipeline |
| [hfb](https://github.com/kinaar8340/hfb) | Hopf Flux Bubble — analog gravity & hopfions |
| [6-string-optimizer](https://github.com/kinaar8340/6-string-optimizer) | S³ burst optimizer |
| [mystery](https://github.com/kinaar8340/mystery) | φ, e, π emergent signature probes |

Papers in the repo (*GW_Burst_Threshold*, *GW_Echo*, *Lagrangian_Derivation*,
*Observer_Synchronization*, *Aaron's_TOE_Complete*) reproduce the locked invariants and
document burst, echo, and observer effects.

### Where to go next in Kingdom Come

| Tab | What you'll find |
|-----|------------------|
| **Hopf Visualizer** | Linked S³ → S² fibers — geometric intuition |
| **Lattice Simulator** | Two-gyro gauged quaternion lattice (stable vs chaotic) |
| **Flux Flywheel** | Periodic table as flux flywheel stability proxy |
| **The Papers** (sub-tab) | Accordion summaries + inline page previews |
| **Observations** | W_g = 350/π signatures in nature and markets |
| **Showcase** | All seven HF Spaces in the ecosystem |
| **Help** | Site navigation, controls, and acronym glossary |

The seven projects collectively explore accumulated twist evolving until the **350/π alarm**
triggers the reset — a self-consistent, testable topological framework.
"""