// Smooth scrolling for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// DOMContentLoaded 이벤트 핸들러
document.addEventListener("DOMContentLoaded", function(){
    // 심리 테스트 HTML을 로드할 컨테이너 요소를 가져옴
    var testContainer = document.getElementById('testContainer');
    
    // 심리 테스트 HTML 파일을 비동기적으로 로드
    fetch('/psychological_test/')  // Django 뷰 URL로 수정
        .then(response => response.text())
        .then(data => {
            // 로드한 HTML 내용을 컨테이너에 삽입
            testContainer.innerHTML = data;
        })
        .catch(error => console.error('Error loading the test:', error));
});

// 심리 테스트 점수를 계산하고 결과를 표시하는 함수
function submitTest() {
    var score = 0;

    // 15개의 질문에 대해 사용자 응답을 수집하고 점수를 계산
    for (var i = 1; i <= 15; i++) {
        var answer = document.getElementById('q' + i).value;
        if (answer === "yes") {
            score += 1;
        }
    }

    // 점수에 따라 결과 텍스트를 설정
    var resultText = "";
    if (score <= 5) {
        resultText = "You have a conservative approach towards money. You value savings and are cautious about spending.";
    } else if (score <= 10) {
        resultText = "You have a balanced approach to finances, neither too cautious nor too reckless.";
    } else {
        resultText = "You tend to take risks with money and may have a more spontaneous approach to spending and saving.";
    }

    // 결과를 표시
    document.getElementById("testResult").innerText = resultText;
    document.getElementById("result").style.display = "block";
}
