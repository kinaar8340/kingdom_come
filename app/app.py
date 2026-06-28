#!/usr/bin/env python3
"""Kingdom Come — Hugging Face Space entrypoint."""

from __future__ import annotations

import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.flux_explorer import explore_flux_element
from kingdom.simulations.lattice import build_lattice_figure, run_lattice_comparison
from kingdom.viz.hopf_plotly import build_hopf_fibration_figure_auto, default_view_mode, is_hf_space

from app.build_info import get_build_label
from app.components.neon import (
    NEON_CSS,
    element_card_html,
    flux_metrics_cards_html,
    synthetic_toe_strip_html,
    synthetic_z_html,
    toe_strip_html,
)
from app.components.periodic_picker import (
    PERIODIC_CSS,
    PERIODIC_TABLE_JS,
    element_picker_choices,
    periodic_table_html,
    picker_label_for_z,
)
from app.components.theme import HERO_HTML, KINGDOM_CSS, footer_html
from app.pages.help import HELP_MD, QUICKSTART_MD
from app.pages.home import HOME_MD, ONBOARDING_MD, SHOWCASE_CARDS
from app.pages.hopf_guide import HF_VIEW_MODE_MD, HOPF_INTRO_MD, HOPF_PANEL_GUIDE_MD
from app.pages.observations import (
    CATATUMBO_GALLERY,
    INVESTIGATION_1_MD,
    INVESTIGATION_2_MD,
    JUPITER_GALLERY,
    OBSERVATIONS_FOOTER_MD,
    OBSERVATIONS_INTRO_MD,
)
from app.pages.papers import (
    PAPERS_INTRO_MD,
    default_paper_key,
    load_paper,
    paper_choices,
    papers_index_html,
)
from app.pages.showcase import SHOWCASE_HTML
from app.pages.theory import DERIVATION_HOPF_MD, THEORY_MD

PAPERS_DIR = ROOT / "app" / "assets" / "papers"
OBSERVATIONS_DIR = ROOT / "app" / "assets" / "observations"

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
):
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
    payload = explore_flux_element(z)
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
        periodic_table_html(z),
        card,
        payload["cloud_fig"],
        payload["compare_fig"],
        flux_metrics_cards_html(fly),
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


_KINGDOM_THEME = gr.themes.Base(
    primary_hue="cyan",
    secondary_hue="blue",
    neutral_hue="slate",
).set(
    body_background_fill="#0a1628",
    body_text_color="#d4e4f7",
    block_background_fill="#12243d",
    block_border_color="rgba(26,143,227,0.25)",
    button_primary_background_fill="#1a8fe3",
    button_primary_text_color="#ffffff",
)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Kingdom Come") as demo:
        gr.HTML(HERO_HTML)

        with gr.Tabs():
            with gr.Tab("Home"):
                gr.Markdown(QUICKSTART_MD)
                with gr.Accordion("First-time visitor? Start here", open=False):
                    gr.Markdown(ONBOARDING_MD)
                gr.Markdown(HOME_MD)
                gr.HTML(SHOWCASE_CARDS)

            with gr.Tab("Help"):
                gr.Markdown(HELP_MD)

            with gr.Tab("Hopf Visualizer"):
                gr.Markdown(HOPF_INTRO_MD)
                if is_hf_space():
                    gr.Markdown(HF_VIEW_MODE_MD)
                else:
                    gr.Markdown(
                        "Choose **2D** for maximum compatibility or **3D** for interactive WebGL rotation (local)."
                    )
                _on_hf = is_hf_space()
                with gr.Row():
                    if _on_hf:
                        view_mode = gr.State("2D projections (recommended)")
                    else:
                        view_mode = gr.Radio(
                            ["2D projections (recommended)", "3D interactive (WebGL)"],
                            value="2D projections (recommended)",
                            label="View mode",
                        )
                    n_fibers = gr.Slider(3, 16, value=8, step=1, label="Number of fibers")
                    n_points = gr.Slider(60, 300, value=160, step=20, label="Points per fiber")
                    scale = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="Projection scale")
                with gr.Row():
                    eta = gr.Slider(0.1, 1.4, value=0.6, step=0.05, label="Highlight η")
                    xi1 = gr.Slider(0.0, 6.28, value=1.2, step=0.1, label="Highlight ξ₁")
                with gr.Row():
                    show_base = gr.Checkbox(value=True, label="Show S² base sphere")
                    show_highlight = gr.Checkbox(value=True, label="Highlight single fiber")
                gr.Markdown("**Try a preset** — loads parameters and updates the plot automatically.")
                with gr.Row():
                    preset_btns = [
                        gr.Button(name, size="sm") for name in HOPF_PRESETS
                    ]
                    reset_btn = gr.Button("Reset defaults", size="sm")
                with gr.Accordion("What you're looking at — panels ①–④", open=True):
                    gr.Markdown(HOPF_PANEL_GUIDE_MD)
                hopf_plot = gr.Plot(label="Hopf Fibration")
                with gr.Row():
                    refresh = gr.Button("Update visualization", variant="primary")
                hopf_inputs = [
                    n_fibers,
                    n_points,
                    eta,
                    xi1,
                    show_base,
                    show_highlight,
                    scale,
                    view_mode,
                ]
                refresh.click(render_hopf_visualizer, inputs=hopf_inputs, outputs=hopf_plot)
                demo.load(render_hopf_visualizer, inputs=hopf_inputs, outputs=hopf_plot)

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
                    )

                for preset_name, btn in zip(HOPF_PRESETS, preset_btns):
                    btn.click(
                        fn=lambda name=preset_name: apply_preset(name),
                        outputs=[n_fibers, n_points, eta, xi1, scale],
                    ).then(render_hopf_visualizer, inputs=hopf_inputs, outputs=hopf_plot)

                reset_btn.click(
                    fn=reset_hopf_defaults,
                    outputs=hopf_inputs,
                ).then(render_hopf_visualizer, inputs=hopf_inputs, outputs=hopf_plot)

            with gr.Tab("The Model"):
                gr.Markdown(THEORY_MD)
                with gr.Accordion("Derivation: Hopf Map via Quaternions", open=True):
                    gr.Markdown(DERIVATION_HOPF_MD)

            with gr.Tab("Papers"):
                gr.Markdown(PAPERS_INTRO_MD)
                gr.HTML(papers_index_html())
                with gr.Row():
                    paper_dropdown = gr.Dropdown(
                        choices=paper_choices(),
                        value=default_paper_key(),
                        label="Select paper",
                        filterable=True,
                        scale=2,
                    )
                    paper_download = gr.File(
                        label="Download PDF",
                        interactive=False,
                        scale=1,
                    )
                paper_description = gr.Markdown()
                paper_viewer = gr.HTML(label="PDF viewer")
                paper_outputs = [paper_download, paper_viewer, paper_description]
                paper_dropdown.change(load_paper, inputs=paper_dropdown, outputs=paper_outputs)
                demo.load(load_paper, inputs=paper_dropdown, outputs=paper_outputs)

            with gr.Tab("Lattice Simulator"):
                gr.Markdown(
                    "Two-gyro **gauged quaternion lattice** from the toe repo — "
                    "compare stable (gauge=0.85) vs chaotic (gauge=0.08) flux flywheel dynamics."
                )
                with gr.Row():
                    lat_frames = gr.Slider(60, 400, value=150, step=10, label="Frames")
                    lat_sites = gr.Slider(24, 128, value=72, step=8, label="Lattice sites")
                    lat_gauge = gr.Slider(0.5, 0.95, value=0.85, step=0.05, label="Stable gauge strength")
                lattice_plot = gr.Plot(label="Lattice metrics")
                lattice_summary = gr.Markdown()
                lattice_run = gr.Button("Run lattice comparison", variant="primary")
                lattice_run.click(
                    render_lattice_sim,
                    inputs=[lat_frames, lat_sites, lat_gauge],
                    outputs=[lattice_plot, lattice_summary],
                )
                demo.load(
                    render_lattice_sim,
                    inputs=[lat_frames, lat_sites, lat_gauge],
                    outputs=[lattice_plot, lattice_summary],
                )

            with gr.Tab("Flux Flywheel"):
                gr.Markdown(
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
                with gr.Accordion("Periodic table (click any element)", open=True):
                    periodic_table = gr.HTML(js_on_load=PERIODIC_TABLE_JS)
                    noble_jump_row = gr.Row()
                # Hero: element card (left) · electron cloud plot (right, 2× width)
                with gr.Row():
                    with gr.Column(scale=1, min_width=240):
                        element_card = gr.HTML(label="Element")
                    with gr.Column(scale=2):
                        electron_plot = gr.Plot(label="Electron cloud + flux ring")
                with gr.Row():
                    with gr.Column(scale=1):
                        compare_plot = gr.Plot(label="Chemistry vs TOE flux")
                    with gr.Column(scale=1):
                        flux_metrics_panel = gr.HTML(label="Flux metrics")
                toe_panel = gr.HTML(label="TOE interpretation")
                with gr.Accordion("Magic Island heatmap", open=False):
                    magic_island_plot = gr.Plot()
                flux_panel_outputs = [
                    z_dropdown,
                    periodic_table,
                    element_card,
                    electron_plot,
                    compare_plot,
                    flux_metrics_panel,
                    toe_panel,
                    magic_island_plot,
                ]
                flux_jump_outputs = [z_slider, *flux_panel_outputs]
                with noble_jump_row:
                    gr.Markdown("**Noble gas quick-jump:**")
                    for z_val, sym in NOBLE_GAS_JUMP:
                        btn = gr.Button(sym, size="sm", min_width=48)
                        btn.click(
                            fn=lambda z=z_val: select_flux_z(z),
                            outputs=flux_jump_outputs,
                        )
                z_slider.change(on_flux_slider, inputs=z_slider, outputs=flux_panel_outputs)
                z_dropdown.change(on_flux_dropdown, inputs=z_dropdown, outputs=flux_jump_outputs)
                periodic_table.pick(on_periodic_pick, outputs=flux_jump_outputs)
                demo.load(on_flux_slider, inputs=z_slider, outputs=flux_panel_outputs)

            with gr.Tab("Observations"):
                gr.Markdown(OBSERVATIONS_INTRO_MD)
                with gr.Accordion(
                    "Investigation 1: Catatumbo Lightning Hotspot — Earth",
                    open=True,
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
                    gr.Markdown(INVESTIGATION_1_MD)
                with gr.Accordion(
                    "Investigation 2: Great Red Spot — Jupiter",
                    open=True,
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
                    gr.Markdown(INVESTIGATION_2_MD)
                gr.Markdown(OBSERVATIONS_FOOTER_MD)

            with gr.Tab("Showcase"):
                gr.Markdown(
                    "Related Hugging Face Spaces in the TOE ecosystem. "
                    "Each card links to a live Space with a one-line connection to Kingdom Come."
                )
                gr.HTML(SHOWCASE_HTML)

        gr.HTML(footer_html(get_build_label()))

    return demo


demo = build_app()


def main() -> None:
    import os

    on_hf = bool(os.environ.get("SPACE_ID"))
    port = int(os.environ.get("GRADIO_SERVER_PORT", "7860"))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        css=KINGDOM_CSS + NEON_CSS + PERIODIC_CSS,
        theme=_KINGDOM_THEME,
        allowed_paths=[str(PAPERS_DIR), str(OBSERVATIONS_DIR)],
        inbrowser=not on_hf,
        # HF sets GRADIO_SSR_MODE=true by default; the Node SSR proxy can emit
        # harmless asyncio __del__ noise on Python 3.12. Client-side mode is
        # stable for our Plotly-heavy app and avoids the dual-port proxy.
        ssr_mode=False,
    )


if __name__ == "__main__":
    main()