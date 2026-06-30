"""Papers tab assets and accordion content."""

from pathlib import Path

from app.pages.papers import (
    PAPER_ENTRIES,
    PAPERS_DIR,
    discover_paper_pdfs,
    paper_missing_md,
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


def test_each_paper_has_summary():
    for entry in PAPER_ENTRIES:
        assert entry.summary_md.strip()
        assert len(entry.summary_md) > 40


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


def test_missing_paper_markdown(tmp_path, monkeypatch):
    from app.pages import papers as papers_mod

    missing = tmp_path / "papers"
    missing.mkdir()
    monkeypatch.setattr(papers_mod, "PAPERS_DIR", missing)
    monkeypatch.setattr(papers_mod, "PAPERS_SEARCH_DIRS", (missing,))
    md = paper_missing_md(PAPER_ENTRIES[0])
    assert "PDF not found" in md
    assert "Aarons_TOE_Complete.pdf" in md