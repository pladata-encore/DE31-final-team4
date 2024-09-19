document.addEventListener('DOMContentLoaded', function() {
    const dictionaryButton = document.getElementById('dictionaryButton');
    const dictionaryModal = new bootstrap.Modal(document.getElementById('dictionaryModal'));
    const dictionaryForm = document.getElementById('dictionaryForm');
    const dictionaryResults = document.getElementById('dictionaryResults');

    // 사전 버튼 클릭 시 모달 열기
    dictionaryButton.addEventListener('click', function() {
        dictionaryModal.show();
    });

    // 검색 폼 제출 시 AJAX로 검색 요청
    dictionaryForm.addEventListener('submit', function(e) {
        e.preventDefault();  // 기본 폼 동작 방지
        const searchTerm = document.getElementById('dictionarySearchInput').value;

        // 검색 요청
        fetch(`/search/?q=${searchTerm}`)
            .then(response => response.json())
            .then(data => {
                let resultHtml = '<ul>';
                if (data.results.length > 0) {
                    data.results.forEach(result => {
                        resultHtml += `<li>${result.term}: ${result.details}</li>`;
                    });
                } else {
                    resultHtml = `<p>${data.message}</p>`;
                }
                resultHtml += '</ul>';
                dictionaryResults.innerHTML = resultHtml;
            })
            .catch(error => console.log('Error:', error));
    });
});
