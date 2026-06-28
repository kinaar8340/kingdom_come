"""Papers tab — TOE manuscripts from the toe repo."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

PAPERS_ASSET = "app/assets/papers"
PAPERS_DIR = Path(__file__).resolve().parents[1] / "assets" / "papers"
TOE_PAPERS_REPO = "https://github.com/kinaar8340/toe/tree/main/papers"

PAPERS_INTRO_MD = """
## Papers

Manuscripts from Aaron's Hopf Fibration Theory of Everything — sourced from the
[toe/papers](https://github.com/kinaar8340/toe/tree/main/papers) repository.
Select a paper below to read inline or download the PDF.
"""


@dataclass(frozen=True)
class PaperEntry:
    key: str
    title: str
    description: str
    filename: str

    @property
    def path(self) -> Path:
        return PAPERS_DIR / self.filename


PAPER_ENTRIES: tuple[PaperEntry, ...] = (
    PaperEntry(
        key="toe_complete",
        title="Aaron's TOE — Complete",
        description="Full Theory of Everything manuscript — Hopf fibration backbone, flux flywheels, and emergent physics.",
        filename="Aaron's_TOE_Complete.pdf",
    ),
    PaperEntry(
        key="lagrangian",
        title="Lagrangian Derivation",
        description="Lagrangian formulation of the gauged Hopf lattice and flux flywheel dynamics.",
        filename="Lagrangian_Derivation.pdf",
    ),
    PaperEntry(
        key="relativistic",
        title="Relativistic Completion",
        description="Relativistic extension of the topological flux framework.",
        filename="Relativistic_Completion.pdf",
    ),
    PaperEntry(
        key="observer_sync",
        title="Observer Synchronization",
        description="Phase holonomy between linked fibers and observer-linked non-locality.",
        filename="Observer_Synchronization.pdf",
    ),
    PaperEntry(
        key="gw_echo",
        title="Gravitational Wave Echo",
        description="GW echo signatures predicted by the porous-vacuum flux model.",
        filename="GW_Echo.pdf",
    ),
    PaperEntry(
        key="gw_echo_derivation",
        title="GW Echo Derivation",
        description="Derivation of echo timing and amplitude from Hopf-lattice boundary conditions.",
        filename="GW_Echo_Derivation.pdf",
    ),
    PaperEntry(
        key="gw_burst",
        title="GW Burst Threshold",
        description="Burst threshold conditions for gravitational-wave flux discharge events.",
        filename="GW_Burst_Threshold.pdf",
    ),
)

PAPERS_BY_KEY: dict[str, PaperEntry] = {entry.key: entry for entry in PAPER_ENTRIES}


def paper_choices() -> list[tuple[str, str]]:
    """Dropdown labels mapped to paper keys."""
    return [(entry.title, entry.key) for entry in PAPER_ENTRIES]


def default_paper_key() -> str:
    return PAPER_ENTRIES[0].key


def discover_paper_pdfs() -> list[Path]:
    """All PDF files present in the papers asset directory."""
    return sorted(PAPERS_DIR.glob("*.pdf"), key=lambda p: p.name.lower())


def paper_file_url(path: Path) -> str:
    """Gradio static file URL for an allowed-path PDF."""
    return f"/gradio_api/file={quote(str(path.resolve()), safe='/')}"


@lru_cache(maxsize=16)
def _pdf_data_uri(filename: str) -> str:
    """Base64 data URI — reliable inline PDF rendering inside HF Space iframes."""
    path = PAPERS_DIR / filename
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:application/pdf;base64,{encoded}"


def paper_viewer_html(entry: PaperEntry) -> str:
    """Inline PDF viewer with fallback download link."""
    data_uri = _pdf_data_uri(entry.filename)
    url = paper_file_url(entry.path)
    return f"""
<div class="kc-paper-viewer">
  <div class="kc-paper-toolbar">
    <strong>{entry.title}</strong>
    <a href="{url}" target="_blank" rel="noopener">Download PDF ↗</a>
  </div>
  <embed class="kc-paper-frame" src="{data_uri}" type="application/pdf" title="{entry.title}" />
  <p class="kc-paper-fallback">
    PDF not rendering? Use <strong>Download PDF</strong> above or the file widget below.
  </p>
</div>
"""


def papers_index_html() -> str:
    """Sidebar-style index of all papers."""
    cards = []
    for entry in PAPER_ENTRIES:
        url = paper_file_url(entry.path)
        cards.append(
            f"""
  <a class="kc-paper-card" href="{url}" target="_blank" rel="noopener">
    <span class="kc-paper-card-icon">📄</span>
    <span class="kc-paper-card-body">
      <strong>{entry.title}</strong>
      <em>{entry.description}</em>
    </span>
  </a>"""
        )
    return f"""
<div class="kc-paper-index">
  <p class="kc-paper-index-lead">All manuscripts ({len(PAPER_ENTRIES)} PDFs) ·
     <a href="{TOE_PAPERS_REPO}" target="_blank" rel="noopener">source repo</a></p>
  {''.join(cards)}
</div>
"""


def load_paper(paper_key: str) -> tuple[str, str, str]:
    """Return file path, viewer HTML, and description for a selected paper."""
    entry = PAPERS_BY_KEY.get(paper_key, PAPER_ENTRIES[0])
    return str(entry.path.resolve()), paper_viewer_html(entry), entry.description