from sqlalchemy.orm import Session, joinedload

from app.models.interview import Interview
from app.models.question import Question


class InterviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, user_id: int, domain: str, difficulty: str, total_questions: int
    ) -> Interview:
        interview = Interview(
            user_id=user_id,
            domain=domain,
            difficulty=difficulty,
            total_questions=total_questions,
        )
        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)
        return interview

    def add_questions(self, interview_id: int, questions_data: list[dict]) -> list[Question]:
        import json
        records = [
            Question(
                interview_id=interview_id,
                question_text=q["question_text"],
                ideal_answer=q.get("ideal_answer"),
                keywords=json.dumps(q.get("keywords", [])) if isinstance(q.get("keywords"), list) else q.get("keywords")
            )
            for q in questions_data
        ]
        self.db.add_all(records)
        self.db.commit()
        for record in records:
            self.db.refresh(record)
        return records

    def get_for_user(self, interview_id: int, user_id: int) -> Interview | None:
        return (
            self.db.query(Interview)
            .options(joinedload(Interview.questions))
            .filter(Interview.id == interview_id, Interview.user_id == user_id)
            .first()
        )

    def get_question(self, interview_id: int, question_id: int) -> Question | None:
        return (
            self.db.query(Question)
            .filter(Question.interview_id == interview_id, Question.id == question_id)
            .first()
        )

    def save_answer(
        self,
        question: Question,
        answer: str,
        feedback: str | None = None,
        score: float | None = None,
        feedback_critique: str | None = None,
        feedback_improvement: str | None = None,
    ) -> Question:
        question.user_answer = answer
        question.feedback = feedback
        question.score = score
        question.feedback_critique = feedback_critique
        question.feedback_improvement = feedback_improvement
        self.db.commit()
        self.db.refresh(question)
        return question

    def update_overall_score(self, interview: Interview, score: float) -> Interview:
        interview.overall_score = score
        self.db.commit()
        self.db.refresh(interview)
        return interview
