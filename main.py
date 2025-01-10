import json
import sys 
from calculateur_taux_imposition_qc.calculateur import get_taxes_rates

if __name__ == "__main__":
    try:
        if len(sys.argv) != 3 or sys.argv[1] == "--help":
            print("Usage: python main.py <salaire_annuel> [annee]")
            sys.exit(1)

        result = get_taxes_rates(float(sys.argv[1]), int(sys.argv[2]))

        print(json.dumps(result, indent=4, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
