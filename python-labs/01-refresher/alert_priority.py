severity = input("Severity: ").strip().upper()
affected_count = int(input("Affected Equipment Count: "))
equipment_online = input("Equipment Online: ").strip().lower()
is_online = equipment_online == "yes"

if severity == "HIGH" or not is_online:
    decision = "ESCALATE IMMEDIATELY"
elif severity == "MEDIUM" and affected_count >= 2:
    decision = "INVESTIGATE PROMPTLY"
else:
    decision = "MONITOR"

print()
print(f"Decision: {decision}")