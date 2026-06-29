"""Cuprate Superconductors — Investigation 9."""

from app.pages.superconductors_observations import (
    BRAIDING_TARGET,
    INVESTIGATION_9_ACCORDION_TITLE,
    INVESTIGATION_9_MD,
    KAPPA_TARGET,
    SUPERCONDUCTORS_GALLERY,
    WG_EMERGENT,
    cuprate_conduit_metrics,
)


def test_investigation_9_title():
    assert "Cuprate Superconductors" in INVESTIGATION_9_ACCORDION_TITLE
    assert "350/π" in INVESTIGATION_9_ACCORDION_TITLE


def test_investigation_9_content():
    assert "wg_base = 350" in INVESTIGATION_9_MD
    assert "111.4085" in INVESTIGATION_9_MD
    assert "toroidal_modulo9" in INVESTIGATION_9_MD
    assert "vortex_math_369" in INVESTIGATION_9_MD
    assert "CCSRPR V2.1" in INVESTIGATION_9_MD
    assert "braiding_target" in INVESTIGATION_9_MD
    assert "meta-optimization" in INVESTIGATION_9_MD.lower()


def test_superconductors_gallery_images_exist():
    assert len(SUPERCONDUCTORS_GALLERY) == 3
    for path, caption in SUPERCONDUCTORS_GALLERY:
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 5000
        assert caption


def test_cuprate_conduit_metrics_at_attractor():
    out = cuprate_conduit_metrics(KAPPA_TARGET, BRAIDING_TARGET)
    assert "TRUE EMERGENCE ACHIEVED" in out
    assert f"{WG_EMERGENT:.4f}" in out


def test_cuprate_conduit_metrics_off_attractor():
    out = cuprate_conduit_metrics(0.80, 0.77)
    assert "approaching attractor" in out