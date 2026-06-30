"""Tests for Monster irrep fingerprint heatmap."""

from __future__ import annotations

from pathlib import Path

from kingdom.data.monster_a001379 import MOONSHINE_J_COEFF, MONSTER_IRREP_DEGREES
from kingdom.viz.monster_irreps import (
    SUPERSINGULAR_PRIMES,
    build_monster_irrep_heatmap,
    load_monster_irreps_table,
)


def test_monster_degrees_count_and_moonshine():
    assert len(MONSTER_IRREP_DEGREES) == 194
    assert MONSTER_IRREP_DEGREES[0] == 1
    assert MONSTER_IRREP_DEGREES[1] == 196883
    assert MOONSHINE_J_COEFF == 196884


def test_irreps_tsv_loads_194_rows():
    tsv = Path(__file__).resolve().parents[1] / "app" / "assets" / "monster" / "irreps_sum.tsv"
    df = load_monster_irreps_table(str(tsv))
    assert len(df) == 194
    assert list(df.columns)[:3] == ["irrep_index", "padic_2", "padic_3"]
    assert len(SUPERSINGULAR_PRIMES) == 15
    assert int(df.loc[df["irrep_index"] == 0, "row_exponent_sum"].iloc[0]) == 0


def test_heatmap_builds_all_sort_modes():
    for mode in (
        "exponent_sum_desc",
        "irrep_index_asc",
        "degree_asc",
        "degree_desc",
    ):
        fig = build_monster_irrep_heatmap(sort_mode=mode, highlight_irrep=1)
        assert len(fig.data) == 1
        assert fig.data[0].type == "heatmap"


def test_home_model_mentions_monster():
    from app.pages.home import HOME_THE_MODEL_MD

    assert "Monster Fingerprints" in HOME_THE_MODEL_MD
    assert "196883" in HOME_THE_MODEL_MD