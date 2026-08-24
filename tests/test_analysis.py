"""Regression tests for the core CSI 300 analysis workflow."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import numpy as np
import pandas as pd

from inspect_csi300 import inspect_prices
from src.day02_return_analysis import calculate_returns
from src.m02_extreme_days import analyze_extremes


def sample_prices() -> pd.DataFrame:
    """Return a small deterministic data set spanning the configured event window."""
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2024-09-23",
                    "2024-09-24",
                    "2024-09-25",
                    "2024-09-26",
                    "2024-09-27",
                    "2024-09-30",
                    "2024-10-08",
                    "2024-10-09",
                ]
            ),
            "open": [99, 101, 104, 106, 110, 116, 136, 127],
            "high": [101, 105, 107, 111, 116, 124, 137, 128],
            "low": [98, 100, 103, 105, 109, 115, 129, 120],
            "close": [100, 104, 106, 110, 115, 123, 130, 121],
        }
    )


class ReturnAnalysisTests(unittest.TestCase):
    def test_simple_and_log_nav_paths_match(self) -> None:
        analysis, metrics = calculate_returns(sample_prices())

        self.assertAlmostEqual(metrics["ending_nav"], 1.21)
        self.assertAlmostEqual(metrics["cumulative_return"], 0.21)
        np.testing.assert_allclose(analysis["nav"], analysis["nav_from_log"])

    def test_event_window_outputs_are_reproducible(self) -> None:
        prices = sample_prices()
        prices["simple_return"] = prices["close"].pct_change(fill_method=None)

        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            summary = analyze_extremes(prices, output_dir)

            self.assertEqual(summary["event_trading_days"], 6.0)
            self.assertAlmostEqual(summary["event_cumulative_return"], 0.30)
            self.assertAlmostEqual(
                summary["intraday_open_to_close_return"], 130 / 136 - 1
            )
            self.assertTrue((output_dir / "largest_gains.csv").is_file())
            self.assertTrue((output_dir / "largest_losses.csv").is_file())
            self.assertTrue((output_dir / "event_window_2024.csv").is_file())


class DataQualityTests(unittest.TestCase):
    def write_prices(self, directory: Path, frame: pd.DataFrame) -> Path:
        csv_path = directory / "prices.csv"
        frame.to_csv(csv_path, index=False, encoding="utf-8-sig")
        return csv_path

    def test_valid_prices_pass_quality_checks(self) -> None:
        with TemporaryDirectory() as temp_dir:
            csv_path = self.write_prices(Path(temp_dir), sample_prices())
            with redirect_stdout(StringIO()):
                result = inspect_prices(csv_path)

        self.assertEqual(len(result), 8)
        self.assertTrue(result["date"].is_monotonic_increasing)

    def test_duplicate_dates_fail_quality_checks(self) -> None:
        frame = sample_prices()
        frame.loc[1, "date"] = frame.loc[0, "date"]

        with TemporaryDirectory() as temp_dir:
            csv_path = self.write_prices(Path(temp_dir), frame)
            with redirect_stdout(StringIO()):
                with self.assertRaisesRegex(ValueError, "Data quality checks failed"):
                    inspect_prices(csv_path)


if __name__ == "__main__":
    unittest.main()

