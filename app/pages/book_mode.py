"""Book Mode — map QGA manuscript chapters to live portal widgets.

Companion to https://github.com/kinaar8340/qga (Kingdom Come: A Quaternionic
Geometric Approach to Number Theory and Physics).
"""

from __future__ import annotations

from dataclasses import dataclass

BOOK_REPO_URL = "https://github.com/kinaar8340/qga"
BOOK_PDF_HINT = "book/Kingdom_Come_QGA.pdf (in the qga repo)"

# Main Tabs() indices after Book Mode is inserted (see app.py).
# 0 Home · 1 Help · 2 Book Mode · 3 Hopf · 4 Toroidal · 5 Monster ·
# 6 Lattice · 7 Flux Flywheel · 8 Observations · 9 Showcase
WIDGET_TAB_INDEX: dict[str, int] = {
    "home": 0,
    "help": 1,
    "book": 2,
    "hopf": 3,
    "toroidal": 4,
    "monster": 5,
    "lattice": 6,
    "flux": 7,
    "observations": 8,
    "showcase": 9,
}


@dataclass(frozen=True)
class BookChapter:
    key: str
    title: str
    part: str
    summary: str
    widget: str  # key into WIDGET_TAB_INDEX
    widget_label: str
    how_to: str
    claim_focus: str


CHAPTERS: tuple[BookChapter, ...] = (
    BookChapter(
        key="ch0",
        title="Ch. 0 — Preview",
        part="Preview",
        summary="Pythagorean triples → four squares → $S^3$ → Hopf → flux flywheels → $Z\\mapsto$ map.",
        widget="hopf",
        widget_label="Hopf Visualizer",
        how_to="Open **Hopf Visualizer** → Classic Hopf → Update. Then peek at **Flux Flywheel** for $Z$.",
        claim_focus="Theorem / Model / Hypothesis labels introduced",
    ),
    BookChapter(
        key="ch1",
        title="Ch. 1 — Quaternions",
        part="Part I · Foundations",
        summary="Norm, $S^3$, Lipschitz/Hurwitz, four-square theorem, double cover of $SO(3)$.",
        widget="hopf",
        widget_label="Hopf Visualizer",
        how_to="Unit quaternions are points of the Hopf total space — explore fibers after reading §1.3.",
        claim_focus="Four-square + norm multiplicativity = Theorem",
    ),
    BookChapter(
        key="ch2",
        title="Ch. 2 — Hopf Fibration",
        part="Part I · Foundations",
        summary="Hopf map $S^3\\to S^2$, linking, stereographic views, bundle structure.",
        widget="hopf",
        widget_label="Hopf Visualizer",
        how_to="**Hopf Visualizer**: Classic Hopf · 2D dashboard · compare xy/xz/base/phase panels.",
        claim_focus="Linking / Hopf invariant = Theorem; Farey analogue = Model",
    ),
    BookChapter(
        key="ch3",
        title="Ch. 3 — Gauged Hopf Lattice",
        part="Part II · Farey lift",
        summary="Hurwitz lattice, adjacency (OP1), gauge actions, birth of flux flywheels.",
        widget="lattice",
        widget_label="Lattice Simulator",
        how_to="**Lattice Simulator** → Run lattice comparison (stable vs chaotic).",
        claim_focus="Adjacency rules = Model · OP1",
    ),
    BookChapter(
        key="ch4",
        title="Ch. 4 — Symmetries",
        part="Part II · Farey lift",
        summary="Left/right multiplications, LFT comparison, periodic orbits, gauge on flux.",
        widget="lattice",
        widget_label="Lattice Simulator",
        how_to="Watch identity preservation under gauge evolution; contrast stable/chaotic modes.",
        claim_focus="Isometries = Theorem; modular parallel = Model",
    ),
    BookChapter(
        key="ch5",
        title="Ch. 5 — Flux Topographs",
        part="Part III · Forms",
        summary="Flux functionals, separators, periodicity, Magic Islands intro (OP2).",
        widget="flux",
        widget_label="Flux Flywheel",
        how_to="**Flux Flywheel** + Magic Island heatmap accordion; compare $Z$ stability scores.",
        claim_focus="Topographs = Model · OP2",
    ),
    BookChapter(
        key="ch6",
        title="Ch. 6 — Classification & Magic Islands",
        part="Part III · Forms",
        summary="Four types, reduced configs, class-number analogue (OP3).",
        widget="flux",
        widget_label="Flux Flywheel",
        how_to="Sweep $Z$ and open Magic Island heatmap; note noble-gas peaks.",
        claim_focus="Classification heuristics = Model · OP3",
    ),
    BookChapter(
        key="ch7",
        title="Ch. 7 — $Z\\mapsto$ Flux Map",
        part="Part III · Representations",
        summary="map_z_to_flywheel, representation reading, electron clouds (OP4).",
        widget="flux",
        widget_label="Flux Flywheel",
        how_to="Pick He ($Z=2$), Ne ($10$), Fe ($26$), Au ($79$) — compare score/class/clouds.",
        claim_focus="Coded map = Software fact; chemistry emergence = Model/Hypothesis",
    ),
    BookChapter(
        key="ch8",
        title="Ch. 8 — Composition & Class Groups",
        part="Part IV · Arithmetic",
        summary="Gauss composition lift, class-group analogue (OP6 sandbox).",
        widget="home",
        widget_label="Home · The Model",
        how_to="Read The Model for narrative; full labs live in the qga repo (`lib/composition.py`).",
        claim_focus="Composition law = Model · OP6",
    ),
    BookChapter(
        key="ch9",
        title="Ch. 9 — Quaternion Algebras",
        part="Part IV · Arithmetic",
        summary="Ramification, Hurwitz order, ideal class groups; algebraic home for OP6.",
        widget="home",
        widget_label="Home · The Model",
        how_to="Derivation accordion on Home; algebraic labs in qga `lib/quaternion_algebra.py`.",
        claim_focus="Hurwitz class number 1 = Theorem",
    ),
    BookChapter(
        key="ch10",
        title="Ch. 10 — Observations & Validation",
        part="Part V · Observations",
        summary="$350/\\pi$, Table T4, open-problem summary (OP5).",
        widget="observations",
        widget_label="Observations",
        how_to="**Observations** tab: Bitcoin Pi Cycle, TLS, superconductors, pulsars, fidelity trends.",
        claim_focus="Multi-domain $W_g$ = Hypothesis · Table T4 validation",
    ),
)


def chapter_dropdown_choices() -> list[tuple[str, str]]:
    return [(c.title, c.key) for c in CHAPTERS]


def chapter_by_key(key: str) -> BookChapter:
    for c in CHAPTERS:
        if c.key == key:
            return c
    return CHAPTERS[0]


def chapter_detail_md(key: str) -> str:
    c = chapter_by_key(key)
    return f"""
### {c.title}

**{c.part}**

{c.summary}

| | |
|--|--|
| **Live tab** | {c.widget_label} |
| **How to use** | {c.how_to} |
| **Claim focus** | {c.claim_focus} |

Press **Open linked live tab** to jump to the companion widget, or use the mini demos below for an in-place preview.
"""


BOOK_MODE_INTRO_MD = f"""
# Book Mode

Interactive companion to the manuscript
**[Kingdom Come: A Quaternionic Geometric Approach to Number Theory and Physics]({BOOK_REPO_URL})**
(short name **QGA**).

| | |
|--|--|
| **Source** | [{BOOK_REPO_URL}]({BOOK_REPO_URL}) |
| **PDF** | `{BOOK_PDF_HINT}` |
| **Claim labels** | **Theorem** · **Model** · **Hypothesis** · **Software fact** |

Select a chapter, open its live tab, or run a mini demo without leaving Book Mode.
"""


BOOK_TOC_MD = """
## Manuscript map

| Part | Chapters | Live widgets |
|------|----------|----------------|
| Preview | 0 | Hopf Visualizer · Flux Flywheel |
| **I** Foundations | 1–2 | Hopf Visualizer |
| **II** Farey lift | 3–4 | Lattice Simulator |
| **III** Forms / $Z$-map | 5–7 | Flux Flywheel |
| **IV** Arithmetic | 8–9 | Home · The Model (+ qga `lib/`) |
| **V** Observations | 10 | Observations |

Open problems OP1–OP6 are summarized in the book Appendix B and `notes/open_problems.md`.
"""


PART_I_MD = """
### Part I — Foundations (Ch. 1–2)

- **Ch. 1** Quaternions: norm, $S^3$, Hurwitz order, four squares, $\\mathrm{Spin}(3)\\to SO(3)$.
- **Ch. 2** Hopf fibration: fibers, linking, stereographic panels, charts.

**Live:** Hopf Visualizer (Classic Hopf preset). Mini demo below samples fibers immediately.
"""

PART_II_MD = """
### Part II — Gauged Hopf Lattice (Ch. 3–4)

- **Ch. 3** Lattice construction, adjacency (**OP1**), flux flywheels.
- **Ch. 4** Left/right gauge symmetries, periods, identity preservation.

**Live:** Lattice Simulator — stable vs chaotic gauge. Mini demo runs a short comparison.
"""

PART_III_MD = """
### Part III — Forms, Islands, $Z\\mapsto$ map (Ch. 5–7)

- **Ch. 5** Flux topographs (**OP2**).
- **Ch. 6** Classification & Magic Islands (**OP3**).
- **Ch. 7** $Z\\mapsto$ flywheel map (**OP4**).

**Live:** Flux Flywheel — set $Z$ and read stability / electron cloud. Mini demo uses He by default.
"""

PART_IV_MD = """
### Part IV — Arithmetic depth (Ch. 8–9)

- **Ch. 8** Composition & class-group analogues (**OP6** sandbox).
- **Ch. 9** Quaternion algebras, Hurwitz ideals (class number 1 = Theorem).

**Live:** narrative on Home · The Model. Full composition/algebra labs run offline in the
[qga](https://github.com/kinaar8340/qga) repo (`lib/composition.py`, `lib/quaternion_algebra.py`).
"""

PART_V_MD = """
### Part V — Observations & validation (Ch. 10)

- Multi-domain $W_g = 350/\\pi$ (**Hypothesis**, **OP5**).
- Table T4 validation checklist (book Appendix D).
- Pulsars, Bitcoin Pi Cycle, TLS, superconductors, fidelity trends.

**Live:** Observations tab. Use investigation accordions; jump to Flux Flywheel from trend plots where wired.
"""


def widget_key_for_chapter(key: str) -> str:
    return chapter_by_key(key).widget


def main_tab_index_for_widget(widget: str) -> int:
    return WIDGET_TAB_INDEX.get(widget, WIDGET_TAB_INDEX["book"])
