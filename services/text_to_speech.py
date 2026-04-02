from gtts import gTTS


def generate_audio(text, output_path):
    tts = gTTS(text=text)
    tts.save(output_path)
