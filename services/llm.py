from transformers import pipeline

generator = pipeline("text-generation", model="distilgpt2")


def format_response(user_query, raw_answer):
    prompt = f"Convert this into a clear and short customer support response.\nQuery: {user_query}\nAnswer: {raw_answer}\nResponse:"

    result = generator(prompt, max_new_tokens=30, do_sample=False)

    text = result[0]["generated_text"]

    if "Response:" in text:
        text = text.split("Response:")[-1].strip()

    return text
