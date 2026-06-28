"""Observations tab content."""

from pathlib import Path

from app.pages.observations import (
    CATATUMBO_IMAGE,
    INVESTIGATION_1_MD,
    INVESTIGATION_2_MD,
    JUPITER_GALLERY,
    OBSERVATIONS_FOOTER_MD,
    OBSERVATIONS_INTRO_MD,
)

ROOT = Path(__file__).resolve().parents[1]


def test_observations_intro_mentions_winding():
    assert "Synchronicities in Nature" in OBSERVATIONS_INTRO_MD
    assert "350" in OBSERVATIONS_INTRO_MD
    assert "111.40846" in OBSERVATIONS_INTRO_MD


def test_investigation_1_catatumbo_content():
    assert "Catatumbo" in INVESTIGATION_1_MD
    assert "9.344" in INVESTIGATION_1_MD
    assert "Hopfion" in INVESTIGATION_1_MD
    assert "upload.wikimedia.org" not in INVESTIGATION_1_MD


def test_investigation_2_jupiter_content():
    assert "Great Red Spot" in INVESTIGATION_2_MD
    assert "22" in INVESTIGATION_2_MD
    assert "macroscopic Hopfion" in INVESTIGATION_2_MD
    assert "upload.wikimedia.org" not in INVESTIGATION_2_MD


def test_observation_images_exist():
    assert CATATUMBO_IMAGE.is_file()
    assert CATATUMBO_IMAGE.stat().st_size > 5000
    assert len(JUPITER_GALLERY) == 3
    for path, _caption in JUPITER_GALLERY:
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 5000


def test_observations_footer_living_document():
    assert "living document" in OBSERVATIONS_FOOTER_MD