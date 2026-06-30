"""Periodic trend plots for Observations tab."""

from types import SimpleNamespace

from kingdom.viz.observations_trends import (
    create_fidelity_trend_plot,
    create_soc_mu_vs_experimental_plot,
    create_stability_vs_en_plot,
    create_stability_vs_ie_plot,
    fidelity_trend_dataframe,
    filter_trends_by_period,
    load_observations_trend_dataframes,
    load_observations_trend_figures,
    observations_trends_dataframe,
    stability_en_trend_dataframe,
    stability_ie_trend_dataframe,
    z_from_plot_select,
    z_from_scatter_select,
)


def test_observations_trends_dataframe_covers_table():
    df = observations_trends_dataframe(118)
    assert len(df) == 118
    assert "fidelity_score" in df.columns
    assert "model_stability" in df.columns
    assert df["element"].iloc[25] == "Fe"
    assert df.dropna(subset=["fidelity_score"]).shape[0] >= 100


def test_fidelity_trend_plot_builds():
    fig = create_fidelity_trend_plot()
    assert len(fig.data) >= 1
    assert "Fidelity" in fig.layout.title.text


def test_stability_vs_ie_plot_has_trend_or_points():
    fig = create_stability_vs_ie_plot()
    assert len(fig.data) >= 1
    names = [getattr(t, "name", "") for t in fig.data]
    assert any("Period" in (n or "") for n in names) or "OLS trend" in names


def test_soc_mu_plot_builds():
    fig = create_soc_mu_vs_experimental_plot()
    assert fig.layout.title.text is not None


def test_load_observations_trend_figures_tuple():
    figs = load_observations_trend_figures(30)
    assert len(figs) == 4
    for fig in figs:
        assert fig.layout.height is not None


def test_filter_trends_by_period():
    df = observations_trends_dataframe(30)
    filtered = filter_trends_by_period(df, [4])
    assert filtered["period"].nunique() == 1
    assert filtered["period"].iloc[0] == 4


def test_z_from_plot_select_customdata():
    evt = SimpleNamespace(value=[26, "Fe"], index=(0, 3))
    assert z_from_plot_select(evt) == 26


def test_z_from_scatter_select_fidelity_midpoint():
    df = fidelity_trend_dataframe(observations_trends_dataframe(30))
    evt = SimpleNamespace(index=(25.5, 26.5), selected=True)
    assert z_from_scatter_select(evt, df, x_col="Z") == 26


def test_z_from_scatter_select_stability_lookup():
    df = stability_ie_trend_dataframe(observations_trends_dataframe(30))
    row = df[df["element"] == "Fe"].iloc[0]
    evt = SimpleNamespace(
        index=(
            row["model_stability"] - 0.01,
            row["model_stability"] + 0.01,
            row["experimental_ie"] - 0.01,
            row["experimental_ie"] + 0.01,
        ),
        selected=True,
    )
    assert z_from_scatter_select(
        evt,
        df,
        x_col="model_stability",
        y_col="experimental_ie",
    ) == 26


def test_stability_vs_en_plot_builds():
    fig = create_stability_vs_en_plot()
    assert len(fig.data) >= 1
    assert "Allen" in fig.layout.title.text


def test_stability_en_trend_dataframe_has_en():
    df = stability_en_trend_dataframe(observations_trends_dataframe(30))
    assert "experimental_en" in df.columns
    assert df["experimental_en"].notna().any()


def test_load_observations_trend_dataframes_tuple():
    dfs = load_observations_trend_dataframes(30)
    assert len(dfs) == 4
    fidelity_df, stability_df, stability_en_df, mu_df = dfs
    assert "Z" in fidelity_df.columns
    assert "fidelity_score" in fidelity_df.columns
    assert "model_stability" in stability_df.columns
    assert "experimental_en" in stability_en_df.columns
    assert list(mu_df.columns)


def test_fidelity_plot_customdata_includes_z():
    fig = create_fidelity_trend_plot(observations_trends_dataframe(30))
    assert fig.data[0].customdata is not None
    assert int(fig.data[0].customdata[0][0]) >= 1


def test_period_filtered_trend_figures():
    figs = load_observations_trend_figures(30, periods=[2, 3])
    assert len(figs) == 4