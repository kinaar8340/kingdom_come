"""UI math label patching for plain-text Gradio tabs."""

from app.components.ui_math import UI_MATH_LABEL_JS, WG_TAB_LABEL


def test_wg_tab_label_for_js_patch():
    assert WG_TAB_LABEL == "Constant"


def test_ui_math_label_js_patches_wg():
    assert "WgConstant" in UI_MATH_LABEL_JS
    assert "W<sub>g</sub> Constant" in UI_MATH_LABEL_JS
    assert "MutationObserver" in UI_MATH_LABEL_JS