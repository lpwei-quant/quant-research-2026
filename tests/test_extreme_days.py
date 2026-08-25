import numpy as np
import pandas as pd

from src.extreme_days_analysis import calculate_window_return, summarize_extreme_days


def sample_prices() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2026-01-02", "2026-01-05", "2026-01-06", "2026-01-07"]
            ),
            "open": [100.0, 101.0, 96.0, 102.0],
            "close": [100.0, 102.0, 96.0, 104.0],
        }
    )


def test_summarize_extreme_days_adds_intraday_context() -> None:
    gains, losses = summarize_extreme_days(sample_prices(), count=1)

    assert gains.loc[0, "date"] == pd.Timestamp("2026-01-07")
    assert losses.loc[0, "date"] == pd.Timestamp("2026-01-06")
    assert np.isclose(gains.loc[0, "open_to_close_return"], 104 / 102 - 1)


def test_calculate_window_return_uses_prior_close() -> None:
    count, return_value = calculate_window_return(
        sample_prices(), "2026-01-05", "2026-01-07"
    )

    assert count == 3
    assert np.isclose(return_value, 0.04)
