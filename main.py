"""
    This module calculates tax rates for Quebec, Canada.

    It provides functionality to calculate either the general tax rate or the capital gain tax rate based on the provided annual salary and year.

    Usage:
        python main.py [--capital] <salaire_annuel> [annee]

    Arguments:
        --help          Show usage information.
        --capital       Calculate the capital gain tax rate.
        <salaire_annuel> Annual salary for which the tax rate is to be calculated.
        [annee]         Optional year for which the tax rate is to be calculated.

    Functions:
        get_tax_rate(salaire_annuel: float, annee: int) -> dict
            Calculate the general tax rate for the given annual salary and year.
        get_capital_gain_tax_rate(salaire_annuel: float) -> dict
            Calculate the capital gain tax rate for the given annual salary.

    Exceptions:
        Any exceptions encountered during execution are caught and displayed as JSON error messages.
"""

import json
import sys
from calculateur_taux_imposition_qc import get_tax_rate, get_capital_gain_tax_rate

if __name__ == "__main__":
    try:
        if sys.argv[1] == "--help":
            print("Usage: python main.py [--capital] <salaire_annuel> [annee]")
            sys.exit(1)

        if sys.argv[1] == "--capital":
            result = get_capital_gain_tax_rate(float(sys.argv[2]))
        else:
            result = get_tax_rate(float(sys.argv[1]), int(sys.argv[2]))

        print(json.dumps(result, indent=4, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
