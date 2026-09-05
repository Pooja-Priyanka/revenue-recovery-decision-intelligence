import pandas as pd

file_path = "data/processed/temporal_account_features.csv"

df = pd.read_csv(file_path)

print("====================================")
print("TEMPORAL FEATURE DATASET")
print("====================================")

print("\nShape:")
print(df.shape)

print("\nColumns:")
for column in df.columns:
    print("-", column)

print("\nMissing values:")
print(df.isnull().sum())

print("\nTarget distribution:")
print(df["churn_target"].value_counts())

print("\nFirst 5 rows:")
print(df.head())

print("\nTarget percentage:")
print(df["churn_target"].value_counts(normalize=True) * 100)