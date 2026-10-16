import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import milp, LinearConstraint, Bounds


# ============================================================
# SETTINGS
# ============================================================

DATA_PATH = "data/homec_processed.csv"

SELECTED_DATE = "2016-11-28"

OUTPUT_CSV = "results/optimization_results.csv"

GRAPH_PATH = "graphs/before_after_optimization.png"

INTERVAL_HOURS = 0.25

# Only this percentage of flexible load can be shifted.
SHIFTABLE_PERCENT = 0.30


# ============================================================
# FLEXIBLE APPLIANCES
# ============================================================

FLEXIBLE_APPLIANCES = [
    "Car charger [kW]",
    "Water heater [kW]",
    "Laundry [kW]",
    "Pool Pump [kW]"
]


# ============================================================
# OPTIMIZATION WINDOWS
# These are project modeling assumptions.
# ============================================================

OPTIMIZATION_WINDOWS = {

    "Car charger [kW]": (0, 23),

    "Water heater [kW]": (5, 22),

    "Laundry [kW]": (8, 20),

    "Pool Pump [kW]": (6, 18)
}


# ============================================================
# FIXED APPLIANCES
# ============================================================

FIXED_APPLIANCES = [
    "Air conditioning [kW]",
    "Home Theater [kW]",
    "Outdoor lights [kW]",
    "microwave [kW]"
]


# ============================================================
# LOAD DATA
# ============================================================

print("\n--- LOADING DATA ---")

df = pd.read_csv(DATA_PATH)

df["time"] = pd.to_datetime(df["time"])

df = df[
    df["time"].dt.date
    == pd.Timestamp(SELECTED_DATE).date()
].copy()

print("Selected date:", SELECTED_DATE)
print("Rows:", len(df))


# ============================================================
# RESAMPLE TO 15 MINUTES
# ============================================================

print("\n--- RESAMPLING TO 15-MINUTE INTERVALS ---")

columns_needed = (
    FLEXIBLE_APPLIANCES
    + FIXED_APPLIANCES
)

df = df.set_index("time")

df_15 = (
    df[columns_needed]
    .resample("15min")
    .mean()
)

df_15 = df_15.dropna()

print("15-minute slots:", len(df_15))


# ============================================================
# FIXED LOAD
# ============================================================

df_15["fixed_load"] = (
    df_15[FIXED_APPLIANCES].sum(axis=1)
)


# ============================================================
# ACTUAL FLEXIBLE LOAD
# ============================================================

df_15["actual_flexible_load"] = (
    df_15[FLEXIBLE_APPLIANCES].sum(axis=1)
)

df_15["actual_total_load"] = (
    df_15["fixed_load"]
    + df_15["actual_flexible_load"]
)


# ============================================================
# CALCULATE SHIFTABLE LOAD
# ============================================================

print("\n--- SHIFTABLE LOAD ---")

for appliance in FLEXIBLE_APPLIANCES:

    df_15[
        "shiftable_" + appliance
    ] = (
        df_15[appliance]
        * SHIFTABLE_PERCENT
    )

    df_15[
        "fixed_" + appliance
    ] = (
        df_15[appliance]
        * (1 - SHIFTABLE_PERCENT)
    )

    energy = (
        df_15[
            "shiftable_" + appliance
        ].sum()
        * INTERVAL_HOURS
    )

    print(
        f"{appliance}: "
        f"{energy:.4f} kWh shiftable"
    )


# ============================================================
# VARIABLES
# ============================================================

n_appliances = len(FLEXIBLE_APPLIANCES)

n_slots = len(df_15)

load_variables = (
    n_appliances * n_slots
)

peak_index = load_variables

n_variables = load_variables + 1


# ============================================================
# OBJECTIVE
# ============================================================

objective = np.zeros(n_variables)

# Minimize maximum total load

objective[peak_index] = 1


# ============================================================
# ENERGY PRESERVATION
# ============================================================

A_energy = np.zeros(
    (n_appliances, n_variables)
)

energy_lower = np.zeros(n_appliances)

energy_upper = np.zeros(n_appliances)


for a, appliance in enumerate(
    FLEXIBLE_APPLIANCES
):

    shiftable_column = (
        "shiftable_" + appliance
    )

    required_energy = (
        df_15[shiftable_column].sum()
        * INTERVAL_HOURS
    )

    for t in range(n_slots):

        index = (
            a * n_slots + t
        )

        A_energy[a, index] = (
            INTERVAL_HOURS
        )

    energy_lower[a] = required_energy
    energy_upper[a] = required_energy


# ============================================================
# PEAK CONSTRAINT
# ============================================================

A_peak = np.zeros(
    (n_slots, n_variables)
)

peak_lower = np.full(
    n_slots,
    -np.inf
)

peak_upper = np.zeros(n_slots)


for t in range(n_slots):

    for a, appliance in enumerate(
        FLEXIBLE_APPLIANCES
    ):

        index = (
            a * n_slots + t
        )

        A_peak[t, index] = 1

    A_peak[t, peak_index] = -1

    fixed_load = (
        df_15["fixed_load"].iloc[t]
    )

    for appliance in FLEXIBLE_APPLIANCES:

        fixed_load += (
            df_15[
                "fixed_" + appliance
            ].iloc[t]
        )

    peak_upper[t] = -fixed_load


# ============================================================
# OPERATING WINDOWS
# ============================================================

window_rows = []

window_lower = []

window_upper = []


for a, appliance in enumerate(
    FLEXIBLE_APPLIANCES
):

    start_hour, end_hour = (
        OPTIMIZATION_WINDOWS[appliance]
    )

    for t in range(n_slots):

        hour = df_15.index[t].hour

        # Outside allowed window:
        # shiftable load must be zero.

        if (
            hour < start_hour
            or hour > end_hour
        ):

            row = np.zeros(n_variables)

            index = (
                a * n_slots + t
            )

            row[index] = 1

            window_rows.append(row)

            window_lower.append(0)

            window_upper.append(0)


# ============================================================
# MAXIMUM SHIFTABLE POWER
# ============================================================

# Limit shifted power to twice the maximum
# observed shiftable power for each appliance.

power_upper = np.full(
    n_variables,
    np.inf
)

for a, appliance in enumerate(
    FLEXIBLE_APPLIANCES
):

    maximum = (
        df_15[
            "shiftable_" + appliance
        ].max()
    )

    for t in range(n_slots):

        index = (
            a * n_slots + t
        )

        power_upper[index] = (
            maximum * 2
        )


# Peak variable remains unrestricted

power_upper[peak_index] = np.inf


# ============================================================
# COMBINE CONSTRAINTS
# ============================================================

A = np.vstack([
    A_energy,
    A_peak,
    np.array(window_rows)
])

lower = np.concatenate([
    energy_lower,
    peak_lower,
    np.array(window_lower)
])

upper = np.concatenate([
    energy_upper,
    peak_upper,
    np.array(window_upper)
])


constraints = LinearConstraint(
    A,
    lower,
    upper
)


# ============================================================
# VARIABLE BOUNDS
# ============================================================

variable_lower = np.zeros(n_variables)

bounds = Bounds(
    variable_lower,
    power_upper
)


# ============================================================
# CONTINUOUS VARIABLES
# ============================================================

integrality = np.zeros(
    n_variables
)


# ============================================================
# RUN OPTIMIZATION
# ============================================================

print("\n--- RUNNING CONSTRAINED OPTIMIZATION ---")

result = milp(
    c=objective,
    integrality=integrality,
    bounds=bounds,
    constraints=constraints,
    options={
        "time_limit": 120
    }
)


# ============================================================
# CHECK RESULT
# ============================================================

if not result.success:

    print("\nOptimization failed.")

    print("Message:", result.message)

    raise SystemExit


print("\n--- OPTIMIZATION SUCCESSFUL ---")

print("Solver message:")
print(result.message)


# ============================================================
# EXTRACT OPTIMIZED LOAD
# ============================================================

solution = result.x

for a, appliance in enumerate(
    FLEXIBLE_APPLIANCES
):

    values = []

    for t in range(n_slots):

        index = (
            a * n_slots + t
        )

        values.append(
            solution[index]
        )

    df_15[
        "optimized_shiftable_" + appliance
    ] = values


# ============================================================
# CALCULATE OPTIMIZED APPLIANCE LOAD
# ============================================================

optimized_columns = []

for appliance in FLEXIBLE_APPLIANCES:

    optimized_column = (
        "optimized_" + appliance
    )

    fixed_column = (
        "fixed_" + appliance
    )

    shiftable_column = (
        "optimized_shiftable_" + appliance
    )

    df_15[optimized_column] = (
        df_15[fixed_column]
        + df_15[shiftable_column]
    )

    optimized_columns.append(
        optimized_column
    )


# ============================================================
# OPTIMIZED TOTAL LOAD
# ============================================================

df_15["optimized_flexible_load"] = (
    df_15[optimized_columns].sum(axis=1)
)

df_15["optimized_total_load"] = (
    df_15["fixed_load"]
    + df_15["optimized_flexible_load"]
)


# ============================================================
# PEAK RESULTS
# ============================================================

before_peak = (
    df_15["actual_total_load"].max()
)

after_peak = (
    df_15["optimized_total_load"].max()
)

peak_reduction = (
    before_peak - after_peak
)

peak_reduction_percent = (
    peak_reduction
    / before_peak
    * 100
)


# ============================================================
# ENERGY RESULTS
# ============================================================

before_energy = (
    df_15["actual_total_load"].sum()
    * INTERVAL_HOURS
)

after_energy = (
    df_15["optimized_total_load"].sum()
    * INTERVAL_HOURS
)

energy_difference = (
    before_energy - after_energy
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n========================================")
print("     CONSTRAINED OPTIMIZATION RESULTS")
print("========================================")

print(
    f"Before peak load : "
    f"{before_peak:.4f} kW"
)

print(
    f"After peak load  : "
    f"{after_peak:.4f} kW"
)

print(
    f"Peak reduction   : "
    f"{peak_reduction:.4f} kW"
)

print(
    f"Peak reduction % : "
    f"{peak_reduction_percent:.2f}%"
)

print()

print(
    f"Before energy : "
    f"{before_energy:.4f} kWh"
)

print(
    f"After energy  : "
    f"{after_energy:.4f} kWh"
)

print(
    f"Energy difference : "
    f"{energy_difference:.6f} kWh"
)

print("========================================")


# ============================================================
# SAVE RESULTS
# ============================================================

output = df_15.reset_index()

output.to_csv(
    OUTPUT_CSV,
    index=False
)

print("\nResults saved to:")
print(OUTPUT_CSV)


# ============================================================
# CREATE GRAPH
# ============================================================

plt.figure(figsize=(14, 6))

plt.plot(
    output["time"],
    output["actual_total_load"],
    label="Before Optimization"
)

plt.plot(
    output["time"],
    output["optimized_total_load"],
    label="After Optimization"
)

plt.xlabel("Time")

plt.ylabel("Power (kW)")

plt.title(
    "Before vs After Constrained Optimization"
)

plt.legend()

plt.grid(True)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    GRAPH_PATH,
    dpi=300
)

plt.close()

print("\nGraph saved to:")
print(GRAPH_PATH)

print("\n--- CONSTRAINED OPTIMIZATION COMPLETED ---")