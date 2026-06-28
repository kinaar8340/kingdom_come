#!/usr/bin/env python3
"""Kingdom Come — Hugging Face Space entrypoint."""

from __future__ import annotations

import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from kingdom.core.flux_flywheel import map_z_to_flywheel
from kingdom.simulations.lattice import build_lattice_figure, run_lattice_comparison
from kingdom.viz.hopf_plotly import build_hopf_fibration_figure_auto, default_view_mode, is_hf_space

from app.build_info import get_build_label
from app.components.theme import HERO_HTML, KINGDOM_CSS, footer_html
from app.pages.help import HELP_MD, QUICKSTART_MD
from app.pages.home import HOME_MD, ONBOARDING_MD, SHOWCASE_CARDS
from app.pages.showcase import SHOWCASE_HTML
from app.pages.theory import DERIVATION_HOPF_MD, THEORY_MD

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


def render_flywheel(z: int) -> str:
    result = map_z_to_flywheel(int(z))
    lines = [f"**Z = {result['Z']}** — {result['stability_class']}", ""]
    for key in (
        "stability_score",
        "delta_omega",
        "omega_L",
        "omega_R",
        "gauge_strength",
        "num_layers",
        "num_polarities",
        "pseudo_Z",
        "notes",
    ):
        lines.append(f"- **{key}**: {result[key]}")
    return "\n".join(lines)


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
                gr.Markdown(
                    "Explore linked Hopf fibers stereographically projected to ℝ³, "
                    "with the S² base chart alongside. "
                    + (
                        "**2D projections** are used here (Hugging Face iframes often block WebGL). "
                        if is_hf_space()
                        else "Choose **2D** for compatibility or **3D** for interactive rotation."
                    )
                )
                view_choices = [
                    "2D projections (recommended)",
                    "3D interactive (WebGL)",
                ]
                default_view = (
                    "2D projections (recommended)"
                    if default_view_mode() == "2d"
                    else "3D interactive (WebGL)"
                )
                with gr.Row():
                    view_mode = gr.Radio(
                        view_choices,
                        value=default_view,
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
                gr.Markdown("**Try a preset** — loads parameters, then click *Update visualization*.")
                with gr.Row():
                    preset_btns = [
                        gr.Button(name, size="sm") for name in HOPF_PRESETS
                    ]
                    reset_btn = gr.Button("Reset defaults", size="sm")
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
                    dv = (
                        "2D projections (recommended)"
                        if default_view_mode() == "2d"
                        else "3D interactive (WebGL)"
                    )
                    return (
                        d["n_fibers"],
                        d["n_points"],
                        d["eta"],
                        d["xi1"],
                        d["show_base"],
                        d["show_highlight"],
                        d["scale"],
                        dv,
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
                gr.Markdown("Map atomic number **Z** to flux flywheel stability (Magic Island calibration).")
                z_slider = gr.Slider(1, 180, value=2, step=1, label="Atomic number Z")
                flywheel_out = gr.Markdown()
                z_slider.change(render_flywheel, inputs=z_slider, outputs=flywheel_out)
                demo.load(render_flywheel, inputs=z_slider, outputs=flywheel_out)

            with gr.Tab("Showcase"):
                gr.Markdown(
                    "Related Hugging Face Spaces and GitHub repositories in the TOE ecosystem. "
                    "Each card links to the live project with a one-line connection to Kingdom Come."
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
        css=KINGDOM_CSS,
        theme=_KINGDOM_THEME,
        inbrowser=not on_hf,
    )


if __name__ == "__main__":
    main()