"""Hopf Visualizer — in-panel guide copy."""

HOPF_INTRO_MD = """
Each point on **S²** (bottom-left) has a **fiber** — a circle in **S³**. Stereographic projection
reveals these as linked loops in ℝ³ (top panels). **Gold** traces your highlighted fiber; colors
mark distinct fibers with Hopf linking number 1.
"""

HOPF_PANEL_GUIDE_MD = """
**What you're looking at (panels ①–④)**

| Panel | Meaning |
|-------|---------|
| **① ℝ³ xy** | Linked Villarceau circles — stereographic view of Hopf fibers |
| **② ℝ³ xz** | Orthogonal slice — same fibers, side projection |
| **③ S² base** | Where each fiber lands on the Hopf base sphere (stereographic chart) |
| **④ Phase ξ₂** | Gold highlight fiber colored by fiber-phase angle |

*Topology primer: fibers are linked like chain links; this linking is the topological backbone of the TOE model.*
"""

HF_VIEW_MODE_MD = """
**Rendering:** 2D projections only on Hugging Face.

Interactive 3D rotation needs WebGL, which HF Space iframes block in most browsers.
All four panels use standard 2D Plotly — no WebGL required. For 3D, clone the
[GitHub repo](https://github.com/kinaar8340/kingdom_come) and run locally.
"""