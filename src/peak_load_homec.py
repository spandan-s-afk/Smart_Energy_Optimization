import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. LOAD PROCESSED DATA
# ============================================================

DATA_PATH = "data/homec_processed.csv"

print("\n--- LOADING HOMEC PROCESSED DATA ---")

df = pd.read_csv(DATA_PATH)

df["time"] = pd.to_datetime(df["time"])

print("Dataset shape:", df.shape)


# ============================================================
# 2. CREATE HOURLY POWER PROFILE
# ============================================================

print("\n--- CALCULATING HOURLY POWER PROFILE ---")

df["hour"] = df["time"].dt.hour

hourly_power = (
    df.groupby("hour")["total_appliance_power"]
    .mean()
    .reset_index()
)

hourly_power.columns = ["hour", "average_power_kW"]


# ============================================================
# 3. FIND PEAK AND LOW DEMAND HOURS
# ============================================================

peak_row = hourly_power.loc[
    hourly_power["average_power_kW"].idxmax()
]

low_row = hourly_power.loc[
    hourly_power["average_power_kW"].idxmin()
]

peak_hour = int(peak_row["hour"])
peak_power = peak_row["average_power_kW"]

low_hour = int(low_row["hour"])
low_power = low_row["average_power_kW"]


# ============================================================
# 4. DISPLAY RESULTS
# ============================================================

print("\n========================================")
print("       PEAK LOAD ANALYSIS")
print("========================================")

print(
    f"Peak demand hour : {peak_hour:02d}:00"
)

print(
    f"Peak average power : {peak_power:.4f} kW"
)

print()

print(
    f"Lowest demand hour : {low_hour:02d}:00"
)

print(
    f"Lowest average power : {low_power:.4f} kW"
)

print("========================================")


# ============================================================
# 5. DISPLAY HOURLY VALUES
# ============================================================

print("\n--- HOURLY AVERAGE POWER ---")

for _, row in hourly_power.iterrows():

    print(
        f"{int(row['hour']):02d}:00  ->  "
        f"{row['average_power_kW']:.4f} kW"
    )


# ============================================================
# 6. SAVE HOURLY RESULTS
# ============================================================

OUTPUT_PATH = "results/hourly_power_profile.csv"

hourly_power.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nHourly results saved to:")
print(OUTPUT_PATH)


# ============================================================
# 7. CREATE GRAPH
# ============================================================

GRAPH_PATH = "graphs/hourly_peak_load_homec.png"

plt.figure(figsize=(12, 6))

plt.plot(
    hourly_power["hour"],
    hourly_power["average_power_kW"],
    marker="o"
)

plt.axvline(
    peak_hour,
    linestyle="--",
    label=f"Peak Hour: {peak_hour:02d}:00"
)

plt.xlabel("Hour of Day")

plt.ylabel("Average Appliance Power (kW)")

plt.title(
    "Hourly Average Monitored Appliance Power"
)

plt.xticks(range(24))

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    GRAPH_PATH,
    dpi=300
)

plt.close()

print("\nGraph saved to:")
print(GRAPH_PATH)

print("\n--- PEAK LOAD ANALYSIS COMPLETED ---")