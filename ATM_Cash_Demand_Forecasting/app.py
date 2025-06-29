# import sqlite3
# from flask import Flask, render_template, request, jsonify
# import pickle
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from datetime import datetime, timedelta
#
# # Load trained XGBoost model
# with open("model.pkl", "rb") as f:
#     model = pickle.load(f)
#
# app = Flask(__name__)
#
# # Define ATM locations (mapping locations to numerical values)
# ATM_LOCATIONS = {
#     "Kanifing": 0,
#     "Senegambia": 1,
#     "Brikame": 2,
#     "Airport": 3,
#     "Farafenni": 4
# }
#
# # Initialize SQLite database
# def init_db():
#     conn = sqlite3.connect("forecast.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS predictions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             forecast_date TEXT,
#             atm_location TEXT,
#             predicted_withdrawal REAL
#         )
#     """)
#     conn.commit()
#     conn.close()
#
# init_db()  # Create table if it doesn't exist
#
# @app.route("/")
# def home():
#     return render_template("index.html", locations=ATM_LOCATIONS.keys())
#
# @app.route("/predict_next7", methods=["POST"])
# def predict_next7():
#     try:
#         # Get user-selected start date and location
#         start_date_str = request.form["date"]
#         selected_location = request.form["location"]
#         start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
#
#         # Convert location to numerical value
#         location_value = ATM_LOCATIONS.get(selected_location, 0)
#
#         # Generate the next 7 days
#         predictions = []
#         dates = []
#         values = []
#
#         conn = sqlite3.connect("forecast.db")
#         cursor = conn.cursor()
#
#         for i in range(7):
#             future_date = start_date + timedelta(days=i)
#
#             # Feature extraction
#             features = np.array([
#                 [
#                     future_date.day,  # Day
#                     future_date.month,  # Month
#                     future_date.year,  # Year
#                     future_date.isocalendar()[1],  # WeekOfYear
#                     future_date.weekday(),  # DayOfWeek
#                     0,  # IsHoliday (Assuming 0)
#                     0,  # WeatherImpact (Assuming normal weather)
#                     location_value  # ATM Location
#                 ]
#             ])
#
#             # Predict withdrawal amount
#             prediction = model.predict(features)[0]
#             predictions.append((future_date.strftime("%Y-%m-%d"), round(prediction, 2)))
#             dates.append(future_date.strftime("%Y-%m-%d"))
#             values.append(prediction)
#
#             # Store in SQLite
#             cursor.execute("""
#                 INSERT INTO predictions (forecast_date, atm_location, predicted_withdrawal)
#                 VALUES (?, ?, ?)
#             """, (future_date.strftime("%Y-%m-%d"), selected_location, prediction))
#
#         conn.commit()
#         conn.close()
#
#         # Generate Matplotlib graph
#         plt.figure(figsize=(10, 5))
#         plt.plot(dates, values, marker="o", linestyle="-", color="blue", label=f"Predicted Withdrawals - {selected_location}")
#         plt.xlabel("Date")
#         plt.ylabel("Predicted Withdrawals")
#         plt.title(f"ATM Cash Demand Forecast (Next 7 Days) - {selected_location}")
#         plt.xticks(rotation=45)
#         plt.legend()
#         plt.grid(True)
#
#         # Save chart
#         chart_path = "static/forecast_chart.png"
#         plt.savefig(chart_path)
#         plt.close()
#
#         return render_template("index.html", predictions=predictions, chart_url=chart_path, locations=ATM_LOCATIONS.keys())
#
#     except Exception as e:
#         return jsonify({"error": str(e)})
#
# @app.route("/view_predictions")
# def view_predictions():
#     """Retrieve past predictions from the database and display them."""
#     conn = sqlite3.connect("forecast.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT forecast_date, atm_location, predicted_withdrawal FROM predictions ORDER BY forecast_date DESC")
#     past_predictions = cursor.fetchall()
#     conn.close()
#
#     return render_template("history.html", past_predictions=past_predictions)
#
# if __name__ == "__main__":
#     app.run(debug=True)













import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sqlite3
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load trained XGBoost model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Define ATM locations
ATM_LOCATIONS = {
    "Kanifing": 0,
    "Senegambia": 1,
    "Brikame": 2,
    "Airport": 3,
    "Farafenni": 4
}

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect("forecast.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            forecast_date TEXT,
            atm_location TEXT,
            predicted_withdrawal REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Streamlit UI
st.set_page_config(page_title="ATM Cash Forecast", layout="wide")
st.title("📊 ATM Cash Demand Forecasting App")

tab1, tab2 = st.tabs(["📈 Forecast", "🗃️ View History"])

with tab1:
    st.subheader("Forecast for Next 7 Days")

    selected_location = st.selectbox("Select ATM Location", ATM_LOCATIONS.keys())
    selected_date = st.date_input("Select Start Date", datetime.today())

    if st.button("Forecast"):
        location_value = ATM_LOCATIONS[selected_location]
        conn = sqlite3.connect("forecast.db")
        cursor = conn.cursor()

        predictions = []
        dates = []
        values = []

        for i in range(7):
            future_date = selected_date + timedelta(days=i)
            features = np.array([[
                future_date.day,
                future_date.month,
                future_date.year,
                future_date.isocalendar()[1],
                future_date.weekday(),
                0,  # IsHoliday
                0,  # WeatherImpact
                location_value
            ]])

            prediction = model.predict(features)[0]
            predictions.append((future_date.strftime("%Y-%m-%d"), round(prediction, 2)))
            dates.append(future_date.strftime("%Y-%m-%d"))
            values.append(prediction)

            # Save to database
            cursor.execute("""
                INSERT INTO predictions (forecast_date, atm_location, predicted_withdrawal) 
                VALUES (?, ?, ?)
            """, (future_date.strftime("%Y-%m-%d"), selected_location, prediction))

        conn.commit()
        conn.close()

        df = pd.DataFrame({
            "Date": dates,
            "Predicted Withdrawal (GMD)": [round(v, 2) for v in values]
        })

        st.success("Prediction completed!")
        st.dataframe(df)

        # Plot
        fig, ax = plt.subplots()
        ax.plot(dates, values, marker='o', color='blue')
        ax.set_title(f"Predicted Withdrawals for {selected_location}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Withdrawal Amount (GMD)")
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)

with tab2:
    st.subheader("Past Predictions")

    conn = sqlite3.connect("forecast.db")
    cursor = conn.cursor()
    cursor.execute("SELECT forecast_date, atm_location, predicted_withdrawal FROM predictions ORDER BY forecast_date DESC")
    data = cursor.fetchall()
    conn.close()

    if data:
        history_df = pd.DataFrame(data, columns=["Date", "ATM Location", "Predicted Withdrawal"])
        st.dataframe(history_df)
    else:
        st.info("No prediction history found.")
