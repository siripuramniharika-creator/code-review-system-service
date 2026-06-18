from fastapi import APIRouter, BackgroundTasks
from app.schemas.review import ReviewRequest
from app.models.review import Review
from app.database.db import SessionLocal
from app.services.ai_worker import process_review

router = APIRouter()


@router.post("/review")
def create_review(payload: ReviewRequest, background_tasks: BackgroundTasks):

    db = SessionLocal()

    review = Review(
        code=payload.code,
        language=payload.language,
        status="PROCESSING"
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    # run AI in background
    background_tasks.add_task(
        process_review,
        review.id,
        payload.code,
        payload.language
    )

    return {"review_id": review.id}


@router.get("/review/{review_id}")
def get_review(review_id: int):

    db = SessionLocal()
    review = db.query(Review).get(review_id)
    print(review.improved_code)
    print(review.quality_score)

    return {
        "id": review.id,
        "code": review.code,
        "language": review.language,
        "status": review.status,
        "quality_score": review.quality_score,
        "security_score": review.security_score,
        "performance_score": review.performance_score,
        "issues": review.issues,
        "suggestions": review.suggestions,
        "improved_code": review.improved_code,
        "created_at": review.created_at
    }