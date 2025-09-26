import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import os

def trainmodel(datadir, modelpath):
    """
    loads sequenced data, defines a deeper lstm model, and trains it
    intelligently with early stopping and a learning rate scheduler.
    """
    print("loading sequence data...")
    xpath = f"{datadir}/x_sequences.npy"
    ypath = f"{datadir}/y_sequences.npy"
    x = np.load(xpath)
    y = np.load(ypath)
    print(f"data loaded. x_shape: {x.shape}, y_shape: {y.shape}")

    trainsize = int(len(x) * 0.8)
    xtrain, xval = x[:trainsize], x[trainsize:]
    ytrain, yval = y[:trainsize], y[trainsize:]
    print(f"train/validation split: {len(xtrain)} / {len(xval)}")

    model = Sequential([
        LSTM(units=100, return_sequences=True, input_shape=(x.shape[1], x.shape[2])),
        Dropout(0.3),
        LSTM(units=100, return_sequences=True),
        Dropout(0.3),
        LSTM(units=50, return_sequences=False),
        Dropout(0.3),
        Dense(units=25),
        Dense(units=1) 
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    model.summary()
    print("upgraded model compiled.")

    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.00001)

    print("starting upgraded model training (will use gpu if available)...")
    history = model.fit(
        xtrain, ytrain,
        epochs=50, 
        batch_size=128, 
        validation_data=(xval, yval),
        callbacks=[early_stopping, reduce_lr],
        verbose=1
    )

    model.save(modelpath)
    print(f"training complete. best model saved to: {modelpath}")

if __name__ == "__main__":
    datadir = 'lstm_data'
    modeldir = 'model'
    modelpath = os.path.join(modeldir, 'kp_forecaster_v2.keras') 

    if not os.path.exists(modeldir):
        os.makedirs(modeldir)

    trainmodel(datadir, modelpath)