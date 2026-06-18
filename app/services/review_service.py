from app.database.db import SessionLocal
from app.models.review import Review
import threading
from app.services.ai_worker import process_review 

def create_review(language: str, code: str):

    db = SessionLocal()

    # Step 1: Save request
    review = Review(
        language=language,
        code=code,
        status="PROCESSING"
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    review_id = review.id

    db.close()

    # Step 2: Start background AI process (IMPORTANT)
    threading.Thread(
        target=process_review,
        args=(review_id, code, language),
        daemon=True
    ).start()

    # Step 3: Return immediately
    return {
        "review_id": review_id,
        "status": "PROCESSING",
        "message": "Analysis started"
    }