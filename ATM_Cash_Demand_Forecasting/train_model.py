import pandas as pd
import xgboost as xgb
import pickle

# Load dataset
df = pd.read_csv("dataset/atm_cash_data.csv")

# Feature engineering
df["Day"] = pd.to_datetime(df["Date"]).dt.day
df["Month"] = pd.to_datetime(df["Date"]).dt.month
df["Year"] = pd.to_datetime(df["Date"]).dt.year
df["WeekOfYear"] = pd.to_datetime(df["Date"]).dt.isocalendar().week
#df["Day_Of_Week"] = pd.to_datetime(df["Date"]).dt.weekday

df['Location'] = df['Location'].map({'Urban': 0, 'Rural': 1})

# Features & target
X = df[["Day", "Month", "Year", "WeekOfYear", 'DayOfWeek', 'IsHoliday', 'WeatherImpact', 'Location']]
y = df["Withdrawals"]

# Train XGBoost model
model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100)
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)