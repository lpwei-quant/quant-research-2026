"""Identify extreme CSI 300 return days and calendar gaps."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.return_nav_analysis import DEFAULT_DATA_PATH, prepare_price_data


def summarize_extreme_days(
    frame: pd.DataFrame,
    count: int = 5,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return the largest gains and losses with intraday context."""
    if count <= 0:
        raise ValueError("count must be positive")

    result = prepare_price_data(frame)
    if "open" not in result.columns:
        raise ValueError("open column is required for intraday context")

    result["open"] = pd.to_numeric(result["open"], errors="raise")
    if result["open"].isna().any():
        raise ValueError("open contains missing values")
    if (result["open"] <= 0).any():
        raise ValueError("open must be strictly positive")

    result["open_to_close_return"] = result["close"] / result["open"] - 1.0
    columns = ["date", "open", "close", "simple_return", "open_to_close_return"]
    gains = result.nlargest(count, "simple_return")[columns].reset_index(drop=True)
    losses = result.nsmallest(count, "simple_return")[columns].reset_index(drop=True)
    return gains, losses


def calculate_window_return(
    frame: pd.DataFrame,
    start_date: str,
    end_date: str,
) -> tuple[int, float]:
    """Calculate close-to-close return from the close before a selected window."""
    result = prepare_price_data(frame)
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    if start > end:
        raise ValueError("start_date must not be after end_date")

    selected = result[result["date"].between(start, end)]
    if selected.empty:
        raise ValueError("selected window contains no observations")

    first_index = int(selected.index[0])
    if first_index == 0:
        raise ValueError("a prior close is required to calculate the window return")

    prior_close = float(result.loc[first_index - 1, "close"])
    final_close = float(selected.iloc[-1]["close"])
    return len(selected), final_close / prior_close - 1.0


def run_analysis(data_path: Path = DEFAULT_DATA_PATH) -> None:
    """Print a bounded extreme-day report from the local CSV."""
    frame = pd.read_csv(data_path, parse_dates=["date"])
    gains, losses = summarize_extreme_days(frame)
    count, event_return = calculate_window_return(frame, "2024-09-24", "2024-10-08")

    display_columns = [
        "date",
        "close",
        "simple_return",
        "open_to_close_return",
    ]
    print("Largest gains:")
    print(gains[display_columns].to_string(index=False))
    print("\nLargest losses:")
    print(losses[display_columns].to_string(index=False))
    print(
        "\n2024-09-24 to 2024-10-08: "
        f"{count} trading sessions, close-to-close return {event_return:.2%}"
    )


if __name__ == "__main__":
    run_analysis()
