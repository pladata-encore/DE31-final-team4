function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function loadSectorDetails(sector, color) {
    console.log("Loading sector details for: " + sector);

    const noteElement = document.getElementById('sector-details');
    let transparentColor = color.replace('rgb', 'rgba').replace(')', ', 0.3)'); // 투명도 0.3 추가
    
    fetch(`/sector-details/${sector}/`)
        .then(response => {
            if (!response.ok) {
                console.error("Error fetching data: ", response.statusText);
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            console.log("Data received: ", data);
            
            // 데이터 정렬: 등락률 기준 내림차순
            data.sort((a, b) => b.UpDownRate - a.UpDownRate);
            // 기존 내용 지우기
            noteElement.innerHTML = ''; 

            // 데이터가 로드된 후 제목 추가
            const sectorTitle = document.createElement('h5');
            sectorTitle.textContent = sector; // 섹터 이름 설정
            sectorTitle.style.textAlign = 'center'; // 제목 중앙 정렬
            sectorTitle.style.fontFamily = 'NanumB';
            noteElement.appendChild(sectorTitle); // 제목 추가

            if (data.length > 0) {
                const table = document.createElement('table');
                table.classList.add('table', 'table-bordered');

                // 테이블 헤더 추가
                const header = table.insertRow();
                header.innerHTML = `
                    <th style="text-align: left;">종목</th>
                    <th style="text-align: right;">현재가</th>
                    <th style="text-align: right;">등락률</th>
                `;

                // 데이터 추가
                data.forEach(item => {
                    const row = table.insertRow();
                    const upDownRateColor = item.UpDownRate > 0 ? 'red' : (item.UpDownRate < 0 ? 'blue' : 'black'); // 색상 결정
                    row.innerHTML = `
                        <td style="text-align: left;">${item.name}</td>
                        <td style="text-align: right;">${formatNumber(item.current_price)}</td>
                        <td style="text-align: right; color: ${upDownRateColor};">${item.UpDownRate}%</td>
                    `;
                });

                noteElement.appendChild(table);
            } else {
                noteElement.innerHTML += '<p>해당 섹터의 데이터가 없습니다.</p>';
            }

            // 데이터 로드 후 배경색 변경
            noteElement.style.backgroundColor = transparentColor;  // 배경색을 클릭한 섹터의 색상으로 변경
        })
        .catch(error => {
            console.error("Error fetching sector details:", error);
        });
}
