"""Papers tab — TOE manuscripts (accordion + download, no inline viewer)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = Path(__file__).resolve().parents[1] / "assets" / "papers"
PAPERS_SOURCE_DIR = _REPO_ROOT / "papers"
TOE_PAPERS_REPO = "https://github.com/kinaar8340/toe/tree/main/papers"
KINGDOM_PAPERS_REPO = "https://github.com/kinaar8340/kingdom_come/tree/main/papers"

PAPERS_SEARCH_DIRS: tuple[Path, ...] = (PAPERS_DIR, PAPERS_SOURCE_DIR)

FILENAME_ALIASES: dict[str, tuple[str, ...]] = {
    "Aarons_TOE_Complete.pdf": ("Aarons_TOE_Complete.pdf", "Aaron's_TOE_Complete.pdf"),
}

PAPERS_INTRO_MD = """
## Papers

Manuscripts from Aaron's Hopf Fibration Theory of Everything — sourced from
[toe/papers](https://github.com/kinaar8340/toe/tree/main/papers) and
[kingdom_come/papers](https://github.com/kinaar8340/kingdom_come/tree/main/papers).

Expand any section below for a summary, then use **Download PDF** to open the full
manuscript in your browser (works in Firefox, Brave, and all privacy browsers).
"""


@dataclass(frozen=True)
class PaperEntry:
    key: str
    title: str
    description: str
    filename: str
    summary_md: str

    @property
    def path(self) -> Path:
        return PAPERS_DIR / self.filename


PAPER_ENTRIES: tuple[PaperEntry, ...] = (
    PaperEntry(
        key="toe_complete",
        title="Aaron's TOE — Complete",
        description="Full Theory of Everything manuscript — Hopf fibration backbone, flux flywheels, and emergent physics.",
        filename="Aarons_TOE_Complete.pdf",
        summary_md="""
**Scope:** Complete Theory of Everything manuscript.

**Covers:**
- Hopf fibration backbone (S³ → S²) and quaternion structure
- Flux flywheels as stable topological matter configurations
- Gauged Hopf lattice and porous vacuum sponge
- Emergent $W_g = 350/\\pi$ alarm threshold and burst–reset clock dynamics
- Observer synchronization and testable predictions

**Anchor constant:** $W_g = 350/\\pi \\approx 111.40846$
""",
    ),
    PaperEntry(
        key="lagrangian",
        title="Lagrangian Derivation",
        description="Lagrangian formulation of the gauged Hopf lattice and flux flywheel dynamics.",
        filename="Lagrangian_Derivation.pdf",
        summary_md="""
**Scope:** Effective Lagrangian for the gauged Hopf lattice.

**Covers:**
- Field variables for flux flywheels on the lattice
- Gauge coupling, twist accumulation, and braiding terms
- Derivation path from geometry → equations of motion → simulation invariants
- Connection to the $W_g$ burst threshold in *GW_Burst_Threshold*
""",
    ),
    PaperEntry(
        key="relativistic",
        title="Relativistic Completion",
        description="Relativistic extension of the topological flux framework.",
        filename="Relativistic_Completion.pdf",
        summary_md="""
**Scope:** Relativistic extension of the topological flux substrate.

**Covers:**
- Lorentz-compatible formulation of the gauged lattice
- Flux flywheel dynamics at relativistic twist rates
- Completion of the TOE framework beyond the non-relativistic core
""",
    ),
    PaperEntry(
        key="observer_sync",
        title="Observer Synchronization",
        description="Phase holonomy between linked fibers and observer-linked non-locality.",
        filename="Observer_Synchronization.pdf",
        summary_md="""
**Scope:** Observer-linked phase holonomy on the Hopf lattice.

**Covers:**
- Why embedded observers may not detect every burst as an external signal
- Phase holonomy damping between linked S¹ fibers
- Non-local coherence predictions and null-result interpretation
""",
    ),
    PaperEntry(
        key="gw_echo",
        title="Gravitational Wave Echo",
        description="GW echo signatures predicted by the porous-vacuum flux model.",
        filename="GW_Echo.pdf",
        summary_md="""
**Scope:** Gravitational-wave echo phenomenology from the porous vacuum.

**Covers:**
- Echo timing and amplitude tied to lattice boundary conditions
- Flux-discharge events after $W_g$ threshold crossings
- Observational signatures distinguishable from standard GR ringdown
""",
    ),
    PaperEntry(
        key="gw_echo_derivation",
        title="GW Echo Derivation",
        description="Derivation of echo timing and amplitude from Hopf-lattice boundary conditions.",
        filename="GW_Echo_Derivation.pdf",
        summary_md="""
**Scope:** Mathematical derivation companion to *GW Echo*.

**Covers:**
- Hopf-lattice boundary conditions → echo delay formulae
- Amplitude scaling with gauged twist and braiding phase
- Step-by-step link from simulation invariants to GW observables
""",
    ),
    PaperEntry(
        key="gw_burst",
        title="GW Burst Threshold",
        description="Burst threshold conditions for gravitational-wave flux discharge events.",
        filename="GW_Burst_Threshold.pdf",
        summary_md="""
**Scope:** Burst threshold and discharge conditions for GW flux events.

**Covers:**
- Critical accumulated twist $S_{\\text{crit}} = W_g = 350/\\pi$
- Topological instability trigger and punctuated release
- Sawtooth accumulation–reset cycle as a universal clock mechanism
- Links to RubikConeConduit simulation reproducibility
""",
    ),
)


def resolve_paper_path(entry: PaperEntry) -> Path | None:
    """Locate a paper PDF in runtime assets or repo-root papers/ with alias fallback."""
    candidates = FILENAME_ALIASES.get(entry.filename, (entry.filename,))
    for directory in PAPERS_SEARCH_DIRS:
        if not directory.is_dir():
            continue
        for name in candidates:
            path = directory / name
            if path.is_file():
                return path.resolve()
    return None


def discover_paper_pdfs() -> list[Path]:
    """All PDF files present in runtime and source paper directories."""
    seen: set[str] = set()
    found: list[Path] = []
    for directory in PAPERS_SEARCH_DIRS:
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.pdf"), key=lambda p: p.name.lower()):
            if path.name not in seen:
                seen.add(path.name)
                found.append(path.resolve())
    return found


def paper_missing_md(entry: PaperEntry) -> str:
    """Markdown shown when a catalogued PDF is absent."""
    discovered = ", ".join(f"`{p.name}`" for p in discover_paper_pdfs()) or "*(none)*"
    aliases = ", ".join(f"`{n}`" for n in FILENAME_ALIASES.get(entry.filename, (entry.filename,)))
    return f"""
**PDF not found on this Space.**

- Expected: `{entry.filename}`
- Also tried: {aliases}
- Found on disk: {discovered}

Sync from [kingdom_come/papers]({KINGDOM_PAPERS_REPO}) or [toe/papers]({TOE_PAPERS_REPO}).
"""