from app.database.db import SessionLocal
from app.models.review import Review
from app.services.phi3_service import run_phi3_analysis
import json
import re


def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {}


def process_review(review_id: int, code: str, language: str):

    db = SessionLocal()

    try:
        print("AI started:", review_id)

        raw_output = run_phi3_analysis(code, language)
        result = extract_json(raw_output)

        review = db.query(Review).get(review_id)

        review.quality_score = result.get("quality_score", 0)
        review.security_score = result.get("security_score", 0)
        review.performance_score = result.get("performance_score", 0)

        review.issues = json.dumps(result.get("issues", []))
        review.suggestions = json.dumps(result.get("suggestions", []))
        review.improved_code = result.get("improved_code", "")

        review.status = "COMPLETED"

        db.commit()

        print("AI completed:", review_id)

    except Exception as e:
        print("AI error:", e)
        review = db.query(Review).get(review_id)
        review.status = "FAILED"
        db.commit()

    finally:
        db.close()