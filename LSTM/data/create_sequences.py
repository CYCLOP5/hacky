import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

def createseqs(inputpath, outdir):

    print(f"loading: {inputpath}")
    df = pd.read_parquet(inputpath)

    df['kptarget'] = df['kp_index'].shift(-24)
    df.dropna(inplace=True)
    print("target created")

    target = df['kptarget']
    features = df.drop('kptarget', axis=1)

    fscaler = MinMaxScaler(feature_range=(0, 1))
    scaledfeatures = fscaler.fit_transform(features)

    fscalerpath = f"{outdir}/featurescaler.pkl"
    joblib.dump(fscaler, fscalerpath)
    print(f"feature scaler saved: {fscalerpath}")

    tscaler = MinMaxScaler(feature_range=(0, 1))
    scaledtarget = tscaler.fit_transform(target.values.reshape(-1, 1))
    tscalerpath = f"{outdir}/targetscaler.pkl"
    joblib.dump(tscaler, tscalerpath)
    print(f"target scaler saved: {tscalerpath}")

    lookback = 72
    x, y = [], []

    print(f"creating sequences, lookback: {lookback}")
    for i in range(len(scaledfeatures) - lookback):
        seq = scaledfeatures[i:(i + lookback)]
        lbl = scaledtarget[i + lookback]
        x.append(seq)
        y.append(lbl)

    x = np.array(x)
    y = np.array(y)

    print(f"sequences created: {x.shape[0]}")
    print(f"x shape: {x.shape}")
    print(f"y shape: {y.shape}")

    xpath = f"{outdir}/x_sequences.npy"
    ypath = f"{outdir}/y_sequences.npy"
    np.save(xpath, x)
    np.save(ypath, y)

    print(f"x saved: {xpath}")
    print(f"y saved: {ypath}")
    print("done.")

if __name__ == "__main__":
    inputfile = 'processed_borealis_data.parquet'
    outdir = 'lstm_data'

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    createseqs(inputfile, outdir)