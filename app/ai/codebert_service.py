from transformers import AutoTokenizer, AutoModel
import torch

MODEL_NAME = "microsoft/codebert-base"

# Load tokenizer + model once (VERY IMPORTANT for performance)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

model.eval()  # inference mode


def get_code_embedding(code: str):
    """
    Convert source code into AI embedding vector using CodeBERT
    """

    inputs = tokenizer(
        code,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    # take mean pooling of token embeddings
    embedding = outputs.last_hidden_state.mean(dim=1)

    return embedding.squeeze().numpy()