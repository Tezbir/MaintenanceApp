from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from .sesh import get_db
from .model import User
from .schemas import UserCreate, UserOut, TokenOut
from .auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserOut)
def signup(body: UserCreate, db: Session = Depends(get_db)):
    exists = db.execute(select(User).where(User.user_email == body.user_email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        user_name=body.user_name,
        user_email=body.user_email,
        user_password=hash_password(body.user_password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenOut)
def login(body: UserCreate, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.user_email == body.user_email)).scalar_one_or_none()
    if not user or not verify_password(body.user_password, user.user_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(user.user_id))
    return TokenOut(access_token=token)
