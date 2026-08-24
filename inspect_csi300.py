"""Run reproducible quality checks on the downloaded CSI 300 data."""

from argparse import ArgumentParser
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"date", "open", "high", "low", "close"}


def inspect_prices(csv_path: Path) -> pd.DataFrame:
    frame = pd.read_csv(csv_path, encoding="utf-8-sig", parse_dates=["date"])

    missing_columns = REQUIRED_COLUMNS.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    if frame.empty:
        raise ValueError("Price file is empty")

    duplicate_dates = int(frame["date"].duplicated().sum())
    missing_values = frame[list(REQUIRED_COLUMNS)].isna().sum()
    non_positive_prices = int(
        (frame[["open", "high", "low", "close"]] <= 0).any(axis=1).sum()
    )

    print(f"Rows: {len(frame):,}")
    print(f"Date range: {frame['date'].min().date()} to {frame['date'].max().date()}")
    print(f"Duplicate dates: {duplicate_dates}")
    print(f"Dates sorted ascending: {frame['date'].is_monotonic_increasing}")
    print(f"Rows with non-positive prices: {non_positive_prices}")
    print("Missing values in required columns:")
    print(missing_values.to_string())

    if duplicate_dates or non_positive_prices or int(missing_values.sum()):
        raise ValueError("Data quality checks failed; inspect the summary above")

    return frame.sort_values("date").reset_index(drop=True)


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/csi300_daily.csv"),
        help="Input CSV path",
    )
    return parser.parse_args()


if __name__ == "__main__":
    inspect_prices(parse_args().input)

