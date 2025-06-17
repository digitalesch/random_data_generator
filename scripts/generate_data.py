import csv
import uuid
from faker import Faker
import random
from datetime import datetime, timedelta
import os

DESTINATION = "data/inputs/"

fake = Faker()

def random_date_within_year():
    end = datetime.now()
    start = end - timedelta(days=365)
    return start + timedelta(days=random.randint(0, 365))

def random_interest_rate():
    return round(random.uniform(0.0200, 0.3000), 4)  # 2% to 30%

def random_payment_schedule():
    return random.choice(["DAILY", "WEEKLY", "MONTHLY"])

def random_payment_method():
    return random.choice(["ACH", "CARD", "CHECK", "WIRE"])

# Constants
num_applications = 10000
loan_purposes = [
    "Business expansion", "Equipment purchase", "Inventory restock",
    "Marketing campaign", "Software upgrade", "Short-term operations",
    "Renovation project", "New product launch", "Working capital",
    "Vehicle purchase", "Payroll financing", "Emergency funding"
]
application_statuses = ["PENDING", "APPROVED", "REJECTED"]
us_state_codes = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]
# Containers
applications = []
disbursements = []
payments = []
merchants = []

# Generate data
for _ in range(num_applications):
    app_id = uuid.uuid4().hex
    merchant_id = uuid.uuid4().hex
    app_date = random_date_within_year()
    processing_time = app_date + timedelta(hours=random.randint(0, 72))
    app_status = random.choice(application_statuses)

    merchants.append({
        "merchant_id": merchant_id,
        "business_name": fake.company()[:200],
        "industry_code": str(random.randint(1000, 9999)),
        "state_code": random.choice(us_state_codes),
        "annual_revenue": random.uniform(10000, 5000000),
        "employees_count": random.randint(1, 500),
        "risk_score": random.uniform(0.00, 1.00),
        "onboarding_date": app_date
    })


    applications.append({
        "application_id": app_id,
        "merchant_id": merchant_id,
        "application_date": app_date.strftime("%Y-%m-%d"),
        "requested_amount": round(random.uniform(1000, 50000), 2),
        "loan_purpose": random.choice(loan_purposes),
        "application_status": app_status,
        "credit_score": random.randint(300, 850),
        "processing_time": processing_time.isoformat()
    })

    # Generate disbursement only for approved applications
    if app_status == "APPROVED":
        disb_id = uuid.uuid4().hex
        disb_date = app_date + timedelta(days=random.randint(1, 7))
        disbursed_amount = round(random.uniform(500, 50000), 2)
        term_months = random.choice([3, 6, 9, 12, 18, 24])

        disbursements.append({
            "disbursement_id": disb_id,
            "application_id": app_id,
            "merchant_id": merchant_id,
            "disbursed_amount": disbursed_amount,
            "disbursement_date": disb_date.strftime("%Y-%m-%d"),
            "interest_rate": random_interest_rate(),
            "term_months": term_months,
            "repayment_schedule": random_payment_schedule()
        })

        # Generate payments
        num_payments = random.randint(1, 10)
        for i in range(num_payments):
            payment_date = disb_date + timedelta(days=i * 15)
            is_scheduled = random.choice([True, False])
            days_late = random.randint(-5, 10) if not is_scheduled else 0
            payments.append({
                "payment_id": uuid.uuid4().hex,
                "disbursement_id": disb_id,
                "merchant_id": merchant_id,
                "payment_date": (payment_date + timedelta(days=days_late)).strftime("%Y-%m-%d"),
                "payment_amount": round(disbursed_amount / num_payments, 2),
                "payment_method": random_payment_method(),
                "is_scheduled": is_scheduled,
                "days_from_due": days_late,
                "processing_timestamp": (payment_date + timedelta(days=days_late, hours=random.randint(0, 23))).isoformat()
            })

# Write CSVs
def write_csv(file_path, file_name, field_names, data):
    os.makedirs(file_path, exist_ok=True)
    destination_path = os.path.join(file_path,file_name)
    with open(destination_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)
        print(f"✅ Generated: {destination_path}")

write_csv(f"{DESTINATION}","merchants.csv", merchants[0].keys(), merchants)
write_csv(f"{DESTINATION}","applications.csv", applications[0].keys(), applications)
write_csv(f"{DESTINATION}","disbursements.csv", disbursements[0].keys(), disbursements)
write_csv(f"{DESTINATION}","payments.csv", payments[0].keys(), payments)

