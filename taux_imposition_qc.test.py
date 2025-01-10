import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
import json
from main import load_tax_brackets, calculate_taxes, calculate_marginal_rate, main

class TestTauxImposition(unittest.TestCase):

    def setUp(self):
        self.federal_brackets = [
            (0, 50000, 0.15),
            (50000, 100000, 0.20),
            (100000, float("inf"), 0.25),
        ]

        self.provincial_brackets = [
            (0, 40000, 0.10),
            (40000, 80000, 0.15),
            (80000, float("inf"), 0.20),
        ]

    def test_load_tax_brackets(self):
        mock_csv_content = (
            "annee,type,tranche_min,tranche_max,taux\n"
            "2024,federal,0,50000,0.15\n"
            "2024,federal,50000,100000,0.20\n"
            "2024,federal,100000,inf,0.25\n"
            "2024,provincial,0,40000,0.10\n"
            "2024,provincial,40000,80000,0.15\n"
            "2024,provincial,80000,inf,0.20\n"
            "2025,provincial,0,inf,0.01\n"
        )

        with patch("builtins.open", mock_open(read_data=mock_csv_content)):
            federal_brackets = load_tax_brackets("mock.csv", 2024, "federal")
            provincial_brackets = load_tax_brackets("mock.csv", 2024, "provincial")

        self.assertEqual(federal_brackets, self.federal_brackets)
        self.assertEqual(provincial_brackets, self.provincial_brackets)

    def test_calculate_taxes(self):
        income = 75000

        federal_tax = calculate_taxes(income, self.federal_brackets)
        provincial_tax = calculate_taxes(income, self.provincial_brackets)

        self.assertAlmostEqual(federal_tax, 12500)  # 50,000 * 0.15 + 25,000 * 0.20
        self.assertAlmostEqual(provincial_tax, 9250)  # 40,000 * 0.10 + 35,000 * 0.15

    def test_calculate_marginal_rate(self):
        income = 75000

        federal_marginal_rate = calculate_marginal_rate(income, self.federal_brackets)
        provincial_marginal_rate = calculate_marginal_rate(income, self.provincial_brackets)

        self.assertEqual(federal_marginal_rate, 0.20)
        self.assertEqual(provincial_marginal_rate, 0.15)

    @patch("builtins.print")
    def test_main_output(self, mock_print):
        test_args = ["main.py", "75000", "2024"]
        mock_csv_content = (
            "annee,type,tranche_min,tranche_max,taux\n"
            "2024,federal,0,50000,0.15\n"
            "2024,federal,50000,100000,0.20\n"
            "2024,federal,100000,inf,0.25\n"
            "2024,provincial,0,40000,0.10\n"
            "2024,provincial,40000,80000,0.15\n"
            "2024,provincial,80000,inf,0.20\n"
        )

        with patch("sys.argv", test_args), patch("builtins.open", mock_open(read_data=mock_csv_content)):
            with patch("main.datetime") as mock_datetime:
                mock_datetime.now.return_value = datetime(2024, 1, 1)
                main()

        mock_print.assert_called_once()
        output = json.loads(mock_print.call_args[0][0])

        expected_output = {
            "taux_effectif_quebecois": 0.1233,  # 9250 / 75000
            "taux_effectif_canadien": 0.1667,  # 12500 / 75000
            "taux_effectif_total": 0.29,  # (9250 + 12500) / 75000
            "taux_marginal_quebecois": 0.15,
            "taux_marginal_canadien": 0.20,
            "taux_marginal_total": 0.35,
        }

        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()
