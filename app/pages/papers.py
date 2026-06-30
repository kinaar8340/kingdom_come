"""Papers tab — TOE manuscripts from the toe repo."""

from __future__ import annotations

from dataclasses import dataclass
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
        filename="Aarons_TOE_Complete.pdf",
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


def _missing_paper_html(entry: PaperEntry) -> str:
    """User-visible error when a catalogued PDF is absent from the Space."""
    discovered = ", ".join(p.name for p in discover_paper_pdfs()) or "(none)"
    return f"""
<div class="kc-paper-viewer kc-paper-missing">
  <p><strong>{entry.title}</strong> — PDF not found on this Space.</p>
  <p>Expected: <code>{entry.path}</code></p>
  <p>Found in <code>app/assets/papers/</code>: {discovered}</p>
  <p>Upload the missing PDF to the Space repo or download from
     <a href="{TOE_PAPERS_REPO}" target="_blank" rel="noopener">toe/papers</a>.</p>
</div>
"""


def paper_viewer_html(entry: PaperEntry) -> str:
    """Inline PDF viewer served via Gradio allowed_paths (HF-safe)."""
    path = entry.path
    if not path.is_file():
        return _missing_paper_html(entry)

    url = paper_file_url(path)
    return f"""
<div class="kc-paper-viewer">
  <div class="kc-paper-toolbar">
    <strong>{entry.title}</strong>
    <a href="{url}" target="_blank" rel="noopener">Open PDF ↗</a>
  </div>
  <iframe class="kc-paper-frame" src="{url}" title="{entry.title}"></iframe>
  <p class="kc-paper-fallback">
    PDF not rendering inline?
    <a href="{url}" target="_blank" rel="noopener">Open in new tab</a>
    or use <strong>Download PDF</strong> below.
  </p>
</div>
"""


def papers_index_html() -> str:
    """Sidebar-style index of all papers."""
    cards = []
    for entry in PAPER_ENTRIES:
        if not entry.path.is_file():
            continue
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
  <p class="kc-paper-index-lead">All manuscripts ({len(cards)} PDFs) ·
     <a href="{TOE_PAPERS_REPO}" target="_blank" rel="noopener">source repo</a></p>
  {''.join(cards)}
</div>
"""


def load_paper(paper_key: str) -> tuple[str | None, str, str]:
    """Return file path, viewer HTML, and description for a selected paper."""
    entry = PAPERS_BY_KEY.get(paper_key, PAPER_ENTRIES[0])
    if not entry.path.is_file():
        return None, _missing_paper_html(entry), entry.description
    return str(entry.path.resolve()), paper_viewer_html(entry), entry.description