SEVERITY_SCORE = {
    "low": 1,
    "medium": 3,
    "high": 5
}

def soc_agent(alerts):
    recommendations = []

    for alert in alerts:
        event = alert["event"]
        severity = event.get("severity", "low")

        # Score de base
        risk_score = SEVERITY_SCORE.get(severity, 1)

        # Bonus scénario progressif
        if "Progressive" in alert["type"]:
            risk_score += 2

        # Bonus multi-événements
        related = alert.get("related_events", 1)
        if related > 1:
            risk_score += 1

        recommendations.append({
            "summary": alert["type"],
            "recommendation": generate_recommendation(alert),
            "confidence": "medium",
            "risk_score": risk_score,
            "event": event
        })

    return recommendations


def generate_recommendation(alert):
    if "IAM" in alert["type"]:
        return "Investigate privileged account activity"
    if "API" in alert["type"]:
        return "Analyze API access patterns and client identity"
    if "Network" in alert["type"]:
        return "Inspect network traffic and isolate suspicious host"
    return "Perform detailed SOC investigation"


