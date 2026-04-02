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


def _choose_prompt(raw_answer):
    lower = raw_answer.lower()

    if "not found" in lower:
        return (
            "Rewrite this as a polite customer support reply in one short sentence.\n"
            "Keep the meaning exactly the same.\n"
            "Example: Order ORD999 not found -> Sorry, I could not find order ORD999.\n\n"
            f"Text: {raw_answer}\n"
            "Reply:"
        )

    if "refund" in lower:
        return (
            "Rewrite this as a polite customer support reply in one short sentence.\n"
            "Keep the meaning exactly the same.\n"
            "Example: Refunds are processed via original payment method in 5 days -> "
            "Your refund will be processed via the original payment method within 5 days.\n\n"
            f"Text: {raw_answer}\n"
            "Reply:"
        )

    if "return" in lower or "returns" in lower:
        return (
            "Rewrite into one clear customer support sentence.\n"
            "Keep all details exactly the same.\n"
            "Do not apologize.\n"
            "Do not add new information.\n\n"
            f"{raw_answer}\n"
            "Response:"
        )

    if "in transit" in lower:
        return (
            "Rewrite this as a polite customer support reply in one short sentence.\n"
            "Keep the meaning exactly the same.\n"
            "Example: Order ORD124 is in transit and will arrive by 2026-03-30 -> "
            "Your order ORD124 is in transit and is expected to arrive by 2026-03-30.\n\n"
            f"Text: {raw_answer}\n"
            "Reply:"
        )

    if "delivered" in lower:
        return (
            "Rewrite this as a polite customer support reply in one short sentence.\n"
            "Keep the meaning exactly the same.\n"
            "Example: Order ORD123 was delivered on 2026-03-20 -> "
            "Your order ORD123 was delivered on 2026-03-20.\n\n"
            f"Text: {raw_answer}\n"
            "Reply:"
        )

    return (
        "Rewrite this as a polite customer support reply in one short sentence.\n"
        "Keep the meaning exactly the same.\n\n"
        f"Text: {raw_answer}\n"
        "Reply:"
    )


def format_response(user_query, raw_answer):
    prompt = _choose_prompt(raw_answer)

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=256).to(
        device
    )

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            num_beams=4,
            do_sample=False,
            repetition_penalty=1.15,
            no_repeat_ngram_size=3,
            early_stopping=True,
        )

    text = _clean(tokenizer.decode(outputs[0], skip_special_tokens=True))

    if not text:
        return raw_answer

    bad_starts = ("you are", "i am", "sorry, but i am", "reply:")
    if text.lower().startswith(bad_starts):
        return raw_answer

    return text
