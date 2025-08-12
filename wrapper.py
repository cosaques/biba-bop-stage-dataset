# 1. Wrapper
class MultiTPOTWrapper:
    def __init__(self, models):
        self.models = models

    def fit(self, X, y=None):
        return self

    def predict(self, X):
        import numpy as np
        predictions = [m.predict(X) for m in self.models]
        return np.vstack(predictions).T