import numpy as np
import pandas as pd
import pytest

from src.return_nav_analysis import calculate_return_nav, prepare_price_data


def sample_prices() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2026-01-05", "2026-01-02", "2026-01-06", "2026-01-07", "2026-01-08"]
            ),
            "close": [102.0, 100.0, 99.0, 103.0, 104.0],
        }
    )


def test_prepare_price_data_sorts_and_keeps_only_structural_missing_return() -> None:
    prepared = prepare_price_data(sample_prices())

    assert prepared["date"].is_monotonic_increasing
    assert prepared["simple_return"].isna().sum() == 1
    assert pd.isna(prepared.loc[0, "simple_return"])


def test_calculate_return_nav_cross_validates_equivalent_paths() -> None:
    prepared = prepare_price_data(sample_prices())
    result = calculate_return_nav(prepared)

    assert result.loc[0, "simple_return"] == 0.0
    assert np.allclose(result["nav"], result["nav_from_log"], rtol=1e-12, atol=1e-12)
    assert np.isclose(result.iloc[-1]["nav"], 1.04)


def test_prepare_price_data_rejects_missing_close_inside_series() -> None:
    prices = sample_prices()
    prices.loc[2, "close"] = np.nan

    with pytest.raises(ValueError, match="close contains missing values"):
        prepare_price_data(prices)


def test_prepare_price_data_rejects_duplicate_dates() -> None:
    prices = sample_prices()
    prices.loc[2, "date"] = prices.loc[1, "date"]

    with pytest.raises(ValueError, match="duplicate dates"):
        prepare_price_data(prices)
