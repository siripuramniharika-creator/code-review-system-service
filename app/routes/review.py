from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.review import ReviewRequest
from app.services.review_service import create_review
from app.database.db import get_db
from app.models.review import Review

router = APIRouter()


@router.post("/review")
def review_code(payload: ReviewRequest):
    return create_review(
        language=payload.language,
        code=payload.code
    )


@router.get("/review/{review_id}")
def get_review(review_id: int, db: Session = Depends(get_db)):

    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return review