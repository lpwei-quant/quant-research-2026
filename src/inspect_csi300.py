"""Print a bounded data-quality report for the local CSI 300 CSV."""

from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "csi300_daily.csv"


def inspect_data(data_path: Path = DATA_PATH) -> pd.DataFrame:
    frame = pd.read_csv(data_path, encoding="utf-8-sig", parse_dates=["date"])
    print(f"Shape: {frame.shape}")
    print("\nData types:")
    print(frame.dtypes)
    print("\nMissing values:")
    print(frame.isna().sum())
    print(f"\nDate range: {frame['date'].min().date()} to {frame['date'].max().date()}")
    print("\nNumeric summary:")
    print(frame.describe(include="all"))
    return frame


if __name__ == "__main__":
    inspect_data()
