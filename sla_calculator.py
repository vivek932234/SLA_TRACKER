
from datetime import datetime, time, timedelta

SLA_LIMITS = {
    "P1": 4,
    "P2": 8,
    "P3": 24,
    "P4": 72,
}


def calculate_calendar_hours(start, end):
    """P1: Every hour counts, 24 hours a day."""
    return (end - start).total_seconds() / 3600


def calculate_working_hours(start, end, holidays=None):
    """P2-P4: Weekdays only, from 09:00 to 18:00."""
    holidays = set(holidays or [])
    total_seconds = 0

    current_date = start.date()
    last_date = end.date()

    while current_date <= last_date:
        if current_date.weekday() < 5 and current_date not in holidays:
            work_start = datetime.combine(
                current_date, time(9, 0)
            )
            work_end = datetime.combine(
                current_date, time(18, 0)
            )

            actual_start = max(start, work_start)
            actual_end = min(end, work_end)

            if actual_end > actual_start:
                total_seconds += (
                    actual_end - actual_start
                ).total_seconds()

        current_date += timedelta(days=1)

    return total_seconds / 3600


from datetime import datetime



def calculate_sla(ticket, holidays=None, now=None):
    priority = ticket["priority"]
    start = ticket["created_at"]
    end = ticket["resolved_at"]

    # Level 3 includes open complaints up to the current time.
    if end is None:
        end = now if now is not None else datetime.now()

    if priority == "P1":
        hours_taken = calculate_calendar_hours(start, end)
    else:
        hours_taken = calculate_working_hours(
            start, end, holidays
        )

    sla_hours = SLA_LIMITS[priority]
    usage_percent = (hours_taken / sla_hours) * 100

   
    if hours_taken > sla_hours:
        risk_status = "Breached"
    elif usage_percent >= 75:
        risk_status = "At Risk"
    else:
        risk_status = "Safe"

    return {
        "ticket_id": ticket["ticket_id"],
        "priority": priority,
        "hours_taken": round(hours_taken, 2),
        "sla_hours": sla_hours,
        "breached": "Yes" if hours_taken > sla_hours else "No",
        "usage_percent": round(usage_percent, 2),
        "risk_status": risk_status,
    }


