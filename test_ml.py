import pytest
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from ml.model import train_model, inference, compute_model_metrics


def test_train_model():
    """
    Test that train_model returns a RandomForestClassifier instance.
    """
    X_train = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y_train = np.array([0, 1, 0, 1])
    model = train_model(X_train, y_train)
    assert isinstance(model, RandomForestClassifier)

def test_inference():
    """
    Test that inference returns predictions with the same number of rows as the input.
    """
    X_train = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y_train = np.array([0, 1, 0, 1])
    model = train_model(X_train, y_train)
    preds = inference(model, X_train)
    assert len(preds) == len(y_train)


def test_compute_model_metrics():
    """
    Test that compute_model_metrics returns correct precision, recall, and F1
    on a known, hand-calculated example.
    """
    y_true = np.array([1, 1, 0, 0])
    y_preds = np.array([1, 0, 0, 0])
    precision, recall, fbeta = compute_model_metrics(y_true, y_preds)
    assert precision == 1.0
    assert recall == 0.5
    assert fbeta == pytest.approx(0.6667, abs=0.001)
