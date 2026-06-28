"""Observations tab content."""

from app.pages.observations import (
    INVESTIGATION_1_MD,
    INVESTIGATION_2_MD,
    OBSERVATIONS_FOOTER_MD,
    OBSERVATIONS_INTRO_MD,
)


def test_observations_intro_mentions_winding():
    assert "Synchronicities in Nature" in OBSERVATIONS_INTRO_MD
    assert "350" in OBSERVATIONS_INTRO_MD
    assert "111.40846" in OBSERVATIONS_INTRO_MD


def test_investigation_1_catatumbo_content():
    assert "Catatumbo" in INVESTIGATION_1_MD
    assert "9.344" in INVESTIGATION_1_MD
    assert "Hopfion" in INVESTIGATION_1_MD
    assert "![Catatumbo" in INVESTIGATION_1_MD


def test_investigation_2_jupiter_content():
    assert "Great Red Spot" in INVESTIGATION_2_MD
    assert "22" in INVESTIGATION_2_MD
    assert "macroscopic Hopfion" in INVESTIGATION_2_MD
    assert "![Jupiter" in INVESTIGATION_2_MD


def test_observations_footer_living_document():
    assert "living document" in OBSERVATIONS_FOOTER_MD