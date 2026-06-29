"""TLS Fichte & Buche trees — Investigation 7."""

from app.pages.tls_trees_observations import (
    INVESTIGATION_7_ACCORDION_TITLE,
    INVESTIGATION_7_MD,
    TLS_TREES_GALLERY,
)


def test_investigation_7_title():
    assert "TLS Point Clouds" in INVESTIGATION_7_ACCORDION_TITLE
    assert "350/π" in INVESTIGATION_7_ACCORDION_TITLE


def test_investigation_7_content():
    assert "Fichte/35_1.txt" in INVESTIGATION_7_MD
    assert "Buche/3.pts" in INVESTIGATION_7_MD
    assert "10.25625/FOHUJM" in INVESTIGATION_7_MD
    assert "111.408" in INVESTIGATION_7_MD
    assert "CloudCompare" in INVESTIGATION_7_MD


def test_tls_trees_gallery_images_exist():
    assert len(TLS_TREES_GALLERY) == 3
    for path, caption in TLS_TREES_GALLERY:
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 5000
        assert caption