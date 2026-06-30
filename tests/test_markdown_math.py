"""LaTeX delimiter config for Gradio Markdown."""

from app.components.markdown_math import KC_LATEX_DELIMITERS, kc_markdown


def test_kc_latex_delimiters_include_inline_dollar():
    inline = [d for d in KC_LATEX_DELIMITERS if d.get("left") == "$" and not d.get("display")]
    display = [d for d in KC_LATEX_DELIMITERS if d.get("left") == "$$"]
    assert inline, "inline $...$ delimiter required for W_g, S^3, etc."
    assert display, "display $$...$$ delimiter required for equations"


def test_kc_markdown_sets_delimiters():
    md = kc_markdown("$W_{g}$")
    assert md.latex_delimiters == KC_LATEX_DELIMITERS