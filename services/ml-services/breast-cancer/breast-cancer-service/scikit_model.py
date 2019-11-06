from joblib import load
import numpy as np


class Model:
    """Class representing the wrapper for the loaded model

    """

    def __init__(self, model_file_path, means, stds):
        """
        :param model_file_path: file path to loaded model
        :param means: means for features normalization
        :param stds: standard deviations for features normalization
        """
        self.model = load(model_file_path)
        self.means = means
        self.stds = stds

    def predict_proba(self, features):
        """Predict probability distribution of classes

        :param features: json with features which represent one record
        :return: json with probability distribution of classes for given record
        """
        return self.model.predict_proba(self.scale_features(features))

    def scale_features(self, features):
        """Scale features of record using normalization

        :param features: json with features to scale
        :return: numpy array with scaled features
        """
        return np.array([self.standard_scaler(value, self.means[key], self.stds[key]) if key in self.means else value
                        for key, value in features.items()]).reshape(1, -1)

    def standard_scaler(self, value, mean, std):
        """ Scale value

        :param value: value to scale
        :param mean: mean of the population
        :param std: standard deviation of the population
        :return: scaled value
        """
        return (value - mean) / std
