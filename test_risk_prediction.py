
def predict_risk(hours_taken, sla_hours):
    percentage = (hours_taken / sla_hours) * 100

    if percentage >= 100:
        return "Breached"
    elif percentage >= 75:
        return "At Risk"
    return "Safe"


assert predict_risk(4, 8) == "Safe"
assert predict_risk(6, 8) == "At Risk"
assert predict_risk(7.5, 8) == "At Risk"
assert predict_risk(8, 8) == "Breached"
assert predict_risk(9, 8) == "Breached"

print("All risk prediction tests passed!")
