"""Calculate CSI 300 returns and cross-validated normalized net value."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = REPO_ROOT / "data" / "csi300_daily.csv"
DEFAULT_FIGURE_PATH = REPO_ROOT / "output" / "figures" / "csi300_nav_curve.png"


def prepare_price_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate, sort, and add a simple-return column to price data."""
    required = {"date", "close"}
    missing_columns = required.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"missing required columns: {sorted(missing_columns)}")
    if frame.empty:
        raise ValueError("price data is empty")

    prepared = frame.copy()
    prepared["date"] = pd.to_datetime(prepared["date"], errors="raise")
    if prepared["date"].isna().any():
        raise ValueError("date contains missing values")
    if prepared["date"].duplicated().any():
        raise ValueError("duplicate dates found")

    prepared["close"] = pd.to_numeric(prepared["close"], errors="raise")
    if prepared["close"].isna().any():
        raise ValueError("close contains missing values")
    if (prepared["close"] <= 0).any():
        raise ValueError("close must be strictly positive")

    prepared = prepared.sort_values("date").reset_index(drop=True)
    prepared["simple_return"] = prepared["close"].pct_change(fill_method=None)

    missing_positions = np.flatnonzero(prepared["simple_return"].isna().to_numpy())
    if not np.array_equal(missing_positions, np.array([0])):
        raise ValueError(
            "simple_return must be missing only in the first row; "
            f"found missing positions {missing_positions.tolist()}"
        )

    return prepared


def calculate_return_nav(frame: pd.DataFrame) -> pd.DataFrame:
    """Build NAV through simple and log returns and assert path agreement."""
    if "simple_return" not in frame.columns:
        raise ValueError("simple_return column is required; call prepare_price_data first")

    result = frame.copy()
    missing_positions = np.flatnonzero(result["simple_return"].isna().to_numpy())
    if not np.array_equal(missing_positions, np.array([0])):
        raise ValueError(
            "simple_return must be missing only in the first row before initialization"
        )

    result.loc[0, "simple_return"] = 0.0
    if (result["simple_return"] <= -1).any():
        raise ValueError("simple_return must be greater than -1 for log conversion")

    result["log_return"] = np.log1p(result["simple_return"])
    result["nav"] = (1.0 + result["simple_return"]).cumprod()
    result["nav_from_log"] = np.exp(result["log_return"].cumsum())

    if not np.allclose(
        result["nav"].to_numpy(),
        result["nav_from_log"].to_numpy(),
        rtol=1e-12,
        atol=1e-12,
    ):
        max_difference = float((result["nav"] - result["nav_from_log"]).abs().max())
        raise AssertionError(
            "simple-return and log-return NAV paths disagree; "
            f"maximum absolute difference={max_difference:.3e}"
        )

    return result


def save_nav_figure(frame: pd.DataFrame, output_path: Path = DEFAULT_FIGURE_PATH) -> Path:
    """Save a deterministic NAV figure and return its path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(frame["date"], frame["nav"], label="CSI 300 NAV", linewidth=1.6)
    ax.axhline(1.0, linestyle="--", linewidth=1.0, label="Initial NAV")
    ax.set_title("CSI 300 Normalized Net Value")
    ax.set_xlabel("Date")
    ax.set_ylabel("Net Value")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


def run_analysis(
    data_path: Path = DEFAULT_DATA_PATH,
    figure_path: Path = DEFAULT_FIGURE_PATH,
) -> pd.DataFrame:
    """Run the complete local analysis workflow."""
    prices = pd.read_csv(data_path, parse_dates=["date"])
    result = calculate_return_nav(prepare_price_data(prices))
    saved_figure = save_nav_figure(result, figure_path)

    print(f"Rows: {len(result)}")
    print(f"Date range: {result['date'].min().date()} to {result['date'].max().date()}")
    print(f"Final NAV: {result['nav'].iloc[-1]:.6f}")
    print("NAV cross-check: PASS")
    print(f"Figure: {saved_figure}")
    return result


if __name__ == "__main__":
    run_analysis()
