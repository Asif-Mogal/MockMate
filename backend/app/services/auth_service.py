from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users

    def register(self, payload: RegisterRequest):
        existing = self.users.get_by_email(payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )
        return self.users.create(
            name=payload.name,
            email=payload.email,
            password_hash=hash_password(payload.password),
        )

    def login(self, payload: LoginRequest) -> TokenResponse:
        user = self.users.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )
        return TokenResponse(access_token=create_access_token(str(user.id)))
