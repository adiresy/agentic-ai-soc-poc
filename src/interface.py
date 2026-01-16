def analyst_review(recs):
    for r in recs:
        print("ALERT:", r["summary"])
        print("RECOMMENDATION:", r["recommendation"])
        input("Validate recommendation (Enter): ")