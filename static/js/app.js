const form = document.querySelector(".card");
const task =
    document.getElementById(
        "task"
    );

const inputText =
    document.getElementById(
        "inputText"
    );

const inputLabel = document.querySelector('label[for="inputText"]');
const button = document.getElementById("submitButton");
const buttonText = document.getElementById("buttonText");
const spinner = document.getElementById("spinner");


const resultCard =
    document.getElementById(
        "resultCard"
    );

const result =
    document.getElementById(
        "result"
    );

const errorBox =
    document.getElementById(
        "error"
    );

const copyButton = document.getElementById("copyButton");

const taskInfo = {

    qa: {

        label: "Your Question",

        placeholder:
            "Example: What is photosynthesis?"

    },

    explain: {

        label: "Topic to Explain",

        placeholder:
            "Example: Explain the Pythagoras theorem simply."

    },

    quiz: {

        label: "Passage or Topic",

        placeholder:
            "Paste a passage or enter a topic for a 3-question MCQ quiz."

    },

    summarize: {

        label: "Text to Summarize",

        placeholder:
            "Paste the educational text you want to summarize."

    },

    learn: {

        label: "Topic for Learning Path",

        placeholder:
            "Example: SQL, Python, Data Structures, Machine Learning"

    }

};


task.addEventListener(
    "change",
    updateForm
);


updateForm();


function updateForm() {

    const info =
        taskInfo[
            task.value
        ];

    inputLabel.textContent =
        info.label;

    inputText.placeholder =
        info.placeholder;
}


form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const value =
            inputText.value.trim();


        if (!value) {

            return;

        }


        hideError();

        setLoading(true);

        resultCard.classList.add(
            "hidden"
        );


        const endpointMap = {

            qa: "/qa",

            explain: "/explain",

            quiz: "/quiz",

            summarize: "/summarize",

            learn:
                "/learn/recommendations"

        };


        const payloadMap = {

            qa: {
                question: value
            },

            explain: {
                text: value
            },

            quiz: {
                text: value
            },

            summarize: {
                text: value
            },

            learn: {
                topic: value
            }

        };


        try {

            const response =
                await fetch(
                    endpointMap[
                        task.value
                    ],
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                payloadMap[
                                    task.value
                                ]
                            )

                    }
                );


            const responseText = await response.text();
            let data;

            try {
                data = responseText ? JSON.parse(responseText) : {};
            } catch {
                data = { detail: responseText };
            }


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    data.result ||
                    "Request failed."
                );

            }


            renderResult(data);


            resultCard.classList.remove(
                "hidden"
            );


            resultCard.scrollIntoView({
                behavior: "smooth"
            });


        } catch (error) {

            showError(
                error.message
            );

        } finally {

            setLoading(false);

        }

    }
);


function renderResult(data) {

    if (
        task.value === "quiz"
    ) {

        renderQuiz(
            data.questions || []
        );

        return;

    }


    result.innerHTML =
        markdownToHtml(
            data.result || ""
        );
}


function renderQuiz(
    questions
) {

    result.innerHTML = "";


    questions.forEach(
        function(item, index) {

            const box =
                document.createElement(
                    "div"
                );

            box.className =
                "quiz-question";


            const title =
                document.createElement(
                    "h3"
                );

            title.textContent =
                `${index + 1}. ${item.question}`;


            box.appendChild(
                title
            );


            const feedback =
                document.createElement(
                    "div"
                );

            feedback.className =
                "answer";


            item.options.forEach(
                function(option) {

                    const optionButton =
                        document.createElement(
                            "button"
                        );


                    optionButton.type =
                        "button";


                    optionButton.className =
                        "quiz-option";


                    optionButton.textContent =
                        option;


                    optionButton.addEventListener(
                        "click",
                        function() {

                            const buttons =
                                box.querySelectorAll(
                                    ".quiz-option"
                                );


                            buttons.forEach(
                                function(btn) {

                                    btn.disabled =
                                        true;

                                }
                            );


                            if (
                                option ===
                                item.correct_answer
                            ) {

                                optionButton.classList.add(
                                    "correct"
                                );

                                feedback.textContent =
                                    "Correct!";

                            } else {

                                optionButton.classList.add(
                                    "wrong"
                                );


                                buttons.forEach(
                                    function(btn) {

                                        if (
                                            btn.textContent ===
                                            item.correct_answer
                                        ) {

                                            btn.classList.add(
                                                "correct"
                                            );

                                        }

                                    }
                                );


                                feedback.textContent =
                                    `Correct answer: ${item.correct_answer}`;

                            }

                        }
                    );


                    box.appendChild(
                        optionButton
                    );

                }
            );


            box.appendChild(
                feedback
            );


            result.appendChild(
                box
            );

        }
    );
}


function markdownToHtml(
    text
) {

    const escaped =
        escapeHtml(text);


    return escaped

        .replace(
            /^### (.*)$/gm,
            "<h3>$1</h3>"
        )

        .replace(
            /^## (.*)$/gm,
            "<h2>$1</h2>"
        )

        .replace(
            /^# (.*)$/gm,
            "<h1>$1</h1>"
        )

        .replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        )

        .replace(
            /^\s*[-*] (.*)$/gm,
            "<li>$1</li>"
        )

        .replace(
            /\n{2,}/g,
            "</p><p>"
        )

        .replace(
            /\n/g,
            "<br>"
        )

        .replace(
            /(<li>.*<\/li>)/gs,
            "<ul>$1</ul>"
        );

}


function escapeHtml(
    value
) {

    return value

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );

}


function setLoading(
    loading
) {

    button.disabled =
        loading;


    buttonText.textContent =
        loading
            ? "Generating..."
            : "Generate";


    spinner.classList.toggle(
        "hidden",
        !loading
    );

}


function showError(
    message
) {

    errorBox.textContent =
        message;

    errorBox.classList.remove(
        "hidden"
    );

}


function hideError() {

    errorBox.textContent = "";

    errorBox.classList.add(
        "hidden"
    );

}


copyButton.addEventListener(
    "click",
    async function() {

        await navigator.clipboard
            .writeText(
                result.innerText
            );


        copyButton.textContent =
            "Copied!";


        setTimeout(
            function() {

                copyButton.textContent =
                    "Copy";

            },
            1200
        );

    }
);