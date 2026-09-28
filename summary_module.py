from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following text in a simple and clear way.

Text:
{text}

Give:
- Main points
- Important facts
- Short and easy sentences
- A useful summary for a student
"""

    return generate_text(prompt)