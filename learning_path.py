from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a simple learning path for the following topic:

Topic:
{topic}

Include:
- Beginner level
- Intermediate level
- Advanced level
- Suggested timeline
- Practice ideas
- Useful resource types
- One final project

Keep it clear and beginner-friendly for a college student.
"""

    return generate_text(prompt)