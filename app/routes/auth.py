from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.utils.helpers import normalize
from app.utils.jwt_handler import create_access_token
from jose import jwt, JWTError
from app.utils.password_utils import hash_password, verify_password

from app.models.user_models import (
    SignupRequest,
    LoginRequest,
    ForgotPasswordRequest
)

from app.database.db import get_db
from app.database.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup")
async def signup(
    user: SignupRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = User(
        fullname=user.fullname,
        email=user.email,
        password=hash_password(user.password),
        contact=user.contact,
        security_question=user.security_question,
        security_answer=user.security_answer.lower().strip()
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
async def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
    token = create_access_token({
        "email": db_user.email,
        "fullname": db_user.fullname
    })

    return {
        "message": "Login successful",
        "token": token
    }


@router.post("/forgot-password")
async def forgot_password(
    user: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email.lower().strip()
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if (
        db_user.security_question != user.security_question
        or
        normalize(db_user.security_answer ) != normalize(user.security_answer)
    ):
       raise HTTPException(
            status_code=400,
            detail="Security question or answer is incorrect"
        )

    db_user.password = hash_password(user.new_password)

    db.commit()

    return {
        "message": "Password updated successfully"
    }
@router.get("/user/{email}")
async def get_user(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "fullname": user.fullname,
        "email": user.email
    }
@router.post("/refresh")
def refresh_token(data: dict):
    try:
        payload = jwt.decode(
            data["refresh_token"],
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        new_access_token = create_access_token({
            "email": payload["email"]
        })

        return {
            "access_token": new_access_token
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")