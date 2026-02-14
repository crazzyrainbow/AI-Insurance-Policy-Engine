from fastapi import APIRouter
from app.schemas.claim import ClaimInput
from app.services.fraud_service import score_claim

router = APIRouter(prefix="/claims", tags=["Claims"])


@router.post("/fraud-score")
def fraud_score(request: ClaimInput):
    return score_claim(
        request.claim_amount,
        request.prior_claims
    )
