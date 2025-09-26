from flask import Flask, request, jsonify
import pandas as pd
from risk_models import calculate_premium_for_satellite

app = Flask(__name__)

try:
    forecast_data = pd.read_csv('data.csv')
    forecast_data['date'] = pd.to_datetime(forecast_data['date'])
    print("ook ball.")
except FileNotFoundError:
    forecast_data = None

@app.route('/get_premium', methods=['POST'])
def get_premium():
    if forecast_data is None:
        return jsonify({"error": "Forecast data not available"}), 500

    data = request.json
    event_date = pd.to_datetime(data['date'])
    satellite_value = float(data['satellite_value'])

    daily_forecasts = forecast_data[forecast_data['date'].dt.date == event_date.date()]

    if daily_forecasts.empty:
        return jsonify({"error": "No forecast data for the selected date."}), 404

    premium_details = calculate_premium_for_satellite(daily_forecasts, satellite_value)

    return jsonify(premium_details)

if __name__ == '__main__':
    app.run(debug=True)