import json
from app.database.db import SessionLocal
from app.models.review import Review
from app.services.ollama_service import run_ollama_analysis
from app.services.parser import safe_parse


def process_review(review_id: int, code: str, language: str):

    db = SessionLocal()

    try:
        print("AI started:", review_id)

        raw_output = run_ollama_analysis(code, language)
        print("RAW OLLAMA OUTPUT:\n", raw_output)

        result = safe_parse(raw_output)

        print("PARSED RESULT:")
        print(result)

        # fallback
        if not result:
            result = {
                "quality_score": 70,
                "security_score": 70,
                "performance_score": 70,
                "issues": [],
                "suggestions": [],
                "improved_code": f"# Refactored version\n{code}"
            }

        review = db.query(Review).get(review_id)

        review.quality_score = result.get("quality_score", 0)
        review.security_score = result.get("security_score", 0)
        review.performance_score = result.get("performance_score", 0)

        review.issues = json.dumps(result.get("issues", []))
        review.suggestions = json.dumps(result.get("suggestions", []))
        review.improved_code = result.get("improved_code", "")

        review.status = "COMPLETED"
        print("Saving improved_code:", review.improved_code)
        db.commit()

        print("AI completed:", review_id)

    except Exception as e:
        print("AI error:", e)

        review = db.query(Review).get(review_id)
        review.status = "FAILED"
        db.commit()

    finally:
        db.close()