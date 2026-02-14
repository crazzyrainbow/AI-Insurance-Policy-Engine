from pydantic import BaseModel


class ClaimInput(BaseModel):
    claim_amount: float
    prior_claims: int
