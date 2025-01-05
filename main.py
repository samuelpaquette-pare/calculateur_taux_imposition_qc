""" Ce script permet de calculer les impôts fédéraux et provinciaux pour un salaire annuel donné. """

import csv
import json
import sys
from datetime import datetime


def load_tax_brackets(filename: str, year: int, tax_type: str) -> list:
    """Loads the tax brackets for a given year and tax type from a CSV file.

    Args:
        filename (str): Path to the CSV file containing the tax brackets.
        year (int): Year to load the tax brackets for.
        tax_type (str): federal or provincial tax brackets to load.

    Returns:
        list: List of tax brackets for the given year and tax type.
    """
    brackets = []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["annee"]) == year and row["type"] == tax_type:
                brackets.append(
                    (
                        float(row["tranche_min"]),
                        (
                            float("inf")
                            if row["tranche_max"] == "inf"
                            else float(row["tranche_max"])
                        ),
                        float(row["taux"]),
                    )
                )
    return brackets


def calculate_taxes(income: int, brackets: list) -> float:
    """Calculates the total taxes for a given income and tax brackets.

    Args:
        income (int): The yearly income to calculate the taxes for.
        brackets (list): The tax brackets to use for the calculation.

    Returns:
        float: The total taxes for the given income.
    """
    return sum(
        (min(income, upper) - lower) * rate
        for lower, upper, rate in brackets
        if income > lower
    )


def calculate_marginal_rate(income: int, brackets: list) -> float:
    """Calculates the marginal tax rate for a given income and tax brackets.

    Args:
        income (int): The income to calculate the marginal tax rate for.
        brackets (list): The tax brackets to use for the calculation.

    Returns:
        float: The marginal tax rate for the given income.
    """
    return next((rate for lower, upper, rate in brackets if income > lower and income <= upper), 0)

def main():
    try:
        if len(sys.argv) != 3 or sys.argv[1] == "--help":
            print("Usage: python main.py <salaire_annuel> [annee]")
            sys.exit(1)

        salaire_annuel = float(sys.argv[1])
        annee = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year

        if salaire_annuel <= 0:
            raise ValueError("Le salaire doit être un nombre positif.")

        if annee < 2023 or annee > datetime.now().year:
            raise ValueError("L'année doit être comprise entre 2023 et 2025.")

        federal_brackets = load_tax_brackets("tax_brackets.csv", annee, "federal")
        federal_tax = calculate_taxes(salaire_annuel, federal_brackets)
        federal_marginal_rate = calculate_marginal_rate(salaire_annuel, federal_brackets)

        provincial_brackets = load_tax_brackets("tax_brackets.csv", annee, "provincial")
        provincial_tax = calculate_taxes(salaire_annuel, provincial_brackets)
        provincial_marginal_rate = calculate_marginal_rate(
            salaire_annuel, provincial_brackets
        )

        total_tax = federal_tax + provincial_tax
        total_effective_rate = total_tax / salaire_annuel
        total_marginal_rate = federal_marginal_rate + provincial_marginal_rate

        result = {
            "taux_effectif_quebecois": f"{provincial_tax / salaire_annuel:.4f}",
            "taux_effectif_canadien": f"{federal_tax / salaire_annuel:.4f}",
            "taux_effectif_total": f"{total_effective_rate:.4f}",
            "taux_marginal_quebecois": provincial_marginal_rate,
            "taux_marginal_canadien": federal_marginal_rate,
            "taux_marginal_total": total_marginal_rate,
        }
        print(json.dumps(result, indent=4, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
