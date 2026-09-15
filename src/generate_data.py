from pathlib import Path
import random
from datetime import datetime, timedelta

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)

first_names = [
    "Aarav", "Ananya", "Rahul", "Priya", "Arjun",
    "Sneha", "Vikram", "Kavya", "Rohan", "Meera"
]

last_names = [
    "Sharma", "Reddy", "Kumar", "Patel", "Singh",
    "Rao", "Das", "Verma", "Nair", "Gupta"
]

states = [
    "Andhra Pradesh",
    "Telangana",
    "Karnataka",
    "Tamil Nadu",
    "Maharashtra"
]

departments = [
    "Health",
    "Education",
    "Rural Development",
    "Social Welfare",
    "Transport"
]

records = []

start_date = datetime(2025, 1, 1)

for i in range(1, 1001):
    first = random.choice(first_names)
    last = random.choice(last_names)

    record = {
        "record_id": f"JS{i:05d}",
        "full_name": f"{first} {last}",
        "age": random.randint(18, 75),
        "state": random.choice(states),
        "department": random.choice(departments),
        "annual_income": round(random.uniform(80000, 1500000), 2),
        "service_requests": random.randint(0, 25),
        "registration_date": (
            start_date + timedelta(days=random.randint(0, 600))
        ).strftime("%Y-%m-%d"),
        "email": f"{first.lower()}.{last.lower()}{i}@example.org",
        "phone": f"9{random.randint(100000000, 999999999)}",
    }

    records.append(record)


df = pd.DataFrame(records)

# Introduce realistic data-quality issues.

# Missing values
df.loc[[17, 88, 231], "email"] = None
df.loc[[42, 199, 701], "annual_income"] = None
df.loc[[73, 455], "state"] = None

# Invalid ages
df.loc[101, "age"] = 8
df.loc[602, "age"] = 143

# Inconsistent category spelling
df.loc[120, "state"] = "Andhra pradesh"
df.loc[350, "state"] = "Telangana "
df.loc[480, "department"] = "health"

# Invalid email
df.loc[275, "email"] = "not-an-email"

# Invalid phone
df.loc[390, "phone"] = "12345"

# Date format inconsistency
df.loc[515, "registration_date"] = "15/07/2026"
df.loc[720, "registration_date"] = "2026/08/12"

# Duplicate records
df = pd.concat([df, df.iloc[[50, 150, 250]]], ignore_index=True)

output_file = RAW_DATA_DIR / "public_service_records.csv"
df.to_csv(output_file, index=False)

print(f"Generated {len(df)} records.")
print(f"Saved to: {output_file}")