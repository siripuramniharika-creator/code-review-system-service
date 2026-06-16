import numpy as np
from app.ai.embedding import get_processed_embedding


def cosine_similarity(vec1, vec2):
    """
    Basic similarity function (used later for comparisons)
    """
    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )


def quality_score(code: str):
    """
    Estimate code quality based on embedding characteristics
    """

    emb = get_processed_embedding(code)

    # heuristic scoring (will later be replaced with ML model)
    variance = np.var(emb)
    length_factor = min(len(code) / 500, 1)

    score = 70 + (variance * 100) - (length_factor * 10)

    return int(max(min(score, 100), 0))


def security_score(code: str):
    """
    Detect security risk patterns + embedding signals
    """

    emb = get_processed_embedding(code)

    risk_keywords = [
        "eval", "exec", "password", "token",
        "SELECT *", "input(", "system("
    ]

    risk_count = sum(1 for kw in risk_keywords if kw in code.lower())

    score = 100 - (risk_count * 15) - (np.mean(emb) * 10)

    return int(max(min(score, 100), 0))


def performance_score(code: str):
    """
    Estimate performance issues
    """

    emb = get_processed_embedding(code)

    loops = code.count("for ") + code.count("while ")
    nested_penalty = code.count("for ") * code.count("for ")

    score = 100 - (loops * 5) - (nested_penalty * 2)

    # stabilize using embedding signal
    score -= abs(np.mean(emb)) * 5

    return int(max(min(score, 100), 0))


def analyze_code(code: str):
    """
    MAIN AI FUNCTION → used by FastAPI endpoint
    """

    return {
        "quality_score": quality_score(code),
        "security_score": security_score(code),
        "performance_score": performance_score(code),
    }