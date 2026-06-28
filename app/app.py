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
from kingdom.viz.hopf_plotly import build_hopf_fibration_figure

from app.components.theme import FOOTER_HTML, HERO_HTML, KINGDOM_CSS
from app.pages.home import HOME_MD, SHOWCASE_CARDS
from app.pages.theory import DERIVATION_HOPF_MD, THEORY_MD


def render_hopf_visualizer(
    n_fibers: int,
    n_points: int,
    eta: float,
    xi1: float,
    show_base: bool,
    show_highlight: bool,
    scale: float,
):
    return build_hopf_fibration_figure(
        n_fibers=int(n_fibers),
        n_points=int(n_points),
        eta=float(eta),
        xi1=float(xi1),
        show_base_sphere=show_base,
        show_single_fiber_highlight=show_highlight,
        projection_scale=float(scale),
    )


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
                gr.Markdown(HOME_MD)
                gr.HTML(SHOWCASE_CARDS)

            with gr.Tab("Hopf Visualizer"):
                gr.Markdown(
                    "Explore linked Hopf fibers stereographically projected to ℝ³, "
                    "with the S² base space alongside. Drag to rotate; scroll to zoom."
                )
                with gr.Row():
                    n_fibers = gr.Slider(3, 16, value=8, step=1, label="Number of fibers")
                    n_points = gr.Slider(60, 300, value=160, step=20, label="Points per fiber")
                    scale = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="Projection scale")
                with gr.Row():
                    eta = gr.Slider(0.1, 1.4, value=0.6, step=0.05, label="Highlight η")
                    xi1 = gr.Slider(0.0, 6.28, value=1.2, step=0.1, label="Highlight ξ₁")
                with gr.Row():
                    show_base = gr.Checkbox(value=True, label="Show S² base sphere")
                    show_highlight = gr.Checkbox(value=True, label="Highlight single fiber")
                hopf_plot = gr.Plot(label="Hopf Fibration")
                refresh = gr.Button("Update visualization", variant="primary")
                refresh.click(
                    render_hopf_visualizer,
                    inputs=[n_fibers, n_points, eta, xi1, show_base, show_highlight, scale],
                    outputs=hopf_plot,
                )
                demo.load(
                    render_hopf_visualizer,
                    inputs=[n_fibers, n_points, eta, xi1, show_base, show_highlight, scale],
                    outputs=hopf_plot,
                )

            with gr.Tab("The Model"):
                gr.Markdown(THEORY_MD)
                with gr.Accordion("Derivation: Hopf Map via Quaternions", open=True):
                    gr.Markdown(DERIVATION_HOPF_MD)

            with gr.Tab("Flux Flywheel"):
                gr.Markdown("Map atomic number **Z** to flux flywheel stability (Magic Island calibration).")
                z_slider = gr.Slider(1, 180, value=2, step=1, label="Atomic number Z")
                flywheel_out = gr.Markdown()
                z_slider.change(render_flywheel, inputs=z_slider, outputs=flywheel_out)
                demo.load(render_flywheel, inputs=z_slider, outputs=flywheel_out)

            with gr.Tab("Showcase"):
                gr.Markdown(
                    """
## Hugging Face Spaces

| Space | TOE context |
|-------|-------------|
| [Hopf Flux Bubble](https://huggingface.co/spaces/kinaar111/hopf-flux-bubble) | Gauged flux topology, Hopfion walls |
| [Orbital Braille VQC](https://huggingface.co/spaces/kinaar111/orbital-braille-vqc) | Quaternion OAM encoding |
| [QVpic](https://github.com/kinaar8340/qvpic) | Lattice swarm, stability sweeps |

## GitHub

- [toe](https://github.com/kinaar8340/toe) — core conduit & lattice
- [vqc_sims_public](https://github.com/kinaar8340/vqc_sims_public) — VQC simulations
- [kingdom-come](https://github.com/kinaar8340/kingdom-come) — this repository
                    """
                )

        gr.HTML(FOOTER_HTML)

    return demo


if __name__ == "__main__":
    app = build_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        css=KINGDOM_CSS,
        theme=_KINGDOM_THEME,
    )