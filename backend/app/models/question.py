from sqlalchemy import Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    interview_id: Mapped[int] = mapped_column(ForeignKey("interviews.id"), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    user_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    ideal_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    keywords: Mapped[str | None] = mapped_column(Text, nullable=True)
    feedback_critique: Mapped[str | None] = mapped_column(Text, nullable=True)
    feedback_improvement: Mapped[str | None] = mapped_column(Text, nullable=True)

    interview = relationship("Interview", back_populates="questions")
