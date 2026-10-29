
from datetime import datetime

VALID_PRIORITIES = {"P1", "P2", "P3", "P4"}

DATE_FORMATS = [
    "%Y-%m-%d %H:%M",  # 2026-10-05 10:00
    "%d/%m/%Y %H:%M",  # 05/10/2026 10:00
    "%Y/%m/%d %H:%M",  # 2026/10/08 14:00
]


def parse_date(value):
    value = (value or "").strip()

    if not value:
        return None

    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            continue

    raise ValueError(f"Invalid date format: {value}")


def validate_ticket(ticket):
    errors = []

    ticket_id = (ticket.get("ticket_id") or "").strip()
    priority = (ticket.get("priority") or "").strip().upper()
    created_value = ticket.get("created_at")
    resolved_value = ticket.get("resolved_at")

    created_at = None
    resolved_at = None

    if not ticket_id:
        errors.append("Missing ticket_id")

    if priority not in VALID_PRIORITIES:
        errors.append("Invalid priority")

    try:
        created_at = parse_date(created_value)
        if created_at is None:
            errors.append("Missing created_at")
    except ValueError as error:
        errors.append(str(error))

    try:
        resolved_at = parse_date(resolved_value)
    except ValueError as error:
        errors.append(str(error))

    if (
        created_at is not None
        and resolved_at is not None
        and resolved_at < created_at
    ):
        errors.append("Resolved before created")

    return {
        "ticket_id": ticket_id,
        "priority": priority,
        "created_at": created_at,
        "resolved_at": resolved_at,
        "errors": errors,
        "valid": len(errors) == 0,
    }
