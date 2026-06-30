"""Combined flux flywheel + element explorer."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import plotly.graph_objects as go

from kingdom.core.elements import EXPLORER_Z_MAX, NOBLE_GAS_Z, get_element, is_explorable_element
from kingdom.core.experimental_data import (
    calculate_comparison_fidelity,
    compare_atomic_radius,
    compare_electronegativity,
    compare_ionization_energy_relative,
    compare_to_experiment,
)
from kingdom.core.flux_flywheel import map_z_to_flywheel, map_z_to_flywheel_extended
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


def _observable_table_row(
    *,
    category: str,
    model_spin_only: str,
    model_soc: str,
    experimental: str,
    delta: str,
    source: str,
    quality: str,
    note: str,
) -> dict:
    return {
        "category": category,
        "model_spin_only": model_spin_only,
        "model_soc": model_soc,
        "experimental": experimental,
        "delta": delta,
        "source": source,
        "quality": quality,
        "note": note,
    }


def build_observables_validation(z: int, extended: dict) -> dict:
    """
    Model-vs-experiment validation bundle: fidelity score + table rows.

    Returns fidelity_score, fidelity_details, fidelity_note, rows, comparisons.
    """
    table: list[dict] = []

    spin_only = float(extended["magnetic_moment_BM"])
    soc_value = extended.get("magnetic_moment_soc_BM")
    soc_applied = extended.get("spin_orbit_applied", False)
    g_j = extended.get("lande_g_J", 0)
    term_j = extended.get("ground_term_J", 0)

    model_mu = float(soc_value) if soc_applied and soc_value is not None else spin_only
    mu_cmp = compare_to_experiment(z, model_mu, "magnetic_moment")

    soc_display = "—"
    if soc_applied and soc_value is not None and abs(float(soc_value) - spin_only) > 0.05:
        soc_display = f"{float(soc_value):.2f} BM (g_J={g_j}, J={term_j})"

    exp_mu = f"{mu_cmp['experimental_display']} BM" if mu_cmp["available"] else "—"
    delta_mu = f"{mu_cmp['delta']:+.2f} BM" if mu_cmp["delta"] is not None else "—"

    table.append(_observable_table_row(
        category="Magnetic Moment",
        model_spin_only=f"{spin_only:.2f} BM",
        model_soc=soc_display,
        experimental=exp_mu,
        delta=delta_mu,
        source=mu_cmp["source"] or "—",
        quality=mu_cmp["quality"],
        note=mu_cmp["note"],
    ))

    stability = float(extended["stability_score"])
    real_ie = float(extended["real_ionization_energy_eV"])
    ie_cmp = compare_ionization_energy_relative(z, stability)

    if ie_cmp["available"]:
        stab_z = ie_cmp.get("stability_z_score", 0.0)
        ie_z = ie_cmp.get("ie_z_score", 0.0)
        exp_ie = f"{ie_cmp['experimental_value']:.2f} eV (IE z {ie_z:+.2f})"
        delta_ie = f"Δz {ie_cmp['delta']:+.2f}"
        source_ie = f"Period-relative · {ie_cmp['source'] or 'NIST'}"
        quality_ie = ie_cmp["quality"]
        note_ie = ie_cmp["note"]
        model_ie = f"stab z {stab_z:+.2f}"
    else:
        implied_ie = float(extended.get("ie_model_implied_eV", 0.0))
        exp_ie = f"{real_ie:.2f} eV"
        delta_ie = "—"
        source_ie = "—"
        quality_ie = ie_cmp["quality"]
        note_ie = ie_cmp["note"]
        model_ie = f"{implied_ie:.2f} eV proxy"

    table.append(_observable_table_row(
        category="Ionization Energy",
        model_spin_only=model_ie,
        model_soc="—",
        experimental=exp_ie,
        delta=delta_ie,
        source=source_ie,
        quality=quality_ie,
        note=note_ie,
    ))

    implied_ea = float(extended.get("ea_model_implied_eV", 0.0))
    real_ea = float(extended.get("real_electron_affinity_eV", 0.0))
    ea_cmp = compare_to_experiment(z, implied_ea, "electron_affinity")

    if ea_cmp["available"]:
        exp_ea = f"{ea_cmp['experimental_value']:.2f} eV"
        delta_ea = f"{ea_cmp['delta']:+.2f} eV"
        source_ea = ea_cmp["source"] or "—"
        quality_ea = ea_cmp["quality"]
        note_ea = ea_cmp["note"]
    else:
        exp_ea = f"{real_ea:.2f} eV"
        delta_ea = f"{implied_ea - real_ea:+.2f} eV"
        source_ea = "Lookup + fallback"
        quality_ea = "Estimated"
        note_ea = "No NIST anchor — heuristic fallback used"

    table.append(_observable_table_row(
        category="Electron Affinity",
        model_spin_only=f"{implied_ea:.2f} eV",
        model_soc="—",
        experimental=exp_ea,
        delta=delta_ea,
        source=source_ea,
        quality=quality_ea,
        note=note_ea,
    ))

    radius_cmp = compare_atomic_radius(z, stability)
    if radius_cmp["available"]:
        model_radius = radius_cmp.get("model_value")
        model_display = f"{model_radius:.1f} pm" if model_radius is not None else "—"
        delta_radius = (
            f"{radius_cmp['delta']:+.1f} pm"
            if radius_cmp.get("delta") is not None
            else "—"
        )
        table.append(_observable_table_row(
            category="Atomic Radius (Covalent)",
            model_spin_only=model_display,
            model_soc="—",
            experimental=radius_cmp["experimental_display"] or "—",
            delta=delta_radius,
            source=radius_cmp["source"] or "—",
            quality=radius_cmp["quality"],
            note=radius_cmp["note"],
        ))

    en_cmp = compare_electronegativity(z, stability)
    if en_cmp["available"]:
        model_z = en_cmp.get("model_z_score", 0.0)
        en_z = en_cmp.get("en_z_score", 0.0)
        model_en = en_cmp.get("model_value")
        model_en_display = f"{model_en:.2f} (model z {model_z:+.2f})" if model_en is not None else "—"
        exp_en = f"{en_cmp['experimental_value']:.3f} (EN z {en_z:+.2f})"
        delta_en = f"Δz {en_cmp['delta']:+.2f}"
        source_en = f"Period-relative · {en_cmp['source'] or 'Allen (1989)'}"
        table.append(_observable_table_row(
            category="Electronegativity (Allen)",
            model_spin_only=model_en_display,
            model_soc="—",
            experimental=exp_en,
            delta=delta_en,
            source=source_en,
            quality=en_cmp["quality"],
            note=en_cmp["note"],
        ))

    comparisons = {
        "magnetic_moment": mu_cmp,
        "ionization_energy": ie_cmp,
        "electron_affinity": ea_cmp,
        "atomic_radius": radius_cmp,
        "electronegativity": en_cmp,
    }
    fidelity = calculate_comparison_fidelity(comparisons, z=z)

    return {
        "fidelity_score": fidelity["score"],
        "fidelity_core_score": fidelity.get("core_model_fidelity"),
        "fidelity_category_scores": fidelity.get("category_scores", {}),
        "fidelity_proxy_quality": fidelity.get("proxy_quality", {}),
        "fidelity_details": fidelity["details"],
        "fidelity_note": fidelity["note"],
        "rows": table,
        "comparisons": comparisons,
    }


def build_observables_table(z: int, extended: dict) -> list[dict]:
    """Table rows only (backward-compatible helper)."""
    return build_observables_validation(z, extended)["rows"]


def flux_observables_table(extended: dict, z: int | None = None) -> list[list[str]]:
    """Flattened key-value rows (legacy) plus structured validation rows."""
    z_val = int(extended.get("Z", z or 1))
    rows = [
        ["IE (1st, eV)", str(extended["real_ionization_energy_eV"])],
        ["Unpaired e⁻", str(extended["unpaired_electrons"])],
        ["μ spin-only (BM)", str(extended["magnetic_moment_BM"])],
        ["μ SOC (BM)", str(extended.get("magnetic_moment_soc_BM", extended["magnetic_moment_BM"]))],
    ]
    if extended.get("magnetic_moment_exp_available"):
        exp_disp = extended.get("magnetic_moment_exp_display", "—")
        source = extended.get("magnetic_moment_exp_source", "")
        quality = extended.get("magnetic_moment_exp_quality", "")
        rows.append(["μ experimental (BM)", f"{exp_disp} ({source})"])
        delta_soc = extended.get("mu_delta_soc_vs_exp_BM")
        if delta_soc is not None:
            rows.append(["Δ SOC vs exp (BM)", f"{delta_soc:+.2f}"])
        fidelity = extended.get("mu_validation_score")
        if fidelity is not None:
            rows.append(["μ fidelity (/10)", str(fidelity)])
        if quality:
            rows.append(["μ data quality", quality])

    fidelity_score = extended.get("comparison_fidelity_score")
    if fidelity_score is not None:
        rows.append(["Overall comparison fidelity (/10)", str(fidelity_score)])
        core = extended.get("comparison_fidelity_core_score")
        if core is not None:
            rows.append(["Core model fidelity (/10)", str(core)])
        for cat, cat_score in (extended.get("comparison_fidelity_category_scores") or {}).items():
            label = "N/A" if cat_score is None else str(cat_score)
            rows.append([f"  Category · {cat}", label])
        details = extended.get("comparison_fidelity_details") or {}
        for key, score in details.items():
            rows.append([f"  Observable · {key}", str(score)])

    for entry in build_observables_table(z_val, extended):
        rows.append([f"— {entry['category']}", entry["experimental"]])
        if entry["delta"] != "—":
            rows.append([f"  Δ ({entry['category']})", entry["delta"]])
        rows.append([f"  Source ({entry['category']})", entry["source"]])
        rows.append([f"  Quality ({entry['category']})", entry["quality"]])

    rows.extend([
        ["Diamagnetic", "yes" if extended["is_diamagnetic"] else "no"],
        ["Model ↔ reality", str(extended["model_vs_reality_alignment"])],
        ["Validation", extended["validation_notes"]],
    ])
    return rows


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


def explore_flux_element_extended(z: int) -> dict:
    """Flux Flywheel payload with laboratory observables and validation metrics."""
    payload = explore_flux_element(z)
    extended = map_z_to_flywheel_extended(z)
    validation = build_observables_validation(z, extended)
    extended = {
        **extended,
        "comparison_fidelity_score": validation["fidelity_score"],
        "comparison_fidelity_core_score": validation.get("fidelity_core_score"),
        "comparison_fidelity_category_scores": validation.get("fidelity_category_scores", {}),
        "comparison_fidelity_proxy_quality": validation.get("fidelity_proxy_quality", {}),
        "comparison_fidelity_details": validation["fidelity_details"],
        "comparison_fidelity_note": validation["fidelity_note"],
    }
    return {
        **payload,
        "flywheel": extended,
        "metrics_table": flux_metrics_table(extended),
        "observables_table": flux_observables_table(extended, z=z),
        "observables_validation": validation,
    }