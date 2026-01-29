import json
import random
from datetime import datetime, timedelta


def generate_customer_name(i):
    names = [
        "John Doe",
        "jane smith",
        "ALICE WONDERLAND",
        "Bob Structure",
        "charlie brown",
        "DAVID MILLER",
    ]
    name = random.choice(names)
    # Randomly mess with casing
    if i % 5 == 0:
        return name.upper()
    if i % 3 == 0:
        return name.lower()
    return name


def generate_dirty_email(name, i):
    email = f"{name.replace(' ', '.').lower()}@example.com"
    if i % 10 == 0:
        return " " + email + "  "  # Extra spaces
    if i % 15 == 0:
        return ""  # Empty string instead of NULL
    return email


# Generate V1 - 500 Records
customers_v1 = []
for i in range(100, 600):
    cust_id = f"cust_{i}"
    name = generate_customer_name(i)
    customers_v1.append(
        {
            "cust_id": cust_id,
            "full_name": name,
            "email": generate_dirty_email(name, i),
            "address": f"{random.randint(1, 999)} Main St, City_{random.randint(1, 50)}",
            "phone": f"555-{random.randint(1000, 9999)}",
            "updated_at": "2026-01-01T08:00:00Z",
        }
    )

# Add explicit duplicates for DE practice
customers_v1.append(customers_v1[0].copy())

# Generate V2 - 150 Records (Updates + New)
customers_v2 = []
# 100 Updates (SCD Type 2 triggers)
for i in range(100, 200):
    cust = customers_v1[i - 100].copy()
    cust["address"] = f"{random.randint(1, 999)} New Avenue, NewCity_99"
    cust["updated_at"] = "2026-01-15T10:00:00Z"
    customers_v2.append(cust)

# 50 New Customers
for i in range(600, 650):
    name = generate_customer_name(i)
    customers_v2.append(
        {
            "cust_id": f"cust_{i}",
            "full_name": name,
            "email": generate_dirty_email(name, i),
            "address": f"{random.randint(1, 999)} Growth St, StartupCity",
            "phone": f"555-{random.randint(1000, 9999)}",
            "updated_at": "2026-01-16T09:00:00Z",
        }
    )

with open("customers_v1.json", "w") as f:
    json.dump(customers_v1, f, indent=2)
with open("customers_v2.json", "w") as f:
    json.dump(customers_v2, f, indent=2)

print("Files generated: customers_v1.json (501 rows), customers_v2.json (150 rows)")
