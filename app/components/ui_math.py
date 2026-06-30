"""Plain-text UI labels (tabs, accordions) — patch W_g to subscript via client JS."""

from __future__ import annotations

# Gradio Tab labels are plain text (no LaTeX). Short label — full $W_{g}$ math is in tab body.
WG_TAB_LABEL = "Constant"

# Patches tab buttons / accordion summaries that cannot use kc_markdown LaTeX.
UI_MATH_LABEL_JS = r"""
() => {
  const patch = (root) => {
    root.querySelectorAll("button, summary").forEach((el) => {
      if (el.dataset.kcMathPatched === "1") return;
      const text = el.textContent || "";
      if (text.includes("WgConstant") || text.includes("Wg Constant")) {
        el.innerHTML = el.innerHTML.replace(/Wg\s*Constant/g, 'W<sub>g</sub> Constant');
        el.dataset.kcMathPatched = "1";
        return;
      }
      if (!text.includes("W_g")) return;
      el.innerHTML = el.innerHTML.replace(/W_g\s*/g, 'W<sub>g</sub> ');
      el.dataset.kcMathPatched = "1";
    });
  };
  patch(document);
  const obs = new MutationObserver(() => patch(document));
  obs.observe(document.body, { childList: true, subtree: true });
  return [];
}
"""