"""UI math label patching for plain-text Gradio tabs."""

from app.components.ui_math import UI_MATH_LABEL_JS, WG_TAB_LABEL


def test_wg_tab_label_for_js_patch():
    assert WG_TAB_LABEL == "W_g Constant"
    assert "W_g" in WG_TAB_LABEL


def test_ui_math_label_js_patches_wg():
    assert "W_g" in UI_MATH_LABEL_JS
    assert "W<sub>g</sub>" in UI_MATH_LABEL_JS
    assert "MutationObserver" in UI_MATH_LABEL_JS