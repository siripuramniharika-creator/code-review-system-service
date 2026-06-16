from app.ai.codebert_service import get_code_embedding

code = """
def add(a, b):
    return a + b
"""

vec = get_code_embedding(code)

print("Vector size:", len(vec))
print("First 10 values:", vec[:10])