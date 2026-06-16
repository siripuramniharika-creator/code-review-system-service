import re


def explain_issue(code: str):
    """
    AI-style explanation generator for code issues
    (we will later upgrade to LLM explanations)
    """

    issues = []

    # -------------------------
    # 1. eval detection
    # -------------------------
    if re.search(r"eval\s*\(", code):
        issues.append({
            "line": None,
            "title": "Avoid using eval()",
            "severity": "Critical",
            "explanation": (
                "eval() executes raw Python code, which can lead to "
                "serious security vulnerabilities like Remote Code Execution."
            ),
            "fix": "Use safe parsing methods or predefined functions instead."
        })

    # -------------------------
    # 2. exec detection
    # -------------------------
    if re.search(r"exec\s*\(", code):
        issues.append({
            "line": None,
            "title": "Avoid using exec()",
            "severity": "Critical",
            "explanation": (
                "exec() executes dynamic code which can be exploited by attackers."
            ),
            "fix": "Avoid dynamic execution. Use function mapping or safe evaluation."
        })

    # -------------------------
    # 3. SQL injection pattern
    # -------------------------
    if "select *" in code.lower() and "+" in code:
        issues.append({
            "line": None,
            "title": "Possible SQL Injection",
            "severity": "Critical",
            "explanation": (
                "String concatenation in SQL queries can allow attackers "
                "to inject malicious SQL commands."
            ),
            "fix": "Use parameterized queries or ORM methods."
        })

    # -------------------------
    # 4. nested loops
    # -------------------------
    if code.count("for ") > 1:
        issues.append({
            "line": None,
            "title": "Multiple loops detected",
            "severity": "Warning",
            "explanation": (
                "Nested or multiple loops can increase time complexity "
                "and reduce performance."
            ),
            "fix": "Try optimizing logic or using vectorized operations."
        })

    return issues