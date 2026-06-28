"""Showcase tab — related Spaces and repos with thumbnails."""

SHOWCASE_HTML = """
<div class="kc-showcase-grid">

  <a class="kc-showcase-card" href="https://huggingface.co/spaces/kinaar111/hopf-flux-bubble" target="_blank">
    <img src="https://raw.githubusercontent.com/kinaar8340/vqc_proto/main/hfb.png"
         alt="Hopf Flux Bubble preview" loading="lazy" />
    <div class="kc-showcase-body">
      <h3>Hopf Flux Bubble</h3>
      <p>Gauged flux metrics, Hopfion textures, analog gravity. Demonstrates topological
         defect walls and effective-metric explorations in the TOE lattice picture.</p>
      <span class="kc-tag">HF Space</span>
    </div>
  </a>

  <a class="kc-showcase-card" href="https://huggingface.co/spaces/kinaar111/orbital-braille-vqc" target="_blank">
    <div class="kc-showcase-thumb kc-thumb-vqc" aria-hidden="true"></div>
    <div class="kc-showcase-body">
      <h3>Orbital Braille VQC</h3>
      <p>Quaternion-encoded OAM propagation — helix-within-helix beams, PWM-gated orbits,
         and the optics control-panel UI lineage Kingdom Come inherits.</p>
      <span class="kc-tag">HF Space</span>
    </div>
  </a>

  <a class="kc-showcase-card" href="https://github.com/kinaar8340/qvpic" target="_blank">
    <div class="kc-showcase-body kc-no-img">
      <h3>QVpic</h3>
      <p>Lattice swarm demos, magic-island stability sweeps, z-flywheel mapping, and
         periodic-table emergence prototypes feeding Kingdom Come's flux flywheel tab.</p>
      <span class="kc-tag">GitHub</span>
    </div>
  </a>

  <a class="kc-showcase-card" href="https://github.com/kinaar8340/toe" target="_blank">
    <div class="kc-showcase-body kc-no-img">
      <h3>toe</h3>
      <p>Core RubikConeConduit / lattice conduit, two-gyro simulations, and the source
         for Kingdom Come's Lattice Simulator integration.</p>
      <span class="kc-tag">GitHub</span>
    </div>
  </a>

  <a class="kc-showcase-card" href="https://github.com/kinaar8340/vqc_sims_public" target="_blank">
    <div class="kc-showcase-body kc-no-img">
      <h3>vqc_sims_public</h3>
      <p>Quaternion vortex encode/decode pipelines, OAM knot analysis, and Roemmele-proxy
         visualizations connecting topology to beam physics.</p>
      <span class="kc-tag">GitHub</span>
    </div>
  </a>

  <a class="kc-showcase-card" href="https://github.com/kinaar8340/kingdom_come" target="_blank">
    <img src="app/assets/hopf_preview.png" alt="Kingdom Come Hopf preview" loading="lazy" />
    <div class="kc-showcase-body">
      <h3>kingdom_come</h3>
      <p>This repository — source of truth for code, docs, derivations, and the Gradio
         portal you are using now.</p>
      <span class="kc-tag">GitHub · you are here</span>
    </div>
  </a>

</div>
"""