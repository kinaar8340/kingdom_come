"""Observations tab content."""

from pathlib import Path

from app.pages.observations import (
    CATATUMBO_GALLERY,
    INVESTIGATION_1_MD,
    INVESTIGATION_2_MD,
    INVESTIGATION_3_HOOK_MD,
    INVESTIGATION_3_NUMERICAL_MD,
    INVESTIGATION_3_SYNC_MD,
    INVESTIGATION_3_TOE_MD,
    JUPITER_GALLERY,
    OBSERVATIONS_FOOTER_MD,
    OBSERVATIONS_INTRO_MD,
    THREEBODY_FRAMING_IMAGE,
    THREEBODY_RESONATORS_IMAGE,
    THREEBODY_SYNC_IMAGE,
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


def test_investigation_2_jupiter_content():
    assert "Great Red Spot" in INVESTIGATION_2_MD
    assert "macroscopic Hopfion" in INVESTIGATION_2_MD


def test_investigation_3_threebody_content():
    assert "three-body" in INVESTIGATION_3_HOOK_MD.lower()
    assert "collective attractors" in INVESTIGATION_3_HOOK_MD
    assert "T^3" in INVESTIGATION_3_TOE_MD
    assert "48" in INVESTIGATION_3_NUMERICAL_MD
    assert "STRONG" in INVESTIGATION_3_NUMERICAL_MD
    assert "Pointer synchronization" in INVESTIGATION_3_SYNC_MD
    assert "Celestial mechanics" in INVESTIGATION_3_SYNC_MD


def test_observation_images_exist():
    for gallery in (CATATUMBO_GALLERY, JUPITER_GALLERY):
        assert len(gallery) == 3
        for path, _caption in gallery:
            assert path.is_file(), f"missing {path}"
            assert path.stat().st_size > 5000
    for path in (
        THREEBODY_FRAMING_IMAGE,
        THREEBODY_RESONATORS_IMAGE,
        THREEBODY_SYNC_IMAGE,
    ):
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 5000


def test_observations_footer_living_document():
    assert "living document" in OBSERVATIONS_FOOTER_MD