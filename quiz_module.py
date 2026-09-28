from pydantic import BaseModel, Field, model_validator

from gemini_client import generate_structured


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str

    @model_validator(mode="after")
    def correct_answer_is_an_option(self):
        if self.correct_answer not in self.options:
            raise ValueError("correct_answer must be one of the options")
        return self


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)


def generate_quiz(text: str):
    prompt = f"""
Create exactly 3 multiple-choice questions from the topic below.

Topic:
{text}

Return JSON matching this structure:
{{
    "questions": [
        {{
            "question": "Question text",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correct_answer": "One option exactly as written"
        }}
    ]
}}

Create exactly 3 questions. Keep them simple and suitable for a student.
"""

    return generate_structured(prompt, QuizResponse).model_dump()