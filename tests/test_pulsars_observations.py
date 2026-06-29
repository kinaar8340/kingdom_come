"""Pulsars PTA — Investigation 10."""

from app.pages.pulsars_observations import (
    INVESTIGATION_10_ACCORDION_TITLE,
    INVESTIGATION_10_MD,
    META_OPTIMIZER_URL,
    PULSARS_GALLERY,
    REFERENCE_PULSAR_HZ,
    pulsar_quick_check,
)


def test_investigation_10_title():
    assert "Pulsars" in INVESTIGATION_10_ACCORDION_TITLE
    assert "350/π" in INVESTIGATION_10_ACCORDION_TITLE


def test_investigation_10_content():
    assert "Hellings" in INVESTIGATION_10_MD
    assert "716" in INVESTIGATION_10_MD
    assert "6.427" in INVESTIGATION_10_MD
    assert "616" in INVESTIGATION_10_MD
    assert META_OPTIMIZER_URL in INVESTIGATION_10_MD
    assert "NANOGrav" in INVESTIGATION_10_MD


def test_pulsars_gallery_images_exist():
    assert len(PULSARS_GALLERY) == 3
    for path, caption in PULSARS_GALLERY:
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 5000
        assert caption


def test_pulsar_quick_check_716_hz():
    out = pulsar_quick_check(REFERENCE_PULSAR_HZ)
    assert "6.4268" in out
    assert "18,616" in out


def test_pulsar_quick_check_invalid():
    assert "positive" in pulsar_quick_check(0).lower()