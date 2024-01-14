import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report,ConfusionMatrixDisplay

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Custom function for plotting each metric
def plot_history(history, figsize=(6,12), marker='o'):

    # Get list of metrics from history
    metrics = [c for c in history.history if not c.startswith('val_')]

    ## Separate row for each metric
    fig, axes = plt.subplots(nrows=len(metrics),figsize=figsize)

    # For each metric
    for i, metric_name in enumerate(metrics):

        # Get the axis for the current metric
        ax = axes[i]

        # Get metric from history.history
        metric_values = history.history[metric_name]
        # Get epochs from history
        epochs = history.epoch

        # Plot the training metric
        ax.plot(epochs, metric_values, label=metric_name, marker=marker)

        ## Check if val_{metric} exists. if so, plot:
        val_metric_name = f"val_{metric_name}"
        if val_metric_name in history.history:
            # Get validation values and plot
            metric_values = history.history[val_metric_name]
            ax.plot(epochs,metric_values,label=val_metric_name, marker=marker)

        # Final subplot adjustments
        ax.legend()
        ax.set_title(metric_name)
    fig.tight_layout()

    return fig, axes


def neural_networks_builder(preprocessor, X_train, y_train, X_test, y_test,epochs=10,
                            validation_split=.2, layers=[{'n': 10, 'activation': 'relu'}, {'n': 3, 'activation': 'sigmoid'}]):

  le = LabelEncoder()
  y_train_enc = le.fit_transform(y_train)
  y_test_enc = le.transform(y_test)

  X_train_tf = preprocessor.fit_transform(X_train)
  X_test_tf = preprocessor.transform(X_test)

  input_shape = X_train_tf.shape[1]


  # Sequential model
  model = Sequential()

  # First hidden layer
  model.add(Dense(layers[0]['n'], # How many neurons you have in your first hidden layer
                  input_dim = input_shape, # What is the shape of your input features (number of columns)
                  activation = layers[0]['activation'])) # What activation function are you using?

  for layer in layers[1:]:
    # Second hidden layer
    model.add(Dense(layer['n'], # How many neurons you have in your second hidden layer
                    activation =layer['activation'])) # What activation function are you using?


  ### Metrics are specified during the.compile step
  # Step 2: Compile
  model.compile(loss = 'bce', optimizer = 'adam'
                , metrics=['accuracy',
                          tf.keras.metrics.Recall(name='recall'),
                          tf.keras.metrics.Precision(name='precision'),
                          ])
  model.summary()


  # =======================================================plot_history start

  # =======================================================plot_history end


  # Step 3: Fit our model
  history = model.fit(X_train_tf, y_train_enc,
                      validation_split=validation_split,
                      epochs=epochs)

  plot_history(history);

  # Evaluate neural network with builtin evaluation
  result = model.evaluate(X_test_tf, y_test_enc,return_dict=True)

  # make predictions
  y_pred_test = model.predict(X_test_tf)

  # round the predictions
  y_pred_test = np.round(y_pred_test)


  print(classification_report(y_test_enc, y_pred_test))

  ConfusionMatrixDisplay.from_predictions(y_test_enc, y_pred_test, cmap='Blues',
                                        normalize='true');


  return model
