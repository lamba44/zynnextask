# Voice AI Support Assistant (E-commerce)

## Overview

This project is a simple voice-enabled support assistant for an e-commerce platform.
It takes an audio query, converts it to text, processes it using a predefined dataset (orders & policies), and returns both a text and audio response.

The system runs entirely via CLI and demonstrates an end-to-end pipeline:
speech → text → logic → LLM → speech.

---

## Setup

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Run the application:

```
python main.py
```

3. Enter the path of the audio file when prompted:

```
sample_audio/query1.wav
```

4. Output:

- Response is printed in the terminal
- Audio response is saved as `response.mp3`

---

## Assumptions

- Queries will contain keywords like **order, track, refund, return**, etc.
- Users may mention order IDs in formats like `ORD123` or `ORD 123`.
- The provided JSON files are the **only source of truth**.
- LLM is used only for formatting responses, not for generating facts.
- System handles one query at a time (no conversation memory).

---

## Design Decisions & Tradeoffs

- Used **Whisper** for offline speech-to-text to avoid external dependencies.
- Used **FLAN-T5 (small)** as a lightweight, free LLM for response formatting.
- Core logic (order lookup, policy handling) is **rule-based** to ensure correctness.
- LLM output is partially constrained to avoid hallucinations.
- CLI interface was chosen over API/UI for faster implementation.

Tradeoff:

- Prioritized **reliability and speed** over advanced NLP or conversational ability.

---

## Improvements

- Some responses are correct but may be **incomplete or not fully natural**.
- Better prompt tuning or a stronger instruction model can improve response quality.
- More robust intent detection (instead of keyword matching).
- Support for multi-turn conversations.
- Add UI or API layer for better usability.
- Improve handling of noisy or unclear audio inputs.

---
