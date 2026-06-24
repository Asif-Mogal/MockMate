from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    domain: Mapped[str] = mapped_column(String(80), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(40), nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    weaknesses: Mapped[str | None] = mapped_column(Text, nullable=True)
    recommendations: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="interviews")
    questions = relationship(
        "Question", back_populates="interview", cascade="all, delete-orphan"
    )
