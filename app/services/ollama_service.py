import requests


def run_ollama_analysis(code: str, language: str):

    prompt = f"""
You are an expert senior software engineer performing strict code review.

You MUST return ONLY valid JSON.
Do NOT include:
- explanations
- markdown
- ``` code blocks
- extra text

-------------------------------------------------
STRICT OUTPUT RULES (VERY IMPORTANT)
-------------------------------------------------

1. OUTPUT MUST BE VALID JSON ONLY

2. SCORES RULE:
- quality_score: integer between 1 and 100
- security_score: integer between 1 and 100
- performance_score: integer between 1 and 100

3. ISSUES FORMAT:
MUST be an array of objects:

[
  {{
    "title": string,
    "severity": "Low" | "Medium" | "High",
    "description": string
  }}
]

4. SUGGESTIONS FORMAT:
MUST be an array of objects:

[
  {{
    "title": string,
    "description": string
  }}
]

5. IMPROVED CODE RULES (MOST IMPORTANT):

- MUST be valid Python code
- MUST preserve original logic
- MUST be readable and realistic
- MUST NOT contain fake constructs like:
  [1,1][0] + [1,1][1]
  unnatural tricks
- MUST use proper Python syntax
- MUST NOT include markdown or backticks
- MUST escape new lines as \\n

Example:
"def test():\\n    return 2 + 2"

If fixing eval():
 BAD: weird expressions or lists
✔ GOOD: return 2 + 2

6. IF NO ISSUES → return []
7. IF NO SUGGESTIONS → return []

-------------------------------------------------
CODE TO ANALYZE:
-------------------------------------------------

{code}

LANGUAGE:
{language}

-------------------------------------------------
RETURN EXACT JSON FORMAT:
-------------------------------------------------

{{
  "quality_score": 85,
  "security_score": 85,
  "performance_score": 85,
  "issues": [],
  "suggestions": [],
  "improved_code": "string"
}}

REMEMBER:
- OUTPUT MUST BE PURE JSON
- NO EXTRA TEXT
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5-coder:3b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json().get("response", "")