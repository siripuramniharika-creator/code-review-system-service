from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
)
model.to("cpu")
def run_phi3_analysis(code: str, language: str):

    prompt = f"""
You are a senior software engineer.

Analyze this {language} code and return ONLY JSON.

CODE:
{code}

JSON format:
{{
  "quality_score": 0-10,
  "security_score": 0-10,
  "performance_score": 0-10,
  "issues": [],
  "suggestions": [],
  "improved_code": ""
}}
"""

    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to("cpu") for k, v in inputs.items()}

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=False,
            num_beams=1
        )

    return tokenizer.decode(output[0], skip_special_tokens=True)