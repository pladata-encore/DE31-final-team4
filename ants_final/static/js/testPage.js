class TestPage {
    constructor(data, saveUrl) {
        this.data = data;
        this.saveUrl = saveUrl; // 저장할 URL을 전달받음
        this.current = 0;
        this.point = 0;

        this.init(); // 초기화 호출
    }

    init() {
        this.renderStartPage(); // 시작 페이지 렌더링
        this.updateProgressBar();
    }

    // 시작 페이지 렌더링
    renderStartPage() {
        const questionElement = document.querySelector('.custom-question');
        const questionTextElement = document.querySelector('.custom-question-text');
        const buttonWrap = document.querySelector('.custom-button-wrap');

        // 시작 페이지의 제목과 설명 설정
        questionElement.textContent = testData.startPageTitle;
        questionTextElement.textContent = testData.startPageDescription;

        // 기존 버튼 제거
        buttonWrap.innerHTML = '';

        // "테스트하러 가기" 버튼 생성
        const startButton = document.createElement('button');
        startButton.textContent = '테스트하러 가기';
        startButton.classList.add('custom-button');

        // 버튼 클릭 시 첫 번째 질문을 렌더링
        startButton.addEventListener('click', () => {
            this.renderQuestion();
            this.updateProgressBar();
            var progressBarContainer = document.querySelector('.progress-bar-container');
            progressBarContainer.style.visibility = 'visible';
        });

        buttonWrap.appendChild(startButton);
    }

    updateProgressBar() {
        const progressBar = document.getElementById('progressBar');
        const totalQuestions = this.data.data.length;
        const progressPercentage = ((this.current + 1) / totalQuestions) * 100; // 진행 비율 계산
        progressBar.style.width = `${progressPercentage}%`; // 진행 바의 폭 설정

        const imageLeftPosition = `calc(${progressPercentage}% - 15px)`; // 이미지의 위치를 진행 바의 너비에 맞게 조정
        progressImage.style.left = imageLeftPosition; // 이미지의 left 속성 업데이트
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
        questionData.answerList.forEach((answer) => {
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

        // 진행 바 업데이트
        this.updateProgressBar();
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
        var progressBarContainer = document.querySelector('.progress-bar-container');
        progressBarContainer.style.visibility = 'hidden';
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
