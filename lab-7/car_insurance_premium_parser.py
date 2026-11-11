
from datetime import datetime


def normalize_registration(plate):
    """
    Removes spaces, dashes and dots from a registration number
    and converts it to uppercase.
    Returns an empty string for invalid input.
    """
    if not isinstance(plate, str):
        return ""

    plate = plate.strip().upper()

    for ch in [' ', '-', '.']:
        plate = plate.replace(ch, '')

    return plate


def total_claim_amount(text):
    """
    Adds valid whole-number claim amounts separated by semicolons.
    Invalid or empty entries are ignored.
    """
    if not isinstance(text, str):
        return 0

    total = 0

    for amount in text.split(';'):
        amount = amount.strip()

        if amount.isdigit():
            total += int(amount)

    return total


def driver_age(dob, current_year=2026):
    """
    Calculates age using a valid DD/MM/YYYY date.
    Returns None for invalid input or invalid dates.
    """
    if not isinstance(dob, str):
        return None

    try:
        birth_date = datetime.strptime(dob, "%d/%m/%Y")

        if birth_date.year > current_year:
            return None

        return current_year - birth_date.year

    except ValueError:
        return None


def main():
    print("==== Running normalize_registration ====")
    value = input("Enter a registration number (e.g. ka 01 ab 1234): ")
    print("Normalized registration:", normalize_registration(value))

    print("\n==== Running total_claim_amount ====")
    value = input("Enter past claim amounts separated by ; (e.g. 12000;4500;800): ")
    print("Total claimed:", total_claim_amount(value))

    print("\n==== Running driver_age ====")
    value = input("Enter the driver's date of birth as DD/MM/YYYY (e.g. 14/08/1999): ")
    age = driver_age(value)

    if age is None:
        print("Invalid date of birth")
    else:
        print("Driver age in 2026:", age)


if __name__ == "__main__":
    main()
