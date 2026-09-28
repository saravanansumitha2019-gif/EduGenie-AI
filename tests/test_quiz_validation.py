from quiz_module import QuizQuestion, QuizResponse, generate_quiz


def test_quiz_question_has_four_options():

    question = QuizQuestion(

        question="2 + 2 = ?",

        options=[
            "1",
            "2",
            "3",
            "4"
        ],

        correct_answer="4"
    )


    assert len(
        question.options
    ) == 4


    assert (
        question.correct_answer
        in question.options
    )


def test_generate_quiz_returns_questions(monkeypatch):
    quiz = QuizResponse(
        questions=[
            QuizQuestion(
                question=f"Question {index}?",
                options=["A", "B", "C", "D"],
                correct_answer="A",
            )
            for index in range(1, 4)
        ]
    )
    monkeypatch.setattr(
        "quiz_module.generate_structured",
        lambda prompt, response_schema: quiz,
    )

    result = generate_quiz("The solar system")

    assert len(result["questions"]) == 3
    assert "result" not in result