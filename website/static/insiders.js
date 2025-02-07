document.getElementsByTagName('body')[0].classList.add('bg-dark');

const rowsPerPage = 5;
let insiderTableCurrentPage = 1;


document.addEventListener('DOMContentLoaded', function() {
    fetch('/get-insiders-data')
        .then(response => response.json())
        .then(data => {
            insiders_main_table_data = data.coins;

            active_coin_count = data.status_data.active_coin_count
            active_set_count = data.status_data.active_set_count

            renderInsidersTable(insiders_main_table_data);


            const countElment = document.getElementById('counts');
            countElment.innerHTML = `
                COINS - ${active_coin_count} &nbsp;&nbsp;&nbsp;   SETS - ${active_set_count}
            `;
        })
        .catch(error => console.error('Error fetching data:', error));
});

// table one
function renderInsidersTable(data, page = 1) {
    const tableBody = document.getElementById('firstTableBody');
    tableBody.innerHTML = '';

    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const paginatedData = data.slice(start, end);

    let row_number = (page - 1) * rowsPerPage + 1;
    paginatedData.forEach(row => {
        let tr = document.createElement('tr');
        tr.setAttribute('id', row_number);
        tr.classList.add('table-danger');
        tr.innerHTML = `
            <th scope="row">${row_number}</th>
            <td >
                <div class="d-flex flex-row justify-content-between">
                  <div class="fw-bold">
                      <span>${row.ticker}</span>
                  </div>
                  <div class="fw-bold">
                      <span>Total Sets - ${row.no_of_sets} ( ${row.no_of_buy_sets} , ${row.no_of_sell_sets} )</span>
                  </div>
                </div>
            </td>
            <td  >
                <div class="d-flex justify-content-between">
                    <div class="text-success fw-bold">
                        <span>BUY</span>
                    </div>
                    <div class="text-danger fw-bold">
                        <span>SELL</span>
                    </div>
                </div>
                
            </td>
        `;
        tableBody.appendChild(tr);

        row.fee_payers.forEach(fee_payer_row => {
            let whaleTr = document.createElement('tr');
            if (fee_payer_row.sets[0]!=false && fee_payer_row.sets[1]==false ){
                whaleTr.innerHTML  = `
                <th scope="row"></th>
                <td >
                    <div class="d-flex flex-row justify-content-between">
                        <div>
                            <span>${fee_payer_row.fee_payer}</span>
                        </div>
                        <div class="fw-bold">
                            <span> ${fee_payer_row.sets[0].length}/${row.no_of_sets}</span>
                        </div>
                    </div>
                </td>
                <td>
                    <div class="d-flex justify-content-around" >
                        <div class="text-success fw-bold">
                            <span>${fee_payer_row.sets[0].length}</span>
                        </div>
                        <div>
                            <span class="fw-bold">-</span>
                        </div>
                    </div>
                </td>
            `;

            }else if (fee_payer_row.sets[0]!=false && fee_payer_row.sets[1]!=false ){
                whaleTr.innerHTML = `
                <th scope="row"></th>
                <td >
                    <div class="d-flex flex-row justify-content-between">
                        <div>
                            <span >${fee_payer_row.fee_payer}</span>
                        </div>
                        <div class="fw-bold">
                            <span> ${fee_payer_row.sets[0].length + fee_payer_row.sets[1].length }/${row.no_of_sets}</span>
                        </div>
                    </div>
                </td>
                <td>
                    <div class="d-flex justify-content-around" >
                        <div>
                            <span class="text-success fw-bold">${fee_payer_row.sets[0].length}</span>
                        </div>
                        <div>
                            <span class="text-danger fw-bold">${fee_payer_row.sets[1].length}</span>
                        </div>
                    </div>
                </td>
            `;
            } else {
                whaleTr.innerHTML = `
                <th scope="row"></th>
                <td >
                    <div class="d-flex flex-row justify-content-between">
                        <div>
                            <span>${fee_payer_row.fee_payer}</span>
                        </div>
                        <div class="fw-bold">
                            <span> ${fee_payer_row.sets[1].length }/${row.no_of_sets}</span>
                        </div>
                    </div>
                </td>
                <td>    
                    <div class="d-flex justify-content-around" >
                            <div>
                                <span class="fw-bold">-</span>
                            </div>
                            <div>
                                <span class="text-danger fw-bold">${fee_payer_row.sets[1].length}</span>
                            </div>
                    </div>  
                </td>
            `;


            }


            // whaleTr.innerHTML = `
            //     <th scope="row"></th>
            //     <td >
            //         <div class="d-flex flex-row justify-content-between">
            //             <div>
            //                 <span>${fee_payer_row.fee_payer}</span>
            //             </div>
            //             <div>
            //                 <span> ${fee_payer_row.sets[0].length}/${row.no_of_sets}</span>
            //             </div>
            //         </div>
            //     </td>
            //     <td></td>
            // `;
            tableBody.appendChild(whaleTr);
        });

        row_number++;
    });

    insidersTableRenderPagination(data.length, page);
}

function insidersTableRenderPagination(totalRows, page = 1) {
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    const pagination = document.getElementById('table_one_pagination');
    pagination.innerHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === page ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
        li.addEventListener('click', function () {
            insiderTableCurrentPage = i;
            renderInsidersTable(insiders_main_table_data, insiderTableCurrentPage);
        });
        pagination.appendChild(li);
    }
}

document.getElementById('table_one_searchInput').addEventListener('input', function(event) {
    const searchTerm = event.target.value.toLowerCase();
    if (searchTerm !== "") {
        table_one_search_data = insiders_main_table_data.filter(row => row.ticker.toLowerCase().includes(searchTerm));
        insiderTableCurrentPage = 1;
        renderInsidersTable(table_one_search_data, insiderTableCurrentPage);
    } else {
        insiderTableCurrentPage = 1;
        renderInsidersTable(insiders_main_table_data, insiderTableCurrentPage);
    }
});


///////////////////////////////////////////////////////////////////////////////////////////
