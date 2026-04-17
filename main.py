import os
from src.data_preprocessing import load_data
from src.feature_engineering import create_features
from src.forecasting import train_model, forecast, future_forecast
from src.inventory import inventory_logic

# create outputs folder
os.makedirs("outputs", exist_ok=True)

# ---------------- LOAD DATA ----------------
df = load_data("data/raw/sales.csv")

# ---------------- FEATURE ENGINEERING ----------------
df, df_encoded = create_features(df)

# ---------------- MODEL TRAINING ----------------
model = train_model(df_encoded)

# ---------------- FORECAST ----------------
df_encoded = forecast(model, df_encoded)

# ---------------- 🔥 MERGE BACK  ----------------
df['predicted_sales'] = df_encoded['predicted_sales']
df['actual_vs_predicted_diff'] = df_encoded['actual_vs_predicted_diff']

# ---------------- INVENTORY LOGIC ----------------
inventory = inventory_logic(df)

# ---------------- SAVE MAIN OUTPUT ----------------
inventory.to_csv("outputs/inventory_plan.csv", index=False)

# ---------------- FUTURE FORECAST ----------------
future = future_forecast(model, df_encoded)
future.to_csv("outputs/future_forecast.csv", index=False)

print("✅ File created")
print("Rows:", len(inventory))
print("✅ Future forecast saved")