$(document).ready(function() {
    let currentQuestionIndex = 0;
    let score = 0;
    let selectedOption = null;

    function loadQuestion() {
        if (currentQuestionIndex >= questions.length) {
            showResults();
            return;
        }

        const question = questions[currentQuestionIndex];
        $('#question-text').text(question.question);
        $('#options').empty();

        question.options.forEach((option, index) => {
            const optionHtml = `
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="option" id="option${index}" value="${index}">
                    <label class="form-check-label" for="option${index}">
                        ${option}
                    </label>
                </div>
            `;
            $('#options').append(optionHtml);
        });

        $('#submit-btn').prop('disabled', true);
        $('#feedback').hide();
        updateProgress();
    }

    function updateProgress() {
        const progress = ((currentQuestionIndex) / questions.length) * 100;
        $('#progress-bar').css('width', progress + '%');
    }

    function showResults() {
        $('#quiz-container').hide();
        $('#results-container').show();
        $('#final-score').text(`You scored ${score} out of ${questions.length}`);
    }

    $('#options').on('change', 'input[type="radio"]', function() {
        selectedOption = parseInt($(this).val());
        $('#submit-btn').prop('disabled', false);
    });

    $('#submit-btn').click(function() {
        if (selectedOption === null) return;

        $.ajax({
            url: '/submit_answer',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                question_index: currentQuestionIndex,
                selected_option: selectedOption
            }),
            success: function(response) {
                const alertClass = response.is_correct ? 'alert-success' : 'alert-danger';
                const alertText = response.is_correct ? 'Correct!' : 'Incorrect!';
                $('#feedback-alert').removeClass('alert-success alert-danger').addClass(alertClass).text(alertText);

                if (!response.is_correct && response.fact) {
                    $('#fact').text(response.fact).show();
                } else {
                    $('#fact').hide();
                }

                $('#feedback').show();

                if (response.is_correct) {
                    score++;
                }

                setTimeout(() => {
                    currentQuestionIndex++;
                    loadQuestion();
                }, 4000);
            }
        });
    });

    loadQuestion();
});
