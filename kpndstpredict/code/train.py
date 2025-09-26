import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense


data = np.load('../data/processed_data.npz')
X = data['X']
y = data['y']


model = Sequential([

    LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
    Dropout(0.2),

    LSTM(units=50),
    Dropout(0.2),

    Dense(units=24) 
])

model.compile(optimizer='adam', loss='mean_squared_error')
model.summary()


history = model.fit(
    X, y,
    epochs=20,
    batch_size=64,
    validation_split=0.2
)

model.save('kp_forecasting_model_24hr.h5')  