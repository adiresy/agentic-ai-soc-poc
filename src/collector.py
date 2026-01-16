import json, glob

def collect_logs():
    events = []
    for file in glob.glob("data/*.json"):
        with open(file) as f:
            events.append(json.load(f))
    return events