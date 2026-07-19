"""Book Mode — QGA manuscript map and widget indices."""

from app.pages.book_mode import (
    BOOK_MODE_INTRO_MD,
    BOOK_TOC_MD,
    CHAPTERS,
    WIDGET_TAB_INDEX,
    chapter_by_key,
    chapter_detail_md,
    chapter_dropdown_choices,
    main_tab_index_for_widget,
    widget_key_for_chapter,
)


def test_eleven_chapters_cover_ch0_to_ch10():
    keys = [c.key for c in CHAPTERS]
    assert keys == [f"ch{i}" for i in range(11)]
    assert len(chapter_dropdown_choices()) == 11


def test_widget_keys_are_known_tabs():
    for c in CHAPTERS:
        assert c.widget in WIDGET_TAB_INDEX, c
        assert main_tab_index_for_widget(c.widget) == WIDGET_TAB_INDEX[c.widget]


def test_tab_index_order_matches_app_comment():
    # 0 Home · 1 Help · 2 Book · 3 Hopf · 4 Toroidal · 5 Monster ·
    # 6 Lattice · 7 Flux · 8 Observations · 9 Showcase
    assert WIDGET_TAB_INDEX == {
        "home": 0,
        "help": 1,
        "book": 2,
        "hopf": 3,
        "toroidal": 4,
        "monster": 5,
        "lattice": 6,
        "flux": 7,
        "observations": 8,
        "showcase": 9,
    }


def test_chapter_widget_routing():
    assert widget_key_for_chapter("ch2") == "hopf"
    assert widget_key_for_chapter("ch3") == "lattice"
    assert widget_key_for_chapter("ch7") == "flux"
    assert widget_key_for_chapter("ch10") == "observations"
    assert widget_key_for_chapter("ch9") == "home"
    assert chapter_by_key("missing").key == "ch0"


def test_detail_and_intro_content():
    detail = chapter_detail_md("ch7")
    assert "Flux Flywheel" in detail
    assert "OP4" in detail or "Z" in detail
    assert "github.com/kinaar8340/qga" in BOOK_MODE_INTRO_MD
    assert "Manuscript map" in BOOK_TOC_MD
    assert "Hopf Visualizer" in BOOK_TOC_MD
