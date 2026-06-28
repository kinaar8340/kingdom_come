"""Observations tab content."""

from pathlib import Path

from app.pages.higgs_observations import HIGGS_GALLERY, INVESTIGATION_4_MD
from app.pages.observations import (
    CATATUMBO_GALLERY,
    INVESTIGATION_1_MD,
    INVESTIGATION_2_MD,
    INVESTIGATION_3_MD,
    JUPITER_GALLERY,
    OBSERVATIONS_FOOTER_MD,
    OBSERVATIONS_INTRO_MD,
    THREEBODY_GALLERY,
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
    assert "three-body" in INVESTIGATION_3_MD.lower()
    assert "collective attractors" in INVESTIGATION_3_MD
    assert "T^3" in INVESTIGATION_3_MD
    assert "48" in INVESTIGATION_3_MD
    assert "STRONG" in INVESTIGATION_3_MD
    assert "Pointer synchronization" in INVESTIGATION_3_MD
    assert "Celestial mechanics" in INVESTIGATION_3_MD


def test_investigation_4_higgs_content():
    assert "Higgs Mode" in INVESTIGATION_4_MD
    assert "Shukla" in INVESTIGATION_4_MD
    assert "32" in INVESTIGATION_4_MD
    assert len(HIGGS_GALLERY) == 3


def test_observation_galleries_exist():
    for gallery in (CATATUMBO_GALLERY, JUPITER_GALLERY, THREEBODY_GALLERY, HIGGS_GALLERY):
        assert len(gallery) == 3
        for path, caption in gallery:
            assert path.is_file(), f"missing {path}"
            assert path.stat().st_size > 5000
            assert caption


def test_observations_footer_living_document():
    assert "living document" in OBSERVATIONS_FOOTER_MD