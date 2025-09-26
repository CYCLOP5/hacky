import numpy as np
from tools import predict_kp_distribution

print("--- Running Model Test ---")

dummy_input_data = np.random.rand(24, 9)

print("Shape of dummy input data:", dummy_input_data.shape)
print("Running prediction...")

forecast = predict_kp_distribution(dummy_input_data)

print("\n--- Probabilistic Forecast Result ---")
print(f"  - Most Likely Kp (Median): {forecast['median']:.2f}")
print(f"  - 90% Confidence Range: {forecast['lower']:.2f} to {forecast['upper']:.2f}")
