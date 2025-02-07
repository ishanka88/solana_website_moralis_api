document.getElementsByTagName('body')[0].classList.add('bg-dark');

const rowsPerPage = 5;

let whaleTableCurrentPage = 1;

document.addEventListener('DOMContentLoaded', function() {
    fetch('/get-whales-data')
        .then(response => response.json())
        .then(data => {
            whale_maian_table_data = data.whales;

            active_coin_count = data.status_data.active_coin_count
            active_set_count = data.status_data.active_set_count

            RenderWhaleTable(whale_maian_table_data);


            const countElment = document.getElementById('counts');
            countElment.innerHTML = `
                COINS - ${active_coin_count} &nbsp;&nbsp;&nbsp;   SETS - ${active_set_count}
            `;
        })
        .catch(error => console.error('Error fetching data:', error));
});



// whale two

function RenderWhaleTable(data, page = 1) {
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
                <th scope="row">
                        <div class="icon-link-hover "> 
                            <a class="icon-link icon-link-hover" href="https://solscan.io/account/${row.whale_address}?token_address=${coin.coin_address}#balanceChanges" target="_blank">
                                <i class="bi bi-upc-scan fs-5"></i>
                                <svg class="bi" aria-hidden="true"><use xlink:href="#arrow-right"></use></svg>
                            </a>
                        </div>
                 
                </th>
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
                <td>
                
                </td>
            `;
            
            tableBody.appendChild(coinTr);
        });

        row_number++;
    });

    WhaleTableRenderPagination(data.length, page);
}

function WhaleTableRenderPagination(totalRows, page = 1) {
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    const pagination = document.getElementById('table_two_pagination');
    pagination.innerHTML = '';  // Clear previous pagination

    // Number of pages to display at once
    const pagesToShow = 10;
    const startPage = Math.floor((page - 1) / pagesToShow) * pagesToShow + 1;
    const endPage = Math.min(startPage + pagesToShow - 1, totalPages);

    // Create a wrapper for the pagination content
    const paginationWrapper = document.createElement('div');
    paginationWrapper.className = 'd-flex justify-content-center align-items-center mt-4';  // Flex container for centering

    // Create the pagination component
    const paginationContainer = document.createElement('nav');
    paginationContainer.className = 'pagination';

    // Add Previous button
    const prevButton = document.createElement('li');
    prevButton.className = `page-item ${page === 1 ? 'disabled' : ''}`;  // Disable if on the first page
    prevButton.innerHTML = `<a class="page-link" href="#" aria-label="Previous">Previous</a>`;
    prevButton.addEventListener('click', function (e) {
        e.preventDefault();
        if (page > 1) {
            whaleTableCurrentPage = page - 1;
            RenderWhaleTable(whale_maian_table_data, whaleTableCurrentPage);
        }
    });
    paginationContainer.appendChild(prevButton);

    // Render Page Numbers in a row (only show 10 pages at once)
    for (let i = startPage; i <= endPage; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === page ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
        li.addEventListener('click', function (e) {
            e.preventDefault();
            whaleTableCurrentPage = i;
            RenderWhaleTable(whale_maian_table_data, whaleTableCurrentPage);
        });
        paginationContainer.appendChild(li);
    }

    // Add Next button
    const nextButton = document.createElement('li');
    nextButton.className = `page-item ${page === totalPages ? 'disabled' : ''}`;  // Disable if on the last page
    nextButton.innerHTML = `<a class="page-link" href="#" aria-label="Next">Next</a>`;
    nextButton.addEventListener('click', function (e) {
        e.preventDefault();
        if (page < totalPages) {
            whaleTableCurrentPage = page + 1;
            RenderWhaleTable(whale_maian_table_data, whaleTableCurrentPage);
        }
    });
    paginationContainer.appendChild(nextButton);

    // Add Page Info (e.g., "Page 1 of 213") with blue color and bold
    const pageInfo = document.createElement('span');
    pageInfo.className = 'ms-3 text-warning fw-bold mx-3';  // Add blue color and bold
    pageInfo.innerHTML = `Page ${page} of ${totalPages}`;
    paginationWrapper.appendChild(pageInfo);

    // Append everything to the pagination wrapper
    paginationWrapper.appendChild(paginationContainer);
    pagination.appendChild(paginationWrapper);
}



document.getElementById('table_two_searchInput').addEventListener('input', function(event) {
    const searchTerm = event.target.value.toLowerCase();
    if (searchTerm !== "") {
        table_two_search_data = whale_maian_table_data.filter(row => row.whale_address.toLowerCase().includes(searchTerm));
        whaleTableCurrentPage = 1;
        RenderWhaleTable(table_two_search_data, whaleTableCurrentPage);
    } else {
        whaleTableCurrentPage = 1;
        RenderWhaleTable(whale_maian_table_data, whaleTableCurrentPage);
    }
});
