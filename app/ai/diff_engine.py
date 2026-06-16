import difflib


def generate_diff(original: str, improved: str):
    """
    Generates line-by-line diff between original and improved code
    """

    original_lines = original.splitlines()
    improved_lines = improved.splitlines()

    diff = difflib.unified_diff(
        original_lines,
        improved_lines,
        fromfile="Original Code",
        tofile="AI Improved Code",
        lineterm=""
    )

    return list(diff)