"""Kingdom Come Gradio theme and shared styles."""

KINGDOM_CSS = """
:root {
  --kc-bg: #0a1628;
  --kc-surface: #12243d;
  --kc-teal: #00c9b7;
  --kc-blue: #1a8fe3;
  --kc-gold: #c9a227;
  --kc-text: #d4e4f7;
}
.gradio-container {
  background: linear-gradient(165deg, #0a1628 0%, #0d1f35 45%, #0a1628 100%) !important;
  color: var(--kc-text) !important;
}
.kc-hero {
  text-align: center;
  padding: 2rem 1rem 1.5rem;
  border-bottom: 1px solid rgba(26, 143, 227, 0.25);
  margin-bottom: 1rem;
}
.kc-hero h1 {
  font-size: 2.2rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  background: linear-gradient(90deg, #1a8fe3, #00c9b7, #c9a227);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}
.kc-hero p {
  color: #8ecae6;
  font-size: 1.05rem;
  max-width: 720px;
  margin: 0 auto;
}
.kc-card {
  background: rgba(18, 36, 61, 0.85);
  border: 1px solid rgba(26, 143, 227, 0.2);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin: 0.5rem 0;
}
.kc-card h3 { color: var(--kc-teal); margin-top: 0; }
.kc-footer {
  text-align: center;
  font-size: 0.85rem;
  color: #5a7a9a;
  padding: 1.5rem 0 0.5rem;
  border-top: 1px solid rgba(26, 143, 227, 0.15);
  margin-top: 2rem;
}
"""

HERO_HTML = """
<div class="kc-hero">
  <h1>Kingdom Come</h1>
  <p>A topological foundation for emergent physics via the Hopf Fibration
     and gauged flux lattices — Aaron's Theory of Everything.</p>
</div>
"""

FOOTER_HTML = """
<div class="kc-footer">
  Kingdom Come · Aaron's Hopf Fibration TOE ·
  <a href="https://huggingface.co/kinaar111" target="_blank">Hugging Face</a> ·
  <a href="https://github.com/kinaar8340" target="_blank">GitHub</a>
</div>
"""