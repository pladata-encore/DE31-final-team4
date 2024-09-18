function loadSectorDetails(sector) {
    console.log("Loading sector details for: " + sector);  // 섹터 이름 출력
    // AJAX 요청으로 특정 섹터의 최근 10개의 데이터를 가져옴
    fetch(`/sector-details/${sector}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            console.log("Data received: ", data);  // 받은 데이터 출력
            const detailsDiv = document.getElementById('sector-details');
            detailsDiv.innerHTML = '';  // 기존 데이터를 초기화

            if (data.length > 0) {
                // 데이터를 테이블 형식으로 표시
                const table = document.createElement('table');
                table.classList.add('table', 'table-bordered');

                // 테이블 헤더
                const header = table.insertRow();
                header.innerHTML = `
                    <th>Name</th>
                    <th>Current Price</th>
                    <th>UpDownRate</th>
                `;

                // 데이터 추가
                data.forEach(item => {
                    const row = table.insertRow();
                    row.innerHTML = `
                        <td>${item.name}</td>
                        <td>${item.current_price}</td>
                        <td>${item.UpDownRate}</td>
                    `;
                });

                detailsDiv.appendChild(table);
            } else {
                detailsDiv.innerHTML = '<p>해당 섹터의 데이터가 없습니다.</p>';
            }
        })
        .catch(error => {
            console.error("Error fetching sector details:", error);
        });
}
