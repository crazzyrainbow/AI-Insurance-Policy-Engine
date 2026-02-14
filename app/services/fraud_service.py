from app.ml.fraud_model import predict


def score_claim(claim_amount: float, prior_claims: int):
    prob = predict(claim_amount, prior_claims)

    return {
        "fraud_probability": prob,
        "risk_level": (
            "High" if prob > 0.7
            else "Medium" if prob > 0.4
            else "Low"
        )
    }
