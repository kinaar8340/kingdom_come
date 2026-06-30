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
.kc-showcase-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}
.kc-showcase-card {
  display: block;
  background: rgba(18, 36, 61, 0.9);
  border: 1px solid rgba(26, 143, 227, 0.25);
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  color: var(--kc-text);
  transition: border-color 0.2s, transform 0.15s;
}
.kc-showcase-card:hover {
  border-color: var(--kc-teal);
  transform: translateY(-2px);
}
.kc-showcase-card img,
.kc-showcase-thumb {
  width: 100%;
  height: 140px;
  object-fit: cover;
  display: block;
  background: #0d1f35;
}
.kc-thumb-vqc {
  background: linear-gradient(135deg, #0a0818 0%, #7c2d12 45%, #ea580c 100%);
}
.kc-showcase-body { padding: 0.9rem 1rem 1.1rem; }
.kc-showcase-body h3 { color: var(--kc-teal); margin: 0 0 0.4rem; font-size: 1.05rem; }
.kc-showcase-body p { color: #8ecae6; font-size: 0.88rem; line-height: 1.45; margin: 0; }
.kc-showcase-body.kc-no-img { padding-top: 1.1rem; }
.kc-tag {
  display: inline-block;
  margin-top: 0.6rem;
  padding: 0.15rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
  background: rgba(26, 143, 227, 0.2);
  color: var(--kc-blue);
}
.kc-paper-index {
  margin: 0.75rem 0 1.25rem;
}
.kc-paper-index-lead {
  color: #8ecae6;
  font-size: 0.9rem;
  margin: 0 0 0.75rem;
}
.kc-paper-card {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  padding: 0.75rem 1rem;
  margin: 0.4rem 0;
  background: rgba(18, 36, 61, 0.85);
  border: 1px solid rgba(26, 143, 227, 0.2);
  border-radius: 10px;
  text-decoration: none;
  color: var(--kc-text);
  transition: border-color 0.2s;
}
.kc-paper-card:hover {
  border-color: var(--kc-teal);
}
.kc-paper-card-icon {
  font-size: 1.25rem;
  line-height: 1.2;
}
.kc-paper-card-body {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  flex: 1;
  text-align: left;
  align-items: flex-start;
}
.kc-paper-card-body strong {
  color: var(--kc-teal);
  font-size: 0.95rem;
  text-align: left;
  display: block;
  width: 100%;
}
.kc-paper-card-body em {
  color: #8ecae6;
  font-size: 0.82rem;
  font-style: normal;
  line-height: 1.4;
  text-align: left;
  display: block;
  width: 100%;
}
.gradio-container .tab-nav,
.gradio-container .tabs {
  flex-wrap: wrap !important;
  overflow-x: auto !important;
}
.gradio-container button.tab-nav {
  white-space: nowrap;
  flex-shrink: 0;
}
.kc-higgs-header table {
  width: 100%;
  margin: 0.75rem 0 1.25rem;
  border-collapse: collapse;
}
.kc-higgs-header table td {
  padding: 0.35rem 0.75rem;
  border: 1px solid rgba(26, 143, 227, 0.2);
  color: #8ecae6;
  font-size: 0.9rem;
}
.kc-higgs-header h1 {
  color: var(--kc-teal);
  margin-bottom: 0.5rem;
}
.kc-home-hopf-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: stretch;
  gap: 0.75rem;
  margin: 1rem 0 1.25rem;
  padding: 0 0.25rem;
}
.kc-home-hopf-row img {
  flex: 1 1 28%;
  min-width: 160px;
  max-width: 100%;
  height: auto;
  max-height: 220px;
  object-fit: contain;
  background: #000;
  border-radius: 8px;
  border: 1px solid rgba(26, 143, 227, 0.25);
}
@media (max-width: 720px) {
  .kc-home-hopf-row img {
    flex: 1 1 100%;
    max-height: 200px;
  }
}
.kc-obs-image-row .image-container,
.kc-obs-image-row .wrap {
  min-height: 0;
}
.kc-obs-image-row img {
  object-fit: contain;
  background: #0d1f35;
}
.kc-obs-footer {
  text-align: center;
  font-size: 0.88rem;
  color: #5a7a9a;
  margin-top: 1.5rem;
  font-style: italic;
}
.kc-obs-footer em {
  color: #8ecae6;
}
.kc-paper-viewer {
  margin-top: 0.5rem;
}
.kc-paper-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.5rem;
  background: rgba(18, 36, 61, 0.9);
  border: 1px solid rgba(26, 143, 227, 0.2);
  border-radius: 8px;
  font-size: 0.9rem;
}
.kc-paper-toolbar a {
  color: var(--kc-blue);
  text-decoration: none;
  white-space: nowrap;
}
.kc-paper-toolbar a:hover {
  color: var(--kc-teal);
}
.kc-paper-open-btn {
  background: #3b82f6 !important;
  color: #ffffff !important;
  padding: 6px 14px;
  border-radius: 6px;
  font-weight: 500;
}
.kc-paper-open-btn:hover {
  background: #2563eb !important;
  color: #ffffff !important;
}
.kc-paper-brave-hint {
  margin-top: 0.5rem;
  padding: 10px 14px;
  background: #1f2a44;
  border: 1px solid rgba(26, 143, 227, 0.2);
  border-radius: 6px;
  font-size: 0.88rem;
  color: #b8c9dc;
  line-height: 1.45;
}
.kc-paper-frame,
iframe.kc-paper-frame,
embed.kc-paper-frame {
  display: block;
  width: 100%;
  height: min(78vh, 900px);
  min-height: 480px;
  border: 1px solid rgba(26, 143, 227, 0.25);
  border-radius: 8px;
  background: #0d1f35;
}
.kc-paper-fallback {
  text-align: center;
  font-size: 0.82rem;
  color: #5a7a9a;
  margin: 0.5rem 0 0;
}
.kc-paper-fallback a {
  color: var(--kc-blue);
}
.kc-paper-missing {
  padding: 1rem 1.25rem;
  background: rgba(61, 24, 24, 0.55);
  border: 1px solid rgba(227, 90, 90, 0.35);
  border-radius: 8px;
  color: #f0d4d4;
  font-size: 0.9rem;
}
.kc-paper-missing code {
  color: #ffb4b4;
}
.kc-paper-missing a {
  color: var(--kc-blue);
}
.kc-paper-gallery .gallery,
.kc-paper-gallery .grid-wrap {
  width: 100%;
}
.kc-paper-gallery img {
  border-radius: 6px;
  border: 1px solid rgba(26, 143, 227, 0.2);
  background: #0d1f35;
}
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
     and gauged flux lattices — Aaron Michael Kinder's Theory of Everything.</p>
  <p style="font-size:0.95rem;margin-top:0.75rem;">
    <strong>Start here:</strong> Hopf Visualizer → <em>Classic Hopf</em> preset → Update visualization
  </p>
</div>
"""

def footer_html(build_label: str = "Kingdom Come v0.1.0") -> str:
    return f"""
<div class="kc-footer">
  {build_label} · Aaron's Hopf Fibration TOE ·
  <a href="https://huggingface.co/spaces/kinaar111/kingdom" target="_blank">Space</a> ·
  <a href="https://github.com/kinaar8340/kingdom_come" target="_blank">GitHub</a> ·
  <a href="https://huggingface.co/kinaar111" target="_blank">HF Profile</a>
</div>
"""