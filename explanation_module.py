from gemini_client import generate_text


def explain_topic(text: str) -> str:
    prompt = f"""
Explain the following topic in a very simple and beginner-friendly way.

Topic:
{text}

Use:
- Simple language
- Short points
- Small examples when useful
- Easy explanation for a college student
"""

    return generate_text(prompt)