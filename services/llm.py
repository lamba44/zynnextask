import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()


def _clean(text):
    return re.sub(r"\s+", " ", text).strip()


def format_response(user_query, raw_answer):
    prompt = (
        "You are a customer support assistant for an e-commerce store.\n"
        "Rewrite the answer into one natural, short, polite sentence.\n"
        "Keep the facts exactly the same.\n"
        "Do not add any new information.\n"
        "Do not mention that you are an AI.\n\n"
        f"User query: {user_query}\n"
        f"Answer: {raw_answer}\n"
        "Rewrite:"
    )

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=256).to(
        device
    )

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=40,
            num_beams=4,
            do_sample=False,
            repetition_penalty=1.1,
            no_repeat_ngram_size=3,
            early_stopping=True,
        )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    text = _clean(text)

    if text:
        if text[-1] not in ".!?":
            text += "."
        return text

    return raw_answer
