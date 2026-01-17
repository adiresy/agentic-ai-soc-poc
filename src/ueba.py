def detect_anomalies(events):
    alerts = []

    for e in events:
        if e.get("asset") == "IAM" and e.get("action") == "login_failed":
            alerts.append({
                "type": "Suspicious authentication",
                "event": e
            })

        if e.get("asset") == "Cloud" and e.get("severity") == "high":
            alerts.append({
                "type": "High-risk cloud activity",
                "event": e
            })

        if e.get("asset") == "API" and "rate_limit" in e.get("action", ""):
            alerts.append({
                "type": "Abnormal API behavior",
                "event": e
            })

    return alerts
