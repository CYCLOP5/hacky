import requests
import pandas as pd
from datetime import datetime, timedelta
from crewai.tools import BaseTool

# Import the new LSTM handler (optional)
try:
    from lstm_model_handler import LSTMModelHandler  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    LSTMModelHandler = None

# --- Tool 1: Direct NOAA Forecast ---
class SpaceWeatherTools(BaseTool):
    name: str = "NOAA Space Weather Forecast Tool"
    description: str = (
        "Fetches and processes the official NOAA 3-day Planetary K-index (Kp) forecast. "
        "This tool uses the same data source as the web interface 3-day forecast page "
        "to ensure consistency across all AI agents and user-facing displays."
    )

    def _run(self) -> str:
        """
        Fetch the official NOAA 3-day forecast - same source as the web interface uses.
        This ensures consistency between AI agents and the forecast page.
        """
        # Use the same API endpoint as the 3-day forecast page for consistency
        try:
            response = requests.get("http://localhost:8000/api/forecast-3day")
            response.raise_for_status()
            forecast_data = response.json()
            
            if not forecast_data or not forecast_data.get('breakdown'):
                return "Error: No 3-day forecast data available from NOAA."
            
            # Extract the first day's data (next 24 hours)
            first_day_periods = [row for row in forecast_data['breakdown'] if row.get('values')]
            
            if not first_day_periods:
                return "Error: No forecast breakdown data available for analysis."
            
            # Get all Kp values for the first day (next 24 hours)
            first_day_kp_values = []
            for period_data in first_day_periods:
                if period_data.get('values') and len(period_data['values']) > 0:
                    first_day_kp_values.append(period_data['values'][0])  # First day values
            
            if not first_day_kp_values:
                return "Error: No Kp values found in the first day of the forecast."
            
            # Calculate the worst-case (maximum) Kp for next 24 hours
            worst_case_kp = max(first_day_kp_values)
            expected_max_kp = forecast_data.get('expected_max_kp', worst_case_kp)
            
            # Use the official expected maximum if available, otherwise use calculated worst case
            final_kp = expected_max_kp if expected_max_kp is not None else worst_case_kp
            
            return (
                f"Successfully fetched official NOAA 3-day forecast data. "
                f"The maximum predicted Kp index for the next 24 hours is {final_kp:.2f}. "
                f"This data is consistent with the 3-day forecast page. "
                f"Forecast issued: {forecast_data.get('issued', 'Unknown')}. "
                f"NOAA rationale: {forecast_data.get('rationale', 'No additional context provided.')[:200]}..."
            )

        except requests.exceptions.RequestException as e:
            # Fallback to direct NOAA API if local server is unavailable
            return self._fallback_direct_noaa()
        except Exception as e:
            return f"Error: Unexpected error while fetching 3-day forecast: {e}"
    
    def _fallback_direct_noaa(self) -> str:
        """
        Fallback method that fetches directly from NOAA if the local API is unavailable.
        This maintains the old behavior as a backup.
        """
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
            return f"Successfully fetched NOAA data (fallback). The maximum predicted Kp index for the next 24 hours is {worst_case_kp:.2f}."

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
        if LSTMModelHandler is None:
            return "Error: LSTM model handler not available."
        handler = LSTMModelHandler()
        if not getattr(handler, "model", None) or not getattr(handler, "scaler", None):
            return "Error: LSTM model is not available or could not be loaded."
        
        prediction = handler.predict(recent_solar_wind_data)
        
        if prediction is not None:
            return f"The custom LSTM model predicts a Kp index of: {prediction:.2f}"
        else:
            return "Error: LSTM model failed to produce a prediction. Check input data format and model files."

