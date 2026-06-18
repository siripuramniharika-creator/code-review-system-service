import json
import re

def safe_parse(raw_output):
    try:
        if isinstance(raw_output, dict):
            return raw_output

        if not isinstance(raw_output, str):
            return {}

        text = raw_output.strip()

        # Remove markdown code fences
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        # Extract JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            print("No JSON found")
            return {}

        json_str = match.group()

        return json.loads(json_str)

    except Exception as e:
        print("PARSE ERROR:", e)
        return {}