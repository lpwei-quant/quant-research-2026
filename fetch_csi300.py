"""Fetch CSI 300 daily index data from AkShare."""

from argparse import ArgumentParser
from pathlib import Path

import akshare as ak


REQUIRED_COLUMNS = {"date", "open", "high", "low", "close"}


def fetch_csi300(start_date: str, end_date: str, output_path: Path) -> None:
    """Fetch, validate, sort, and save CSI 300 daily prices."""
    frame = ak.stock_zh_index_daily_tx(
        symbol="sh000300",
        start_date=start_date,
        end_date=end_date,
    )
    missing_columns = REQUIRED_COLUMNS.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"AkShare response is missing columns: {sorted(missing_columns)}")
    if frame.empty:
        raise ValueError("AkShare returned no rows for the requested date range")

    frame["date"] = frame["date"].astype("datetime64[ns]")
    frame = frame.sort_values("date").drop_duplicates("date").reset_index(drop=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(
        f"Saved {len(frame):,} rows from {frame['date'].min().date()} "
        f"to {frame['date'].max().date()} at {output_path}"
    )


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--start", default="20230723", help="Start date: YYYYMMDD")
    parser.add_argument("--end", default="20260723", help="End date: YYYYMMDD")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/csi300_daily.csv"),
        help="Output CSV path",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    fetch_csi300(args.start, args.end, args.output)

