"""Periodic trend plots for Observations tab."""

from kingdom.viz.observations_trends import (
    create_fidelity_trend_plot,
    create_soc_mu_vs_experimental_plot,
    create_stability_vs_ie_plot,
    load_observations_trend_figures,
    observations_trends_dataframe,
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