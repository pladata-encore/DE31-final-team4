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

        // 질문 텍스트를 설정
        questionElement.textContent = `Q${this.current + 1}.`;
        questionTextElement.textContent = questionData.question;

        // 기존 버튼 제거
        buttonWrap.innerHTML = '';

        // 선택지 버튼을 생성하여 추가
        questionData.answerList.forEach((answer, index) => {
            const button = document.createElement('button');
            button.textContent = answer.answer;
            button.classList.add('custom-button'); // 버튼 스타일을 위해 클래스 추가

            // 버튼 클릭 시 포인트를 추가하고 다음 질문으로 넘어감
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
    }
}
