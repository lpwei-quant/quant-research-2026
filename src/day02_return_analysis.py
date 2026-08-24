"""Calculate CSI 300 returns, cross-check NAV, and save summary outputs."""

from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import pandas as pd


TRADING_DAYS = 252
REQUIRED_COLUMNS = {"date", "close"}


def load_prices(csv_path: Path) -> pd.DataFrame:
    frame = pd.read_csv(csv_path, encoding="utf-8-sig", parse_dates=["date"])
    missing_columns = REQUIRED_COLUMNS.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    if frame.empty:
        raise ValueError("Price file is empty")
    if frame["date"].duplicated().any():
        raise ValueError("Price file contains duplicate dates")
    if frame["close"].isna().any() or (frame["close"] <= 0).any():
        raise ValueError("Close prices must be positive and non-missing")
    return frame.sort_values("date").reset_index(drop=True)


def calculate_returns(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    result = frame.copy()
    result["simple_return"] = result["close"].pct_change(fill_method=None)
    result["log_return"] = np.log1p(result["simple_return"])
    result["nav"] = (1 + result["simple_return"].fillna(0)).cumprod()
    result["nav_from_log"] = np.exp(result["log_return"].fillna(0).cumsum())

    if not np.allclose(result["nav"], result["nav_from_log"], rtol=1e-10, atol=1e-12):
        raise AssertionError("Simple-return and log-return NAV paths do not match")

    valid_returns = result["simple_return"].dropna()
    observations = len(valid_returns)
    if observations == 0:
        raise ValueError("At least two price observations are required")
    cumulative_return = float(result["nav"].iloc[-1] - 1)
    annualized_return = float((1 + cumulative_return) ** (TRADING_DAYS / observations) - 1)
    annualized_volatility = float(valid_returns.std(ddof=1) * np.sqrt(TRADING_DAYS))
    drawdown = result["nav"] / result["nav"].cummax() - 1

    metrics = {
        "observations": float(observations),
        "cumulative_return": cumulative_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "max_drawdown": float(drawdown.min()),
        "ending_nav": float(result["nav"].iloc[-1]),
    }
    return result, metrics


def save_outputs(
    frame: pd.DataFrame,
    metrics: dict[str, float],
    figure_path: Path,
    metrics_path: Path,
) -> None:
    import matplotlib.pyplot as plt

    figure_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(frame["date"], frame["nav"], label="CSI 300 NAV")
    ax.axhline(y=1.0, linestyle="--", linewidth=1, label="Initial NAV")
    ax.set_title("CSI 300 Normalized Net Value")
    ax.set_xlabel("Date")
    ax.set_ylabel("Net Value")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(figure_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    pd.Series(metrics, name="value").to_csv(metrics_path, header=True)


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/csi300_daily.csv"),
        help="Input CSV path",
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path("output/figures/csi300_nav_curve.png"),
        help="Output figure path",
    )
    parser.add_argument(
        "--metrics",
        type=Path,
        default=Path("output/metrics.csv"),
        help="Output metrics CSV path",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    prices = load_prices(args.input)
    analysis, summary = calculate_returns(prices)
    save_outputs(analysis, summary, args.figure, args.metrics)

    print("Analysis summary:")
    for key, value in summary.items():
        if key == "observations":
            print(f"- {key}: {int(value):,}")
        else:
            print(f"- {key}: {value:.4%}" if "nav" not in key else f"- {key}: {value:.4f}")
    print(f"Saved figure to {args.figure}")
    print(f"Saved metrics to {args.metrics}")

