import math
import unittest
from experiment import evaluate, simulate, stride_metrics


class MeasurementTests(unittest.TestCase):
    def test_identity_has_zero_error(self):
        result = evaluate(noise=0)
        for metric in result["metrics"].values():
            self.assertAlmostEqual(metric["mae"], 0)

    def test_extrema_match_hand_calculation(self):
        self.assertEqual(stride_metrics([0, 3, -1, 2], 4),
                         [{"stride": 0, "min_diff": 1, "max_diff": 1}])

    def test_offset_invariance(self):
        signal, _ = simulate(noise=0)
        shifted = [v + 100 for v in signal]
        for a, b in zip(stride_metrics(signal, 60), stride_metrics(shifted, 60)):
            self.assertAlmostEqual(a["min_diff"], b["min_diff"])
            self.assertAlmostEqual(a["max_diff"], b["max_diff"])

    def test_missing_stride_is_excluded(self):
        self.assertEqual(stride_metrics([1, None, 2, 3], 4), [])

    def test_reproducible_seed(self):
        self.assertEqual(evaluate(), evaluate())

    def test_roll_changes_estimates(self):
        self.assertGreater(evaluate(noise=0, roll=10)["metrics"]["max_diff"]["mae"], 1)

    def test_invalid_nonfinite_inputs(self):
        for noise in (-1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                evaluate(noise=noise)

    def test_no_usable_data_has_no_numeric_claim(self):
        result = evaluate(dropout=0.99)
        self.assertEqual(result["status"], "insufficient_data")
        self.assertIsNone(result["metrics"]["min_diff"]["mae"])


if __name__ == "__main__":
    unittest.main()
