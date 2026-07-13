#!/usr/bin/env python3
"""Kingdom Come — Hugging Face Space entrypoint."""

from __future__ import annotations

import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.flux_explorer import explore_flux_element_extended
from kingdom.simulations.lattice import build_lattice_figure, run_lattice_comparison
from kingdom.viz.hopf_plotly import (
    bake_hopf_animation_frames,
    build_hopf_animation_frame,
    build_hopf_fibration_figure_auto,
    build_hopf_s2_explorer,
    default_view_mode,
    export_kingdom_hopf_animation_mp4,
    fiber_family_choices,
    is_hf_space,
)

from app.build_info import get_build_label
from app.components.neon import (
    install_neon_plugin,
    element_card_html,
    flux_metrics_cards_html,
    flux_observables_analysis_html,
    flux_observables_right_html,
    flux_observables_table_html,
    synthetic_toe_strip_html,
    synthetic_z_html,
    toe_strip_html,
)
from app.components.periodic_picker import (
    FLUX_PERIODIC_CSS,
    PERIODIC_CSS,
    PERIODIC_TABLE_JS,
    element_picker_choices,
    known_periodic_table_html,
    superheavy_periodic_table_html,
    picker_label_for_z,
)
from app.components.markdown_math import kc_markdown
from app.components.ui_math import UI_MATH_LABEL_JS, WG_TAB_LABEL
from app.components.theme import HERO_HTML, build_kingdom_css, footer_html
from app.pages.higgs_observations import (
    HIGGS_GALLERY,
    INVESTIGATION_4_ACCORDION_TITLE,
    INVESTIGATION_4_MD,
)
from app.pages.phi_e_pi_mystery import (
    INVESTIGATION_6_ACCORDION_TITLE,
    INVESTIGATION_6_MD,
    PHI_E_PI_GALLERY,
)
from app.pages.schumann_observations import (
    INVESTIGATION_5_ACCORDION_TITLE,
    INVESTIGATION_5_MD,
    SCHUMANN_GALLERY,
)
from app.pages.bitcoin_pi_cycle_observations import (
    BITCOIN_PI_GALLERY,
    INVESTIGATION_8_ACCORDION_TITLE,
    INVESTIGATION_8_EMERGENCE_MD,
    INVESTIGATION_8_EXEC_MD,
    INVESTIGATION_8_GALLERY_INTRO_MD,
    INVESTIGATION_8_HEADER_HTML,
    INVESTIGATION_8_IMPLICATIONS_MD,
    INVESTIGATION_8_INDICATOR_MD,
    INVESTIGATION_8_REPORT_MD,
)
from app.pages.tls_trees_observations import (
    INVESTIGATION_7_ACCORDION_TITLE,
    INVESTIGATION_7_MD,
    TLS_TREES_GALLERY,
)
from app.pages.superconductors_observations import (
    BRAIDING_TARGET,
    INVESTIGATION_9_ACCORDION_TITLE,
    INVESTIGATION_9_MD,
    KAPPA_TARGET,
    SUPERCONDUCTORS_GALLERY,
    cuprate_conduit_metrics,
)
from app.pages.pulsars_observations import (
    INVESTIGATION_10_ACCORDION_TITLE,
    INVESTIGATION_10_MD,
    KAPPA_DEFAULT as PULSAR_KAPPA_DEFAULT,
    PULSARS_GALLERY,
    REFERENCE_PULSAR_HZ,
    pulsar_quick_check,
)
from app.pages.help import (
    HELP_ACRONYMS_MD,
    HELP_CONTROLS_MD,
    HELP_GETTING_STARTED_MD,
    HELP_NAVIGATE_MD,
    HELP_TECH_MD,
)
from app.pages.home import (
    HOME_CLOCK_MD,
    HOME_EXPLORE_MD,
    HOME_INTRO_GALLERY,
    HOME_INTRO_MD,
    HOME_THE_MODEL_MD,
    HOME_WG_MD,
)
from app.pages.hopf_guide import HF_VIEW_MODE_MD, HOPF_INTRO_MD, HOPF_PANEL_GUIDE_MD
from app.pages.toroidal_periodic import (
    TOROIDAL_GALLERY,
    TOROIDAL_HF_NOTE_MD,
    TOROIDAL_INTRO_MD,
    render_toroidal_periodic,
)
from app.pages.monster_fingerprints import (
    MONSTER_INTRO_MD,
    MOONSHINE_ANCHOR_MD,
    render_monster_heatmap,
)
from app.pages.flux_trends_observations import (
    FLUX_TRENDS_MD,
    render_flux_trend_plots,
    _normalize_periods,
)
from kingdom.viz.observations_trends import (
    PERIOD_COLOR_MAP,
    load_observations_trend_dataframes,
    z_from_scatter_select,
)
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
from app.pages.papers import (
    PAPER_ENTRIES,
    PAPERS_INTRO_MD,
    load_paper_gallery,
    paper_missing_md,
    paper_summary_md,
    resolve_paper_path,
)
from app.pages.showcase import SHOWCASE_HTML
from app.pages.theory import DERIVATION_HOPF_MD

PAPERS_DIR = ROOT / "app" / "assets" / "papers"
PAPERS_SOURCE_DIR = ROOT / "papers"
HOME_ASSETS_DIR = ROOT / "app" / "assets" / "home"
OBSERVATIONS_DIR = ROOT / "app" / "assets" / "observations"
HIGGS_DIR = ROOT / "app" / "assets" / "higgs"
SCHUMANN_DIR = ROOT / "app" / "assets" / "schumann"
MYSTERY_DIR = ROOT / "app" / "assets" / "mystery"
TLS_TREES_DIR = ROOT / "app" / "assets" / "tls_trees"
BITCOIN_PI_DIR = ROOT / "app" / "assets" / "bitcoin_pi"
SUPERCONDUCTORS_DIR = ROOT / "app" / "assets" / "superconductors"
PULSARS_DIR = ROOT / "app" / "assets" / "pulsars"
TOROIDAL_DIR = ROOT / "app" / "assets" / "toroidal"
MONSTER_DIR = ROOT / "app" / "assets" / "monster"

HOPF_PRESETS: dict[str, tuple[int, int, float, float, float]] = {
    "Classic Hopf": (8, 160, 0.6, 1.2, 1.0),
    "Dense fiber weave": (14, 200, 0.45, 2.1, 1.2),
    "Wide projection": (6, 120, 0.8, 0.5, 1.8),
}

HOPF_DEFAULTS = {
    "n_fibers": 8,
    "n_points": 160,
    "eta": 0.6,
    "xi1": 1.2,
    "scale": 1.0,
    "show_base": True,
    "show_highlight": True,
}


def render_hopf_visualizer(
    n_fibers: int,
    n_points: int,
    eta: float,
    xi1: float,
    show_base: bool,
    show_highlight: bool,
    scale: float,
    view_mode: str,
    explorer_mode: bool = False,
    animate_mode: bool = False,
    anim_mode: str = "xi1_orbit",
    n_frames: int = 36,
    frame_idx: int = 0,
):
    vm = view_mode if isinstance(view_mode, str) else str(view_mode)
    # Detect explorer / animate before HF WebGL clamp (both are HF-safe 2D).
    explorer = explorer_mode or ("explorer" in vm.lower())
    animate = animate_mode or ("animate" in vm.lower())
    if animate:
        # Precomputed Plotly frames + slider index (smooth HF-safe path).
        return build_hopf_animation_frame(
            n_fibers=int(n_fibers),
            n_points=min(int(n_points), 120),
            frame_idx=int(frame_idx),
            n_frames=int(n_frames),
            mode=str(anim_mode),
            eta=float(eta),
            xi1=float(xi1),
            projection_scale=float(scale),
            bake=True,
        )
    if explorer:
        return build_hopf_s2_explorer(
            n_fibers=int(n_fibers),
            n_points=int(n_points),
            eta=float(eta),
            xi1=float(xi1),
            projection_scale=float(scale),
        )
    # Belt-and-suspenders: never attempt WebGL on Hugging Face.
    if is_hf_space():
        view_mode = "2D projections (recommended)"
    return build_hopf_fibration_figure_auto(
        view_mode=view_mode,
        n_fibers=int(n_fibers),
        n_points=int(n_points),
        eta=float(eta),
        xi1=float(xi1),
        show_base_sphere=show_base,
        show_single_fiber_highlight=show_highlight,
        projection_scale=float(scale),
    )


def hopf_fiber_dropdown_choices(n_fibers: int = 12) -> list[str]:
    return [label for label, _e, _x in fiber_family_choices(n_fibers=int(n_fibers))]


def hopf_select_fiber(n_fibers: int, choice: str) -> tuple[float, float]:
    """Map dropdown label → (η, ξ₁)."""
    for label, eta, xi1 in fiber_family_choices(n_fibers=int(n_fibers)):
        if label == choice:
            return float(eta), float(xi1)
    return 0.6, 1.2


def render_lattice_sim(frames: int, n_sites: int, gauge: float):
    stable, chaotic = run_lattice_comparison(
        frames=int(frames),
        n_sites=int(n_sites),
        gauge_stable=float(gauge),
    )
    summary = (
        f"**Stable** — identity score {stable.stability_score:.3f}, "
        f"bursts {stable.total_bursts} · "
        f"**Chaotic** — identity score {chaotic.stability_score:.3f}, "
        f"bursts {chaotic.total_bursts}"
    )
    return build_lattice_figure(stable, chaotic), summary


_PICKER_LABEL_TO_Z: dict[str, int] = dict(element_picker_choices())
NOBLE_GAS_JUMP = ((2, "He"), (10, "Ne"), (18, "Ar"), (36, "Kr"), (54, "Xe"), (86, "Rn"), (118, "Og"))


def _flux_panels(z: int):
    """Render all Flux Flywheel panels for atomic number Z."""
    z = max(1, min(180, int(z)))
    payload = explore_flux_element_extended(z)
    element = payload["element"]
    fly = payload["flywheel"]
    art = payload["element_art"]
    if element is not None:
        card = element_card_html(element, fly, art_path=art)
        toe = toe_strip_html(element, fly)
    else:
        card = synthetic_z_html(z, fly)
        toe = synthetic_toe_strip_html(z, fly)
    return (
        picker_label_for_z(z),
        known_periodic_table_html(z),
        superheavy_periodic_table_html(z),
        card,
        payload["cloud_fig"],
        payload["compare_fig"],
        flux_observables_analysis_html(fly),
        flux_metrics_cards_html(fly),
        flux_observables_right_html(fly),
        flux_observables_table_html(fly),
        toe,
        payload["magic_island"],
    )


def select_flux_z(z: int):
    """Jump to Z — updates slider, dropdown, and all panels."""
    z = max(1, min(180, int(z)))
    return (z,) + _flux_panels(z)


def on_flux_slider(z: int):
    return _flux_panels(z)


def on_flux_dropdown(label: str):
    z = _PICKER_LABEL_TO_Z.get(label, 2)
    return select_flux_z(z)


def on_periodic_pick(evt: gr.EventData):
    """Handle periodic-table cell click from gr.HTML js_on_load trigger."""
    return select_flux_z(int(evt.z))


def _trend_select_noop():
    return tuple(gr.update() for _ in range(13))


def on_fidelity_trend_select(evt: gr.SelectData, periods: list[str] | None):
    """Route fidelity ScatterPlot selection → Flux Flywheel for that Z."""
    df, _, _, _ = load_observations_trend_dataframes(118, _normalize_periods(periods))
    z = z_from_scatter_select(evt, df, x_col="Z")
    if z is None:
        return _trend_select_noop()
    return select_flux_z(z)


def on_stability_trend_select(evt: gr.SelectData, periods: list[str] | None):
    """Route stability ScatterPlot selection → Flux Flywheel for that Z."""
    _, df, _, _ = load_observations_trend_dataframes(118, _normalize_periods(periods))
    z = z_from_scatter_select(
        evt, df, x_col="model_stability", y_col="experimental_ie"
    )
    if z is None:
        return _trend_select_noop()
    return select_flux_z(z)


def on_stability_en_trend_select(evt: gr.SelectData, periods: list[str] | None):
    """Route stability vs EN ScatterPlot selection → Flux Flywheel for that Z."""
    _, _, df, _ = load_observations_trend_dataframes(118, _normalize_periods(periods))
    z = z_from_scatter_select(
        evt, df, x_col="model_stability", y_col="experimental_en"
    )
    if z is None:
        return _trend_select_noop()
    return select_flux_z(z)


def on_mu_trend_select(evt: gr.SelectData, periods: list[str] | None):
    """Route SOC μ ScatterPlot selection → Flux Flywheel for that Z."""
    _, _, _, df = load_observations_trend_dataframes(118, _normalize_periods(periods))
    z = z_from_scatter_select(
        evt, df, x_col="experimental_mu_BM", y_col="soc_mu_BM"
    )
    if z is None:
        return _trend_select_noop()
    return select_flux_z(z)


_KINGDOM_THEME = gr.themes.Base(
    primary_hue="cyan",
    secondary_hue="blue",
    neutral_hue="slate",
).set(
    body_background_fill="#000000",
    body_text_color="#d4e4f7",
    background_fill_primary="#000000",
    background_fill_secondary="#0a0a0a",
    block_background_fill="rgba(18,36,61,0.30)",
    block_label_background_fill="#000000",
    input_background_fill="rgba(18,36,61,0.40)",
    panel_background_fill="rgba(18,36,61,0.30)",
    table_even_background_fill="rgba(18,36,61,0.30)",
    table_odd_background_fill="rgba(18,36,61,0.40)",
    block_border_color="rgba(26,143,227,0.25)",
    button_primary_background_fill="#1a8fe3",
    button_primary_text_color="#ffffff",
)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Kingdom Come") as demo:
        gr.HTML(HERO_HTML)

        with gr.Tabs():
            with gr.Tab("Home"):
                kc_markdown(HOME_INTRO_MD)
                with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                    for image_path, caption in HOME_INTRO_GALLERY:
                        gr.Image(
                            str(image_path),
                            label=caption,
                            interactive=False,
                            scale=1,
                            height=220,
                        )
                with gr.Tabs():
                    with gr.Tab("The Model"):
                        kc_markdown(HOME_THE_MODEL_MD)
                        with gr.Accordion("Derivation: Hopf Map via Quaternions", open=False):
                            kc_markdown(DERIVATION_HOPF_MD)
                    with gr.Tab("The Clock"):
                        kc_markdown(HOME_CLOCK_MD)
                    with gr.Tab(WG_TAB_LABEL, elem_id="kc-tab-wg"):
                        kc_markdown(HOME_WG_MD)
                    with gr.Tab("The Papers"):
                        kc_markdown(PAPERS_INTRO_MD)
                        for paper in PAPER_ENTRIES:
                            with gr.Accordion(paper.title, open=False) as paper_accordion:
                                kc_markdown(paper_summary_md(paper.key))
                                kc_markdown("### Paper pages (inline preview)")
                                page_gallery = gr.Gallery(
                                    label="PDF pages",
                                    columns=1,
                                    object_fit="contain",
                                    height=800,
                                    show_label=False,
                                    elem_classes=["kc-paper-gallery"],
                                )
                                paper_path = resolve_paper_path(paper)
                                if paper_path is not None:
                                    gr.File(
                                        value=str(paper_path),
                                        label=f"Download — {paper.filename}",
                                        interactive=False,
                                    )
                                else:
                                    kc_markdown(paper_missing_md(paper))
                                paper_accordion.expand(
                                    fn=lambda key=paper.key: load_paper_gallery(key),
                                    outputs=page_gallery,
                                    show_progress="minimal",
                                )
                    with gr.Tab("Explore"):
                        kc_markdown(HOME_EXPLORE_MD)

            with gr.Tab("Help"):
                with gr.Tabs():
                    with gr.Tab("Navigate"):
                        kc_markdown(HELP_NAVIGATE_MD)
                    with gr.Tab("Getting Started"):
                        kc_markdown(HELP_GETTING_STARTED_MD)
                    with gr.Tab("Controls"):
                        kc_markdown(HELP_CONTROLS_MD)
                    with gr.Tab("Acronyms"):
                        kc_markdown(HELP_ACRONYMS_MD)
                    with gr.Tab("Tech Stack"):
                        kc_markdown(HELP_TECH_MD)

            with gr.Tab("Hopf Visualizer") as hopf_tab:
                kc_markdown(HOPF_INTRO_MD)
                if is_hf_space():
                    kc_markdown(HF_VIEW_MODE_MD)
                else:
                    kc_markdown(
                        "Choose **2D dashboard** for maximum compatibility, **S² explorer** to pick fibers, "
                        "**Animate** for Play/Pause frame demos, or **3D** for WebGL rotation (local only)."
                    )
                _on_hf = is_hf_space()
                _view_choices = [
                    "2D projections (recommended)",
                    "S² explorer (pick fiber)",
                    "Animate (2D frames)",
                ]
                if not _on_hf:
                    _view_choices.append("3D interactive (WebGL)")
                with gr.Row():
                    view_mode = gr.Radio(
                        _view_choices,
                        value="2D projections (recommended)",
                        label="View mode",
                    )
                    n_fibers = gr.Slider(3, 16, value=8, step=1, label="Number of fibers")
                    n_points = gr.Slider(60, 300, value=160, step=20, label="Points per fiber")
                    scale = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="Projection scale")
                with gr.Row():
                    eta = gr.Slider(0.1, 1.4, value=0.6, step=0.05, label="Highlight η")
                    xi1 = gr.Slider(0.0, 6.28, value=1.2, step=0.1, label="Highlight ξ₁")
                    fiber_pick = gr.Dropdown(
                        choices=hopf_fiber_dropdown_choices(8),
                        value=None,
                        label="S² fiber pick (sets η, ξ₁)",
                        allow_custom_value=False,
                    )
                with gr.Row():
                    show_base = gr.Checkbox(value=True, label="Show S² base sphere")
                    show_highlight = gr.Checkbox(value=True, label="Highlight single fiber")
                    anim_mode = gr.Dropdown(
                        choices=[
                            "xi1_orbit",
                            "eta_breath",
                            "gauge_twist",
                        ],
                        value="xi1_orbit",
                        label="Animation mode (Animate view)",
                    )
                    n_frames = gr.Slider(12, 72, value=36, step=4, label="Animation frames")
                with gr.Row():
                    anim_frame = gr.Slider(
                        0,
                        47,
                        value=0,
                        step=1,
                        label="Frame (Animate — scrub after Bake / Update)",
                    )
                    anim_play = gr.Button("▶ Play", size="sm")
                    anim_pause = gr.Button("⏸ Pause", size="sm")
                    anim_export = gr.Button("Export MP4", size="sm")
                anim_timer = gr.Timer(0.07, active=False)
                anim_status = gr.Markdown("")
                kc_markdown(
                    "**Try a preset** or **S² fiber pick**. In **Animate** mode: "
                    "**Update visualization** precomputes smooth Plotly frames once, then "
                    "scrub **Frame** or **▶ Play** (instant swap — no re-sampling). "
                    "Optional **Export MP4** for high-quality video (`gr.Video`)."
                )
                with gr.Row():
                    preset_btns = [
                        gr.Button(name, size="sm") for name in HOPF_PRESETS
                    ]
                    reset_btn = gr.Button("Reset defaults", size="sm")
                with gr.Accordion("What you're looking at — panels ①–④", open=True):
                    kc_markdown(HOPF_PANEL_GUIDE_MD)
                hopf_plot = gr.Plot(label="Hopf Fibration")
                hopf_video = gr.Video(label="Exported animation (MP4)", visible=False)
                with gr.Row():
                    refresh = gr.Button("Update visualization", variant="primary")

                def _render(
                    n_fibers_v,
                    n_points_v,
                    eta_v,
                    xi1_v,
                    show_base_v,
                    show_highlight_v,
                    scale_v,
                    view_mode_v,
                    anim_mode_v,
                    n_frames_v,
                    frame_v,
                ):
                    vm = view_mode_v if isinstance(view_mode_v, str) else str(view_mode_v)
                    explorer = "explorer" in vm.lower()
                    animate = "animate" in vm.lower()
                    fig = render_hopf_visualizer(
                        n_fibers_v,
                        n_points_v,
                        eta_v,
                        xi1_v,
                        show_base_v,
                        show_highlight_v,
                        scale_v,
                        view_mode_v,
                        explorer_mode=explorer,
                        animate_mode=animate,
                        anim_mode=anim_mode_v,
                        n_frames=n_frames_v,
                        frame_idx=frame_v,
                    )
                    if animate:
                        status = (
                            f"Precomputed **{int(n_frames_v)}** frames "
                            f"(`{anim_mode_v}`) — scrub or Play for smooth playback."
                        )
                    else:
                        status = ""
                    return fig, status

                hopf_inputs = [
                    n_fibers,
                    n_points,
                    eta,
                    xi1,
                    show_base,
                    show_highlight,
                    scale,
                    view_mode,
                    anim_mode,
                    n_frames,
                    anim_frame,
                ]
                hopf_outputs = [hopf_plot, anim_status]
                refresh.click(_render, inputs=hopf_inputs, outputs=hopf_outputs)
                hopf_tab.select(
                    _render,
                    inputs=hopf_inputs,
                    outputs=hopf_outputs,
                    trigger_mode="once",
                    show_progress="minimal",
                )

                def _refresh_fiber_choices(n_f):
                    return gr.update(choices=hopf_fiber_dropdown_choices(int(n_f)))

                n_fibers.change(_refresh_fiber_choices, inputs=[n_fibers], outputs=[fiber_pick])

                def _apply_fiber_pick(n_f, choice):
                    if not choice:
                        return gr.update(), gr.update()
                    e, x = hopf_select_fiber(int(n_f), choice)
                    return e, x

                fiber_pick.change(
                    _apply_fiber_pick,
                    inputs=[n_fibers, fiber_pick],
                    outputs=[eta, xi1],
                ).then(_render, inputs=hopf_inputs, outputs=hopf_outputs)

                def _sync_frame_slider(n_f):
                    n = max(1, int(n_f))
                    return gr.update(maximum=n - 1, value=0)

                def _bake_and_show(
                    n_fibers_v,
                    n_points_v,
                    eta_v,
                    xi1_v,
                    scale_v,
                    anim_mode_v,
                    n_frames_v,
                    frame_v,
                ):
                    """Force bake then return selected frame (params change)."""
                    bake_hopf_animation_frames(
                        n_fibers=int(n_fibers_v),
                        n_points=min(int(n_points_v), 120),
                        n_frames=int(n_frames_v),
                        mode=str(anim_mode_v),
                        eta=float(eta_v),
                        xi1=float(xi1_v),
                        projection_scale=float(scale_v),
                        force=True,
                    )
                    fig = build_hopf_animation_frame(
                        n_fibers=int(n_fibers_v),
                        n_points=min(int(n_points_v), 120),
                        frame_idx=int(frame_v),
                        n_frames=int(n_frames_v),
                        mode=str(anim_mode_v),
                        eta=float(eta_v),
                        xi1=float(xi1_v),
                        projection_scale=float(scale_v),
                        bake=True,
                    )
                    return fig, (
                        f"Baked **{int(n_frames_v)}** frames "
                        f"(`{anim_mode_v}`) — scrub is instant."
                    )

                def _show_cached_frame(
                    n_fibers_v,
                    n_points_v,
                    eta_v,
                    xi1_v,
                    scale_v,
                    anim_mode_v,
                    n_frames_v,
                    frame_v,
                    view_mode_v,
                ):
                    vm = view_mode_v if isinstance(view_mode_v, str) else str(view_mode_v)
                    if "animate" not in vm.lower():
                        return gr.update(), gr.update()
                    fig = build_hopf_animation_frame(
                        n_fibers=int(n_fibers_v),
                        n_points=min(int(n_points_v), 120),
                        frame_idx=int(frame_v),
                        n_frames=int(n_frames_v),
                        mode=str(anim_mode_v),
                        eta=float(eta_v),
                        xi1=float(xi1_v),
                        projection_scale=float(scale_v),
                        bake=True,
                    )
                    return fig, gr.update()

                n_frames.change(_sync_frame_slider, inputs=[n_frames], outputs=[anim_frame])

                def _on_param_change(
                    n_fibers_v,
                    n_points_v,
                    eta_v,
                    xi1_v,
                    show_base_v,
                    show_highlight_v,
                    scale_v,
                    view_mode_v,
                    anim_mode_v,
                    n_frames_v,
                    frame_v,
                ):
                    """Re-bake animation frames only in Animate mode; else normal render."""
                    vm = view_mode_v if isinstance(view_mode_v, str) else str(view_mode_v)
                    if "animate" in vm.lower():
                        return _bake_and_show(
                            n_fibers_v,
                            n_points_v,
                            eta_v,
                            xi1_v,
                            scale_v,
                            anim_mode_v,
                            n_frames_v,
                            frame_v,
                        )
                    return _render(
                        n_fibers_v,
                        n_points_v,
                        eta_v,
                        xi1_v,
                        show_base_v,
                        show_highlight_v,
                        scale_v,
                        view_mode_v,
                        anim_mode_v,
                        n_frames_v,
                        frame_v,
                    )

                # Param changes: re-bake if Animate, else static re-render
                for comp in (n_fibers, n_points, eta, xi1, scale, anim_mode, n_frames, view_mode):
                    comp.change(
                        _on_param_change,
                        inputs=hopf_inputs,
                        outputs=hopf_outputs,
                    )
                # Scrub only indexes cache — fast path (Animate only)
                anim_frame.change(
                    _show_cached_frame,
                    inputs=[
                        n_fibers,
                        n_points,
                        eta,
                        xi1,
                        scale,
                        anim_mode,
                        n_frames,
                        anim_frame,
                        view_mode,
                    ],
                    outputs=hopf_outputs,
                )

                anim_play.click(lambda: gr.update(active=True), outputs=[anim_timer])
                anim_pause.click(lambda: gr.update(active=False), outputs=[anim_timer])

                def _tick_frame(frame_v, n_frames_v, view_mode_v):
                    vm = view_mode_v if isinstance(view_mode_v, str) else str(view_mode_v)
                    if "animate" not in vm.lower():
                        return gr.update()
                    n = max(1, int(n_frames_v))
                    return (int(frame_v) + 1) % n

                anim_timer.tick(
                    _tick_frame,
                    inputs=[anim_frame, n_frames, view_mode],
                    outputs=[anim_frame],
                )

                def _export_mp4(
                    n_fibers_v,
                    n_points_v,
                    eta_v,
                    xi1_v,
                    scale_v,
                    anim_mode_v,
                    n_frames_v,
                ):
                    try:
                        path = export_kingdom_hopf_animation_mp4(
                            n_fibers=int(n_fibers_v),
                            n_points=min(int(n_points_v), 100),
                            n_frames=min(int(n_frames_v), 60),
                            mode=str(anim_mode_v),
                            eta=float(eta_v),
                            xi1=float(xi1_v),
                            projection_scale=float(scale_v),
                            fps=18,
                        )
                        return (
                            gr.update(value=path, visible=True),
                            f"Exported MP4 → `{path}`",
                        )
                    except Exception as exc:
                        return (
                            gr.update(visible=False),
                            f"MP4 export failed (need kaleido + imageio-ffmpeg): `{exc}`",
                        )

                anim_export.click(
                    _export_mp4,
                    inputs=[n_fibers, n_points, eta, xi1, scale, anim_mode, n_frames],
                    outputs=[hopf_video, anim_status],
                )

                def apply_preset(name: str):
                    n_f, n_p, e, x, s = HOPF_PRESETS[name]
                    return n_f, n_p, e, x, s

                def reset_hopf_defaults():
                    d = HOPF_DEFAULTS
                    return (
                        d["n_fibers"],
                        d["n_points"],
                        d["eta"],
                        d["xi1"],
                        d["show_base"],
                        d["show_highlight"],
                        d["scale"],
                        "2D projections (recommended)",
                        "xi1_orbit",
                        48,
                        0,
                    )

                for preset_name, btn in zip(HOPF_PRESETS, preset_btns):
                    btn.click(
                        fn=lambda name=preset_name: apply_preset(name),
                        outputs=[n_fibers, n_points, eta, xi1, scale],
                    ).then(_render, inputs=hopf_inputs, outputs=hopf_outputs)

                reset_btn.click(
                    fn=reset_hopf_defaults,
                    outputs=hopf_inputs,
                ).then(_render, inputs=hopf_inputs, outputs=hopf_outputs)

            with gr.Tab("Toroidal Periodic") as toroidal_tab:
                kc_markdown(TOROIDAL_INTRO_MD)
                if is_hf_space():
                    kc_markdown(TOROIDAL_HF_NOTE_MD)
                else:
                    kc_markdown(
                        "Choose **2D** for maximum compatibility or **3D** for interactive "
                        "WebGL rotation (local)."
                    )
                with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                    for image_path, caption in TOROIDAL_GALLERY:
                        if image_path.is_file():
                            gr.Image(
                                str(image_path),
                                label=caption,
                                interactive=False,
                                scale=1,
                                height=280,
                            )
                _toroidal_on_hf = is_hf_space()
                with gr.Row():
                    toroidal_z_highlight = gr.Slider(
                        0,
                        118,
                        value=54,
                        step=1,
                        label="Highlight Z (0 = none)",
                    )
                    toroidal_major_r = gr.Slider(
                        2.0, 5.0, value=3.0, step=0.1, label="Major radius"
                    )
                    toroidal_minor_r = gr.Slider(
                        0.5, 2.0, value=1.0, step=0.1, label="Minor radius"
                    )
                with gr.Row():
                    toroidal_wireframe = gr.Checkbox(value=True, label="Wireframe torus")
                    toroidal_coil = gr.Checkbox(value=True, label="(1,7) coil path")
                    toroidal_flux_rings = gr.Checkbox(value=True, label="Flux flywheel rings")
                    toroidal_noble_locks = gr.Checkbox(value=True, label="Noble gas locks")
                    toroidal_labels = gr.Checkbox(value=True, label="Element symbols")
                    toroidal_period_bands = gr.Checkbox(value=True, label="Period banding on coil")
                    toroidal_focus_mode = gr.Checkbox(value=False, label="Focus mode (highlight only)")
                with gr.Row():
                    toroidal_manifold = gr.Radio(
                        ["Elements only", "Monster irreps only", "Dual overlay"],
                        value="Elements only",
                        label="Manifold view",
                    )
                    toroidal_z_irrep_map = gr.Dropdown(
                        [
                            "Linear (Z−1 → irrep)",
                            "Stability rank",
                            "Noble lock",
                            "Period × group",
                        ],
                        value="Linear (Z−1 → irrep)",
                        label="Z↔irrep mapping (exploratory)",
                    )
                with gr.Row():
                    toroidal_show_links = gr.Checkbox(
                        value=True,
                        label="Show Z↔irrep links (dual / highlight)",
                    )
                    toroidal_show_all_links = gr.Checkbox(
                        value=False,
                        label="Show all 118 links (dual only)",
                    )
                with gr.Row():
                    if _toroidal_on_hf:
                        toroidal_view_mode = gr.State("2D projection")
                    else:
                        toroidal_view_mode = gr.Radio(
                            ["2D projection", "3D interactive (WebGL)"],
                            value="2D projection",
                            label="View mode",
                        )
                    toroidal_projection = gr.Radio(
                        ["XY orthographic", "XZ side view", "YZ side view"],
                        value="XY orthographic",
                        label="2D projection (when 2D / HF)",
                    )
                toroidal_plot = gr.Plot(label="Toroidal Periodic × Flux Flywheel")
                with gr.Row():
                    toroidal_refresh = gr.Button("Update visualization", variant="primary")
                    toroidal_flux_btn = gr.Button("Open in Flux Flywheel", variant="secondary")
                toroidal_inputs = [
                    toroidal_z_highlight,
                    toroidal_major_r,
                    toroidal_minor_r,
                    toroidal_wireframe,
                    toroidal_coil,
                    toroidal_flux_rings,
                    toroidal_noble_locks,
                    toroidal_labels,
                    toroidal_period_bands,
                    toroidal_focus_mode,
                    toroidal_projection,
                    toroidal_manifold,
                    toroidal_z_irrep_map,
                    toroidal_show_links,
                    toroidal_show_all_links,
                    toroidal_view_mode,
                ]
                toroidal_refresh.click(
                    render_toroidal_periodic,
                    inputs=toroidal_inputs,
                    outputs=toroidal_plot,
                )
                toroidal_tab.select(
                    render_toroidal_periodic,
                    inputs=toroidal_inputs,
                    outputs=toroidal_plot,
                    trigger_mode="once",
                    show_progress="minimal",
                )

            with gr.Tab("Monster Fingerprints") as monster_tab:
                kc_markdown(MONSTER_INTRO_MD)
                with gr.Accordion("Monstrous Moonshine anchor", open=True):
                    kc_markdown(MOONSHINE_ANCHOR_MD)
                with gr.Row():
                    monster_sort = gr.Dropdown(
                        [
                            "Exponent sum (heavy first)",
                            "Irrep index (0–193)",
                            "Degree (ascending)",
                            "Degree (descending)",
                        ],
                        value="Exponent sum (heavy first)",
                        label="Row sort",
                    )
                    monster_color = gr.Radio(
                        ["Linear exponents", "Log(1 + exponent)"],
                        value="Linear exponents",
                        label="Color scale",
                    )
                    monster_highlight = gr.Slider(
                        -1,
                        193,
                        value=1,
                        step=1,
                        label="Highlight irrep index (-1 = none)",
                    )
                monster_plot = gr.Plot(label="Supersingular prime exponent heatmap")
                with gr.Row():
                    monster_refresh = gr.Button("Update heatmap", variant="primary")
                monster_inputs = [monster_sort, monster_color, monster_highlight]
                monster_refresh.click(
                    render_monster_heatmap,
                    inputs=monster_inputs,
                    outputs=monster_plot,
                )
                monster_tab.select(
                    render_monster_heatmap,
                    inputs=monster_inputs,
                    outputs=monster_plot,
                    trigger_mode="once",
                    show_progress="minimal",
                )

            with gr.Tab("Lattice Simulator") as lattice_tab:
                kc_markdown(
                    "Two-gyro **gauged quaternion lattice** from the toe repo — "
                    "compare stable (gauge=0.85) vs chaotic (gauge=0.08) flux flywheel dynamics."
                )
                with gr.Row():
                    lat_frames = gr.Slider(60, 400, value=150, step=10, label="Frames")
                    lat_sites = gr.Slider(24, 128, value=72, step=8, label="Lattice sites")
                    lat_gauge = gr.Slider(0.5, 0.95, value=0.85, step=0.05, label="Stable gauge strength")
                lattice_plot = gr.Plot(label="Lattice metrics")
                lattice_summary = kc_markdown()
                lattice_run = gr.Button("Run lattice comparison", variant="primary")
                lattice_run.click(
                    render_lattice_sim,
                    inputs=[lat_frames, lat_sites, lat_gauge],
                    outputs=[lattice_plot, lattice_summary],
                )
                lattice_tab.select(
                    render_lattice_sim,
                    inputs=[lat_frames, lat_sites, lat_gauge],
                    outputs=[lattice_plot, lattice_summary],
                    trigger_mode="once",
                    show_progress="minimal",
                )

            with gr.Tab("Flux Flywheel") as flux_tab:
                with gr.Column(elem_classes=["kc-flux-page"]):
                    kc_markdown(
                        "**Element explorer + flux flywheel** — pick any Z from the table or dropdown. "
                        "Z = 1–118 known · Z = 119–180 superheavy (predicted) · Z = 129 Magic Island ID."
                    )
                    with gr.Row():
                        z_dropdown = gr.Dropdown(
                            choices=[label for label, _ in element_picker_choices()],
                            value=picker_label_for_z(2),
                            label="Jump to element",
                            filterable=True,
                            scale=2,
                        )
                        z_slider = gr.Slider(1, 180, value=2, step=1, label="Atomic number Z", scale=2)
                    with gr.Accordion(
                        "Periodic table of known elements (Z=1-118)",
                        open=False,
                    ):
                        known_periodic_table = gr.HTML(js_on_load=PERIODIC_TABLE_JS)
                        noble_jump_row = gr.Row()
                    with gr.Accordion(
                        "Periodic table of unknown elements (Z=119-180) superheavy (predicted)",
                        open=False,
                    ):
                        superheavy_periodic_table = gr.HTML(js_on_load=PERIODIC_TABLE_JS)
                    with gr.Row(equal_height=False):
                        with gr.Column(
                            scale=1,
                            min_width=280,
                            elem_classes=["kc-flux-left-col"],
                        ):
                            element_card = gr.HTML(label="Element")
                            electron_plot = gr.Plot(label="Electron cloud + flux ring")
                            compare_plot = gr.Plot(label="Chemistry vs TOE flux")
                            flux_analysis_panel = gr.HTML(label="Chemistry analysis")
                        with gr.Column(
                            scale=1,
                            min_width=280,
                            elem_classes=["kc-flux-right-col"],
                        ):
                            flux_metrics_panel = gr.HTML(label="Flux metrics")
                            flux_observables_panel = gr.HTML(
                                label="Observables & fidelity"
                            )
                    flux_validation_panel = gr.HTML(label="Model vs experiment")
                    toe_panel = gr.HTML(label="TOE interpretation")
                    with gr.Accordion("Magic Island heatmap", open=False):
                        magic_island_plot = gr.Plot()
                    flux_panel_outputs = [
                        z_dropdown,
                        known_periodic_table,
                        superheavy_periodic_table,
                        element_card,
                        electron_plot,
                        compare_plot,
                        flux_analysis_panel,
                        flux_metrics_panel,
                        flux_observables_panel,
                        flux_validation_panel,
                        toe_panel,
                        magic_island_plot,
                    ]
                    flux_jump_outputs = [z_slider, *flux_panel_outputs]
                    with noble_jump_row:
                        kc_markdown("**Noble gas quick-jump:**")
                        for z_val, sym in NOBLE_GAS_JUMP:
                            btn = gr.Button(sym, size="sm", min_width=48)
                            btn.click(
                                fn=lambda z=z_val: select_flux_z(z),
                                outputs=flux_jump_outputs,
                            )
                    z_slider.change(on_flux_slider, inputs=z_slider, outputs=flux_panel_outputs)
                    z_dropdown.change(on_flux_dropdown, inputs=z_dropdown, outputs=flux_jump_outputs)
                    known_periodic_table.pick(on_periodic_pick, outputs=flux_jump_outputs)
                    superheavy_periodic_table.pick(on_periodic_pick, outputs=flux_jump_outputs)
                flux_tab.select(
                    on_flux_slider,
                    inputs=z_slider,
                    outputs=flux_panel_outputs,
                    trigger_mode="once",
                    show_progress="minimal",
                )

                def on_toroidal_flux_jump(z_highlight: float):
                    z = int(z_highlight)
                    if z < 1:
                        z = 54
                    return select_flux_z(z)

                toroidal_flux_btn.click(
                    fn=on_toroidal_flux_jump,
                    inputs=[toroidal_z_highlight],
                    outputs=flux_jump_outputs,
                )

            with gr.Tab("Observations", elem_classes=["kc-observations-tab"]) as observations_tab:
                kc_markdown(OBSERVATIONS_INTRO_MD)
                with gr.Accordion(
                    "Periodic Trends — Flux Flywheel Validation",
                    open=True,
                ):
                    kc_markdown(FLUX_TRENDS_MD)
                    period_trend_filter = gr.Dropdown(
                        choices=[str(p) for p in range(1, 8)],
                        value=[str(p) for p in range(1, 8)],
                        multiselect=True,
                        label="Filter by period(s)",
                    )
                    _trend_plot_kwargs = dict(
                        color="period",
                        color_map=PERIOD_COLOR_MAP,
                        tooltip="all",
                        height=440,
                    )
                    with gr.Row():
                        fidelity_trend_plot = gr.ScatterPlot(
                            label="Fidelity score trend",
                            x="Z",
                            y="fidelity_score",
                            title="Comparison Fidelity Score vs Atomic Number",
                            x_title="Atomic Number (Z)",
                            y_title="Fidelity Score (0–10)",
                            y_lim=[0, 10],
                            **_trend_plot_kwargs,
                        )
                        stability_ie_plot = gr.ScatterPlot(
                            label="Stability vs ionization energy",
                            x="model_stability",
                            y="experimental_ie",
                            title="Model Stability Score vs Experimental Ionization Energy",
                            x_title="Model Stability Score",
                            y_title="Experimental IE (eV)",
                            **_trend_plot_kwargs,
                        )
                    with gr.Row():
                        stability_en_plot = gr.ScatterPlot(
                            label="Stability vs Allen electronegativity",
                            x="model_stability",
                            y="experimental_en",
                            title="Model Stability Score vs Allen Electronegativity",
                            x_title="Model Stability Score",
                            y_title="Allen Electronegativity",
                            **_trend_plot_kwargs,
                        )
                        mu_validation_plot = gr.ScatterPlot(
                            label="SOC μ vs experimental",
                            x="experimental_mu_BM",
                            y="soc_mu_BM",
                            title="SOC Magnetic Moment vs Experimental μ",
                            x_title="Experimental μ (BM)",
                            y_title="SOC μ (BM)",
                            height=380,
                            color="period",
                            color_map=PERIOD_COLOR_MAP,
                            tooltip="all",
                        )
                    flux_trends_outputs = [
                        fidelity_trend_plot,
                        stability_ie_plot,
                        stability_en_plot,
                        mu_validation_plot,
                    ]
                    gr.Button("Refresh trend analysis", size="sm").click(
                        render_flux_trend_plots,
                        inputs=[period_trend_filter],
                        outputs=flux_trends_outputs,
                    )
                    period_trend_filter.change(
                        render_flux_trend_plots,
                        inputs=[period_trend_filter],
                        outputs=flux_trends_outputs,
                    )
                    fidelity_trend_plot.select(
                        on_fidelity_trend_select,
                        inputs=[period_trend_filter],
                        outputs=flux_jump_outputs,
                    )
                    stability_ie_plot.select(
                        on_stability_trend_select,
                        inputs=[period_trend_filter],
                        outputs=flux_jump_outputs,
                    )
                    stability_en_plot.select(
                        on_stability_en_trend_select,
                        inputs=[period_trend_filter],
                        outputs=flux_jump_outputs,
                    )
                    mu_validation_plot.select(
                        on_mu_trend_select,
                        inputs=[period_trend_filter],
                        outputs=flux_jump_outputs,
                    )
                with gr.Accordion(
                    "Investigation 1: Catatumbo Lightning Hotspot — Earth",
                    open=False,
                ):
                    with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                        for image_path, caption in CATATUMBO_GALLERY:
                            gr.Image(
                                str(image_path),
                                label=caption,
                                interactive=False,
                                scale=1,
                                height=280,
                            )
                    kc_markdown(INVESTIGATION_1_MD)
                with gr.Accordion(
                    "Investigation 2: Great Red Spot — Jupiter",
                    open=False,
                ):
                    with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                        for image_path, caption in JUPITER_GALLERY:
                            gr.Image(
                                str(image_path),
                                label=caption,
                                interactive=False,
                                scale=1,
                                height=280,
                            )
                    kc_markdown(INVESTIGATION_2_MD)
                with gr.Accordion(
                    "Investigation 3: Emergent Periodic Orbits in Gravitational Three-Body Systems",
                    open=False,
                ):
                    with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                        for image_path, caption in THREEBODY_GALLERY:
                            gr.Image(
                                str(image_path),
                                label=caption,
                                interactive=False,
                                scale=1,
                                height=280,
                            )
                    kc_markdown(INVESTIGATION_3_MD)
                with gr.Accordion(
                    INVESTIGATION_4_ACCORDION_TITLE,
                    open=False,
                ):
                    with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                        for image_path, caption in HIGGS_GALLERY:
                            gr.Image(
                                str(image_path),
                                label=caption,
                                interactive=False,
                                scale=1,
                                height=280,
                            )
                    kc_markdown(INVESTIGATION_4_MD)
                with gr.Accordion(
                    INVESTIGATION_5_ACCORDION_TITLE,
                    open=False,
                ):
                    with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                        for image_path, caption in SCHUMANN_GALLERY:
                            gr.Image(
                                str(image_path),
                                label=caption,
                                interactive=False,
                                scale=1,
                                height=280,
                            )
                    kc_markdown(INVESTIGATION_5_MD)
                with gr.Accordion(
                    INVESTIGATION_6_ACCORDION_TITLE,
                    open=False,
                ):
                    with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                        for image_path, caption in PHI_E_PI_GALLERY:
                            gr.Image(
                                str(image_path),
                                label=caption,
                                interactive=False,
                                scale=1,
                                height=280,
                            )
                    kc_markdown(INVESTIGATION_6_MD)
                with gr.Accordion(
                    INVESTIGATION_7_ACCORDION_TITLE,
                    open=False,
                ):
                    with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                        for image_path, caption in TLS_TREES_GALLERY:
                            gr.Image(
                                str(image_path),
                                label=caption,
                                interactive=False,
                                scale=1,
                                height=280,
                            )
                    kc_markdown(INVESTIGATION_7_MD)
                with gr.Accordion(
                    INVESTIGATION_8_ACCORDION_TITLE,
                    open=False,
                ):
                    gr.HTML(INVESTIGATION_8_HEADER_HTML)
                    kc_markdown(INVESTIGATION_8_EXEC_MD)
                    kc_markdown(INVESTIGATION_8_INDICATOR_MD)
                    kc_markdown(INVESTIGATION_8_EMERGENCE_MD)
                    kc_markdown(INVESTIGATION_8_GALLERY_INTRO_MD)
                    with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                        for image_path, caption in BITCOIN_PI_GALLERY:
                            gr.Image(
                                str(image_path),
                                label=caption,
                                interactive=False,
                                scale=1,
                                height=280,
                            )
                    kc_markdown(INVESTIGATION_8_IMPLICATIONS_MD)
                    report_copy = gr.Textbox(
                        value=INVESTIGATION_8_REPORT_MD,
                        visible=False,
                        label="report",
                    )
                    gr.Button(
                        "Copy report as Markdown",
                        size="sm",
                    ).click(
                        fn=None,
                        inputs=[report_copy],
                        outputs=None,
                        js="(text) => { navigator.clipboard.writeText(text); return []; }",
                    )
                with gr.Accordion(
                    INVESTIGATION_9_ACCORDION_TITLE,
                    open=False,
                ):
                    with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                        for image_path, caption in SUPERCONDUCTORS_GALLERY:
                            gr.Image(
                                str(image_path),
                                label=caption,
                                interactive=False,
                                scale=1,
                                height=280,
                            )
                    kc_markdown(INVESTIGATION_9_MD)
                    with gr.Row():
                        kappa_slider = gr.Slider(
                            minimum=0.70,
                            maximum=0.82,
                            value=KAPPA_TARGET,
                            step=0.001,
                            label="κ — interlayer / pairing coupling",
                        )
                        braiding_slider = gr.Slider(
                            minimum=0.74,
                            maximum=0.78,
                            value=BRAIDING_TARGET,
                            step=0.0001,
                            label="braiding_target — anyonic phase",
                        )
                    conduit_readout = kc_markdown(
                        cuprate_conduit_metrics(KAPPA_TARGET, BRAIDING_TARGET)
                    )

                    def on_cuprate_sliders(kappa: float, braiding: float) -> str:
                        return cuprate_conduit_metrics(kappa, braiding)

                    kappa_slider.change(
                        on_cuprate_sliders,
                        inputs=[kappa_slider, braiding_slider],
                        outputs=conduit_readout,
                    )
                    braiding_slider.change(
                        on_cuprate_sliders,
                        inputs=[kappa_slider, braiding_slider],
                        outputs=conduit_readout,
                    )
                with gr.Accordion(
                    INVESTIGATION_10_ACCORDION_TITLE,
                    open=False,
                ):
                    with gr.Row(equal_height=True, elem_classes=["kc-obs-image-row"]):
                        for image_path, caption in PULSARS_GALLERY:
                            gr.Image(
                                str(image_path),
                                label=caption,
                                interactive=False,
                                scale=1,
                                height=280,
                            )
                    kc_markdown(INVESTIGATION_10_MD)
                    with gr.Row():
                        pulsar_freq = gr.Number(
                            label="Test pulsar spin frequency (Hz)",
                            value=REFERENCE_PULSAR_HZ,
                            minimum=1,
                            maximum=2000,
                        )
                        pulsar_kappa = gr.Slider(
                            minimum=0.70,
                            maximum=0.95,
                            value=PULSAR_KAPPA_DEFAULT,
                            step=0.01,
                            label="κ — coupling parameter",
                        )
                    pulsar_readout = kc_markdown(
                        pulsar_quick_check(REFERENCE_PULSAR_HZ, PULSAR_KAPPA_DEFAULT)
                    )
                    gr.Button("Run quick check", size="sm").click(
                        pulsar_quick_check,
                        inputs=[pulsar_freq, pulsar_kappa],
                        outputs=pulsar_readout,
                    )
                kc_markdown(OBSERVATIONS_FOOTER_MD)
                observations_tab.select(
                    render_flux_trend_plots,
                    inputs=[period_trend_filter],
                    outputs=flux_trends_outputs,
                    trigger_mode="once",
                    show_progress="minimal",
                )

            with gr.Tab("Showcase"):
                kc_markdown(
                    "Related Hugging Face Spaces in the TOE ecosystem. "
                    "Each card links to a live Space with a one-line connection to Kingdom Come."
                )
                gr.HTML(SHOWCASE_HTML)

        gr.HTML(footer_html(get_build_label()))

        demo.load(fn=None, js=UI_MATH_LABEL_JS)

    return demo


demo = build_app()


def main() -> None:
    import os

    on_hf = bool(os.environ.get("SPACE_ID"))
    port = int(os.environ.get("GRADIO_SERVER_PORT", "7860"))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        css=build_kingdom_css() + install_neon_plugin() + PERIODIC_CSS + FLUX_PERIODIC_CSS,
        theme=_KINGDOM_THEME,
        allowed_paths=[
            str(PAPERS_DIR),
            str(PAPERS_SOURCE_DIR),
            str(HOME_ASSETS_DIR),
            str(OBSERVATIONS_DIR),
            str(HIGGS_DIR),
            str(SCHUMANN_DIR),
            str(MYSTERY_DIR),
            str(TLS_TREES_DIR),
            str(BITCOIN_PI_DIR),
            str(SUPERCONDUCTORS_DIR),
            str(PULSARS_DIR),
            str(TOROIDAL_DIR),
            str(MONSTER_DIR),
        ],
        inbrowser=not on_hf,
        # HF sets GRADIO_SSR_MODE=true by default; the Node SSR proxy can emit
        # harmless asyncio __del__ noise on Python 3.12. Client-side mode is
        # stable for our Plotly-heavy app and avoids the dual-port proxy.
        ssr_mode=False,
    )


if __name__ == "__main__":
    main()