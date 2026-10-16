import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# 1. LOAD PROCESSED DATA
# ============================================================

DATA_PATH = "data/homec_processed.csv"
MODEL_PATH = "models/homec_random_forest_model.pkl"
GRAPH_PATH = "graphs/predicted_vs_actual.png"

print("\n--- LOADING PROCESSED HOMEC DATASET ---")

df = pd.read_csv(DATA_PATH)

df["time"] = pd.to_datetime(df["time"])
df = df.sort_values("time").reset_index(drop=True)

print("Original shape:", df.shape)


# ============================================================
# 2. SELECT TARGET
# ============================================================

TARGET = "total_appliance_power"

print("\n--- TARGET ---")
print(TARGET)


# ============================================================
# 3. RESAMPLE TO 15-MINUTE INTERVALS
# ============================================================

print("\n--- RESAMPLING TO 15-MINUTE INTERVALS ---")

df = df.set_index("time")

numeric_columns = df.select_dtypes(include=np.number).columns

df_15 = df[numeric_columns].resample("15min").mean()

df_15 = df_15.reset_index()

print("15-minute shape:", df_15.shape)


# ============================================================
# 4. CREATE FUTURE TARGET
# ============================================================

# Predict the next 15-minute appliance power

df_15["future_power"] = df_15[TARGET].shift(-1)


# ============================================================
# 5. CREATE PREVIOUS-CONSUMPTION FEATURES
# ============================================================

# Previous 15 minutes
df_15["previous_power"] = df_15[TARGET].shift(1)

# Previous 1 hour
# 4 × 15 minutes = 1 hour
df_15["previous_1h_power"] = df_15[TARGET].shift(4)

# Previous 24 hours
# 96 × 15 minutes = 24 hours
df_15["previous_24h_power"] = df_15[TARGET].shift(96)


# ============================================================
# 6. CREATE TIME FEATURES
# ============================================================

df_15["hour"] = df_15["time"].dt.hour

df_15["day"] = df_15["time"].dt.day

df_15["month"] = df_15["time"].dt.month

df_15["day_of_week"] = df_15["time"].dt.dayofweek

df_15["is_weekend"] = (
    df_15["day_of_week"] >= 5
).astype(int)

# Peak hours defined according to our project analysis
df_15["is_peak_hour"] = (
    df_15["hour"].isin([18, 19, 20, 21, 22])
).astype(int)


# ============================================================
# 7. SELECT WEATHER FEATURES
# ============================================================

weather_features = [
    "temperature",
    "humidity",
    "apparentTemperature",
    "pressure",
    "windSpeed",
    "cloudCover",
    "precipIntensity",
    "dewPoint",
    "precipProbability"
]


# ============================================================
# 8. SELECT MODEL FEATURES
# ============================================================

features = [
    "previous_power",
    "previous_1h_power",
    "previous_24h_power",
    "hour",
    "day",
    "month",
    "day_of_week",
    "is_weekend",
    "is_peak_hour"
]

# Add weather features that exist
for column in weather_features:
    if column in df_15.columns:
        features.append(column)


print("\n--- MODEL FEATURES ---")

for feature in features:
    print(feature)


# ============================================================
# 9. REMOVE MISSING VALUES
# ============================================================

model_data = df_15[features + ["future_power"]].dropna()

print("\n--- MODEL DATA ---")
print("Shape:", model_data.shape)


# ============================================================
# 10. CHRONOLOGICAL TRAIN-TEST SPLIT
# ============================================================

split_index = int(len(model_data) * 0.80)

train_data = model_data.iloc[:split_index]

test_data = model_data.iloc[split_index:]

X_train = train_data[features]
y_train = train_data["future_power"]

X_test = test_data[features]
y_test = test_data["future_power"]


print("\n--- TRAIN TEST SPLIT ---")

print("Training samples:", len(X_train))
print("Testing samples :", len(X_test))


# ============================================================
# 11. TRAIN RANDOM FOREST MODEL
# ============================================================

print("\n--- TRAINING RANDOM FOREST MODEL ---")

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ============================================================
# 12. PREDICTION
# ============================================================

print("\n--- GENERATING PREDICTIONS ---")

y_pred = model.predict(X_test)


# ============================================================
# 13. MODEL EVALUATION
# ============================================================

mae = mean_absolute_error(y_test, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_test, y_pred)
)

r2 = r2_score(y_test, y_pred)


print("\n========================================")
print("       MODEL PERFORMANCE")
print("========================================")

print(f"MAE  : {mae:.6f} kW")
print(f"RMSE : {rmse:.6f} kW")
print(f"R²   : {r2:.6f}")

print("========================================")


# ============================================================
# 14. SAVE MODEL
# ============================================================

with open(MODEL_PATH, "wb") as file:
    pickle.dump(
        {
            "model": model,
            "features": features
        },
        file
    )

print("\n--- MODEL SAVED ---")
print(MODEL_PATH)


# ============================================================
# 15. PREDICTION GRAPH
# ============================================================

print("\n--- CREATING PREDICTION GRAPH ---")

plt.figure(figsize=(12, 5))

# Show only first 300 test samples for readability
samples = min(300, len(y_test))

plt.plot(
    y_test.iloc[:samples].values,
    label="Actual Power"
)

plt.plot(
    y_pred[:samples],
    label="Predicted Power"
)

plt.xlabel("15-Minute Time Intervals")
plt.ylabel("Power (kW)")
plt.title("Actual vs Predicted Appliance Power")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(GRAPH_PATH, dpi=300)

plt.close()

print("Graph saved:", GRAPH_PATH)

print("\n--- ML TRAINING COMPLETED SUCCESSFULLY ---")