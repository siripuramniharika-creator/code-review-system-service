import numpy as np
from app.ai.codebert_service import get_code_embedding


def normalize_vector(vec):
    """
    Normalize embedding vector for consistent scoring
    """
    vec = np.array(vec)
    norm = np.linalg.norm(vec)

    if norm == 0:
        return vec

    return vec / norm


def get_processed_embedding(code: str):
    """
    Main function used by scoring system
    """

    embedding = get_code_embedding(code)
    normalized = normalize_vector(embedding)

    return normalized