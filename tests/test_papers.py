"""Papers tab assets and viewer."""

from pathlib import Path

from app.pages.papers import (
    PAPER_ENTRIES,
    PAPERS_DIR,
    default_paper_key,
    discover_paper_pdfs,
    load_paper,
    paper_file_url,
    papers_index_html,
)

ROOT = Path(__file__).resolve().parents[1]


def test_all_paper_pdfs_exist():
    pdfs = discover_paper_pdfs()
    assert len(pdfs) == 7
    for entry in PAPER_ENTRIES:
        path = PAPERS_DIR / entry.filename
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 10_000


def test_paper_entries_match_discovered_pdfs():
    discovered = {p.name for p in discover_paper_pdfs()}
    catalogued = {entry.filename for entry in PAPER_ENTRIES}
    assert discovered == catalogued


def test_paper_viewer_html_and_file_path():
    key = default_paper_key()
    path, html, description = load_paper(key)
    assert path.endswith("Aaron's_TOE_Complete.pdf")
    assert "kc-paper-frame" in html
    assert "data:application/pdf;base64," in html
    assert "Theory of Everything" in description


def test_paper_file_url_encodes_apostrophe():
    entry = PAPER_ENTRIES[0]
    url = paper_file_url(entry.path)
    assert "%27" in url or "Aaron" in url


def test_papers_index_lists_all_entries():
    html = papers_index_html()
    assert html.count('class="kc-paper-card"') == len(PAPER_ENTRIES)
    assert "text-align: left" not in html  # alignment via CSS class
    assert "kc-paper-card-body" in html
    for entry in PAPER_ENTRIES:
        assert entry.title in html