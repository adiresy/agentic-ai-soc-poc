import json
import glob

def collect_logs():
    events = []

    for file in glob.glob("data/*.json"):
        with open(file, "r") as f:
            for line in f:
                try:
                    event = json.loads(line)
                    event["source_file"] = file
                    events.append(event)
                except json.JSONDecodeError:
                    pass

    return events
