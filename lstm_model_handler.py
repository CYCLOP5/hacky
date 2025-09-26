import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
import os

# --- Constants ---
# Assumes your models are in a sub-folder named 'models'
MODEL_PATH = os.path.join('models', 'your_lstm_model.h5')
SCALER_PATH = os.path.join('models', 'your_scaler.pkl')

# The number of past time steps the model was trained on
N_STEPS = 60 # Example: Trained on 60 minutes of data to predict the next step
# The number of features the model expects (e.g., speed, density, temperature, etc.)
N_FEATURES = 5 # Example: If you used 5 solar wind parameters as input

class LSTMModelHandler:
    """
    A class to encapsulate the loading and prediction logic for a pre-trained
    LSTM model and its associated scaler.
    """
    def __init__(self, model_path=MODEL_PATH, scaler_path=SCALER_PATH):
        self.model = None
        self.scaler = None
        self.load_model_and_scaler(model_path, scaler_path)

    def load_model_and_scaler(self, model_path, scaler_path):
        """
        Loads the Keras model and the joblib scaler from disk.
        Handles errors if the files are not found.
        """
        try:
            print(f"Attempting to load model from: {os.path.abspath(model_path)}")
            self.model = load_model(model_path)
            print(f"Attempting to load scaler from: {os.path.abspath(scaler_path)}")
            self.scaler = joblib.load(scaler_path)
            print("LSTM model and scaler loaded successfully.")
        except FileNotFoundError as e:
            print(f"Warning: Model or scaler file not found. {e}. The LSTM tool will not be usable.")
            self.model = None
            self.scaler = None
        except Exception as e:
            print(f"An error occurred during model/scaler loading: {e}")
            self.model = None
            self.scaler = None

    def prepare_input_data(self, recent_data: pd.DataFrame) -> np.ndarray | None:
        """
        Scales and reshapes the input data to be compatible with the LSTM model.
        
        Args:
            recent_data: A pandas DataFrame containing the last N_STEPS of solar wind data,
                         with columns corresponding to the features the model was trained on.
        
        Returns:
            A numpy array ready for model prediction, or None if an error occurs.
        """
        if self.scaler is None:
            print("Error: Scaler is not loaded. Cannot prepare data.")
            return None
            
        if len(recent_data) < N_STEPS:
            print(f"Error: Not enough data provided. Expected {N_STEPS} time steps, but got {len(recent_data)}.")
            return None

        # Ensure the data has the correct number of features
        if recent_data.shape[1] != N_FEATURES:
            print(f"Error: Incorrect number of features. Expected {N_FEATURES}, but got {recent_data.shape[1]}.")
            return None

        # Scale the data using the pre-trained scaler
        scaled_data = self.scaler.transform(recent_data.tail(N_STEPS))
        
        # Reshape for LSTM input: [1, n_steps, n_features]
        return scaled_data.reshape(1, N_STEPS, N_FEATURES)

    def predict(self, input_data: pd.DataFrame) -> float | None:
        """
        Makes a Kp index prediction using the loaded LSTM model.
        
        Args:
            input_data: A pandas DataFrame of recent solar wind data.
        
        Returns:
            The predicted Kp index as a single float, or None if prediction fails.
        """
        if self.model is None:
            print("Error: Model is not loaded. Cannot make a prediction.")
            return None

        prepared_input = self.prepare_input_data(input_data)
        if prepared_input is None:
            return None
        
        # Make a prediction
        predicted_scaled = self.model.predict(prepared_input)
        
        # The scaler was likely trained on all features including the target.
        # To inverse transform, we need to create a dummy array of the correct shape.
        dummy_array = np.zeros((1, N_FEATURES))
        dummy_array[0, 0] = predicted_scaled[0, 0] # Assuming Kp is the first feature
        
        # Inverse transform to get the actual Kp value
        predicted_kp = self.scaler.inverse_transform(dummy_array)[0, 0]
        
        return predicted_kp

# Example of how you would use this class (for testing)
# if __name__ == '__main__':
#     # This part would not be run by the agent, it's for standalone testing.
#     # You would need dummy model/scaler files and dummy data to run this.
#     handler = LSTMModelHandler()
#     if handler.model and handler.scaler:
#         # Create a dummy DataFrame with the correct shape and columns
#         dummy_data = pd.DataFrame(np.random.rand(N_STEPS, N_FEATURES), columns=[f'feat_{i}' for i in range(N_FEATURES)])
#         prediction = handler.predict(dummy_data)
#         if prediction is not None:
#             print(f"Predicted Kp index: {prediction}")
