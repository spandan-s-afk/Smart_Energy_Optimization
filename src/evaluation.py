import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# LOAD OPTIMIZATION RESULTS
# ============================================================

INPUT_PATH = "results/optimization_results.csv"

print("\n--- LOADING OPTIMIZATION RESULTS ---")

df = pd.read_csv(INPUT_PATH)

df["time"] = pd.to_datetime(df["time"])

print("Rows:", len(df))


# ============================================================
# CALCULATE METRICS
# ============================================================

before_peak = df["actual_total_load"].max()

after_peak = df["optimized_total_load"].max()

before_average = df["actual_total_load"].mean()

after_average = df["optimized_total_load"].mean()

interval_hours = 0.25

before_energy = (
    df["actual_total_load"].sum()
    * interval_hours
)

after_energy = (
    df["optimized_total_load"].sum()
    * interval_hours
)

peak_reduction = (
    before_peak - after_peak
)

peak_reduction_percent = (
    peak_reduction
    / before_peak
    * 100
)

energy_difference = (
    before_energy - after_energy
)


# ============================================================
# CREATE COMPARISON TABLE
# ============================================================

comparison = pd.DataFrame({
    "Metric": [
        "Maximum Load (kW)",
        "Average Load (kW)",
        "Daily Energy (kWh)"
    ],

    "Before Optimization": [
        before_peak,
        before_average,
        before_energy
    ],

    "After Optimization": [
        after_peak,
        after_average,
        after_energy
    ]
})


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n========================================")
print("       BEFORE vs AFTER EVALUATION")
print("========================================")

print(
    comparison.to_string(index=False)
)

print("\n----------------------------------------")

print(
    f"Peak reduction: "
    f"{peak_reduction:.4f} kW"
)

print(
    f"Peak reduction percentage: "
    f"{peak_reduction_percent:.2f}%"
)

print(
    f"Energy difference: "
    f"{energy_difference:.4f} kWh"
)

print("========================================")


# ============================================================
# SAVE COMPARISON
# ============================================================

OUTPUT_PATH = "results/before_after_comparison.csv"

comparison.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nComparison saved to:")

print(OUTPUT_PATH)


# ============================================================
# CREATE BAR CHART
# ============================================================

metrics = [
    "Maximum Load",
    "Average Load",
    "Daily Energy"
]

before_values = [
    before_peak,
    before_average,
    before_energy
]

after_values = [
    after_peak,
    after_average,
    after_energy
]


x = np.arange(len(metrics))

width = 0.35


plt.figure(figsize=(10, 6))

plt.bar(
    x - width / 2,
    before_values,
    width,
    label="Before Optimization"
)

plt.bar(
    x + width / 2,
    after_values,
    width,
    label="After Optimization"
)

plt.xticks(
    x,
    metrics
)

plt.ylabel("Value")

plt.title(
    "Energy Management Before vs After Optimization"
)

plt.legend()

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

GRAPH_PATH = "graphs/before_after_comparison.png"

plt.savefig(
    GRAPH_PATH,
    dpi=300
)

plt.close()

print("\nComparison graph saved to:")

print(GRAPH_PATH)

print("\n--- EVALUATION COMPLETED ---")