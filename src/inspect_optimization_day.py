import pandas as pd

DATA_PATH = "data/homec_processed.csv"

SELECTED_DATE = "2016-11-28"

APPLIANCES = [
    "Car charger [kW]",
    "Water heater [kW]",
    "Laundry [kW]",
    "Pool Pump [kW]"
]

print("\n--- INSPECTING OPTIMIZATION DAY ---")

df = pd.read_csv(DATA_PATH)

df["time"] = pd.to_datetime(df["time"])

df = df[
    df["time"].dt.date
    == pd.Timestamp(SELECTED_DATE).date()
].copy()


print("\nDate:", SELECTED_DATE)
print("Rows:", len(df))


for appliance in APPLIANCES:

    print("\n========================================")
    print(appliance)
    print("========================================")

    series = df[appliance]

    print("Minimum :", round(series.min(), 6), "kW")
    print("Maximum :", round(series.max(), 6), "kW")
    print("Mean    :", round(series.mean(), 6), "kW")
    print("Median  :", round(series.median(), 6), "kW")

    print(
        "25th percentile :",
        round(series.quantile(0.25), 6),
        "kW"
    )

    print(
        "75th percentile :",
        round(series.quantile(0.75), 6),
        "kW"
    )

    print(
        "90th percentile :",
        round(series.quantile(0.90), 6),
        "kW"
    )

    print("\nFirst 20 values:")

    print(
        series.head(20).to_string(index=False)
    )


print("\n--- INSPECTION COMPLETED ---")