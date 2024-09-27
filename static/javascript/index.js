document.addEventListener('DOMContentLoaded', () => {
    const today = new Date().toISOString().split('T')[0].replaceAll('-','/');
    document.getElementById("date").innerHTML = today;

    const this_year = new Date().getFullYear();
    document.getElementById("year").value = this_year;
    console.log(this_year);
    
    const this_month = new Date().getMonth()+1;
    document.getElementById("month").value = this_month;
});

document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.item-data');
    items.forEach(item => {
        item.addEventListener('click', function() {
            const detailWrapper = this.querySelector('.detail-wrapper');
            const divider = this.querySelector('.divider');
            const icon = this.querySelector('.icon img');
            if (detailWrapper.style.display === 'none' || detailWrapper.style.display === '') {
                detailWrapper.style.display = 'flex';
                divider.style.display = 'block'
                icon.style.transform = 'rotate(90deg)';
            } else {
                detailWrapper.style.display = 'none';
                divider.style.display = 'none'
                icon.style.transform = 'rotate(0deg)';
            }
        });
    });
    const today = new Date().toISOString().split('T')[0].replaceAll('-','/');
    document.getElementById("date").innerHTML = today;

    const this_year = new Date().getFullYear();
    document.getElementById("year").value = this_year;
    const this_month = new Date().getMonth()+1;
    document.getElementById("month").value = this_month;
});

async function fetchData() {
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;
    const parent = document.querySelector('.index-wrapper');

    while( parent.childElementCount > 1){
        parent.lastElementChild.remove();
    }

    const res = await fetch(`/get-data?year=${year}&month=${month}`);
    const data = await res.json();

    if (data.data.length === 0) {
        document.getElementById('water-sum').innerHTML = '-';
        document.getElementById('paper-sum').innerHTML = '-';
        const newElement = `<div class="no-data-text">No data</div>`;
        parent.insertAdjacentHTML('beforeend',newElement);
    }else{
        console.log(data);
        if(data.sum[0] != null){
            document.getElementById('water-sum').innerHTML = data.sum[0];
        }else{
            document.getElementById('water-sum').innerHTML = '-';
        }
        if(data.sum[1] != null){
            document.getElementById('paper-sum').innerHTML = data.sum[1];
        }else{
            document.getElementById('paper-sum').innerHTML = '-';
        }
        data.data.forEach(item => {
            const newElement = 
            `<div class="item-data">
            <div class="date">
                ${item.date}
            </div>
            <div class="data-wrapper">
                <div class="summary">
                    <div class="water-sum">
                        <div class="text">Water</div>
                        <div class="sum" id="water_sum">${ item.water_sum }L</div>
                    </div>
                    <div class="paper-sum">
                        <div class="text">Paper</div>
                        <div class="sum" id="paper_sum">${ item.paper_sum }kg</div>
                    </div>
                    <div class="icon">
                        <img src="/static/images/chevron_right_24dp_1A1A1A_FILL0_wght400_GRAD0_opsz24.svg" alt="">
                    </div>
                </div>
                <hr class="divider" style="display: none;">
                <div class="detail-wrapper" style="display: none;">
                    <div class="water-wrapper">
                        <div class="detail">
                            <div class="detail-item-group">
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Cleaning ink Press1
                                    </div>
                                    <div class="detail-data" id="cleaning_ink_press_1">
                                        ${ item.cleaning_ink_press_1 }
                                    </div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Cleaning ink Press2
                                    </div>
                                    <div class="detail-data" id="cleaning_ink_press_2">
                                        ${ item.cleaning_ink_press_2 }
                                    </div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Plate Processing
                                    </div>
                                    <div class="detail-data" id="plate_processing">
                                        ${ item.plate_processing }
                                    </div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Fountain Solution Press1
                                    </div>
                                    <div class="detail-data" id="fountain_solution_press_1">
                                        ${ item.fountain_solution_press_1 }
                                    </div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Fountain Solution Press2
                                    </div>
                                    <div class="detail-data" id="fountain_solution_press_2">
                                        ${ item.fountain_solution_press_2 }
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="paper-wrapper">
                        <div class="detail">
                            <div class="detail-item-group">
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Flaky Waste Paper
                                    </div>
                                    <div class="detail-data">
                                        ${ item.flaky_waste_paper }
                                    </div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Pieces Waste Paper Cutting Machine 1
                                    </div>
                                    <div class="detail-data" id="cutting_machine_1">
                                        ${ item.cutting_machine_1 }
                                    </div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Pieces Waste Paper Cutting Machine 2
                                    </div>
                                    <div class="detail-data" id="cutting_machine_2">
                                        ${ item.cutting_machine_2 }
                                    </div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Pieces Waste Paper Cutting 3-sided trimmer
                                    </div>
                                    <div class="detail-data" id="three_sided_trimmer">
                                        ${ item.three_sided_trimmer }
                                    </div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Sheet Waste Paper Press 1
                                    </div>
                                    <div class="detail-data" id="sheet_waste_paper_1">
                                        ${ item.sheet_waste_paper_1 }
                                    </div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Sheet Waste Paper Press 2
                                    </div>
                                    <div class="detail-data" id="sheet_waste_paper_2">
                                        ${ item.sheet_waste_paper_2 }
                                    </div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Sheet Waste Paper Press 3
                                    </div>
                                    <div class="detail-data" id="sheet_waste_paper_3">
                                        ${ item.sheet_waste_paper_3 }
                                    </div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">
                                        Sheet Waste Paper Press 4(electrophotography)
                                    </div>
                                    <div class="detail-data" id="sheet_waste_paper_4">
                                        ${ item.sheet_waste_paper_4 }
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;
        
        parent.insertAdjacentHTML('beforeend',newElement);
        });
    }

    const items = document.querySelectorAll('.item-data');
    items.forEach(item => {
        item.addEventListener('click', function() {
            const detailWrapper = this.querySelector('.detail-wrapper');
            const divider = this.querySelector('.divider');
            const icon = this.querySelector('.icon img');
            if (detailWrapper.style.display === 'none' || detailWrapper.style.display === '') {
                detailWrapper.style.display = 'flex';
                divider.style.display = 'block'
                icon.style.transform = 'rotate(90deg)';
            } else {
                detailWrapper.style.display = 'none';
                divider.style.display = 'none'
                icon.style.transform = 'rotate(0deg)';
            }
        });
    });
}