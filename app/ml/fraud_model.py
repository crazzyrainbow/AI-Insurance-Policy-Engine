import numpy as np
from sklearn.linear_model import LogisticRegression

# Synthetic training data
X = np.array([
    [10000, 0],
    [5000, 1],
    [20000, 0],
    [15000, 2],
    [8000, 3],
])

y = np.array([0, 1, 0, 1, 1])

model = LogisticRegression()
model.fit(X, y)


def predict(claim_amount: float, prior_claims: int):
    features = np.array([[claim_amount, prior_claims]])
    probability = model.predict_proba(features)[0][1]
    return float(probability)
