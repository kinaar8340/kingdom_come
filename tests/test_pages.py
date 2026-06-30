"""Home and Help page content."""

from app.pages.help import (
    HELP_ACRONYMS_MD,
    HELP_CONTROLS_MD,
    HELP_GETTING_STARTED_MD,
    HELP_NAVIGATE_MD,
    HELP_TECH_MD,
)
from app.pages.home import HOME_CLOCK_MD, HOME_EXPLORE_MD, HOME_FOUNDATION_MD, HOME_WG_MD


def test_home_covers_clock_mechanism():
    assert "flux flywheels" in HOME_FOUNDATION_MD
    assert "RubikConeConduit" in HOME_FOUNDATION_MD
    assert "Vision" in HOME_FOUNDATION_MD
    assert "Mathematical Backbone" in HOME_FOUNDATION_MD
    assert "Observer Synchronization" in HOME_FOUNDATION_MD
    assert "dS" in HOME_CLOCK_MD or "S(t)" in HOME_CLOCK_MD
    assert "111.408" in HOME_CLOCK_MD or "350" in HOME_CLOCK_MD
    assert "350" in HOME_WG_MD
    assert "Observations" in HOME_EXPLORE_MD


def test_help_navigate_links_hf_and_github():
    assert "huggingface.co/spaces/kinaar111" in HELP_NAVIGATE_MD
    assert "github.com/kinaar8340" in HELP_NAVIGATE_MD
    assert "Hopf Visualizer" in HELP_NAVIGATE_MD
    assert "acronyms" in HELP_NAVIGATE_MD


def test_help_acronyms_table_has_core_terms():
    for term in ("VQC", "OAM", "TOE", "W_g", "QVPIC", "HFB", "BMGL"):
        assert term in HELP_ACRONYMS_MD
    assert "| Acronym | Stands For | Definition |" in HELP_ACRONYMS_MD
    assert "Vortex Quaternion Conduit" in HELP_ACRONYMS_MD
    assert "Orbital Angular Momentum" in HELP_ACRONYMS_MD


def test_help_getting_started_references_home():
    assert "Home" in HELP_GETTING_STARTED_MD
    assert "Hopf Visualizer" in HELP_GETTING_STARTED_MD


def test_help_controls_and_tech_present():
    assert "WebGL" in HELP_CONTROLS_MD
    assert "Gradio" in HELP_TECH_MD