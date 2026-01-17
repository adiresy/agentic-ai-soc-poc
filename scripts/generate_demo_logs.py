import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# -----------------------------------------
# Configuration
# -----------------------------------------
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

NUM_EVENTS = 120  # Génère plus de 100 logs

START_TIME = datetime.utcnow() - timedelta(hours=6)

USERS = ["admin01", "admin02", "user01", "user02", "cloud-admin"]
ASSETS = ["IAM", "Network", "Cloud", "API"]
SEVERITIES = ["low", "medium", "high"]

ACTIONS = {
    "IAM": ["login_failed", "login_success", "password_change"],
    "Network": ["blocked_connection", "allowed_connection", "port_scan_detected"],
    "Cloud": ["policy_change", "instance_start", "instance_stop"],
    "API": ["rate_limit_exceeded", "unauthorized_access", "normal_call"]
}

SOURCE_FILES = {
    "IAM": "auth_logs.json",
    "Network": "network_logs.json",
    "Cloud": "cloud_logs.json",
    "API": "api_logs.json"
}

# -----------------------------------------
# Génération des événements
# -----------------------------------------
events_by_file = {v: [] for v in SOURCE_FILES.values()}

for i in range(NUM_EVENTS):
    asset = random.choice(ASSETS)
    action = random.choice(ACTIONS[asset])
    severity = random.choice(SEVERITIES)

    event = {
        "timestamp": (START_TIME + timedelta(minutes=i*3)).isoformat() + "Z",
        "asset": asset,
        "action": action,
        "severity": severity
    }

    if asset == "IAM":
        event["user"] = random.choice(USERS)
        event["source_ip"] = f"10.0.0.{random.randint(1, 50)}"

    elif asset == "Network":
        event["device"] = "firewall01"
        event["source_ip"] = f"203.0.113.{random.randint(1, 200)}"
        event["destination_port"] = random.choice([22, 80, 443, 3389])

    elif asset == "Cloud":
        event["user"] = random.choice(USERS)
        event["service"] = "AWS-IAM"

    elif asset == "API":
        event["api_name"] = "CitizenRegistryAPI"
        event["client_id"] = f"client-{random.randint(1,20)}"

    file_name = SOURCE_FILES[asset]
    events_by_file[file_name].append(event)

# -----------------------------------------
# Écriture des fichiers JSON
# -----------------------------------------
for file_name, events in events_by_file.items():
    with open(OUTPUT_DIR / file_name, "w") as f:
        for event in events:
            json.dump(event, f)
            f.write("\n")

print("✅ Demo logs generated successfully:")
for file_name, events in events_by_file.items():
    print(f" - {file_name}: {len(events)} events")

