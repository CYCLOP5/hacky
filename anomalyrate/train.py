import pandas as pd
import numpy as np


csv_file = "anamolies.csv" 
df = pd.read_csv(csv_file)


df['Kp_clean'] = df['Kp'].astype(str).str.replace(r'[^\d.]', '', regex=True)
df['Kp_clean'] = pd.to_numeric(df['Kp_clean'], errors='coerce')
kp_values = df['Kp_clean'].dropna().values


def mc_dropout_kp_simulation(kp_values, T=100, dropout_rate=0.1):
    kp_values = np.array(kp_values)
    preds = []

    for _ in range(T):
        noise = np.random.normal(0, dropout_rate * kp_values)
        preds.append(kp_values + noise)

    preds = np.array(preds)
    median = np.median(preds, axis=0)
    lower = np.percentile(preds, 10, axis=0)
    upper = np.percentile(preds, 90, axis=0)

    return median, lower, upper

median, lower, upper = mc_dropout_kp_simulation(kp_values, T=100, dropout_rate=0.1)


print("Median Kp Forecast:", np.round(median, 2))
print("10th Percentile (Lower Bound):", np.round(lower, 2))
print("90th Percentile (Upper Bound):", np.round(upper, 2))
