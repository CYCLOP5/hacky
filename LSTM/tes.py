import numpy as np
import tensorflow as tf
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

def evaluatemodel(datadir, modelpath):
    """
    loads the trained model and validation data to evaluate performance.
    """
    print("loading model, data, and scalers...")
    model = tf.keras.models.load_model(modelpath)
    targetscaler = joblib.load(f"{datadir}/targetscaler.pkl")

    x = np.load(f"{datadir}/x_sequences.npy")
    y = np.load(f"{datadir}/y_sequences.npy")

    trainsize = int(len(x) * 0.8)
    xval = x[trainsize:]
    yval = y[trainsize:]
    print(f"validation set loaded. shape: {xval.shape}")

    print("making predictions on validation data...")
    predicted_scaled = model.predict(xval)

    predicted_actual = targetscaler.inverse_transform(predicted_scaled)
    true_actual = targetscaler.inverse_transform(yval)
    print("predictions and true values have been un-scaled.")

    rmse = np.sqrt(mean_squared_error(true_actual, predicted_actual))
    mae = mean_absolute_error(true_actual, predicted_actual)
    print("\n--- model performance ---")
    print(f"root mean squared error (rmse): {rmse:.4f}")
    print(f"mean absolute error (mae): {mae:.4f}")
    print("-------------------------")
    print("note: lower values are better. mae is the average error in the original kp units.")

    print("generating forecast plot...")
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(15, 7))

    plot_slice = slice(500, 1000)
    ax.plot(true_actual[plot_slice], label='actual kp index', color='royalblue', linewidth=2)
    ax.plot(predicted_actual[plot_slice], label='predicted kp index', color='darkorange', linestyle='--', linewidth=2)

    ax.set_title('kp index forecast vs. actual values (validation data sample)', fontsize=16)
    ax.set_xlabel('time (hours into validation set)', fontsize=12)
    ax.set_ylabel('kp index', fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.savefig('forecast_evaluation_plot.png')
    print("plot saved to forecast_evaluation_plot.png. showing plot now.")
    plt.show()

if __name__ == "__main__":
    datadir = 'lstm_data'
    modelpath = 'model/kp_forecaster.keras'
    evaluatemodel(datadir, modelpath)
