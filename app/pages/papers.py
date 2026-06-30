"""Papers tab — PDF pages rendered as inline images (reliable in all browsers)."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from io import BytesIO
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

_REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = Path(__file__).resolve().parents[1] / "assets" / "papers"
PAPERS_SOURCE_DIR = _REPO_ROOT / "papers"
TOE_PAPERS_REPO = "https://github.com/kinaar8340/toe/tree/main/papers"
KINGDOM_PAPERS_REPO = "https://github.com/kinaar8340/kingdom_come/tree/main/papers"

PAPERS_SEARCH_DIRS: tuple[Path, ...] = (PAPERS_DIR, PAPERS_SOURCE_DIR)
FILENAME_ALIASES: dict[str, tuple[str, ...]] = {
    "Aarons_TOE_Complete.pdf": ("Aarons_TOE_Complete.pdf", "Aaron's_TOE_Complete.pdf"),
}

DEFAULT_MAX_PAGES = 12
DEFAULT_DPI = 130

PAPERS_INTRO_MD = """
## Papers

Manuscripts from Aaron's Hopf Fibration Theory of Everything — sourced from
[toe/papers](https://github.com/kinaar8340/toe/tree/main/papers) and
[kingdom_come/papers](https://github.com/kinaar8340/kingdom_come/tree/main/papers).

Expand any section for a summary, click **Load Paper Pages** for an inline page
preview (rendered as images — works in Brave and all browsers), or use
**Download PDF** for the full manuscript.
"""


@dataclass(frozen=True)
class PaperEntry:
    key: str
    title: str
    description: str
    filename: str
    scope: str
    covers: tuple[str, ...]
    anchor: str | None = None

    @property
    def path(self) -> Path:
        return PAPERS_DIR / self.filename


PAPER_ENTRIES: tuple[PaperEntry, ...] = (
    PaperEntry(
        key="toe_complete",
        title="Aaron's TOE — Complete",
        description="Full Theory of Everything manuscript.",
        filename="Aarons_TOE_Complete.pdf",
        scope="Complete Theory of Everything manuscript.",
        covers=(
            "Hopf fibration backbone (S³ → S²) and quaternion structure",
            "Flux flywheels as stable topological matter configurations",
            "Gauged Hopf lattice and porous vacuum sponge",
            "Emergent $W_g = 350/\\pi$ alarm threshold and burst–reset dynamics",
            "Observer synchronization and testable predictions",
        ),
        anchor="$W_g = 350/\\pi \\approx 111.40846$",
    ),
    PaperEntry(
        key="lagrangian",
        title="Lagrangian Derivation",
        description="Lagrangian formulation of the gauged Hopf lattice.",
        filename="Lagrangian_Derivation.pdf",
        scope="Effective Lagrangian for the gauged Hopf lattice.",
        covers=(
            "Field variables for flux flywheels on the lattice",
            "Gauge coupling, twist accumulation, and braiding terms",
            "Derivation from geometry to equations of motion",
            "Connection to the $W_g$ burst threshold",
        ),
    ),
    PaperEntry(
        key="relativistic",
        title="Relativistic Completion",
        description="Relativistic extension of the topological flux framework.",
        filename="Relativistic_Completion.pdf",
        scope="Relativistic extension of the topological flux substrate.",
        covers=(
            "Lorentz-compatible gauged lattice formulation",
            "Flux flywheel dynamics at relativistic twist rates",
            "Completion beyond the non-relativistic TOE core",
        ),
    ),
    PaperEntry(
        key="observer_sync",
        title="Observer Synchronization",
        description="Phase holonomy and observer-linked non-locality.",
        filename="Observer_Synchronization.pdf",
        scope="Observer-linked phase holonomy on the Hopf lattice.",
        covers=(
            "Why embedded observers may miss bursts as external signals",
            "Phase holonomy damping between linked S¹ fibers",
            "Non-local coherence predictions and null-result interpretation",
        ),
    ),
    PaperEntry(
        key="gw_echo",
        title="Gravitational Wave Echo",
        description="GW echo signatures from the porous-vacuum flux model.",
        filename="GW_Echo.pdf",
        scope="Gravitational-wave echo phenomenology from the porous vacuum.",
        covers=(
            "Echo timing and amplitude from lattice boundary conditions",
            "Flux-discharge events after $W_g$ threshold crossings",
            "Signatures distinguishable from standard GR ringdown",
        ),
    ),
    PaperEntry(
        key="gw_echo_derivation",
        title="GW Echo Derivation",
        description="Derivation of echo timing and amplitude.",
        filename="GW_Echo_Derivation.pdf",
        scope="Mathematical derivation companion to *GW Echo*.",
        covers=(
            "Hopf-lattice boundary conditions → echo delay formulae",
            "Amplitude scaling with gauged twist and braiding phase",
            "Link from simulation invariants to GW observables",
        ),
    ),
    PaperEntry(
        key="gw_burst",
        title="GW Burst Threshold",
        description="Burst threshold for gravitational-wave flux discharge.",
        filename="GW_Burst_Threshold.pdf",
        scope="Burst threshold and discharge conditions for GW flux events.",
        covers=(
            "Critical accumulated twist $S_{\\text{crit}} = W_g = 350/\\pi$",
            "Topological instability trigger and punctuated release",
            "Sawtooth accumulation–reset clock mechanism",
            "RubikConeConduit simulation reproducibility",
        ),
        anchor="$W_g = 350/\\pi \\approx 111.40846$",
    ),
)

PAPERS_BY_KEY: dict[str, PaperEntry] = {entry.key: entry for entry in PAPER_ENTRIES}


def get_paper_entry(key: str) -> PaperEntry:
    return PAPERS_BY_KEY.get(key, PAPER_ENTRIES[0])


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


def get_paper_summary(key: str) -> dict[str, str | list[str] | None]:
    """Summary data for accordion headers and markdown."""
    entry = get_paper_entry(key)
    return {
        "title": entry.title,
        "scope": entry.scope,
        "covers": list(entry.covers),
        "anchor": entry.anchor,
        "filename": entry.filename,
        "download_label": f"Download — {entry.filename}",
    }


def paper_summary_md(key: str) -> str:
    """Render summary block for a paper accordion."""
    summary = get_paper_summary(key)
    lines = [f"**Scope:** {summary['scope']}", "", "**Covers:**"]
    for item in summary["covers"]:
        lines.append(f"- {item}")
    if summary.get("anchor"):
        lines.extend(["", f"**Anchor constant:** {summary['anchor']}"])
    return "\n".join(lines)


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


@lru_cache(maxsize=32)
def _render_pdf_pages(
    resolved_path: str,
    max_pages: int = DEFAULT_MAX_PAGES,
    dpi: int = DEFAULT_DPI,
) -> tuple[bytes, ...]:
    """Convert PDF pages to PNG byte blobs (cached by path)."""
    pdf_path = Path(resolved_path)
    if not pdf_path.is_file():
        return ()

    try:
        doc = fitz.open(pdf_path)
        pages: list[bytes] = []
        for i in range(min(len(doc), max_pages)):
            pix = doc[i].get_pixmap(dpi=dpi)
            pages.append(pix.tobytes("png"))
        doc.close()
        return tuple(pages)
    except Exception as exc:
        print(f"Error converting PDF {pdf_path.name}: {exc}")
        return ()


def get_pdf_page_images(
    key: str,
    max_pages: int = DEFAULT_MAX_PAGES,
    dpi: int = DEFAULT_DPI,
) -> list[Image.Image]:
    """Convert PDF pages to PIL images for Gradio Gallery."""
    entry = get_paper_entry(key)
    pdf_path = resolve_paper_path(entry)
    if pdf_path is None:
        return []

    png_pages = _render_pdf_pages(str(pdf_path), max_pages=max_pages, dpi=dpi)
    return [Image.open(BytesIO(blob)) for blob in png_pages]


def load_paper_gallery(key: str) -> list[Image.Image]:
    """Gradio callback — inline page preview for a paper."""
    return get_pdf_page_images(key)