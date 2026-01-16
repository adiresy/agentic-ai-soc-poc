def detect_anomalies(events):
    alerts = []
    for e in events:
        if e.get("action") == "login_failed":
            alerts.append({
                "type": "Suspicious authentication",
                "event": e
            })
    return alerts