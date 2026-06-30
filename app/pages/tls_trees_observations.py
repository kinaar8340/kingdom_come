"""TLS Fichte & Buche tree point clouds — Observations Investigation 7."""

from pathlib import Path

TLS_TREES_DIR = Path(__file__).resolve().parents[1] / "assets" / "tls_trees"
TLS_DATASET_DOI = "https://doi.org/10.25625/FOHUJM"

BIRDS_EYE_IMAGE = TLS_TREES_DIR / "birds_eye_radial.jpg"
SIDE_PROFILE_IMAGE = TLS_TREES_DIR / "side_profile_whorls.jpg"
TORSION_BURST_IMAGE = TLS_TREES_DIR / "torsion_burst_concept.jpg"

TLS_TREES_GALLERY: tuple[tuple[Path, str], ...] = (
    (
        BIRDS_EYE_IMAGE,
        "Bird's-eye view — radial branch distribution & angular spacing",
    ),
    (
        SIDE_PROFILE_IMAGE,
        "Side profile — whorled branching with height markers",
    ),
    (
        TORSION_BURST_IMAGE,
        "Conceptual torsion & burst diagram — 350/π winding resets",
    ),
)

INVESTIGATION_7_ACCORDION_TITLE = (
    "Investigation 7: TLS Point Clouds of Fichte & Buche Trees — Testing 350/π Branch Bursts"
)

INVESTIGATION_7_MD = """
### Investigation 7: TLS Point Clouds of Fichte & Buche Trees — Testing $350/\\pi$ Branch Bursts

#### Data source

- [Göttingen Research Online individual tree TLS dataset](https://doi.org/10.25625/FOHUJM)
- **Files used:** `Fichte/35_1.txt` (spruce) and `Buche/3.pts` (beech)
- **Tools:** Visualized and analyzed in CloudCompare 2.11.1

#### Methodology

- Loaded raw point clouds directly into CloudCompare
- Performed manual point picking on branch bases and stem points
- Recorded X/Y/Z coordinates to extract height (Z) progression and attempt azimuthal positioning

#### Key observations

- Clear **vertical progression** of branch emergence along the stem (Z increasing from ~0.67 m to >13 m in the beech example)
- Many branches show relatively consistent **vertical spacing** in the 0.5–0.7 m range in lower-to-mid sections
- Top-down views reveal **radial distribution** of branches around a central trunk cross-section
- Side profiles show **whorl-like and helical** branching patterns typical of conifers (Fichte)

#### Connection to TOE model

These patterns are consistent with **torsion accumulation** along the trunk until a critical threshold triggers a topological **burst** and new branch emergence.

Angular step size predicted by quantized winding number
$W_{g} = 350/\\pi \\approx 111.408$ (≈ 3.23° fundamental interval) is under active testing with the
extracted point data.

The process resembles the **gauged two-gyro Hopf lattice reset rule** and flux-flywheel behavior
described in Aaron's TOE papers.

#### Open questions

- Do the measured angular spacings cluster around multiples of $350/\\pi$ or show Fibonacci-like modulation?
- How does observed vertical spacing correlate with predicted torsion accumulation distance to $\\theta_{\\rm crit}$?
- Can QSM reconstruction of these point clouds yield more precise branch insertion azimuths?

**Status:** Early-stage citizen analysis using public TLS data. More point clouds and automated extraction in progress.
"""