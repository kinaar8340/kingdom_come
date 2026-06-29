"""Bitcoin Pi Cycle Top — Investigation 8."""

from app.pages.bitcoin_pi_cycle_observations import (
    BITCOIN_PI_GALLERY,
    INVESTIGATION_8_ACCORDION_TITLE,
    INVESTIGATION_8_MD,
)


def test_investigation_8_title():
    assert "Bitcoin Pi Cycle" in INVESTIGATION_8_ACCORDION_TITLE
    assert "350/π" in INVESTIGATION_8_ACCORDION_TITLE


def test_investigation_8_content():
    assert "111.408" in INVESTIGATION_8_MD
    assert "meta_optimize_invariants" in INVESTIGATION_8_MD
    assert "TRUE EMERGENCE ACHIEVED" in INVESTIGATION_8_MD
    assert "global pointer" in INVESTIGATION_8_MD.lower()
    assert "topological protection" in INVESTIGATION_8_MD.lower()


def test_bitcoin_pi_gallery_images_exist():
    assert len(BITCOIN_PI_GALLERY) == 3
    for path, caption in BITCOIN_PI_GALLERY:
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 5000
        assert caption