# Kingdom Come

**A topological foundation for emergent physics via the Hopf Fibration and gauged flux lattices.**

Kingdom Come is Aaron's unified knowledge repository and interactive portal for a Hopf-fibration-based Theory of Everything (TOE). It serves as:

- **Primary**: Authoritative record for derivations, model evolution, and reproducible physics
- **Secondary**: Professional showcase linking six Hugging Face Spaces and GitHub repos

## Quick Start

```bash
cd ~/Projects/kingdom
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Launch the Gradio portal
python app/app.py
```

Open `http://localhost:7860` — start with the **Hopf Visualizer** tab.

## Project Structure

```
kingdom/
├── src/kingdom/          # Core Python package
│   ├── core/             # Hopf fibration, quaternions, flux flywheels
│   ├── viz/              # Plotly visualizers
│   └── simulations/      # VQC, lattice pipelines
├── app/                  # Hugging Face Space entrypoint
├── docs/                 # Theory & derivations (MkDocs-ready)
├── notebooks/            # Step-by-step explorations
└── tests/
```

## Hugging Face Deployment

Point your Space `app_file` to `app/app.py` and include `requirements.txt`.

## Related Work

- [Hugging Face profile](https://huggingface.co/kinaar111)
- [GitHub](https://github.com/kinaar8340)
- [toe](https://github.com/kinaar8340/toe) · [vqc_sims_public](https://github.com/kinaar8340/vqc_sims_public) · [qvpic](https://github.com/kinaar8340/qvpic)

## License

MIT — see [LICENSE](LICENSE).