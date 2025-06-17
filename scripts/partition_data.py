import os
import pandas as pd
import random

SOURCE = "data/inputs/"
DESTINATION = "data/partitions"

def partition_csv_by_year_month(
    input_file: str,
    date_column: str,
    output_dir: str,
    base_filename: str
):
    # Load the CSV
    df = pd.read_csv(input_file, parse_dates=[date_column])

    # Create year/month columns
    df['year'] = df[date_column].dt.year
    df['month'] = df[date_column].dt.month
    df['day'] = df[date_column].dt.day

    # Partition and write files
    for (year, month, day), group in df.groupby(['year', 'month', 'day']):
        path = os.path.join(output_dir, f"{year}",f"{month:02d}",f"{day:02d}")
        os.makedirs(path, exist_ok=True)
        output_path = os.path.join(path, f"{base_filename}_{year}{month:02d}{day:02d}.csv")
        group.drop(columns=['year', 'month','day'], inplace=True)
        # randomizes header output in csv file
        include_header = random.choice([True, False])
        group.to_csv(output_path, index=False,header=include_header)

    print(f"✅ Partitioned files written to: {output_dir}/{year}/{month:02d}/{day:02d}/{base_filename}_YYYYMMDD.csv")


files_to_process = [
    {
        "input_file":       f"{SOURCE}merchants.csv",
        "date_column":      "onboarding_date",
        "output_dir":       f"{DESTINATION}",
        "base_filename":    "merchants"
    },
    {
        "input_file":       f"{SOURCE}applications.csv",
        "date_column":      "application_date",
        "output_dir":       f"{DESTINATION}",
        "base_filename":    "applications"
    },
    {
        "input_file":       f"{SOURCE}disbursements.csv",
        "date_column":      "disbursement_date",
        "output_dir":       f"{DESTINATION}",
        "base_filename":    "disbursements"
    },
    {
        "input_file":       f"{SOURCE}payments.csv",
        "date_column":      "payment_date",
        "output_dir":       f"{DESTINATION}",
        "base_filename":    "payments"
    },
]

for file_spec in files_to_process:
    partition_csv_by_year_month(
        **file_spec
    )