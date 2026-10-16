import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import milp, LinearConstraint, Bounds

BASELINE_PATH = "results/hourly_consumption.csv"

baseline_df = pd.read_csv(BASELINE_PATH)

baseline = baseline_df["Average_Consumption"].values
hours = np.arange(24)

appliances = {
    "Washing Machine": {
        "power": 0.8,
        "duration": 2,
        "start_min": 7,
        "start_max": 18
    },
    "Dishwasher": {
        "power": 1.2,
        "duration": 2,
        "start_min": 8,
        "start_max": 21
    },
    "Water Heater": {
        "power": 2.0,
        "duration": 2,
        "start_min": 5,
        "start_max": 18
    },
    "EV Charger": {
        "power": 3.0,
        "duration": 3,
        "start_min": 0,
        "start_max": 21
    }
}

appliance_names = list(appliances.keys())

start_variables = []

for appliance in appliance_names:
    data = appliances[appliance]

    valid_starts = range(
        data["start_min"],
        data["start_max"] + 1
    )

    for start in valid_starts:
        if start + data["duration"] <= 24:
            start_variables.append(
                (appliance, start)
            )

n_start_variables = len(start_variables)

peak_variable = n_start_variables

n_variables = n_start_variables + 1

c = np.zeros(n_variables)
c[peak_variable] = 1

integrality = np.zeros(n_variables)
integrality[:n_start_variables] = 1

lower_bounds = np.zeros(n_variables)
upper_bounds = np.ones(n_variables)

lower_bounds[peak_variable] = 0
upper_bounds[peak_variable] = np.inf

constraints_matrix = []
lower_constraint = []
upper_constraint = []

for appliance in appliance_names:

    row = np.zeros(n_variables)

    for i, (name, start) in enumerate(start_variables):
        if name == appliance:
            row[i] = 1

    constraints_matrix.append(row)
    lower_constraint.append(1)
    upper_constraint.append(1)

for hour in hours:

    row = np.zeros(n_variables)

    for i, (name, start) in enumerate(start_variables):

        data = appliances[name]

        if start <= hour < start + data["duration"]:
            row[i] = data["power"]

    row[peak_variable] = -1

    constraints_matrix.append(row)

    lower_constraint.append(-np.inf)
    upper_constraint.append(-baseline[hour])

A = np.array(constraints_matrix)

constraint = LinearConstraint(
    A,
    np.array(lower_constraint),
    np.array(upper_constraint)
)

result = milp(
    c=c,
    integrality=integrality,
    bounds=Bounds(
        lower_bounds,
        upper_bounds
    ),
    constraints=constraint
)

if not result.success:
    print("Optimization failed.")
    print(result.message)
    raise SystemExit

solution = result.x

optimized_peak = solution[peak_variable]

optimized_load = baseline.copy()

schedule = []

for i, (appliance, start) in enumerate(start_variables):

    if solution[i] > 0.5:

        power = appliances[appliance]["power"]
        duration = appliances[appliance]["duration"]

        for hour in range(
            start,
            start + duration
        ):
            optimized_load[hour] += power

        schedule.append({
            "Appliance": appliance,
            "Start Hour": start,
            "End Hour": start + duration,
            "Power (kW)": power,
            "Duration (hours)": duration
        })

schedule_df = pd.DataFrame(schedule)

baseline_peak = baseline.max()

print("\n--- BASELINE ENERGY DEMAND ---")
print(f"Peak demand: {baseline_peak:.3f} kW")

print("\n--- OPTIMIZED APPLIANCE SCHEDULE ---")
print(schedule_df.to_string(index=False))

print("\n--- OPTIMIZATION RESULT ---")
print(f"Optimized peak demand: {optimized_peak:.3f} kW")

print("\n--- PEAK COMPARISON ---")
print(f"Baseline peak: {baseline_peak:.3f} kW")
print(f"Optimized peak: {optimized_peak:.3f} kW")

print("\n--- SCHEDULE ---")

for _, row in schedule_df.iterrows():
    print(
        f"{row['Appliance']}: "
        f"{int(row['Start Hour']):02d}:00 - "
        f"{int(row['End Hour']):02d}:00"
    )

schedule_df.to_csv(
    "results/optimized_schedule.csv",
    index=False
)

comparison_df = pd.DataFrame({
    "Hour": hours,
    "Baseline_Load": baseline,
    "Optimized_Load": optimized_load
})

comparison_df.to_csv(
    "results/optimization_comparison.csv",
    index=False
)

plt.figure(figsize=(12, 6))

plt.plot(
    hours,
    baseline,
    marker="o",
    label="Baseline Demand"
)

plt.plot(
    hours,
    optimized_load,
    marker="o",
    label="Optimized Demand"
)

plt.xlabel("Hour of Day")
plt.ylabel("Power (kW)")
plt.title("Baseline vs Optimized Residential Energy Demand")
plt.xticks(hours)
plt.legend()
plt.grid(True)

plt.savefig(
    "graphs/optimization_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()