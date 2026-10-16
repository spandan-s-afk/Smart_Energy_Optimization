import pandas as pd

DATA_PATH = "data/homec_processed.csv"

print("\n--- FINDING SUITABLE OPTIMIZATION DAY ---")

df = pd.read_csv(DATA_PATH)

df["time"] = pd.to_datetime(df["time"])

df["date"] = df["time"].dt.date

flexible_appliances = [
    "Car charger [kW]",
    "Water heater [kW]",
    "Laundry [kW]",
    "Pool Pump [kW]"
]

daily_activity = (
    df.groupby("date")[flexible_appliances]
    .sum()
)

daily_activity["total_flexible_activity"] = (
    daily_activity[flexible_appliances].sum(axis=1)
)

daily_activity = daily_activity.sort_values(
    "total_flexible_activity",
    ascending=False
)

print("\n--- TOP 10 DAYS WITH FLEXIBLE APPLIANCE ACTIVITY ---")

print(
    daily_activity.head(10).to_string()
)

best_day = daily_activity.index[0]

print("\n========================================")
print("SELECTED OPTIMIZATION DAY")
print("========================================")
print("Date:", best_day)
print(
    "Total flexible appliance activity:",
    round(
        daily_activity.loc[
            best_day,
            "total_flexible_activity"
        ],
        4
    )
)
print("========================================")

print("\n--- APPLIANCE ACTIVITY ON SELECTED DAY ---")

for appliance in flexible_appliances:

    value = daily_activity.loc[
        best_day,
        appliance
    ]

    print(
        f"{appliance}: {value:.4f}"
    )

print("\n--- DAY SELECTION COMPLETED ---")