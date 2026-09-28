from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a friendly educational assistant.

Answer the student's question clearly and simply.

Question:
{question}

Give a beginner-friendly answer with short examples when useful.
"""

    return generate_text(prompt)