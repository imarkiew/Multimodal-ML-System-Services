from joblib import load
import numpy as np


class Model:
    def __init__(self, model_file_path, means, stds):
        self.model = load(model_file_path)
        self.means = means
        self.stds = stds

    def predict_proba(self, features):
        return self.model.predict_proba(self.scale_features(features))

    def scale_features(self, features):
        return np.array([self.standard_scaler(value, self.means[key], self.stds[key]) if key in self.means else value
                        for key, value in features.items()]).reshape(1, -1)

    def standard_scaler(self, value, mean, std):
        return (value - mean) / std
