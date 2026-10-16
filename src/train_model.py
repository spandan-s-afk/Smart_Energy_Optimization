import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import numpy as np

DATA_PATH = "data/processed_energy_data.csv"

df = pd.read_csv(DATA_PATH)

features = [
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3",
    "hour",
    "day",
    "month",
    "day_of_week",
    "is_weekend"
]

target = "Global_active_power"

X = df[features]
y = df[target]

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\n--- TRAINING DATA ---")
print(X_train.shape)

print("\n--- TEST DATA ---")
print(X_test.shape)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("\n--- TRAINING MODEL ---")
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)

print("\n--- MODEL PERFORMANCE ---")
print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)

joblib.dump(
    model,
    "models/random_forest_energy_model.pkl"
)

print("\n--- MODEL SAVED ---")
print("models/random_forest_energy_model.pkl")