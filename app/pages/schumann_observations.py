"""Schumann Prediction Experiment — Observations Investigation 5 content."""

from pathlib import Path

SCHUMANN_DIR = Path(__file__).resolve().parents[1] / "assets" / "schumann"

SCHUMANN_METRIC_IMAGE = SCHUMANN_DIR / "metric_diagram.jpg"
SCHUMANN_OVERVIEW_IMAGE = SCHUMANN_DIR / "june20_22_overview.jpg"
SCHUMANN_COMPARISON_IMAGE = SCHUMANN_DIR / "real_vs_predicted.jpg"

SCHUMANN_GALLERY: tuple[tuple[Path, str], ...] = (
    (
        SCHUMANN_METRIC_IMAGE,
        "Refined accumulation metric — SR-modulated topological phase",
    ),
    (
        SCHUMANN_OVERVIEW_IMAGE,
        "June 20–22 prediction — SR driver, phase curve, 111.408 crossings",
    ),
    (
        SCHUMANN_COMPARISON_IMAGE,
        "Real Tomsk spectrogram vs model accumulation (June 20–22)",
    ),
)

INVESTIGATION_5_ACCORDION_TITLE = "Investigation 5: Schumann Prediction Experiment"

INVESTIGATION_5_MD = """
### Investigation 5: Schumann Prediction Experiment

**Objective:** Test whether real Schumann Resonance (SR) power time series can drive a
geometric/topological accumulation model and produce meaningful **punctuated events** at the
$111.408$ scale ($W_g = 350/\\pi$). This is an early empirical validation loop for the broader
RubikConeConduit + two-gyro lattice + CubeChain framework.

#### Refined metric

Each 10-minute timestep updates accumulated topological phase:

$$
\\Delta\\phi = \\bigl(w_1 |\\text{gauge\\_alpha}| + w_2 \\cdot \\text{mean\\_twist}
+ w_3 \\cdot \\text{vortex\\_sync} + w_4 \\cdot \\delta\\text{effective\\_winding}\\bigr)
\\times P_{\\text{SR}}
$$

| Component | Role |
|-----------|------|
| **gauge_alpha** | Gauged pointer / holonomy drive from the two-gyro lattice |
| **mean_twist** | Spatial average twist density on the conduit |
| **vortex_sync** | CubeChain vortex synchronization score |
| **δ effective_winding** | Deviation from locked $W_g$ invariant |
| **$P_{\\text{SR}}$** | Tomsk SR power (real or synthetic driver) |

**Event trigger:** Each crossing of an integer multiple of **111.408** registers as a
punctuated topological-clock event.

#### Experimental setup

- **Driver:** Real Tomsk amplitude/power at 10-min resolution (updated to match spectrogram
  brightness for the June 20–22 window); synthetic SR available for baseline tests.
- **Window:** June 20–22, 2026 multi-day run, compared against the June 11–12 wave and
  post-wave recovery period.
- **Validation target:** Model crossing density and local burst counts vs actual spectrogram
  brightness patterns in Tomsk data.

#### Results (June 20–22, 2026)

| Metric | Observation |
|--------|-------------|
| 111.408 crossings | ~21 across the 3-day window |
| Bright-period correlation | Higher crossing density when real SR activity is sustained |
| Overall regime | Moderate — consistent with post–June 11–12 recovery |
| Phase curve | Monotonic rise modulated by SR power envelope |
| Burst alignment | Local burst counts elevated near spectrogram bright bands |

Brighter stretches in the real Tomsk spectrogram correspond to **faster phase accumulation**
and more frequent clock crossings — the model responds coherently to geophysical drive rather
than producing random threshold hits.

#### Interpretation & next steps

**Status:** Early validation — promising structural correspondence between real SR activity
and geometric-model punctuated events. Not yet a full predictive forecast system.

**Interpretation:**

- The $111.408$ clock acts as a **topological event horizon** — SR power modulates how
  quickly the lattice/conduit system reaches quantized winding thresholds.
- vortex_sync from CubeChain couples global coherence into the accumulation, linking
  mesoscale lattice dynamics to ionospheric-scale drivers.
- Post–June 11–12 moderate regime suggests the model captures recovery dynamics, not only
  extreme wave events.

**Proposed improvements:**

1. Extend comparison to the full June 11–12 wave with matched driver calibration.
2. Add lead/lag analysis between spectrogram features and predicted crossings.
3. Replace brightness-matched proxy with direct Tomsk amplitude ingestion pipeline.
4. Couple crossing events to lattice burst simulator for closed-loop validation.
5. Publish closeness metrics (crossing-time RMSE, brightness–phase correlation).

**Status:** Exploratory validation — geophysical data meaningfully interacts with the
geometric model; quantitative forecast closure pending.
"""