"""Showcase tab assets and HTML."""

from pathlib import Path

from app.pages.showcase import SHOWCASE_ASSET, SHOWCASE_HTML

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "app" / "assets" / "showcase"

EXPECTED = (
    "kingdom.png",
    "six_string_optimizer.png",
    "staging.png",
    "qvpic.png",
    "hopf_flux_bubble.png",
    "orbital_braille_vqc.png",
    "mystery.png",
)


def test_showcase_thumbnails_exist():
    for name in EXPECTED:
        path = ASSET_DIR / name
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 2000


def test_showcase_html_references_all_thumbnails():
    for name in EXPECTED:
        assert f"{SHOWCASE_ASSET}/{name}" in SHOWCASE_HTML
    assert "kc-no-img" not in SHOWCASE_HTML
    assert SHOWCASE_HTML.count("<img ") == 7


def test_showcase_links_are_hf_spaces_only():
    assert "github.com" not in SHOWCASE_HTML
    assert SHOWCASE_HTML.count("huggingface.co/spaces/kinaar111/") == 7
    assert "kinaar111/spaces" in SHOWCASE_HTML