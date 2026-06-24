from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.repositories.interview_repository import InterviewRepository
from app.schemas.interview import (
    AnswerRequest,
    AnswerResponse,
    FinalReport,
    InterviewCreate,
    InterviewResponse,
)
from app.services.gemini_service import GeminiService
from app.services.interview_service import InterviewService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> InterviewService:
    return InterviewService(InterviewRepository(db), GeminiService())


@router.post("", response_model=InterviewResponse, status_code=201)
def create_interview(
    payload: InterviewCreate,
    current_user: User = Depends(get_current_user),
    service: InterviewService = Depends(get_service),
):
    return service.create_interview(current_user.id, payload)


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    service: InterviewService = Depends(get_service),
):
    return service.get_interview(interview_id, current_user.id)


@router.post("/{interview_id}/questions/{question_id}/answer", response_model=AnswerResponse)
def answer_question(
    interview_id: int,
    question_id: int,
    payload: AnswerRequest,
    current_user: User = Depends(get_current_user),
    service: InterviewService = Depends(get_service),
):
    return service.answer_question(interview_id, question_id, current_user.id, payload.answer)


@router.get("/{interview_id}/report", response_model=FinalReport)
def final_report(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    service: InterviewService = Depends(get_service),
):
    return service.final_report(interview_id, current_user.id)
