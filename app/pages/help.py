"""In-app help and quick-start content."""

HELP_MD = """
## How to use Kingdom Come

Kingdom Come is an **interactive knowledge portal** for Aaron's Hopf-fibration-based
Theory of Everything (TOE). It is **not** a game — it is a physics/visualization
workbench linking topology, quaternions, flux lattices, and emergent matter models.

### Recommended first visit (5 minutes)

1. Open **Hopf Visualizer** → leave **2D projections** selected (HF-safe).
2. Click **Classic Hopf** preset → **Update visualization**.
3. Read the four panels: linked fibers (xy/xz), S² base chart, phase-colored highlight.
4. Open **Lattice Simulator** → **Run lattice comparison** (stable vs chaotic).
5. Open **The Model** for core postulates.
6. Try **Flux Flywheel** at Z = 2 (He — noble gas lock), Z = 10 (Ne), or Z = 129 (synthetic sweep ID).

### Hopf Visualizer controls

| Control | Effect |
|---------|--------|
| **View mode** | 2D (recommended on HF) or 3D WebGL (local browsers) |
| **Number of fibers** | Density of linked Villarceau circles |
| **Highlight η, ξ₁** | Which fiber is gold-highlighted |
| **Projection scale** | Zoom stereographic view |
| **Show S² base** | Base-space markers on stereographic chart |

### Tech stack

- **Frontend:** Gradio 6
- **Math / viz:** NumPy, Plotly, SymPy
- **Hardware:** CPU-basic (no GPU required)
- **Source:** [github.com/kinaar8340/kingdom_come](https://github.com/kinaar8340/kingdom_come)

### Limitations

- Hugging Face iframes often block WebGL → use **2D projections** here.
- Flux flywheel mapping is a calibrated proxy (Magic Island Sweep v1.7.1), not full lattice MD.
- Lattice animation integration from `toe` repo is planned.

### Version

Kingdom Come v0.1.0 · RubikConeConduit / TOE lineage
"""

QUICKSTART_MD = """
### New here?

**Kingdom Come** = unified portal for Aaron's Hopf Fibration TOE.

→ Jump to **Hopf Visualizer** and click **Classic Hopf** to see linked fibers instantly.
→ See **Help** tab for a full walkthrough.
"""