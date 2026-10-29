
from datetime import datetime, date

from sla_calculator import (
    calculate_calendar_hours,
    calculate_working_hours,
    SLA_LIMITS,
)

# Test 1: P1 counts every hour.
start = datetime(2026, 10, 5, 10, 0)
end = datetime(2026, 10, 5, 14, 0)

assert calculate_calendar_hours(start, end) == 4.0
assert not (4.0 > SLA_LIMITS["P1"])

# Test 2: P2-P4 count working hours only.
start = datetime(2026, 10, 5, 10, 0)
end = datetime(2026, 10, 5, 19, 30)

hours = calculate_working_hours(start, end)
assert hours == 8.0

# Test 3: Weekends do not count.
start = datetime(2026, 10, 10, 10, 0)  # Saturday
end = datetime(2026, 10, 12, 10, 30)   # Monday

hours = calculate_working_hours(start, end)
assert hours == 1.5

# Test 4: A specified holiday does not count.
holiday = date(2026, 10, 20)
start = datetime(2026, 10, 20, 9, 0)
end = datetime(2026, 10, 20, 18, 0)

hours = calculate_working_hours(start, end, {holiday})
assert hours == 0.0

print("All SLA calculation tests passed!")
