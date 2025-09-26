import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib


data_file = '../data/omni_data.txt'

def find_data_start(filename):
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if line.strip() and line.strip().split()[0].isdigit():
                return i
    return 0

skip_rows = find_data_start(data_file)
print(f"Detected {skip_rows} header lines to skip.")

COLUMN_NAMES = [
    'Year', 'Day', 'Hour', 'ID_IMF', 'ID_SW_Plasma', 'B_Magnitude', 'Bx_GSE_GSM',
    'By_GSM', 'Bz_GSM', 'Proton_Temperature', 'Proton_Density', 'Flow_Speed',
    'Flow_Pressure', 'Kp_Index_10', 'Dst_Index'
]

df = pd.read_csv(
    data_file,
    sep='\s+',
    header=None,
    names=COLUMN_NAMES,
    skiprows=skip_rows
)

df['Timestamp'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Day'].astype(str) + '-' + df['Hour'].astype(str), format='%Y-%j-%H')
df.set_index('Timestamp', inplace=True)

df.drop(['Year', 'Day', 'Hour', 'ID_IMF', 'ID_SW_Plasma'], axis=1, inplace=True)

df.replace({9999.9: np.nan, 999.99: np.nan, 999999: np.nan, 99.99: np.nan}, np.nan, inplace=True)

df.fillna(method='ffill', inplace=True)
df.fillna(method='bfill', inplace=True)

features = df.drop('Kp_Index_10', axis=1)
target = df[['Kp_Index_10']]

scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)

joblib.dump(scaler, 'feature_scaler.pkl')

LOOKBACK_WINDOW = 24
FORECAST_HORIZON = 24  
X, y = [], []

for i in range(len(features_scaled) - LOOKBACK_WINDOW - FORECAST_HORIZON):
    X.append(features_scaled[i:i + LOOKBACK_WINDOW])
    y.append(target.iloc[i + LOOKBACK_WINDOW : i + LOOKBACK_WINDOW + FORECAST_HORIZON])

X, y = np.array(X), np.array(y)

y = y.reshape(y.shape[0], y.shape[1])

np.savez('processed_data.npz', X=X, y=y)