"""Gradio Markdown with inline + display LaTeX enabled.

Gradio 6 defaults to $$...$$ only; without $...$ delimiters inline math shows
as raw text (broken W_g, S^3, Delta symbols) in the browser.
"""

from __future__ import annotations

import gradio as gr

KC_LATEX_DELIMITERS: list[dict[str, str | bool]] = [
    {"left": "$$", "right": "$$", "display": True},
    {"left": "$", "right": "$", "display": False},
    {"left": "\\(", "right": "\\)", "display": False},
    {"left": "\\[", "right": "\\]", "display": True},
]


def kc_markdown(value: str | None = None, **kwargs) -> gr.Markdown:
    """Markdown component with Kingdom Come LaTeX delimiters."""
    kwargs.setdefault("latex_delimiters", KC_LATEX_DELIMITERS)
    return gr.Markdown(value, **kwargs)