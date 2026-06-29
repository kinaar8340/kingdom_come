"""Schumann Prediction Experiment — Observations Investigation 5."""

from app.pages.schumann_observations import (
    INVESTIGATION_5_ACCORDION_TITLE,
    INVESTIGATION_5_MD,
    SCHUMANN_GALLERY,
)


def test_investigation_5_title():
    assert "Schumann Prediction Experiment" in INVESTIGATION_5_ACCORDION_TITLE


def test_investigation_5_content():
    assert "111.408" in INVESTIGATION_5_MD
    assert "350/\\pi" in INVESTIGATION_5_MD
    assert "vortex_sync" in INVESTIGATION_5_MD
    assert "June 20–22" in INVESTIGATION_5_MD or "June 20-22" in INVESTIGATION_5_MD
    assert "~21" in INVESTIGATION_5_MD
    assert "Tomsk" in INVESTIGATION_5_MD
    assert "2068968094270378465" in INVESTIGATION_5_MD
    assert "121" in INVESTIGATION_5_MD


def test_schumann_gallery_images_exist():
    assert len(SCHUMANN_GALLERY) == 3
    for path, caption in SCHUMANN_GALLERY:
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 5000
        assert caption