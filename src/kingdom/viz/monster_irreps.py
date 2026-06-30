"""Monster group irrep fingerprints — supersingular prime exponent heatmap."""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from kingdom.data.monster_a001379 import MONSTER_IRREP_DEGREES
from kingdom.viz.hopf_plotly import kingdom_dark_theme

SUPERSINGULAR_PRIMES: tuple[int, ...] = (
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71,
)

PADIC_COLUMNS: tuple[str, ...] = tuple(f"padic_{p}" for p in SUPERSINGULAR_PRIMES)

SortMode = Literal[
    "exponent_sum_desc",
    "irrep_index_asc",
    "degree_asc",
    "degree_desc",
]

_DEFAULT_TSV = (
    Path(__file__).resolve().parents[3] / "app" / "assets" / "monster" / "irreps_sum.tsv"
)


@lru_cache(maxsize=4)
def load_monster_irreps_table(tsv_path: str | None = None) -> pd.DataFrame:
    """Load irreps_sum.tsv with degree column attached."""
    path = Path(tsv_path) if tsv_path else _DEFAULT_TSV
    df = pd.read_csv(path, sep="\t")
    df = df.rename(columns={"A001379index": "irrep_index"})
    df["degree"] = [MONSTER_IRREP_DEGREES[int(i)] for i in df["irrep_index"]]
    return df


def _sort_dataframe(df: pd.DataFrame, sort_mode: SortMode) -> pd.DataFrame:
    if sort_mode == "exponent_sum_desc":
        return df.sort_values("row_exponent_sum", ascending=False)
    if sort_mode == "irrep_index_asc":
        return df.sort_values("irrep_index", ascending=True)
    if sort_mode == "degree_asc":
        return df.sort_values("degree", ascending=True)
    return df.sort_values("degree", ascending=False)


def _format_degree(degree: int) -> str:
    if degree < 1_000_000:
        return f"{degree:,}"
    exp = int(math.floor(math.log10(float(degree))))
    mant = degree / 10**exp
    return f"{mant:.3g}×10^{exp}"


def _hover_text(row: pd.Series) -> str:
    parts = [
        f"<b>Irrep {int(row['irrep_index'])}</b>",
        f"Degree: {_format_degree(int(row['degree']))}",
        f"Exponent sum: {int(row['row_exponent_sum'])}",
    ]
    nonzero = [
        f"{col.removeprefix('padic_')}^{int(row[col])}"
        for col in PADIC_COLUMNS
        if int(row[col]) > 0
    ]
    if nonzero:
        parts.append("Factors: " + " · ".join(nonzero))
    else:
        parts.append("Trivial factorization (degree 1)")
    return "<br>".join(parts)


def build_monster_irrep_heatmap(
    *,
    sort_mode: SortMode = "exponent_sum_desc",
    color_mode: str = "linear",
    highlight_irrep: int | None = None,
    height: int = 620,
    tsv_path: str | None = None,
) -> go.Figure:
    """
    15 × 194 heatmap of supersingular prime exponents in Monster irrep degrees.
    """
    df = _sort_dataframe(load_monster_irreps_table(tsv_path), sort_mode)
    z_raw = df[list(PADIC_COLUMNS)].to_numpy(dtype=float)
    if str(color_mode).lower().startswith("log"):
        z_plot = np.log1p(z_raw)
        colorbar_title = "log(1 + exponent)"
    else:
        z_plot = z_raw
        colorbar_title = "Prime exponent"

    y_ticktext = [
        f"{int(r.irrep_index)} · sum {int(r.row_exponent_sum)}"
        for r in df.itertuples(index=False)
    ]
    y_positions = list(range(len(df)))
    x_labels = [str(p) for p in SUPERSINGULAR_PRIMES]
    hover = [_hover_text(row) for _, row in df.iterrows()]

    fig = go.Figure(
        data=go.Heatmap(
            x=x_labels,
            y=y_positions,
            z=z_plot,
            customdata=hover,
            hovertemplate="%{customdata}<extra></extra>",
            colorscale=[
                [0.0, "#0a1628"],
                [0.08, "#1e3a5f"],
                [0.35, "#1a8fe3"],
                [0.65, "#00c9b7"],
                [1.0, "#ffd45a"],
            ],
            colorbar=dict(
                title=dict(text=colorbar_title, side="right", font=dict(size=10)),
                thickness=14,
                len=0.55,
                bgcolor="rgba(10,22,40,0.8)",
                tickfont=dict(size=9, color="#a8c4e0"),
            ),
            xgap=1,
            ygap=1,
        )
    )

    if highlight_irrep is not None:
        row_pos = next(
            (
                i
                for i, (_, row) in enumerate(df.iterrows())
                if int(row["irrep_index"]) == int(highlight_irrep)
            ),
            None,
        )
        if row_pos is not None:
            fig.add_hrect(
                y0=row_pos - 0.5,
                y1=row_pos + 0.5,
                fillcolor="rgba(201,162,39,0.18)",
                line_color="#c9a227",
                line_width=2,
                layer="above",
            )

    sort_titles = {
        "exponent_sum_desc": "sorted by exponent sum (heaviest first)",
        "irrep_index_asc": "sorted by irrep index 0–193",
        "degree_asc": "sorted by degree (ascending)",
        "degree_desc": "sorted by degree (descending)",
    }
    theme = kingdom_dark_theme()
    theme.pop("margin", None)
    fig.update_layout(
        **theme,
        height=height,
        title=dict(
            text=(
                "Monster irrep fingerprints — 15 supersingular primes × 194 irreps "
                f"({sort_titles[sort_mode]})"
            ),
            x=0.5,
            font=dict(size=13, color="#e8f4ff"),
        ),
        xaxis=dict(
            title="Supersingular prime p",
            side="top",
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            title="Irrep (index · exponent sum)",
            autorange="reversed",
            tickmode="array",
            tickvals=list(range(0, len(df), 8)),
            ticktext=[y_ticktext[i] for i in range(0, len(df), 8)],
            tickfont=dict(size=8),
        ),
        margin=dict(l=72, r=48, t=72, b=32),
    )
    return fig