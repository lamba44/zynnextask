from transformers import pipeline

generator = pipeline("text-generation", model="distilgpt2")


def format_response(user_query, raw_answer):
    prompt = f"User asked: {user_query}. Answer: {raw_answer}"
    result = generator(prompt, max_length=50, num_return_sequences=1)
    return result[0]["generated_text"]
