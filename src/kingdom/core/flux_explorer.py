"""Combined flux flywheel + element explorer."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import plotly.graph_objects as go

from kingdom.core.elements import EXPLORER_Z_MAX, NOBLE_GAS_Z, get_element, is_explorable_element
from kingdom.core.flux_flywheel import map_z_to_flywheel
from kingdom.viz.electron_cloud import build_chemistry_vs_toe_figure, build_electron_cloud_figure
from kingdom.viz.hopf_plotly import kingdom_dark_theme
from kingdom.viz.magic_island import build_magic_island_heatmap

_ASSETS = Path(__file__).resolve().parents[3] / "app" / "assets" / "elements"
_SUPERHEAVY_ASSETS = Path(__file__).resolve().parents[3] / "app" / "assets" / "superheavy"
_IMAGINE_ASSETS = Path(__file__).resolve().parents[3] / "app" / "assets" / "elements_imagine"
_LEGACY_ASSETS = Path(__file__).resolve().parents[3] / "app" / "assets" / "noble_gases"


def _placeholder_figure(message: str, height: int = 300) -> go.Figure:
    fig = go.Figure()
    theme = kingdom_dark_theme()
    fig.update_layout(
        **theme,
        height=height,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=13, color="#8ecae6"),
    )
    return fig


@lru_cache(maxsize=256)
def _cached_electron_cloud(z: int, stability: float) -> go.Figure:
    element = get_element(z)
    if element is None:
        return _placeholder_figure(f"No element data for Z = {z}")
    return build_electron_cloud_figure(element, stability_score=stability)


@lru_cache(maxsize=256)
def _cached_compare_figure(z: int, stability: float) -> go.Figure:
    element = get_element(z)
    if element is None:
        return _placeholder_figure("No chemistry comparison available", height=165)
    return build_chemistry_vs_toe_figure(element, stability)


@lru_cache(maxsize=256)
def _cached_magic_island(z: int) -> go.Figure:
    return build_magic_island_heatmap(z)


def flux_metrics_table(flywheel: dict) -> list[list[str]]:
    """Key-value rows for the flux metrics Dataframe panel."""
    return [
        ["Stability score", str(flywheel["stability_score"])],
        ["Class", flywheel["stability_class"]],
        ["δω", str(flywheel["delta_omega"])],
        ["ω_L", str(flywheel["omega_L"])],
        ["ω_R", str(flywheel["omega_R"])],
        ["Gauge strength", str(flywheel["gauge_strength"])],
        ["Layers", str(flywheel["num_layers"])],
        ["Polarities", str(flywheel["num_polarities"])],
        ["pseudo_Z (sweep ID)", str(flywheel["pseudo_Z"])],
        ["Notes", flywheel["notes"]],
        ["Reference", flywheel["sweep_reference"]],
    ]


def element_art_path(z: int) -> str | None:
    """Return path to pre-generated element artwork PNG, or None."""
    el = get_element(z)
    if el is None:
        return None
    folders: list[Path] = []
    if el.is_synthetic:
        folders.extend([_IMAGINE_ASSETS / "superheavy", _SUPERHEAVY_ASSETS])
    folders.extend([_IMAGINE_ASSETS, _ASSETS, _LEGACY_ASSETS])
    for folder in folders:
        for name in (el.symbol.lower(), el.symbol):
            path = folder / f"{name}.png"
            if path.is_file():
                return str(path)
    return None


def noble_gas_art_path(z: int) -> str | None:
    """Backward-compatible alias — artwork exists for all Z when assets are generated."""
    return element_art_path(z)


def explore_flux_element(z: int) -> dict:
    """Full Flux Flywheel tab payload for atomic number Z."""
    z = max(1, min(EXPLORER_Z_MAX, int(z)))
    flywheel = map_z_to_flywheel(z)
    element = get_element(z) if is_explorable_element(z) else None
    stability = flywheel["stability_score"]

    return {
        "z": z,
        "flywheel": flywheel,
        "element": element,
        "metrics_table": flux_metrics_table(flywheel),
        "cloud_fig": _cached_electron_cloud(z, stability),
        "compare_fig": _cached_compare_figure(z, stability),
        "magic_island": _cached_magic_island(z),
        "element_art": element_art_path(z),
        "noble_gas_art": element_art_path(z),
        "is_noble": z in NOBLE_GAS_Z,
        "is_magic": element.is_magic_number if element else False,
        "is_synthetic": element.is_synthetic if element else False,
        "is_pseudo_z": z == 129,
    }