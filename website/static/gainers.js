document.getElementsByTagName('body')[0].classList.add('bg-dark');

function addGainers() {
    addGainersCard.classList.remove('d-none');
}
function cancelAddingGainers() {
    addGainersCard.classList.add('d-none');
}


function fun1(id) {

    let targetElement = $('#' + id);
    let value = targetElement.closest('.inner-container').find('input').val();
    if (value!=""){
        let url = "https://solscan.io/token/"+ value
        window.open(url, '_blank')
        
    }
}

// Add Gainers
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form_data'); // Match form ID
    const submitButton = document.getElementById('submitButtonAddingGainers');
  
    submitButton.addEventListener('click', function(event) {
      event.preventDefault(); // Prevent default form submission
      let contractAddress = $('#contractAddress').val();
      let walletAddress = $('#walletAddress').val();
      let ticker = $('#ticker').val();
      let gainedProfit = parseInt($('#gainedProfit').val(), 10);
      check =checkFormData(contractAddress,walletAddress,ticker,gainedProfit)
      if (!check){
          return
      }
      
                    // Confirm again if values are valid
      let finalConfirmation = confirm(`Are you sure to continue?`);
      if (!finalConfirmation) {
            return false
      }

      // Convert FormData to a JSON object
      const data = {
          contractAddress: contractAddress,
          walletAddress: walletAddress,
          ticker: ticker,
          gainedProfit: gainedProfit  // Convert to integer
      };
      // Send data to the server
      fetch('/add-gainers', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data) // Send data as JSON
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(result => {
              console.log(result[1]);
              alert(result[1]);
      })
      .catch(error => {
          console.error('Error:', error);
          alert('Error starting task.'); // Show error message
      });
    });
});  


function checkFormData(contractAddress,walletAddress,ticker,gainedProfit) {

    if (contractAddress.length!=44){
        alert("Incorrect coin Contract address (must be 44 characters)");
        return false

    }

    if (walletAddress.length!=44){
        alert("Incorrect gainer wallet address (must be 44 characters)");
        return false

    }

    // Check for empty required fields
    if (contractAddress === "" || walletAddress === "" || ticker === "" || gainedProfit=== "") {
        alert("Empty inputs");
        return false
    }


    // Confirm if peak and low values are both zero
    if (gainedProfit === 0 ) {
        alert(" Gain profit can't be zero");
        return false

    }

    return true 

}


//////////////////////////////////////////////////////////////


/// Table data rendering
const rowsPerPage = 10;
let table_one_currentPage = 1;

document.addEventListener('DOMContentLoaded', function() {
    fetch('/get-whale-gainers-data')
        .then(response => response.json())
        .then(data => {
            table_one_data = data[0]
            tableOneRenderTable(table_one_data);

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
                <div class="d-flex flex-row justify-content-start">
                  <div class="fw-bold">
                      <span>${row.walletAddress}</span>
                  </div>
                </div>
            </td>
            <td  >
                <div class="d-flex justify-content-start">
                    <div class="fw-bold">
                      <span>Total Coins - ${row.count}</span>
                    </div>
                </div> 
            </td>
            <td  >
                <div class="d-flex justify-content-end">
                    <div class="fw-bold">
                      <span>Total Profit -  ${row.totalProfit.toLocaleString()}</span>
                    </div>
                </div> 
            </td>
        `;
        tableBody.appendChild(tr);

        row.data.forEach(coin => {
            let whaleTr = document.createElement('tr');
            whaleTr.innerHTML  = `
                <th scope="row"></th>
                
                <td >
                    <div class="d-flex flex-row justify-content-between">
                    </div>
                </td>
                <td >
                    <div class="d-flex flex-row justify-content-start fw-bold"">
                        <div>
                            <span>${coin.ticker}</span>
                        </div>
                    </div>
                </td>
                <td>
                    <div class="d-flex justify-content-end" >
                        <div class="text-success fw-bold">
                            <span>${coin.gainedProfit.toLocaleString()}</span>
                        </div>
                    </div>
                </td>
            `;

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
        table_one_search_data = table_one_data.filter(row => row.walletAddress.toLowerCase().includes(searchTerm));
        table_one_currentPage = 1;
        tableOneRenderTable(table_one_search_data, table_one_currentPage);
    } else {
        table_one_currentPage = 1;
        tableOneRenderTable(table_one_data, table_one_currentPage);
    }
});
