import fastavro
import json
import random
from datetime import datetime

# 1. Load Customer IDs to keep data consistent
with open("customers_v1.json", "r") as f:
    customers = json.load(f)
    cust_ids = [c["cust_id"] for c in customers]

# 2. Define Schema V1
schema_v1 = {
    "doc": "Initial banking audit logs",
    "name": "Audit",
    "namespace": "banking",
    "type": "record",
    "fields": [
        {"name": "event_id", "type": "string"},
        {"name": "user_id", "type": "string"},  # mapping to cust_id
        {"name": "action", "type": "string"},  # LOGIN, LOGOUT, TRANSFER
        {"name": "ip_address", "type": "string"},
        {"name": "device_info", "type": "string"},
    ],
}

# 3. Define Schema V2 (Evolved)
# We added 'app_version' with a default value to ensure backward compatibility
schema_v2 = {
    "doc": "Evolved banking audit logs",
    "name": "Audit",
    "namespace": "banking",
    "type": "record",
    "fields": [
        {"name": "event_id", "type": "string"},
        {"name": "user_id", "type": "string"},
        {"name": "action", "type": "string"},
        {"name": "ip_address", "type": "string"},
        {"name": "device_info", "type": "string"},
        {
            "name": "app_version",
            "type": ["null", "string"],
            "default": None,
        },  # New Field
        {"name": "is_flagged", "type": "boolean", "default": False},  # New Field
    ],
}


def generate_logs(count, schema, version_tag):
    records = []
    actions = ["LOGIN", "LOGOUT", "TRANSFER"]
    devices = ["iOS", "Android", "Web-Chrome", "Web-Firefox"]

    for i in range(count):
        rec = {
            "event_id": f"EVT-{version_tag}-{1000 + i}",
            "user_id": random.choice(cust_ids),
            "action": random.choice(actions),
            "ip_address": f"192.168.1.{random.randint(1, 254)}",
            "device_info": random.choice(devices),
        }
        # Add fields if using schema v2
        if "app_version" in [f["name"] for f in schema["fields"]]:
            rec["app_version"] = f"v{random.choice(['2.1', '2.2', '3.0'])}"
            rec["is_flagged"] = random.random() < 0.05  # 5% chance of flagged event

        records.append(rec)
    return records


# Generate and Save V1
logs_v1 = generate_logs(200, schema_v1, "V1")
with open("audit_logs_v1.avro", "wb") as out:
    fastavro.writer(out, schema_v1, logs_v1)

# Generate and Save V2
logs_v2 = generate_logs(200, schema_v2, "V2")
with open("audit_logs_v2.avro", "wb") as out:
    fastavro.writer(out, schema_v2, logs_v2)

print("Generated: audit_logs_v1.avro (200 rows) and audit_logs_v2.avro (200 rows)")
