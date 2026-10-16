import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/processed_energy_data.csv"

df = pd.read_csv(DATA_PATH)

df["Datetime"] = pd.to_datetime(df["Datetime"])

# Calculate hourly average energy consumption
hourly_consumption = (
    df.groupby(df["Datetime"].dt.hour)["Global_active_power"]
    .mean()
)

print("\n--- AVERAGE ENERGY CONSUMPTION BY HOUR ---")

for hour, consumption in hourly_consumption.items():
    print(f"{hour:02d}:00 - {consumption:.3f} kW")

# Identify peak hour
peak_hour = hourly_consumption.idxmax()
peak_consumption = hourly_consumption.max()

# Identify lowest-demand hour
low_hour = hourly_consumption.idxmin()
low_consumption = hourly_consumption.min()

print("\n--- PEAK LOAD ---")
print(f"Peak hour: {peak_hour:02d}:00")
print(f"Average consumption: {peak_consumption:.3f} kW")

print("\n--- LOW DEMAND ---")
print(f"Low-demand hour: {low_hour:02d}:00")
print(f"Average consumption: {low_consumption:.3f} kW")

# Save hourly analysis
hourly_results = pd.DataFrame({
    "Hour": hourly_consumption.index,
    "Average_Consumption": hourly_consumption.values
})

hourly_results.to_csv(
    "results/hourly_consumption.csv",
    index=False
)

# Plot
plt.figure(figsize=(10, 5))

plt.plot(
    hourly_consumption.index,
    hourly_consumption.values,
    marker="o"
)

plt.xlabel("Hour of Day")
plt.ylabel("Average Active Power (kW)")
plt.title("Average Residential Energy Consumption by Hour")
plt.xticks(range(24))
plt.grid(True)

plt.savefig(
    "graphs/hourly_energy_consumption.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()