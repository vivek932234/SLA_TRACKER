
import csv
from datetime import datetime

from validator import validate_ticket
from sla_calculator import calculate_sla
from holidays import KARNATAKA_HOLIDAYS_2026

LEVEL = 3
now = datetime.now()

valid_tickets = []
invalid_tickets = []
results = []

with open("tickets.csv", "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.reader(file)

    headers = next(reader, None)

    if not headers:
        raise ValueError("tickets.csv is empty")

    headers = [header.strip().lower() for header in headers]

    expected_headers = {
        "ticket_id", "priority", "created_at", "resolved_at"
    }

    if not expected_headers.issubset(set(headers)):
        raise ValueError(f"Unexpected CSV columns: {headers}")

    for row in reader:
        if len(row) != len(headers):
            invalid_tickets.append({
                "ticket_id": "",
                "reason": f"Incorrect number of columns: {len(row)}",
            })
            continue

        record = dict(zip(headers, row))
        ticket = validate_ticket(record)

        if not ticket["valid"]:
            invalid_tickets.append({
                "ticket_id": ticket["ticket_id"],
                "reason": "; ".join(ticket["errors"]),
            })
            continue

        valid_tickets.append(ticket)

        if LEVEL == 1:
            if ticket["priority"] != "P1":
                continue
            if ticket["resolved_at"] is None:
                continue

        elif LEVEL == 2 and ticket["resolved_at"] is None:
            continue

        result = calculate_sla(
            ticket,
            holidays=KARNATAKA_HOLIDAYS_2026 if LEVEL == 3 else None,
            now=now,
        )
        results.append(result)
columns = [
    "ticket_id",
    "priority",
    "hours_taken",
    "sla_hours",
    "breached",
    "usage_percent",
    "risk_status",
]
with open("sla_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(results)

with open("invalid_tickets.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file, fieldnames=["ticket_id", "reason"]
    )
    writer.writeheader()
    writer.writerows(invalid_tickets)

print(f"SLA TRACKER - LEVEL {LEVEL}")
print("Reference time:", now.strftime("%Y-%m-%d %H:%M:%S"))

for result in results:
    print(result)

print("\nINVALID TICKETS")
for ticket in invalid_tickets:
    print(ticket)

print("\nFiles created: sla_results.csv, invalid_tickets.csv")
