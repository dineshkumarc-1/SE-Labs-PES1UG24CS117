"""Pharmacy management system for medicine stock and billing."""
import json
import hashlib
import secrets
import ast
import os
import operator
from datetime import datetime, date

# Global pharmacy state
medicines = {}
DB_PASSWORD = os.environ.get("PHARMACY_DB_PASSWORD")


def add_medicine(name, qty=0, price=0.0, expiry="2099-12-31", audit=None):
    """Add medicine stock and record the stock update."""
    if audit is None:
        audit = []

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be a non-empty string.")

    if qty < 0:
        raise ValueError("Medicine quantity cannot be negative.")

    if price < 0:
        raise ValueError("Medicine price cannot be negative.")

    if name not in medicines:
        medicines[name] = {
            "qty": 0,
            "price": price,
            "expiry": expiry,
        }

    medicines[name]["qty"] += qty
    audit.append(
        f"{datetime.now()}: Stocked {qty} units of {name}"
    )
    return audit


def dispense_medicine(name, qty):
    """Dispense medicine and update its available stock."""
    if name not in medicines:
        return False

    if qty <= 0:
        return False

    if medicines[name]["qty"] < qty:
        return False

    medicines[name]["qty"] -= qty

    if medicines[name]["qty"] == 0:
        del medicines[name]

    return True


def get_quantity(name):
    """Return the available quantity of a medicine."""
    if name not in medicines:
        return 0

    return medicines[name]["qty"]


def is_expired(name):
    """Check whether a medicine has passed its expiry date."""
    if name not in medicines:
        return False

    expiry_date = datetime.strptime(
        medicines[name]["expiry"], "%Y-%m-%d"
    ).date()

    return expiry_date < date.today()


def bill_amount(prescription):
    """Calculate the total bill for a prescription."""
    total = 0.0

    for item in prescription:
        medicine_name, quantity = item

        if medicine_name not in medicines:
            raise ValueError(
                f"Medicine '{medicine_name}' is not available."
            )

        if quantity <= 0:
            raise ValueError("Prescription quantity must be positive.")

        total += medicines[medicine_name]["price"] * quantity

    return total


def calculate_dosage(formula):
    """Safely evaluate a basic arithmetic dosage formula."""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp):
            operation = allowed_operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported arithmetic operator.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if abs(left) > 1_000_000 or abs(right) > 1_000_000:
                raise ValueError("Formula values are too large.")

            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Division by zero is not allowed.")

            result = operation(left, right)

            if abs(result) > 1_000_000:
                raise ValueError("Formula result is too large.")

            return result

        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value

        raise ValueError("Invalid dosage formula.")

    try:
        tree = ast.parse(formula, mode="eval")
        return evaluate(tree)
    except (SyntaxError, TypeError, RecursionError) as exc:
        raise ValueError("Invalid dosage formula.") from exc


def patient_id(name, phone):
    """Generate a SHA-256 hash from the patient name and phone."""
    patient_data = (name + phone).encode("utf-8")
    return hashlib.sha256(patient_data).hexdigest()


def generate_rx_number():
    """Generate a random prescription reference number."""
    return "RX-" + str(secrets.randbelow(900000) + 100000)


def save_stock(file="pharmacy.json"):
    """Save medicine stock to a JSON file."""
    with open(file, "w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file, indent=4)


def load_stock(file="pharmacy.json"):
    """Load medicine stock from a JSON file."""
    global medicines

    with open(file, "r", encoding="utf-8") as stock_file:
        loaded_medicines = json.load(stock_file)

    if not isinstance(loaded_medicines, dict):
        raise ValueError("Invalid medicine stock data.")

    medicines = loaded_medicines


def print_label(name):
    """Print a medicine dispensing label."""
    print(f"Dispensing label: {name}")


def expiring_soon(days=30):
    """Return medicines expiring within the specified number of days."""
    result = []

    for medicine, details in medicines.items():
        expiry_date = datetime.strptime(
            details["expiry"], "%Y-%m-%d"
        ).date()

        days_until_expiry = (expiry_date - date.today()).days

        if 0 <= days_until_expiry < days:
            result.append(medicine)

    return result


def pharmacist_login(password):
    """Check the supplied password against the configured password."""
    if not DB_PASSWORD:
        return False

    return secrets.compare_digest(password, DB_PASSWORD)


def print_stock():
    """Print the current medicine stock report."""
    print("===== Pharmacy Stock Report =====")

    for medicine, details in medicines.items():
        print(
            medicine,
            "->",
            details["qty"],
            "units, Rs.",
            details["price"],
            "exp",
            details["expiry"],
        )


def main():
    """Run the pharmacy management demonstration."""
    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    add_medicine("Cetirizine 10mg", 10, 2.0, "2027-03-31")
    add_medicine("Vitamin C", 25, 3.0, "2027-12-31")
    dispense_medicine("Paracetamol 500mg", 30)
    dispense_medicine("Insulin", 2)
    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print("Bill:", bill_amount(
        [("Paracetamol 500mg", 10), ("Amoxicillin 250mg", 5)]))
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print("Login:", pharmacist_login("pharma@123"))
    print_label("Paracetamol 500mg")
    save_stock()
    load_stock()
    print_stock()


main()
