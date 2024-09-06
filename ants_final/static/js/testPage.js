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

// 설문조사 데이터 정의
const surveyData = {
    data: [
        {
            question: '당신이 가장 좋아하는 색은 무엇인가요?',
            answerList: [
                { answer: '빨간색', point: 10 },
                { answer: '파란색', point: 20 },
                { answer: '초록색', point: 30 }
            ]
        },
        {
            question: '당신이 가장 좋아하는 동물은 무엇인가요?',
            answerList: [
                { answer: '강아지', point: 10 },
                { answer: '고양이', point: 20 },
                { answer: '새', point: 30 }
            ]
        }
    ],
    result: [
        { title: '낮은 포인트 결과', description: '당신은 침착하고 차분한 사람입니다.', minPoint: 10, maxPoint: 20 },
        { title: '중간 포인트 결과', description: '당신은 밝고 외향적인 사람입니다.', minPoint: 21, maxPoint: 40 },
        { title: '높은 포인트 결과', description: '당신은 열정적이고 활기찬 사람입니다.', minPoint: 41, maxPoint: 60 }
    ]
};
// TestPage 클래스를 인스턴스화하여 사용
const testPage = new TestPage(surveyData);
