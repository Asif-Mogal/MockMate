import json

from fastapi import HTTPException, status

from app.models.interview import Interview
from app.repositories.interview_repository import InterviewRepository
from app.schemas.interview import FinalReport, InterviewCreate
from app.services.gemini_service import GeminiService

VALID_DOMAINS = {"Java", "Spring Boot", "React", "SQL", "DSA", "HR"}
VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}
VALID_COUNTS = {5, 10, 15}


class InterviewService:
    def __init__(self, interviews: InterviewRepository, gemini: GeminiService):
        self.interviews = interviews
        self.gemini = gemini

    def create_interview(self, user_id: int, payload: InterviewCreate) -> Interview:
        self._validate_setup(payload)
        interview = self.interviews.create(
            user_id=user_id,
            domain=payload.domain,
            difficulty=payload.difficulty,
            total_questions=payload.total_questions,
        )
        questions = self.gemini.generate_questions(
            payload.domain, payload.difficulty, payload.total_questions
        )
        self.interviews.add_questions(interview.id, questions)
        return self.interviews.get_for_user(interview.id, user_id)

    def get_interview(self, interview_id: int, user_id: int) -> Interview:
        interview = self.interviews.get_for_user(interview_id, user_id)
        if not interview:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.")
        return interview

    def answer_question(
        self, interview_id: int, question_id: int, user_id: int, answer: str
    ) -> dict:
        interview = self.get_interview(interview_id, user_id)
        question = self.interviews.get_question(interview.id, question_id)
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")
        self.interviews.save_answer(
            question=question,
            answer=answer,
            feedback=None,
            score=None,
        )
        return {"question_id": question.id, "saved": True}

    def final_report(self, interview_id: int, user_id: int) -> FinalReport:
        interview = self.get_interview(interview_id, user_id)
        
        # IF interview.overall_score IS NOT NULL:
        # Return cached report from database.
        # Do not call Gemini.
        if interview.overall_score is not None:
            try:
                strengths = json.loads(interview.strengths) if interview.strengths else []
            except Exception:
                strengths = []
            try:
                weaknesses = json.loads(interview.weaknesses) if interview.weaknesses else []
            except Exception:
                weaknesses = []
            try:
                recommendations = json.loads(interview.recommendations) if interview.recommendations else []
            except Exception:
                recommendations = []
                
            return FinalReport(
                interview_id=interview.id,
                overall_score=interview.overall_score,
                domain_score=interview.overall_score,
                strengths=strengths,
                weaknesses=weaknesses,
                recommendations=recommendations,
                placement_readiness=self._readiness(interview.overall_score),
                questions=interview.questions,
            )
            
        # ELSE:
        # Collect all questions and answers.
        # Send entire interview to Gemini in a single prompt.
        # Request JSON output.
        evaluation = self.gemini.evaluate_interview(
            interview.domain, interview.difficulty, interview.questions
        )
        
        # Persist score and feedback for every question.
        scores_by_id = {item["question_id"]: item for item in evaluation["question_scores"]}
        
        for q in interview.questions:
            eval_item = scores_by_id.get(q.id)
            score = eval_item["score"] if eval_item else 0.0
            feedback = eval_item["feedback"] if eval_item else "No feedback provided."
            critique = eval_item.get("feedback_critique", "No critique provided.") if eval_item else "No critique provided."
            improvement = eval_item.get("feedback_improvement", "No improvement details provided.") if eval_item else "No improvement details provided."
            self.interviews.save_answer(
                question=q,
                answer=q.user_answer or "",
                feedback=feedback,
                score=score,
                feedback_critique=critique,
                feedback_improvement=improvement
            )
            
        overall = evaluation["overall_score"]
        interview.strengths = json.dumps(evaluation["strengths"])
        interview.weaknesses = json.dumps(evaluation["weaknesses"])
        interview.recommendations = json.dumps(evaluation["recommendations"])
        self.interviews.update_overall_score(interview, overall)
        
        return FinalReport(
            interview_id=interview.id,
            overall_score=overall,
            domain_score=overall,
            strengths=evaluation["strengths"],
            weaknesses=evaluation["weaknesses"],
            recommendations=evaluation["recommendations"],
            placement_readiness=self._readiness(overall),
            questions=interview.questions,
        )

    def _validate_setup(self, payload: InterviewCreate) -> None:
        if payload.domain not in VALID_DOMAINS:
            raise HTTPException(status_code=422, detail="Invalid domain.")
        if payload.difficulty not in VALID_DIFFICULTIES:
            raise HTTPException(status_code=422, detail="Invalid difficulty.")
        if payload.total_questions not in VALID_COUNTS:
            raise HTTPException(status_code=422, detail="Invalid question count.")

    def _readiness(self, score: float) -> str:
        if score >= 85:
            return "Placement Ready"
        if score >= 70:
            return "Almost Ready"
        if score >= 50:
            return "Needs Focused Practice"
        return "Needs Foundation Building"
