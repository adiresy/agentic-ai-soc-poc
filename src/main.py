from collector import collect_logs
from siem import index_events
from ueba import detect_anomalies
from agent import soc_agent
from interface import analyst_review

events = collect_logs()
indexed = index_events(events)
alerts = detect_anomalies(indexed)
recs = soc_agent(alerts)
analyst_review(recs)