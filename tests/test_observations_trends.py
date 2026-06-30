"""Periodic trend plots for Observations tab."""

from types import SimpleNamespace

from kingdom.viz.observations_trends import (
    create_fidelity_trend_plot,
    create_soc_mu_vs_experimental_plot,
    create_stability_vs_ie_plot,
    filter_trends_by_period,
    load_observations_trend_figures,
    observations_trends_dataframe,
    z_from_plot_select,
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
    assert len(figs) == 3
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


def test_fidelity_plot_customdata_includes_z():
    fig = create_fidelity_trend_plot(observations_trends_dataframe(30))
    assert fig.data[0].customdata is not None
    assert int(fig.data[0].customdata[0][0]) >= 1


def test_period_filtered_trend_figures():
    figs = load_observations_trend_figures(30, periods=[2, 3])
    assert len(figs) == 3