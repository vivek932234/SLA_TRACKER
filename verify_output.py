
import csv
import os

for filename in ["sla_results.csv", "invalid_tickets.csv"]:
    print(f"\nChecking {filename}...")

    if not os.path.exists(filename):
        print("ERROR: File not found")
        continue

    with open(filename, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    print("Rows:", len(rows))
    print("Columns:", reader.fieldnames)

    if filename == "sla_results.csv":
        for row in rows[:5]:
            print(row)
    else:
        for row in rows[:5]:
            print(row)
