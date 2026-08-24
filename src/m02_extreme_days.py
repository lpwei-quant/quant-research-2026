"""Identify extreme CSI 300 days and analyze the 2024 rally window."""

from argparse import ArgumentParser
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"date", "open", "close"}
EVENT_START = "2024-09-24"
EVENT_END = "2024-10-08"
INTRADAY_DATE = "2024-10-08"


def load_prices(csv_path: Path) -> pd.DataFrame:
    frame = pd.read_csv(csv_path, encoding="utf-8-sig", parse_dates=["date"])
    missing_columns = REQUIRED_COLUMNS.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    if frame.empty:
        raise ValueError("Price file is empty")
    frame = frame.sort_values("date").reset_index(drop=True)
    frame["simple_return"] = frame["close"].pct_change(fill_method=None)
    return frame


def analyze_extremes(frame: pd.DataFrame, output_dir: Path) -> dict[str, float]:
    output_dir.mkdir(parents=True, exist_ok=True)

    largest_gains = frame.nlargest(5, "simple_return")[
        ["date", "open", "close", "simple_return"]
    ]
    largest_losses = frame.nsmallest(5, "simple_return")[
        ["date", "open", "close", "simple_return"]
    ]
    event_window = frame.loc[
        frame["date"].between(pd.Timestamp(EVENT_START), pd.Timestamp(EVENT_END)),
        ["date", "open", "close", "simple_return"],
    ].copy()
    if event_window.empty:
        raise ValueError("The configured event window is absent from the input data")

    intraday_row = frame.loc[frame["date"].eq(pd.Timestamp(INTRADAY_DATE))]
    if len(intraday_row) != 1:
        raise ValueError(f"Expected one row for {INTRADAY_DATE}, found {len(intraday_row)}")

    largest_gains.to_csv(output_dir / "largest_gains.csv", index=False, encoding="utf-8-sig")
    largest_losses.to_csv(output_dir / "largest_losses.csv", index=False, encoding="utf-8-sig")
    event_window.to_csv(output_dir / "event_window_2024.csv", index=False, encoding="utf-8-sig")

    event_return = float((1 + event_window["simple_return"]).prod() - 1)
    row = intraday_row.iloc[0]
    open_to_close_return = float(row["close"] / row["open"] - 1)

    return {
        "event_trading_days": float(len(event_window)),
        "event_cumulative_return": event_return,
        "intraday_open_to_close_return": open_to_close_return,
        "largest_daily_gain": float(largest_gains.iloc[0]["simple_return"]),
        "largest_daily_loss": float(largest_losses.iloc[0]["simple_return"]),
    }


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/csi300_daily.csv"),
        help="Input CSV path",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output/tables"),
        help="Directory for result tables",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    prices = load_prices(args.input)
    summary = analyze_extremes(prices, args.output_dir)

    print("Extreme-day summary:")
    print(f"- event trading days: {int(summary['event_trading_days'])}")
    print(f"- event cumulative return: {summary['event_cumulative_return']:.2%}")
    print(f"- 2024-10-08 open-to-close return: {summary['intraday_open_to_close_return']:.2%}")
    print(f"- largest daily gain: {summary['largest_daily_gain']:.2%}")
    print(f"- largest daily loss: {summary['largest_daily_loss']:.2%}")
    print(f"Saved result tables to {args.output_dir}")

