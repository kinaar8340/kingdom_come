"""Papers tab — TOE manuscripts from the toe repo."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

PAPERS_ASSET = "app/assets/papers"
_REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = Path(__file__).resolve().parents[1] / "assets" / "papers"
PAPERS_SOURCE_DIR = _REPO_ROOT / "papers"
TOE_PAPERS_REPO = "https://github.com/kinaar8340/toe/tree/main/papers"
KINGDOM_PAPERS_REPO = "https://github.com/kinaar8340/kingdom_come/tree/main/papers"

# Canonical runtime dir first; repo-root papers/ is a fallback source tree.
PAPERS_SEARCH_DIRS: tuple[Path, ...] = (PAPERS_DIR, PAPERS_SOURCE_DIR)

# Accept legacy apostrophe filename if the canonical name is absent.
FILENAME_ALIASES: dict[str, tuple[str, ...]] = {
    "Aarons_TOE_Complete.pdf": ("Aarons_TOE_Complete.pdf", "Aaron's_TOE_Complete.pdf"),
}

PAPERS_INTRO_MD = """
## Papers

Manuscripts from Aaron's Hopf Fibration Theory of Everything — sourced from the
[toe/papers](https://github.com/kinaar8340/toe/tree/main/papers) and
[kingdom_come/papers](https://github.com/kinaar8340/kingdom_come/tree/main/papers) repositories.
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
        """Canonical expected path (may not exist — use resolve_paper_path)."""
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


def paper_choices() -> list[tuple[str, str]]:
    """Dropdown labels mapped to paper keys (available papers first)."""
    available = [(entry.title, entry.key) for entry in PAPER_ENTRIES if resolve_paper_path(entry)]
    if available:
        return available
    return [(entry.title, entry.key) for entry in PAPER_ENTRIES]


def default_paper_key() -> str:
    for entry in PAPER_ENTRIES:
        if resolve_paper_path(entry):
            return entry.key
    return PAPER_ENTRIES[0].key


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


def paper_file_url(path: Path) -> str:
    """Gradio static file URL for direct download / new tab."""
    return f"/gradio_api/file={quote(str(path.resolve()), safe='/')}"


@lru_cache(maxsize=16)
def _pdf_data_uri(resolved_path: str) -> str:
    """Base64 data URI for inline embed (Firefox-friendly srcdoc iframe)."""
    path = Path(resolved_path)
    if not path.is_file():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:application/pdf;base64,{encoded}"


def _missing_paper_html(entry: PaperEntry) -> str:
    """User-visible error when a catalogued PDF is absent from the Space."""
    discovered = ", ".join(p.name for p in discover_paper_pdfs()) or "(none)"
    aliases = ", ".join(FILENAME_ALIASES.get(entry.filename, (entry.filename,)))
    return f"""
<div class="kc-paper-viewer kc-paper-missing">
  <p><strong>{entry.title}</strong> — PDF not found on this Space.</p>
  <p>Expected in <code>app/assets/papers/</code>: <code>{entry.filename}</code></p>
  <p>Also tried aliases: {aliases}</p>
  <p>Found on disk: {discovered}</p>
  <p>Upload the missing PDF to <code>app/assets/papers/</code> or sync from
     <a href="{KINGDOM_PAPERS_REPO}" target="_blank" rel="noopener">kingdom_come/papers</a>
     · <a href="{TOE_PAPERS_REPO}" target="_blank" rel="noopener">toe/papers</a></p>
</div>
"""


def paper_viewer_html(entry: PaperEntry) -> str:
    """Inline PDF viewer with Firefox embed + Brave new-tab fallback."""
    path = resolve_paper_path(entry)
    if path is None:
        return _missing_paper_html(entry)

    url = paper_file_url(path)
    data_uri = _pdf_data_uri(str(path))

    # srcdoc + base64: reliable inline view in Firefox and most Chromium builds.
    embed_html = (
        f"<embed src='{data_uri}' type='application/pdf' title='{entry.title}' />"
        if data_uri
        else f"<p style='color:#ddd;padding:2rem;text-align:center;'>"
        f"Inline embed unavailable — use <strong>Open PDF in new tab</strong>.</p>"
    )
    srcdoc = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<style>html,body{margin:0;height:100%;overflow:hidden;background:#0d1f35;}"
        "embed{width:100%;height:100%;border:0;}</style></head><body>"
        f"{embed_html}"
        "</body></html>"
    )
    safe_srcdoc = srcdoc.replace("&", "&amp;").replace('"', "&quot;")

    return f"""
<div class="kc-paper-viewer">
  <div class="kc-paper-toolbar">
    <strong>{entry.title}</strong>
    <a class="kc-paper-open-btn" href="{url}" target="_blank" rel="noopener">
      Open PDF in new tab →
    </a>
  </div>
  <iframe class="kc-paper-frame" srcdoc="{safe_srcdoc}" title="{entry.title}"></iframe>
  <div class="kc-paper-brave-hint">
    <strong>PDF not loading in Brave or other privacy browsers?</strong><br>
    Click <strong>Open PDF in new tab</strong> above — that bypasses strict iframe
    shields and usually works perfectly. You can also use <strong>Download PDF</strong> below.
  </div>
</div>
"""


def papers_index_html() -> str:
    """Sidebar-style index of all papers."""
    cards = []
    for entry in PAPER_ENTRIES:
        path = resolve_paper_path(entry)
        if path is None:
            continue
        url = paper_file_url(path)
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
     <a href="{KINGDOM_PAPERS_REPO}" target="_blank" rel="noopener">kingdom_come/papers</a></p>
  {''.join(cards)}
</div>
"""


def load_paper(paper_key: str) -> tuple[str | None, str, str]:
    """Return file path, viewer HTML, and description for a selected paper."""
    entry = PAPERS_BY_KEY.get(paper_key, PAPER_ENTRIES[0])
    path = resolve_paper_path(entry)
    if path is None:
        return None, _missing_paper_html(entry), entry.description
    return str(path), paper_viewer_html(entry), entry.description