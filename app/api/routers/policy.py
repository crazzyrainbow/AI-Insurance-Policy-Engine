from fastapi import APIRouter
from app.schemas.policy import QuestionRequest
from app.services.rag_service import answer_question

router = APIRouter(prefix="/policy", tags=["Policy"])


@router.post("/qa")
def policy_qa(request: QuestionRequest):
    return answer_question(
        question=request.question,
        session_id=request.session_id
    )
