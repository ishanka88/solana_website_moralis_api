document.getElementsByTagName('body')[0].classList.add('bg-dark');

const rowsPerPage = 5;
let table_one_currentPage = 1;
let table_two_currentPage = 1;

document.addEventListener('DOMContentLoaded', function() {
    fetch('/get-whales-data')
        .then(response => response.json())
        .then(data => {
            table_one_data = data.coins;
            table_two_data = data.whales;

            active_coin_count = data.status_data.active_coin_count
            active_set_count = data.status_data.active_set_count

            tableOneRenderTable(table_one_data);
            tableTwoRenderTable(table_two_data);


            const countElment = document.getElementById('counts');
            countElment.innerHTML = `
                COINS - ${active_coin_count} &nbsp;&nbsp;&nbsp;   SETS - ${active_set_count}
            `;
        })
        .catch(error => console.error('Error fetching data:', error));
});

// table one
function tableOneRenderTable(data, page = 1) {
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

    tableOneRenderPagination(data.length, page);
}

function tableOneRenderPagination(totalRows, page = 1) {
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    const pagination = document.getElementById('table_one_pagination');
    pagination.innerHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === page ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
        li.addEventListener('click', function () {
            table_one_currentPage = i;
            tableOneRenderTable(table_one_data, table_one_currentPage);
        });
        pagination.appendChild(li);
    }
}

document.getElementById('table_one_searchInput').addEventListener('input', function(event) {
    const searchTerm = event.target.value.toLowerCase();
    if (searchTerm !== "") {
        table_one_search_data = table_one_data.filter(row => row.ticker.toLowerCase().includes(searchTerm));
        table_one_currentPage = 1;
        tableOneRenderTable(table_one_search_data, table_one_currentPage);
    } else {
        table_one_currentPage = 1;
        tableOneRenderTable(table_one_data, table_one_currentPage);
    }
});



// Table two

function tableTwoRenderTable(data, page = 1) {
    const tableBody = document.getElementById('secondTableBody');
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
            <td>
                <div class="d-flex justify-content-between" >
                    <div class="fw-bold">  
                        ${row.whale_address} 
                    </div>
                    <div class="d-flex align-items-start">
                        <div class="icon-link-hover "> 
                            <a class="icon-link icon-link-hover" href="https://solscan.io/account/${row.whale_address}#defiactivities" target="_blank">
                                <i class="bi bi-upc-scan fs-5"></i>
                                <svg class="bi" aria-hidden="true"><use xlink:href="#arrow-right"></use></svg>
                            </a>
                        </div>
                        <div class="icon-link-hover"> 
                            <a class="icon-link icon-link-hover" href="https://dexcheck.ai/app/wallet-analyzer/${row.whale_address}" target="_blank">
                                <i class="bi bi-cash-coin fs-4"></i>
                                <svg class="bi" aria-hidden="true"><use xlink:href="#arrow-right"></use></svg>
                            </a>
                        </div>
                    </div>
                </div>
             
            </td>
            <td>
                <span class="d-flex justify-content-center fw-bold">
                    ${row.total_sets.length}
                </span>
            </td>
            <td>
                <span class="d-flex justify-content-center fw-bold">
                    ${row.coins.length}
                </span>
            </td>
        `;
        tableBody.appendChild(tr);

        row.coins.forEach(coin => {
            let coinTr = document.createElement('tr');
            console.log(coin)
            coinTr.innerHTML = `
                <th scope="row"></th>
                <td> 
                    <div class="d-flex justify-content-between" >
                        <div>
                            <span >${coin.ticker}</span>
                        </div>
                        <div>
                            <span >Total Sets - ${coin.amount_of_sets} ( ${coin.no_of_buy_sets} , ${coin.no_of_sell_sets} )</span>
                        </div>
                    </div>  
                </td>
                <td> 
                    <div class="d-flex justify-content-around" >
                        <div  class="text-success fw-bold">
                            <span>${coin.whale_in_buy_sets.length}</span>
                        </div>
                        <div  class="text-danger fw-bold">
                            <span>${coin.whale_in_sell_sets.length}</span>
                        </div>
                    </div>  
                </td>
                <td></td>
            `;
            
            tableBody.appendChild(coinTr);
        });

        row_number++;
    });

    tableTwoRenderPagination(data.length, page);
}

function tableTwoRenderPagination(totalRows, page = 1) {
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    const pagination = document.getElementById('table_two_pagination');
    pagination.innerHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === page ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
        li.addEventListener('click', function () {
            table_two_currentPage = i;
            tableTwoRenderTable(table_two_data, table_two_currentPage);
        });
        pagination.appendChild(li);
    }
}

document.getElementById('table_two_searchInput').addEventListener('input', function(event) {
    const searchTerm = event.target.value.toLowerCase();
    if (searchTerm !== "") {
        table_two_search_data = table_two_data.filter(row => row.whale_address.toLowerCase().includes(searchTerm));
        table_two_currentPage = 1;
        tableTwoRenderTable(table_two_search_data, table_two_currentPage);
    } else {
        table_two_currentPage = 1;
        tableTwoRenderTable(table_two_data, table_two_currentPage);
    }
});
