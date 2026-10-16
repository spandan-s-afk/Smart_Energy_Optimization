import pandas as pd

DATA_PATH = "data/HomeC_augmented.csv"
OUTPUT_PATH = "data/homec_processed.csv"

print("\n--- LOADING HOMEC DATASET ---")

df = pd.read_csv(DATA_PATH)

print("Original shape:", df.shape)

# Remove unnecessary index column
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Convert time column
df["time"] = pd.to_datetime(df["time"])

# Sort chronologically
df = df.sort_values("time").reset_index(drop=True)

# Identify appliance columns
appliance_columns = [
    "Car charger [kW]",
    "Water heater [kW]",
    "Air conditioning [kW]",
    "Home Theater [kW]",
    "Outdoor lights [kW]",
    "microwave [kW]",
    "Laundry [kW]",
    "Pool Pump [kW]"
]

# Calculate total appliance consumption
df["total_appliance_power"] = df[appliance_columns].sum(axis=1)

# Calculate total energy demand
df["total_household_power"] = (
    df["total_appliance_power"]
)

# Time-based features
df["hour"] = df["time"].dt.hour
df["day"] = df["time"].dt.day
df["month"] = df["time"].dt.month
df["day_of_week"] = df["time"].dt.dayofweek
df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)

# Peak-hour indicator
df["is_peak_hour"] = df["hour"].isin(
    [18, 19, 20, 21, 22]
).astype(int)

# Check missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum().sum())

print("\n--- PROCESSED SHAPE ---")
print(df.shape)

print("\n--- APPLIANCE COLUMNS ---")
for column in appliance_columns:
    print(column)

print("\n--- FIRST 5 ROWS ---")
print(
    df[
        [
            "time",
            "total_appliance_power",
            "hour",
            "day_of_week",
            "is_weekend",
            "is_peak_hour"
        ]
    ].head()
)

# Save processed dataset
df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n--- PROCESSED DATA SAVED ---")
print(OUTPUT_PATH)