document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('form');
    const searchPopup = document.createElement('div');
    const closeButton = document.createElement('span');
    const searchResultsContent = document.createElement('div');

    // 팝업 스타일 설정
    searchPopup.style.position = 'fixed';
    searchPopup.style.top = '100px';
    searchPopup.style.right = '50px';
    searchPopup.style.width = '300px';
    searchPopup.style.maxHeight = '400px';
    searchPopup.style.backgroundColor = '#fff';
    searchPopup.style.border = '1px solid #ccc';
    searchPopup.style.padding = '20px';
    searchPopup.style.zIndex = '10000';
    searchPopup.style.overflowY = 'auto';
    searchPopup.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
    searchPopup.style.display = 'none'; // 기본적으로 숨김

    // 닫기 버튼 스타일 설정
    closeButton.innerHTML = '&times;';
    closeButton.style.position = 'absolute';
    closeButton.style.top = '5px';
    closeButton.style.right = '10px';
    closeButton.style.cursor = 'pointer';
    closeButton.style.fontSize = '20px';
    closeButton.style.color = '#aaa';

    closeButton.addEventListener('click', function() {
        searchPopup.style.display = 'none';
    });

    searchPopup.appendChild(closeButton);
    searchPopup.appendChild(searchResultsContent);
    document.body.appendChild(searchPopup);

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const query = document.querySelector('input[name="q"]').value;

        fetch(`/search/?q=${query}`)
            .then(response => response.text())
            .then(html => {
                searchResultsContent.innerHTML = html;
                searchPopup.style.display = 'block';
            });
    });
});
