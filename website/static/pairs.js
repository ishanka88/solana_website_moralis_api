document.getElementsByTagName('body')[0].classList.add('bg-dark');

const rowsPerPage = 5;
let table_one_currentPage = 1;
let table_two_currentPage = 1;

function set_pair(set1, set2, description) {
    fetch(`/set_pair?set1=${encodeURIComponent(set1)}&set2=${encodeURIComponent(set2)}&description=${encodeURIComponent(description)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
          if(data.status == true){
            window.location.reload(true);
            alert ("Succes")

          }
          if (data.status == false){
            alert(data.message)
          }
          
         // Access the 'data' key in the response
    })
    .catch(error => alert('Error fetching data :', error));
  }

  
document.addEventListener('DOMContentLoaded', function() {
    fetch('/get-pairs-data')
        .then(response => response.json())
        .then(data => {
            table_one_data = data.pairs;
            table_two_data = data.whales;


            tableOneRenderTable(table_one_data);
            tableTwoRenderTable(table_two_data);
        })
        .catch(error => console.error('Error fetching data:', error));
});


function deletePair(set1, set2) {
    // Construct the URL with both parameters
        const url = `/delete_pair?set1=${encodeURIComponent(set1)}&set2=${encodeURIComponent(set2)}`;
        
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
                if (data.status){
                    alert("DELETE SUCESSS")
                    window.location.reload(true);

                }else{
                    alert("ERROR- DELETE UNSUCESSS ")
                }
                    
        })
        .catch(error => alert('Error fetching data:', error));
  }
  

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
            <td> 
                <div class="fw-bold">
                    ${row.ticker} 
                </div>
            </td>
            <td> 
                <div class="fw-bold">
                    ${row.description} 
                </div>
            </td>
            <td> 
                <div class="text-success fw-bold" data-value="${row.buy_set_no}">
                    ${row.buy_set_no} 
                </div>
            </td>
            <td> 
                <div class="d-flex flex-row justify-content-between">
                    <div class="text-danger fw-bold" data-value="${row.sell_set_no}">
                        ${row.sell_set_no} 
                    </div>
                    <div class="icon-link icon-link-hover">
                        <i class="bi bi-trash icon-link icon-link-hover" name="delete"></i>
                    </div>
                </div>
            </td>
        `;
        tableBody.appendChild(tr);
        tr.addEventListener('click', function(event) {

            element_name=event.target.getAttribute('name')
            if(element_name=="delete"){
                // Find the closest 'tr' element
                const clickedRow = event.target.closest('tr');

                // Find 'buy' and 'sell' values
                const buyElement = clickedRow.querySelector('.text-success');
                const sellElement = clickedRow.querySelector('.text-danger');

                if (buyElement && sellElement) {
                    pair_number_1 = buyElement.getAttribute('data-value');
                    pair_number_2 = sellElement.getAttribute('data-value');
                }
                let confirmation = confirm("Do you want to DELETE ?");
                if (!confirmation) {
                      event.preventDefault();
                      return;
                }
                showModal()
            }
    
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
            <td > 
                <div class="fw-bold">
                    ${row.ticker} 
                </div>
            <td > 
                <div class="text-success fw-bold">
                    ${row.buy_set_no} 
                </div>
            </td>
            <td > 
                <div class="text-danger fw-bold">
                    ${row.sell_set_no} 
                </div>
            </td>
        `;
        tableBody.appendChild(tr);
    
        row.whales.forEach(whale => {
            let whaleTr = document.createElement('tr');
            whaleTr.innerHTML = `
                <th scope="row"></th>
                <td > 
                    <div class="fw-bold">
                        ${whale.whale_adress} 
                    </div>
                <td></td>
                <td> </td>
            `;
            tableBody.appendChild(whaleTr);
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
        // Filter rows where any whale's address matches the search term
        table_two_search_data = table_two_data.filter(row =>
            row.whales.some(whale =>
                whale.whale_adress.toLowerCase().includes(searchTerm)
            )
        );
        table_two_currentPage = 1;
    } else {
        table_two_search_data = table_two_data;
        table_two_currentPage = 1;
    }
    
    tableTwoRenderTable(table_two_search_data, table_two_currentPage);
});



document.getElementById('okButton').addEventListener('click', function() {
    const password = "isha@123"
    const name = document.getElementById('nameInput').value;
    if (name) {
        if (name == password){
            hideModal();
            deletePair(pair_number_1,pair_number_2)
        }else{
            alert("Invalid Password")
        }
            
    }
  });

document.getElementById('cancelButton').addEventListener('click', function() { 
    hideModal();
  
});

function showModal() {
    document.getElementById('nameModal').classList.add('show');
    document.getElementById('nameModal').style.display = 'block';
    document.body.classList.add('modal-open');
}
  
function hideModal() {
    document.getElementById('nameModal').classList.remove('show');
    document.getElementById('nameModal').style.display = 'none';
    document.body.classList.remove('modal-open');
}


document.getElementById('setPairButton').addEventListener('click', function(event) {

    // Get the values from the input fields
    let set1 = document.getElementById('set1').value;
    let set2 = document.getElementById('set2').value;
    let description = document.getElementById('description').value;
    // Check if both values are not empty
    if (set1.trim() !== "" && set2.trim() !== "" && description.trim() !== "") {
        let finalConfirmation = confirm(`Are you sure to continue?`);
        if (!finalConfirmation) {
            event.preventDefault();
            return;
        }
        set_pair(set1, set2, description);  // Call the merge function with the values
    } else {
        alert("Pairing entries cannot be null or empty.");
    }
});
