def soc_agent(alerts):
    recs = []
    for a in alerts:
        recs.append({
            "summary": a["type"],
            "recommendation": "Investigate the account activity",
            "confidence": "medium"
        })
    return recs