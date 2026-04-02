from services.speech_to_text import transcribe
from services.logic import handle_query
from services.llm import format_response
from services.text_to_speech import generate_audio

audio_path = input("Enter audio file path: ")

text = transcribe(audio_path)
print("Transcribed:", text)

raw_answer = handle_query(text)
print("Raw Answer:", raw_answer)

final_answer = format_response(text, raw_answer)
print("Final Response:", final_answer)

generate_audio(final_answer, "response.mp3")

print("Audio saved as response.mp3")
