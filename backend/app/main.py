from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text

from app import models  # noqa: F401
from app.api.routes import auth, interviews
from app.core.config import settings
from app.database import Base, engine

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE interviews ADD COLUMN IF NOT EXISTS strengths TEXT;"))
        conn.execute(text("ALTER TABLE interviews ADD COLUMN IF NOT EXISTS weaknesses TEXT;"))
        conn.execute(text("ALTER TABLE interviews ADD COLUMN IF NOT EXISTS recommendations TEXT;"))
        
        conn.execute(text("ALTER TABLE questions ADD COLUMN IF NOT EXISTS ideal_answer TEXT;"))
        conn.execute(text("ALTER TABLE questions ADD COLUMN IF NOT EXISTS keywords TEXT;"))
        conn.execute(text("ALTER TABLE questions ADD COLUMN IF NOT EXISTS feedback_critique TEXT;"))
        conn.execute(text("ALTER TABLE questions ADD COLUMN IF NOT EXISTS feedback_improvement TEXT;"))
        conn.commit()
    except Exception as e:
        print(f"Startup migration failed: {e}")

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(interviews.router, prefix="/api/interviews", tags=["Interviews"])


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": settings.app_name}
