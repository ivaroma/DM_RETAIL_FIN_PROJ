import pandas as pd
import json
import random
import csv
from datetime import datetime, timedelta

# 1. Load your existing Customer IDs to use as Foreign Keys
with open("customers_v1.json", "r") as f:
    cust_v1 = json.load(f)
    cust_ids = [c["cust_id"] for c in cust_v1]

# 2. Generate accounts.csv (Dimension)
# Dirty: Mixed date formats and some NULL account types
account_types = ["Savings", "Current", "Investment", None]
date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"]
accounts = []
account_ids = [f"ACC_{1000 + i}" for i in range(len(cust_ids))]

for i in range(len(cust_ids)):
    fmt = random.choice(date_formats)
    open_date = (
        datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1000))
    ).strftime(fmt)
    accounts.append(
        {
            "account_id": account_ids[i],
            "cust_id": cust_ids[i],
            "account_type": random.choice(account_types),
            "balance": round(random.uniform(100.0, 50000.0), 2),
            "open_date": open_date,
        }
    )
pd.DataFrame(accounts).to_csv("accounts.csv", index=False)

# 3. Generate branches.csv (Dimension)
branches = [
    {"branch_id": "BR_01", "name": "Main Downtown", "city": "New York"},
    {"branch_id": "BR_02", "name": "Westside Hub", "city": "Los Angeles"},
    {"branch_id": "BR_03", "name": "Silicon Valley", "city": "Palo Alto"},
]
pd.DataFrame(branches).to_csv("branches.csv", index=False)


# 4. Generate transactions_batch_1.csv (Fact - Initial)
def gen_tx(num, start_id):
    tx_data = []
    for i in range(num):
        # Dirty: Occasionally use a non-existent account_id
        src = random.choice(account_ids) if random.random() > 0.05 else "ACC_9999"
        tx_data.append(
            {
                "tx_id": f"TXN_{start_id + i}",
                "src_account": src,
                "dst_account": random.choice(account_ids),
                "amount": round(random.uniform(5.0, 2000.0), 2),
                "tx_type": random.choice(["Transfer", "Withdrawal", "Deposit"]),
                "timestamp": "2026-01-20T10:00:00Z",
            }
        )
    return tx_data


tx_batch_1 = gen_tx(500, 5000)
pd.DataFrame(tx_batch_1).to_csv("transactions_batch_1.csv", index=False)

# 5. Generate transactions_batch_2.csv (Fact - Incremental)
# Dirty: Includes 50 duplicates from batch 1
tx_batch_2 = tx_batch_1[:50] + gen_tx(300, 5500)
pd.DataFrame(tx_batch_2).to_csv("transactions_batch_2.csv", index=False)

# 6. Generate credit_scores.parquet
credit_data = pd.DataFrame(
    {
        "cust_id": cust_ids,
        "credit_score": [random.randint(300, 850) for _ in range(len(cust_ids))],
        "risk_level": random.choices(["Low", "Medium", "High"], k=len(cust_ids)),
    }
)
credit_data.to_parquet("credit_scores.parquet")

# 7. Generate exchange_rates.csv
rates = [
    {"currency": "EUR", "rate_to_usd": 1.09, "date": "2026-01-20"},
    {"currency": "GBP", "rate_to_usd": 1.27, "date": "2026-01-20"},
    {"currency": "UAH", "rate_to_usd": 0.026, "date": "2026-01-20"},
]
pd.DataFrame(rates).to_csv("exchange_rates.csv", index=False)

print(
    "Files generated: accounts.csv, branches.csv, transactions_batch_1.csv, transactions_batch_2.csv, credit_scores.parquet, exchange_rates.csv"
)
