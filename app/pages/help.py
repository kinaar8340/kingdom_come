"""In-app help — site navigation, walkthrough, and acronym glossary."""

HELP_NAVIGATE_MD = r"""
## Navigate Kingdom Come

Kingdom Come is the unified portal for Aaron's Hopf-fibration TOE and the seven-project ecosystem.
Use the **main tab bar** at the top of this page to switch between interactive modules.

### In-app tabs

| Tab | What it does | Start here if… |
|-----|--------------|----------------|
| **Home** | Merged foundation + model — vision, math backbone, clock mechanism | You want the big picture first |
| **Help** | This page — navigation, controls, acronyms | You need orientation or a term defined |
| **Hopf Visualizer** | Linked S³ → S² fiber plots (2D on HF, 3D WebGL locally) | You want geometric intuition |

| **Home → Papers** | Accordion summaries + inline page previews + PDF download | You want primary sources |
| **Lattice Simulator** | Two-gyro gauged quaternion lattice (stable vs chaotic) | You want to see burst dynamics |
| **Flux Flywheel** | Periodic table explorer Z = 1–180 + Magic Island heatmap | You want matter as flux configurations |
| **Observations** | Investigations — lightning, Jupiter, 3-body, Higgs, Schumann, Bitcoin π-cycle, cuprates, pulsars | You want nature-scale W_g signatures |
| **Showcase** | Card grid linking all HF Spaces | You want to jump to sibling demos |

### Hugging Face Spaces ([kinaar111/spaces](https://huggingface.co/kinaar111/spaces))

| Space | Link |
|-------|------|
| **Kingdom Come** (you are here) | [spaces/kinaar111/kingdom](https://huggingface.co/spaces/kinaar111/kingdom) |
| **6-String Optimizer** | [spaces/kinaar111/6-string-optimizer](https://huggingface.co/spaces/kinaar111/6-string-optimizer) |
| **QVPIC Identity Conduit** | [spaces/kinaar111/qvpic](https://huggingface.co/spaces/kinaar111/qvpic) |
| **Hopf Flux Bubble** | [spaces/kinaar111/hopf-flux-bubble](https://huggingface.co/spaces/kinaar111/hopf-flux-bubble) |
| **Orbital Braille VQC** | [spaces/kinaar111/orbital-braille-vqc](https://huggingface.co/spaces/kinaar111/orbital-braille-vqc) |
| **Mystery** | [spaces/kinaar111/mystery](https://huggingface.co/spaces/kinaar111/mystery) |

### GitHub repos ([kinaar8340](https://github.com/kinaar8340))

| Repo | Link |
|------|------|
| TOE / RubikConeConduit | [github.com/kinaar8340/toe](https://github.com/kinaar8340/toe) |
| Kingdom Come | [github.com/kinaar8340/kingdom_come](https://github.com/kinaar8340/kingdom_come) |
| QVPIC | [github.com/kinaar8340/qvpic](https://github.com/kinaar8340/qvpic) |
| PIC | [github.com/kinaar8340/pic](https://github.com/kinaar8340/pic) |
| VQC Proto | [github.com/kinaar8340/vqc_proto](https://github.com/kinaar8340/vqc_proto) |
| VQC Sims | [github.com/kinaar8340/vqc_sims_public](https://github.com/kinaar8340/vqc_sims_public) |
| Hopf Flux Bubble | [github.com/kinaar8340/hfb](https://github.com/kinaar8340/hfb) |
| 6-String Optimizer | [github.com/kinaar8340/6-string-optimizer](https://github.com/kinaar8340/6-string-optimizer) |
| Mystery | [github.com/kinaar8340/mystery](https://github.com/kinaar8340/mystery) |
"""

HELP_GETTING_STARTED_MD = r"""
## Getting Started (5 minutes)

Kingdom Come is an **interactive knowledge portal** for Aaron's Hopf-fibration-based
Theory of Everything (TOE). It is **not** a game — it is a physics/visualization workbench
linking topology, quaternions, flux lattices, and emergent matter models.

### Recommended first visit

1. Read **Home** (foundation + vision) and **Home → The Clock** for the \(W_g = 350/\pi\) mechanism.
2. Open **Hopf Visualizer** → click **Classic Hopf** preset → **Update visualization**.
3. Study the four panels: linked fibers (xy/xz), S² base chart, phase-colored highlight.
4. Open **Lattice Simulator** → **Run lattice comparison** (stable vs chaotic).
5. Try **Flux Flywheel** at Z = 2 (He — noble gas lock), Z = 10 (Ne), or Z = 129 (Magic Island ID).

### First-time visitor shortcut

| Step | Tab | Action |
|------|-----|--------|
| 1 | Hopf Visualizer | **Classic Hopf** preset (auto-loads parameters) |
| 2 | Hopf Visualizer | Read panels ①–④ in the accordion |
| 3 | Lattice Simulator | **Run lattice comparison** |
| 4 | Flux Flywheel | Set Z = 2 for the Magic Island anchor |

*Tip: use **Reset defaults** in Hopf Visualizer anytime.*
"""

HELP_CONTROLS_MD = """
## Controls & Tips

### Hopf Visualizer

| Control | Effect |
|---------|--------|
| **View mode** | 2D (recommended on HF) or 3D WebGL (local browsers) |
| **Number of fibers** | Density of linked Villarceau circles |
| **Highlight η, ξ₁** | Which fiber is gold-highlighted |
| **Projection scale** | Zoom stereographic view |
| **Show S² base** | Base-space markers on stereographic chart |
| **Presets** | Classic Hopf, Dense fiber weave, Wide projection |

### Lattice Simulator

| Control | Effect |
|---------|--------|
| **Frames** | Simulation length |
| **Lattice sites** | Grid resolution |
| **Stable gauge strength** | Gauge coupling for the stable run (chaotic uses 0.08) |

### Flux Flywheel

| Control | Effect |
|---------|--------|
| **Atomic number Z** | Slider or dropdown — Z = 1–118 known, 119–180 predicted |
| **Periodic table** | Click any cell to jump |
| **Noble gas buttons** | Quick-jump to He, Ne, Ar, Kr, Xe, Rn, Og |

### Limitations

- Hugging Face iframes often block WebGL → use **2D projections** on HF.
- Flux flywheel mapping is a calibrated proxy (Magic Island Sweep v1.7.1), not full lattice MD.
- Lattice animation integration from the `toe` repo is ongoing.

### Version

Kingdom Come v0.1.0 · RubikConeConduit / TOE lineage
"""

HELP_ACRONYMS_MD = """
## Acronyms Glossary

Terms drawn from pinned repos at [github.com/kinaar8340](https://github.com/kinaar8340).
See also [vqc_proto/GLOSSARY.md](https://github.com/kinaar8340/vqc_proto/blob/main/GLOSSARY.md)
and [hfb/GLOSSARY.md](https://github.com/kinaar8340/hfb/blob/main/GLOSSARY.md).

| Acronym | Stands For | Definition |
|---------|------------|------------|
| **TOE** | Theory of Everything | Hopf-lattice model where flux flywheels on a gauged lattice yield emergent particles, forces, and phenomena. |
| **W_g** | Gauged weight (emergent constant) | Universal alarm threshold 350/π ≈ 111.4085 — critical accumulated twist/stress before topological burst and reset. |
| **VQC** | Vortex Quaternion Conduit | Ultra-high-density quantum data compression and transfer via OAM-flux qubits and quaternion encoding. |
| **OAM** | Orbital Angular Momentum | Angular momentum of a light beam from spatial phase structure (twist number ℓ), independent of polarization. |
| **QVPIC** | Quaternion Vortex Persistent Identity Conduit | Software embodiment of VQC — drift-resistant AI memory via topological invariants on a Clifford-torus base. |
| **PIC** | Persistent Identity Conduit | Geometric helical memory architecture shifting persistence from vectors to global topological features. |
| **RCC** | RubikConeConduit | Core TOE simulator — toroidal flux flywheel lattice with locked W_g and braiding invariants. |
| **HFB** | Hopf Flux Bubble | Emergent effective-metric playground from defects, flows, and Hopf topology — analog gravity demos. |
| **LG** | Laguerre-Gaussian | Standard analytic basis for OAM donut beams (ℓ = topological charge). |
| **DWDM** | Dense Wavelength Division Multiplexing | Parallel wavelength channels; VQC stacks OAM modes within each channel. |
| **BMGL** | Beam-Motion-Gated Learning | Turbulence/error gating protocol tied to OAM rotation rates; γ₁ tunes inhibition strength. |
| **PWM** | Pulse-Width Modulation | Time-gated ON/OFF duty encoding for Orbital Braille glyph orbs on the typehead. |
| **ICA** | Independent Component Analysis | FastICA demixing of overlapping orb intensity channels at VQC decode time. |
| **QEC** | Quantum Error Correction | 16-qubit canonical error suppression in the full VQC pipeline. |
| **SLM** | Spatial Light Modulator | Phase-only display chip for holographic OAM / typehead patterns. |
| **TNN** | Topological Neural Network | Copresheaf diffusion layer on RingConeChain geometry in QVPIC v10.2. |
| **GW** | Gravitational Wave | Burst and echo signatures derived from W_g threshold crossings in TOE papers. |
| **PTA** | Pulsar Timing Array | Radio-timing networks used to test 350/π coupling hypotheses (Observations tab). |
| **BEC** | Bose-Einstein Condensate | Ultracold atomic medium used as tabletop acoustic/optical analog in HFB. |
| **SOC** | Spin-Orbit Coupling | Interaction parameter in p-wave BMGL altermagnetic variant. |
| **HF** | Hugging Face | Host for live Gradio Spaces in the seven-project ecosystem. |
| **κ** | Kappa (coupling) | Global pointer-damping / interlayer coupling parameter; doc value ≈ 0.85 across repos. |
"""

HELP_TECH_MD = r"""
## Tech Stack

| Layer | Tools |
|-------|-------|
| **Frontend** | Gradio 6 |
| **Math / viz** | NumPy, Plotly, SymPy |
| **Hardware** | CPU-basic (no GPU required) |
| **Source** | [github.com/kinaar8340/kingdom_come](https://github.com/kinaar8340/kingdom_come) |

### Related reading

- **Home** tab — clock mechanism and \(W_g\) foundation
- **Home → Papers** — *GW_Burst_Threshold*, *Lagrangian_Derivation*, *Observer_Synchronization*
- **Acronyms** tab (this Help section) — full glossary
"""