import pandas as pd

DATA_PATH = "data/HomeC_augmented.csv"

print("\n--- LOADING DATASET ---")

df = pd.read_csv(DATA_PATH)

print("\n--- DATASET SHAPE ---")
print(df.shape)

print("\n--- COLUMN NAMES ---")
for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- BASIC INFORMATION ---")
print(df.info())