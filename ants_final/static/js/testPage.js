class TestPage {
    constructor(data, saveUrl) {
        this.data = data;
        this.saveUrl = saveUrl; // 저장할 URL을 전달받음
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
            this.point >= result.minPoint && this.point < result.maxPoint
        );

        const questionElement = document.querySelector('.custom-question');
        const questionTextElement = document.querySelector('.custom-question-text');
        const buttonWrap = document.querySelector('.custom-button-wrap');

        questionElement.textContent = result.title;
        questionTextElement.textContent = result.description;
        buttonWrap.innerHTML = ''; // 결과 화면에서 버튼 제거

        // 결과를 서버로 전송 (AJAX 요청)
        this.saveResult(result.title, result.description);

        // 'My Page로 이동' 버튼 보이기
        const myPageButton = document.getElementById('myPageButton');
        myPageButton.style.display = 'inline-block'; // 버튼을 보이게 설정
    }

    saveResult(resultTitle, resultDescription) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // CSRF 토큰 추출

        fetch(this.saveUrl, { // 전달받은 URL을 사용
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                result1: resultTitle,   // 첫 번째 결과
                result2: resultDescription // 두 번째 결과
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log('Test result saved successfully:', data);
                } else {
                    console.error('Error saving test result:', data.message);
                }
            })
            .catch(error => {
                console.error('Error saving test result:', error);
            });
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const testData = {
        // your test data here
    };

    // 테스트 페이지 초기화 (옵션 1 또는 옵션 2에 맞게 URL 지정)
    const testPage = new TestPage(testData, '/save-test-result-option1/');

    // MyPage 버튼 클릭 시 MyPage로 이동
    const myPageButton = document.getElementById('myPageButton');
    myPageButton.addEventListener('click', function () {
        window.location.href = '/mypage/';
    });
});
