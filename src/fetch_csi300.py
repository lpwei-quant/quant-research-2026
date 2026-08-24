"""Download CSI 300 price-index data through AkShare."""

from pathlib import Path

import akshare as ak


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / "data" / "csi300_daily.csv"


def fetch_csi300() -> Path:
    frame = ak.stock_zh_index_daily_tx(
        symbol="sh000300",
        start_date="20230723",
        end_date="20260723",
    )
    if frame.empty:
        raise RuntimeError("AkShare returned no CSI 300 data")

    required = {"date", "open", "close", "high", "low", "amount"}
    missing_columns = required.difference(frame.columns)
    if missing_columns:
        raise RuntimeError(f"AkShare response is missing columns: {sorted(missing_columns)}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"Saved {len(frame)} rows to {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    fetch_csi300()
