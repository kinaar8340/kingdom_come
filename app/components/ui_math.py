"""Plain-text UI labels (tabs, accordions) — patch W_g to subscript via client JS."""

from __future__ import annotations

# Gradio Tab labels are plain text (no LaTeX). Short label — full $W_{g}$ math is in tab body.
WG_TAB_LABEL = "Constant"

# Patches tab buttons / accordion summaries that cannot use kc_markdown LaTeX.
UI_MATH_LABEL_JS = r"""
() => {
  const patchMath = (root) => {
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
  const patchNobleBanners = (root) => {
    root.querySelectorAll("details.kc-obs-noble-banner[data-kc-noble-z]").forEach((el) => {
      if (el.dataset.kcNobleInit === "1") return;
      const z = el.dataset.kcNobleZ;
      const key = "kc-noble-banner-" + z;
      if (localStorage.getItem(key)) el.removeAttribute("open");
      el.addEventListener("toggle", () => {
        if (!el.open) localStorage.setItem(key, "1");
      });
      el.dataset.kcNobleInit = "1";
    });
  };
  const patchInvestigationLabels = (root) => {
    root.querySelectorAll("button, summary, .label-wrap").forEach((el) => {
      if (el.dataset.kcInvPatched === "1") return;
      const text = (el.textContent || "").trim();
      const match = text.match(/^(Investigation \d+:)(.*)$/);
      if (!match) return;
      el.innerHTML =
        '<span class="kc-inv-label-num">' + match[1] + '</span>' +
        '<span class="kc-inv-label-desc">' + match[2] + '</span>';
      el.dataset.kcInvPatched = "1";
    });
  };
  const patch = (root) => {
    patchMath(root);
    patchNobleBanners(root);
    patchInvestigationLabels(root);
  };
  patch(document);
  const obs = new MutationObserver(() => patch(document));
  obs.observe(document.body, { childList: true, subtree: true });
  return [];
}
"""