"""φ-e-π Emergent Signature Mystery — Investigation 6."""

from app.pages.phi_e_pi_mystery import (
    INVESTIGATION_6_ACCORDION_TITLE,
    INVESTIGATION_6_MD,
    PHI_E_PI_GALLERY,
)


def test_investigation_6_title():
    assert "φ-e-π" in INVESTIGATION_6_ACCORDION_TITLE


def test_investigation_6_content():
    assert r"$\phi^2 + e^2 \approx \pi^2$" in INVESTIGATION_6_MD
    assert "0.137486" in INVESTIGATION_6_MD
    assert "31.0" in INVESTIGATION_6_MD
    assert "3, 6, 9" in INVESTIGATION_6_MD
    assert "kinaar8340/mystery" in INVESTIGATION_6_MD


def test_phi_e_pi_gallery_images_exist():
    assert len(PHI_E_PI_GALLERY) == 3
    paths = {p for p, _ in PHI_E_PI_GALLERY}
    assert len(paths) == 3
    for path, caption in PHI_E_PI_GALLERY:
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 5000
        assert caption