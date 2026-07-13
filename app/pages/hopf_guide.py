"""Hopf Visualizer — in-panel guide copy."""

HOPF_INTRO_MD = """
Each point on $S^2$ (bottom-left) has a **fiber** — a circle in $S^3$. Stereographic projection
reveals these as linked loops in $\\mathbb{R}^3$ (top panels). **Gold** traces your highlighted fiber; colors
mark distinct fibers with Hopf linking number 1.
"""

HOPF_PANEL_GUIDE_MD = """
| Panel | Meaning |
|-------|---------|
| **① $\\mathbb{R}^3$ xy** | Linked Villarceau circles — stereographic view of Hopf fibers |
| **② $\\mathbb{R}^3$ xz** | Orthogonal slice — same fibers, side projection |
| **③ $S^2$ base** | Where each fiber lands on the Hopf base sphere (stereographic chart) |
| **④ Phase $\\xi_2$** | Gold highlight fiber colored by fiber-phase angle |

*Topology primer: fibers are linked like chain links; this linking is the topological backbone of the TOE model.*
"""

HF_VIEW_MODE_MD = """
**Rendering:** 2D Plotly only on Hugging Face (including **Animate** frames).

Interactive 3D rotation needs WebGL, which HF Space iframes block in most browsers.
Dashboard, S² explorer, and Animate modes use standard 2D Plotly — no WebGL required.
For local 3D WebGL, clone the [GitHub repo](https://github.com/kinaar8340/kingdom_come).

**Animate modes:** `xi1_orbit` (base walks around $S^2$), `eta_breath` (latitude oscillates),
`gauge_twist` (phase marker along the fiber). Use **Play** on the chart.

Premium real-time 3D lives outside the core library — see the companion
[flux-hopf-explorer](https://github.com/kinaar8340/flux_hopf_explorer) (Three.js / WebGPU).
"""