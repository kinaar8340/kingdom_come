"""Theory overview content."""

THEORY_MD = """
## Aaron's Hopf Fibration TOE

### Vision

Physics emerges from **topologically protected flux structures** on a gauged Hopf lattice
embedded in a porous vacuum. The Hopf fibration $S^3 \\to S^2$ supplies the geometric
backbone; quaternions provide the algebra; stable **flux flywheels** anchor emergent matter.

### Mathematical Backbone

The Hopf map sends a unit 4-vector $(x_1, x_2, x_3, x_4) \\in S^3$ to a point on $S^2$:

$$
y_1 = x_1^2 - x_2^2, \\quad y_2 = 2 x_1 x_2, \\quad y_3 = 2(x_3 x_4 + x_1 x_2)
$$

Each point on $S^2$ has a **fiber** — a circle in $S^3$ — and distinct fibers are **linked**
with Hopf invariant $Q_H = 1$. Stereographic projection reveals these as linked
Villarceau circles (nested tori) in $\\mathbb{R}^3$.

### Flux Flywheels & the Periodic Table

Detuning parameters $(\\delta\\omega, \\text{gauge strength}, \\text{layers})$ select
**stability islands** on the lattice. The Magic Island Sweep (pseudo_Z = 129, score = 8.0)
identified a noble-gas-like ultra-stable lock — a template for emergent element mapping.

### Observer Synchronization

Phase holonomy between linked fibers damps as $\\delta\\Theta(t) = \\delta\\Theta(0)\\, e^{-\\kappa t}$,
providing a topological mechanism for observer-linked non-locality.

### Version

RubikConeConduit lineage · Magic Island Sweep v1.7.1 · Kingdom Come v0.1.0
"""

DERIVATION_HOPF_MD = """
### Derivation: Hopf Map via Quaternions

**Concept.** A unit quaternion $q = w + xi + yj + zk$ lives on $S^3$. Identifying
$z_1 = w + ix$, $z_2 = y + iz$ gives the standard Hopf map to $S^2$.

**Math.** The fiber over a base point is the set of quaternions mapping to that point;
varying the fiber phase $\\xi_2$ traces a great circle in $S^3$.

**Code.** `Quaternion.from_hopf_coords(η, ξ₁, ξ₂)` → `hopf_image()` in `kingdom.core`.

**Physics.** Linked fibers model topologically protected flux tubes in the porous vacuum.
"""