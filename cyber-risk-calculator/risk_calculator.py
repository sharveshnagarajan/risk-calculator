"""Cyber Risk Calculator for Small Businesses (basic version).

Estimates the yearly money loss from cyber risks using two standard formulas:
    SLE (Single Loss Expectancy) = asset value x exposure %
    ALE (Annual Loss Expectancy) = SLE x incidents per year
"""

import csv

HIGH_LIMIT = 100000    # ALE at or above this is HIGH
MEDIUM_LIMIT = 20000   # ALE at or above this is MEDIUM
REPORT_FILE = "report.csv"
SAMPLE_FILE = "sample_risks.csv"
FIELDS = ["name", "asset_value", "exposure_percent", "frequency"]


def calculate_sle(asset_value, exposure_percent):
    """Loss from ONE incident."""
    return asset_value * exposure_percent / 100


def calculate_ale(sle, frequency):
    """Expected loss per YEAR."""
    return sle * frequency


def risk_level(ale):
    """Turn a yearly loss into LOW / MEDIUM / HIGH."""
    if ale >= HIGH_LIMIT:
        return "HIGH"
    if ale >= MEDIUM_LIMIT:
        return "MEDIUM"
    return "LOW"


def build_risk(name, asset_value, exposure_percent, frequency):
    """Validate the inputs and return a risk as a dictionary."""
    name = str(name).strip()
    if not name:
        raise ValueError("Risk name cannot be empty.")
    asset_value = float(asset_value)
    exposure_percent = float(exposure_percent)
    frequency = float(frequency)
    if asset_value < 0:
        raise ValueError("Asset value cannot be negative.")
    if not 0 <= exposure_percent <= 100:
        raise ValueError("Exposure must be between 0 and 100.")
    if frequency < 0:
        raise ValueError("Frequency cannot be negative.")
    sle = calculate_sle(asset_value, exposure_percent)
    ale = calculate_ale(sle, frequency)
    return {
        "name": name,
        "asset_value": asset_value,
        "exposure_percent": exposure_percent,
        "frequency": frequency,
        "sle": sle,
        "ale": ale,
        "level": risk_level(ale),
    }


def rank_risks(risks):
    """Biggest yearly loss first."""
    return sorted(risks, key=lambda r: r["ale"], reverse=True)


def total_loss(risks):
    return sum(r["ale"] for r in risks)


def save_report(risks, path=REPORT_FILE):
    """Write the ranked report to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Risk", "Asset Value", "Single Loss", "Per Year",
                         "Annual Loss", "Level"])
        for r in rank_risks(risks):
            writer.writerow([r["name"], r["asset_value"], r["sle"],
                             r["frequency"], r["ale"], r["level"]])


def load_risks(path=SAMPLE_FILE):
    """Read risks from a CSV file with the columns listed in FIELDS."""
    risks = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            risks.append(build_risk(row["name"], row["asset_value"],
                                    row["exposure_percent"], row["frequency"]))
    return risks


def print_report(risks):
    if not risks:
        print("\nNo risks yet. Add one or load the sample data first.")
        return
    print("\n=== RISK REPORT (highest loss first) ===")
    for r in rank_risks(risks):
        print(f"{r['name']:<24} Rs.{r['ale']:>12,.2f} per year   {r['level']}")
    print(f"\nTotal expected yearly loss: Rs.{total_loss(risks):,.2f}")


def ask_text(prompt):
    return input(prompt).strip()


def ask_number(prompt, minimum=None, maximum=None):
    """Keep asking until the person types a valid number in range."""
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Value must be at least {minimum}.")
        elif maximum is not None and value > maximum:
            print(f"Value must be at most {maximum}.")
        else:
            return value


def add_risk_interactively(risks):
    name = ask_text("Risk name (e.g. Ransomware): ")
    if not name:
        print("Name cannot be empty.")
        return
    asset = ask_number("Value of the asset at risk (Rs.): ", minimum=0)
    exposure = ask_number("% of asset lost in ONE incident (0-100): ", 0, 100)
    freq = ask_number("Incidents per year (0.5 = once in 2 years): ", minimum=0)
    risks.append(build_risk(name, asset, exposure, freq))
    print(f"Added '{name}'.")


def show_menu():
    print("\n=== Cyber Risk Calculator ===")
    print("1. Add a risk")
    print("2. Load sample data")
    print("3. View report")
    print("4. Save report to CSV")
    print("5. Clear all risks")
    print("0. Exit")


def main():
    risks = []
    while True:
        show_menu()
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            break
        if choice == "1":
            add_risk_interactively(risks)
        elif choice == "2":
            try:
                risks.extend(load_risks(SAMPLE_FILE))
                print(f"Loaded sample data. Total risks: {len(risks)}")
            except (OSError, ValueError, KeyError) as err:
                print(f"Could not load sample data: {err}")
        elif choice == "3":
            print_report(risks)
        elif choice == "4":
            if risks:
                save_report(risks)
                print(f"Saved to {REPORT_FILE}")
            else:
                print("Nothing to save yet.")
        elif choice == "5":
            risks.clear()
            print("All risks cleared.")
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please pick 0-5.")
    print("Goodbye!")


if __name__ == "__main__":
    main()
