"""Papers tab assets, summaries, and PDF page rendering."""

from pathlib import Path

from app.pages.papers import (
    PAPER_ENTRIES,
    discover_paper_pdfs,
    get_paper_summary,
    get_pdf_page_images,
    load_all_paper_galleries,
    load_paper_gallery,
    paper_missing_md,
    paper_summary_md,
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


def test_paper_summary_and_markdown():
    summary = get_paper_summary("toe_complete")
    assert summary["title"] == "Aaron's TOE — Complete"
    assert summary["covers"]
    assert summary["anchor"]
    md = paper_summary_md("toe_complete")
    assert "**Scope:**" in md
    assert "350" in md


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


def test_pdf_page_images_for_complete_toe():
    images = get_pdf_page_images("toe_complete", max_pages=2, dpi=72)
    assert len(images) == 2
    assert images[0].size[0] > 100
    assert images[0].size[1] > 100


def test_load_paper_gallery_matches_images():
    gallery = load_paper_gallery("lagrangian")
    assert len(gallery) >= 1
    assert gallery[0].width > 0


def test_load_all_paper_galleries():
    galleries = load_all_paper_galleries()
    assert len(galleries) == len(PAPER_ENTRIES)
    assert all(len(g) >= 1 for g in galleries)