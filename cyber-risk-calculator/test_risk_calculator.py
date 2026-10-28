import os
import tempfile
import unittest

import risk_calculator as rc


class TestCalculations(unittest.TestCase):
    def test_sle(self):
        self.assertEqual(rc.calculate_sle(500000, 40), 200000)

    def test_ale(self):
        self.assertEqual(rc.calculate_ale(200000, 0.5), 100000)

    def test_levels(self):
        self.assertEqual(rc.risk_level(100000), "HIGH")
        self.assertEqual(rc.risk_level(20000), "MEDIUM")
        self.assertEqual(rc.risk_level(19999), "LOW")

    def test_build_risk(self):
        r = rc.build_risk("Ransomware", 500000, 40, 0.5)
        self.assertEqual(r["ale"], 100000)
        self.assertEqual(r["level"], "HIGH")


class TestValidation(unittest.TestCase):
    def test_empty_name(self):
        with self.assertRaises(ValueError):
            rc.build_risk("  ", 100, 10, 1)

    def test_bad_exposure(self):
        with self.assertRaises(ValueError):
            rc.build_risk("X", 100, 150, 1)

    def test_negative_values(self):
        with self.assertRaises(ValueError):
            rc.build_risk("X", -1, 10, 1)
        with self.assertRaises(ValueError):
            rc.build_risk("X", 1, 10, -1)

    def test_not_a_number(self):
        with self.assertRaises(ValueError):
            rc.build_risk("X", "abc", 10, 1)


class TestFiles(unittest.TestCase):
    def test_load_sample_and_rank(self):
        risks = rc.load_risks("sample_risks.csv")
        self.assertEqual(len(risks), 5)
        ranked = rc.rank_risks(risks)
        self.assertEqual(ranked[0]["name"], "Ransomware")
        self.assertGreater(rc.total_loss(risks), 0)

    def test_save_report(self):
        risks = rc.load_risks("sample_risks.csv")
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "out.csv")
            rc.save_report(risks, path)
            with open(path, encoding="utf-8") as f:
                self.assertEqual(len(f.readlines()), 6)  # header + 5 rows


if __name__ == "__main__":
    unittest.main()
