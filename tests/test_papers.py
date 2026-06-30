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
    resolve_paper_path,
)

ROOT = Path(__file__).resolve().parents[1]


def test_all_paper_pdfs_exist():
    pdfs = discover_paper_pdfs()
    assert len(pdfs) >= 7
    for entry in PAPER_ENTRIES:
        path = resolve_paper_path(entry)
        assert path is not None, f"missing {entry.filename}"
        assert path.stat().st_size > 10_000


def test_paper_entries_match_discovered_pdfs():
    discovered = {p.name for p in discover_paper_pdfs()}
    catalogued = {entry.filename for entry in PAPER_ENTRIES}
    assert catalogued.issubset(discovered)
    assert "Aarons_TOE_Complete.pdf" in discovered


def test_paper_viewer_html_and_file_path():
    key = default_paper_key()
    path, html, description = load_paper(key)
    assert path.endswith("Aarons_TOE_Complete.pdf")
    assert "kc-paper-frame" in html
    assert "/gradio_api/file=" in html
    assert "data:application/pdf;base64," not in html
    assert "Theory of Everything" in description


def test_paper_file_url_uses_gradio_path():
    entry = PAPER_ENTRIES[0]
    path = resolve_paper_path(entry)
    assert path is not None
    url = paper_file_url(path)
    assert url.startswith("/gradio_api/file=")
    assert "Aarons_TOE_Complete.pdf" in url


def test_resolve_paper_path_accepts_apostrophe_alias(tmp_path, monkeypatch):
    from app.pages import papers as papers_mod

    assets = tmp_path / "assets"
    assets.mkdir()
    apostrophe = assets / "Aaron's_TOE_Complete.pdf"
    apostrophe.write_bytes(b"%PDF-1.4 test")
    monkeypatch.setattr(papers_mod, "PAPERS_SEARCH_DIRS", (assets,))
    monkeypatch.setattr(papers_mod, "PAPERS_DIR", assets)
    path = resolve_paper_path(PAPER_ENTRIES[0])
    assert path == apostrophe.resolve()


def test_missing_paper_returns_error_html(tmp_path, monkeypatch):
    from app.pages import papers as papers_mod

    missing = tmp_path / "papers"
    missing.mkdir()
    monkeypatch.setattr(papers_mod, "PAPERS_DIR", missing)
    monkeypatch.setattr(papers_mod, "PAPERS_SEARCH_DIRS", (missing,))
    path, html, _ = load_paper(default_paper_key())
    assert path is None
    assert "kc-paper-missing" in html


def test_papers_index_lists_all_entries():
    html = papers_index_html()
    assert html.count('class="kc-paper-card"') == len(PAPER_ENTRIES)
    assert "text-align: left" not in html  # alignment via CSS class
    assert "kc-paper-card-body" in html
    for entry in PAPER_ENTRIES:
        assert entry.title in html