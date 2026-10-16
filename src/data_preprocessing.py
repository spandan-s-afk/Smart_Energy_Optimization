import pandas as pd

DATA_PATH = "data/household_power_consumption.txt"

df = pd.read_csv(
    DATA_PATH,
    sep=";",
    na_values="?"
)

print("\n--- ORIGINAL DATASET ---")
print("Shape:", df.shape)

df["Datetime"] = pd.to_datetime(
    df["Date"] + " " + df["Time"],
    dayfirst=True
)

df = df.drop(["Date", "Time"], axis=1)

numeric_columns = [
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

print("\n--- MISSING VALUES BEFORE FILLING ---")
print(df.isnull().sum())

df[numeric_columns] = df[numeric_columns].ffill()

print("\n--- MISSING VALUES AFTER FILLING ---")
print(df.isnull().sum())

df["hour"] = df["Datetime"].dt.hour
df["day"] = df["Datetime"].dt.day
df["month"] = df["Datetime"].dt.month
df["day_of_week"] = df["Datetime"].dt.dayofweek

df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

print("\n--- PROCESSED DATA ---")
print(df.head())

print("\n--- FINAL COLUMNS ---")
print(df.columns.tolist())

print("\n--- FINAL SHAPE ---")
print(df.shape)

OUTPUT_PATH = "data/processed_energy_data.csv"

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n--- PROCESSED DATA SAVED ---")
print(OUTPUT_PATH)