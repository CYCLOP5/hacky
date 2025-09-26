import requests
import pandas as pd
from datetime import datetime, timedelta
from crewai.tools import BaseTool

# Import the new LSTM handler
from lstm_model_handler import LSTMModelHandler

# --- Tool 1: Direct NOAA Forecast ---
class SpaceWeatherTools(BaseTool):
    name: str = "NOAA Space Weather Forecast Tool"
    description: str = (
        "Fetches and processes the 3-day Planetary K-index (Kp) forecast directly from the NOAA. "
        "This is the primary, most reliable tool for getting the official forecast. "
        "It returns a summary including the worst-case Kp value for the next 24 hours."
    )

    def _run(self) -> str:
        # ... (code from previous step remains unchanged) ...
        url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if not data or len(data) < 2:
                return "Error: Received empty or invalid data from NOAA API."
            
            columns, records = data[0], data[1:]
            df = pd.DataFrame(records, columns=columns)
            df['time_tag'] = pd.to_datetime(df['time_tag'])
            df['kp'] = pd.to_numeric(df['kp'], errors='coerce')
            df = df.dropna(subset=['kp'])

            now_utc = datetime.utcnow()
            forecast_horizon = now_utc + timedelta(hours=24)
            next_24h_df = df[df['time_tag'] <= forecast_horizon]

            if next_24h_df.empty:
                return "Error: No forecast data is available for the next 24 hours."
            
            worst_case_kp = next_24h_df['kp'].max()
            return f"Successfully fetched NOAA data. The maximum predicted Kp index for the next 24 hours is {worst_case_kp:.2f}."

        except Exception as e:
            return f"Error: An unexpected error occurred while fetching NOAA data: {e}"


# --- Tool 2: Custom LSTM Forecasting (The Unused Alternative) ---
class LSTMForecastTool(BaseTool):
    name: str = "Custom LSTM Kp Index Forecasting Tool"
    description: str = (
        "An alternative forecasting tool that uses a pre-trained LSTM model. "
        "It requires a recent history of solar wind data (e.g., speed, density, temperature) "
        "to predict the Kp index. Use this only if the primary NOAA tool fails or for comparison."
    )
    
    def _run(self, recent_solar_wind_data: pd.DataFrame) -> str:
        """
        The main execution method for the LSTM tool.
        """
        handler = LSTMModelHandler()
        if not handler.model or not handler.scaler:
            return "Error: LSTM model is not available or could not be loaded."
        
        prediction = handler.predict(recent_solar_wind_data)
        
        if prediction is not None:
            return f"The custom LSTM model predicts a Kp index of: {prediction:.2f}"
        else:
            return "Error: LSTM model failed to produce a prediction. Check input data format and model files."

