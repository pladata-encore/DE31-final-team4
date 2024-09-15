class TestPage {
    constructor(data) {
        this.data = data;
        this.current = 0;
        this.point = 0;
        this.init();
    }

    init() {
        this.renderQuestion();
    }

    renderQuestion() {
        const questionData = this.data.data[this.current];
        const questionElement = document.querySelector('.custom-question');
        const questionTextElement = document.querySelector('.custom-question-text');
        const buttonWrap = document.querySelector('.custom-button-wrap');

        // 질문 텍스트 설정
        questionElement.textContent = `Q${this.current + 1}.`;
        questionTextElement.textContent = questionData.question;

        // 기존 버튼 제거
        buttonWrap.innerHTML = '';

        // 선택지 버튼 생성하여 추가
        questionData.answerList.forEach((answer, index) => {
            const button = document.createElement('button');
            button.textContent = answer.answer;
            button.classList.add('custom-button');

            // 버튼 클릭 시 포인트를 추가하고 다음 질문으로 이동
            button.addEventListener('click', () => {
                this.point += answer.point;
                this.nextQuestion();
            });

            buttonWrap.appendChild(button);
        });
    }

    nextQuestion() {
        this.current++;
        if (this.current < this.data.data.length) {
            this.renderQuestion();
        } else {
            this.showResult();
        }
    }

    showResult() {
        const result = this.data.result.find(result =>
            this.point >= result.minPoint && this.point <= result.maxPoint
        );

        const questionElement = document.querySelector('.custom-question');
        const questionTextElement = document.querySelector('.custom-question-text');
        const buttonWrap = document.querySelector('.custom-button-wrap');

        questionElement.textContent = result.title;
        questionTextElement.textContent = result.description;
        buttonWrap.innerHTML = ''; // 결과 화면에서 버튼 제거

        // 결과를 서버로 전송 (AJAX 요청)
        this.saveResult(result.title, result.description);
    }

    saveResult(resultTitle, resultDescription) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // CSRF 토큰 추출

        fetch('/save-test-result/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                result1: resultTitle,
                result2: resultDescription
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Test result saved successfully:', data);
        })
        .catch(error => {
            console.error('Error saving test result:', error);
        });
    }
}
