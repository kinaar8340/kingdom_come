"""Higgs Mode perovskite observations tab."""

from app.pages.higgs_observations import (
    HIGGS_GALLERY,
    HIGGS_HEADER_MD,
    HIGGS_SECTION_1_MD,
    HIGGS_SECTION_2_MD,
    HIGGS_SECTION_3_MD,
    HIGGS_SECTION_6_MD,
)


def test_higgs_header_metadata():
    assert "First Optically Driven Higgs Mode" in HIGGS_HEADER_MD
    assert "Shukla et al." in HIGGS_HEADER_MD
    assert "Aaron Kinder" in HIGGS_HEADER_MD
    assert "June 2026" in HIGGS_HEADER_MD
    assert "10.1038/s41563-025-02433-1" in HIGGS_HEADER_MD


def test_higgs_experimental_context():
    assert "(BA)₂PbI₄" in HIGGS_SECTION_1_MD or "(BA)" in HIGGS_SECTION_1_MD
    assert "4×" in HIGGS_SECTION_1_MD
    assert "metastable tetragonal" in HIGGS_SECTION_1_MD


def test_higgs_model_connection():
    assert "two-gyro" in HIGGS_SECTION_2_MD.lower()
    assert "θ_{\\rm crit}" in HIGGS_SECTION_2_MD or "theta" in HIGGS_SECTION_2_MD.lower()
    assert "pointer" in HIGGS_SECTION_2_MD.lower()


def test_higgs_numerical_prototype():
    assert "32" in HIGGS_SECTION_3_MD
    assert "0.0278" in HIGGS_SECTION_3_MD
    assert "0.1944" in HIGGS_SECTION_3_MD
    assert "FFT spectrum" in HIGGS_SECTION_3_MD


def test_higgs_limitations():
    assert "Limitations" in HIGGS_SECTION_6_MD
    assert "living document" in HIGGS_SECTION_6_MD


def test_higgs_gallery_images_exist():
    assert len(HIGGS_GALLERY) == 3
    for path, caption in HIGGS_GALLERY:
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 5000
        assert caption