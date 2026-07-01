from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import CurrentUser, TokenResponse, UserCreate, UserLogin, UserResponse
from ..services.auth_service import authenticate_user, create_access_token, create_user, get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def _user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        is_active=user.is_active,
        created_at=user.created_at.isoformat() if user.created_at else None,
    )


@router.post("/register", response_model=TokenResponse)
def register(request: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, request.email, request.display_name, request.password)
    return TokenResponse(access_token=create_access_token(user), user=_user_response(user))


@router.post("/login", response_model=TokenResponse)
def login(request: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(user), user=_user_response(user))


@router.get("/me", response_model=CurrentUser)
def me(current_user: User = Depends(get_current_user)):
    return CurrentUser(**_user_response(current_user).model_dump())
