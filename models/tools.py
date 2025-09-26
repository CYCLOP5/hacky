import numpy as np
import joblib
from tensorflow.keras.models import load_model

MODEL = load_model('kp_forecasting_model.h5')
SCALER = joblib.load('feature_scaler.pkl')

def predict_kp_distribution(input_features: np.ndarray) -> dict:
    """
    Takes the last 24 hours of feature data, scales it, and returns a 
    probabilistic Kp forecast using Monte Carlo Dropout.
    """

    scaled_features = SCALER.transform(input_features)

    reshaped_features = np.reshape(scaled_features, (1, scaled_features.shape[0], scaled_features.shape[1]))

    predictions = []
    n_simulations = 100

    for _ in range(n_simulations):

        pred = MODEL(reshaped_features, training=True)
        predictions.append(pred[0][0])

    predictions = np.array(predictions)

    result = {
        "lower": np.percentile(predictions, 10) / 10.0,
        "median": np.median(predictions) / 10.0,
        "upper": np.percentile(predictions, 90) / 10.0,
    }
    return result