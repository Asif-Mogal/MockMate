from pydantic import BaseModel, Field


class InterviewCreate(BaseModel):
    domain: str
    difficulty: str
    total_questions: int = Field(ge=5, le=15)


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    user_answer: str | None = None
    feedback: str | None = None
    score: float | None = None
    ideal_answer: str | None = None
    feedback_critique: str | None = None
    feedback_improvement: str | None = None

    model_config = {"from_attributes": True}


class InterviewResponse(BaseModel):
    id: int
    domain: str
    difficulty: str
    total_questions: int
    overall_score: float | None = None
    questions: list[QuestionResponse]

    model_config = {"from_attributes": True}


class AnswerRequest(BaseModel):
    answer: str = Field(min_length=1)


class AnswerEvaluation(BaseModel):
    score: float
    strengths: list[str]
    weaknesses: list[str]
    ideal_answer: str


class AnswerResponse(BaseModel):
    question_id: int
    saved: bool


class FinalReport(BaseModel):
    interview_id: int
    overall_score: float
    domain_score: float
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    placement_readiness: str
    questions: list[QuestionResponse]
