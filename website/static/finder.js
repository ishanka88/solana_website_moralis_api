const rowsPerPage = 10;
let currentPage = 1;
current_status = "active"


function addPendingSetToActive(rowId){
    let confirmation = confirm("Do you want to Add Coin Data to Database ?");
    if (!confirmation) {
      return;
    }
    let confirmation2 = confirm("Are you Sure?");
    if (!confirmation2) {
      return;
    }

    addOrDeletePendingFolderSets("add", rowId)


}

function deletePendingSetToActive(rowId){
    let confirmation = confirm("DELETE - Do you want to DELETE this Coin Data in pending folder ?");
    if (!confirmation) {
      return;
    }
    let confirmation2 = confirm("Are you Sure?");
    if (!confirmation2) {
      return;
    }
    addOrDeletePendingFolderSets("delete", rowId)


}

function addOrDeletePendingFolderSets(action, rowId) {
    // Prepare the data to send in the request
    const formData = {
      
        "action" : action,
        "rowId" : rowId

    }

    fetch('/add-or-delete-prnding-folder-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData) // Send data as JSON
       
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`Error: ${data.error}`);
        } else {
            window.location.reload(true);
            addSets();  // Reload the page after the response

            alert(data[1]);
        }
    })
    .catch(error => alert('Error uploading data:', error));
}

function addSets(){
    searchCoinSetsCard.classList.add('d-none');
    addSetsCard.classList.remove('d-none');

    fetch(`/get-pending-coin-set-data-list`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data[0]){
            alert ("Error - Fetching data from Pending Folder (Database error)")
        }else{
            const element = document.getElementById('pending_coin_sets');
            if (data[1].length == 0){
                element.innerHTML= ` 
                <div class="d-flex justify-content-around">
                   <span>No Pending Sets AVailable</span>
                </div>
                <div></div>
                
                `
            }else{ 
                element.innerHTML= ` 
                <div >
                    <table class="table  table-bordered border-primary ">
                        <thead class="table-dark">
                            <tr>
                            <th scope="col">#</th>
                            <th scope="col">COIN</th>
                            <th scope="col">PRIORITY</th>
                            <th scope="col">DISCRIPTION</th>
                            <th scope="col">FROM DATE</th>
                            <th scope="col">TO DATE</th>
                            <th scope="col">PROFIT</th>
                            <th scope="col">TXN</th>
                            <th scope="col">ACTION</th>
                            </tr>
                        </thead>
                        <tbody class="b-0" id="pending_coins_tableBody">
                            <!-- Table rows will be dynamically generated here -->
                        </tbody>
                    </table>
                </div>
                
                `
                renderPendingTable(data[1],1)
            }

            
        }

          
    })
    .catch(error => alert('Error while Getting PENDING FOLDER Coin Data :', error));
    
}

function renderPendingTable(data, page = 1) {
    const tableBody = document.getElementById('pending_coins_tableBody');
    tableBody.innerHTML = '';

    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const paginatedData = data.slice(start, end);

    let row_number=start
    paginatedData.forEach(row => {
        const tr = document.createElement('tr');
        tr.setAttribute('id', row.set_number);
        tr.setId
        row_number= row_number+1

        contract_address_icon_html= `
        <i class="bi bi-upc-scan icon-link icon-link-hover" onclick="funSolscanForWallet('${row.contract_address}')"></i>
        `
        from_signature_icon_html = `
        <i class="bi bi-upc-scan icon-link icon-link-hover" onclick="funSolscanForSignature('${row.from_signature}')"></i>
        `
        to_signature_icon_html = `
            <i class="bi bi-upc-scan icon-link icon-link-hover" onclick="funSolscanForSignature('${row.to_signature}')"></i>
        `
        if (row.priority == "buy"){
            priority_html = ` <td class="text-success fw-bold">BUY</td>`
        }else{
            priority_html = ` <td class="text-danger fw-bold">SELL</td>`
        }
        let profit = ((row.peak_value - row.low_value) / row.low_value) * 100;


        tr.innerHTML = `
          <th scope="row">${row_number}</th>
          <td > 
              <div class="d-flex justify-content-around">
                  <div class="mr-3">
                      ${row.ticker}
                  </div>
                  <div>
                      ${contract_address_icon_html}
                  </div>
              </div>
          </td>
          ${priority_html}
          <td>${row.description}</td>
          <td > 
              <div class="d-flex justify-content-around">
                  <div class="mr-3">
                      ${row.searched_from_date_time}
                  </div>
                  <div>
                      ${from_signature_icon_html}
                  </div>
              </div>
          </td>
          <td > 
              <div class="d-flex justify-content-around">
                  <div class="mr-3">
                      ${row.searched_to_date_time}
                  </div>
                  <div>
                      ${to_signature_icon_html}
                  </div>
              </div>
          </td>
          <td class="text-success fw-bold">${parseInt(profit)} %</td>
          <td>${row.txns}</td>
          <td> 
            <div class="d-flex flex-row justify-content-around" >
              <div class=" px-2">
                    <button type="button"  class="btn btn-success" onclick="addPendingSetToActive(${row.id} )" >ADD</button>
              </div>
               <div class=" px-2">
                    <button type="button"  class="btn btn-danger" onclick="deletePendingSetToActive(${row.id} )" >DELETE</button>
              </div>
            </div>
          </td>

        `;
        tableBody.appendChild(tr);

    });

    renderPaginationPendingCoins(data,page)


  }

  function renderPaginationPendingCoins(data, page = 1) {
    totalRows = data.length
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    const pendingCoinPagination = document.getElementById('pendingCoinPagination');
    pendingCoinPagination.innerHTML = '';
  
    for (let i = 1; i <= totalPages; i++) {
      const li = document.createElement('li');
      li.className = `page-item ${i === page ? 'active' : ''}`;
      li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
      li.addEventListener('click', function() {
        currentPage = i;
        renderPendingTable(data, currentPage,current_status);
      });
      pendingCoinPagination.appendChild(li);
    }
  
  }









function searchCoinSets() {
    addSetsCard.classList.add('d-none');
    searchCoinSetsCard.classList.remove('d-none');
}

function funExport() {
    exportData()
}

function manualSubmitCoinSet(){
    let confirmation = confirm("Do you want to Import oin Data to Database ?");
    if (!confirmation) {
      return;
    }
}




function fun1(id) {

    let targetElement = $('#' + id);
    let value = targetElement.closest('.inner-container').find('input').val();
    if (value!=""){
        let url = "https://solscan.io/token/"+ value
        window.open(url, '_blank')
        
    }

}
function fun2(id) {

    let targetElement = $('#' + id);
    let value = targetElement.closest('.inner-container').find('input').val();
    //let inputId = closestInput.attr('id');
    if (value!=""){
        let url = "https://solscan.io/tx/"+ value
        window.open(url, '_blank')
    }

}




// For tables rows
function funSolscanForSignature(signature){

    if (signature!=""){
      let url = "https://solscan.io/tx/"+ signature
      window.open(url, '_blank')
    }  
}
// For tables rows
function funSolscanForWallet(signature){

  if (signature!=""){
    let url = "https://solscan.io/token/"+ signature
    window.open(url, '_blank')
  }  
}
  

function action(element_name,element_id){
      
    if (element_name && element_id ){
        clickTableRow(element_name,element_id)
    }

}


function importData() {
  let confirmation = confirm("Do you want to Import Data to Database ?");
  if (!confirmation) {
    window.location.reload(true);
    return;
  }
  const formData = new FormData();
  const files = document.getElementById('fileInput').files;
  
  for (const file of files) {
      formData.append('files', file);
  }

  fetch('/import-data', {
      method: 'POST',
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      if (data.error) {
          alert(`Error: ${data.error}`);
      } else {
          alert(data.message);
          window.location.reload(true);
      }
  })
  .catch(error => alert('Error uploading data:', error));
}



function exportData() {
  fetch(`/export-data`, {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => {
      // Check if the request was successful
      if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
      }
      // Return the response as a Blob
      return response.blob();
  })
  .then(blob => {
      // Create a URL for the Blob object
      const url = window.URL.createObjectURL(blob);
      
      // Create an anchor element and simulate a click to download the file
      const a = document.createElement('a');
      a.href = url;
      a.download = 'exported_data.zip'; // Set the filename for the downloaded file
      document.body.appendChild(a);
      a.click();
      
      // Clean up and revoke the object URL
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
  })
  .catch(error => {
      // Handle any errors
      console.error('Error fetching data:', error);
      alert('Error fetching data: ' + error.message);
  });
}

function setStatus(set_status) {
  fetch(`/get-data?status=${encodeURIComponent(set_status)}`, {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
        data_set = data.data
        tableInfoUpdate(data.coins_count,data.set_counts , data.status_data)
        renderTable(data.data,page = 1,set_status) // Access the 'data' key in the response
  })
  .catch(error => alert('Error fetching data:', error));
}

function merge(set1, set2) {
  fetch(`/merge?set1=${encodeURIComponent(set1)}&set2=${encodeURIComponent(set2)}`, {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
        if(data.status == true){
          alert ("Merge succes")
          window.location.reload(true);

        }
        if (data.status == false){
            alert(data.message)
        }
        
       // Access the 'data' key in the response
  })
  .catch(error => alert('Error while merging check sets numbers :', error));
}

// function update() {
//   fetch(`/update`, {
//       method: 'GET',
//       headers: {
//           'Content-Type': 'application/json'
//       }
//   })
//   .then(response => response.json())
//   .then(data => {
//         if(data.status == true){
//           alert ("Update succes")
//           window.location.reload(true);
//         }
//         if (data.status == false){
//           alert("Error updating")
//         }
        
//        // Access the 'data' key in the response
//   })
//   .catch(error => alert('Error while merging check sets numbers :', error));
// }



// coin count and set counts update at UI
function tableInfoUpdate(coins_count,set_counts,status_data){
     const element = document.getElementById('details');
     element.innerHTML= ` 
            <ul class="p-1 m-0 align-self-center fw-bold" >
              <span>COINS - ${coins_count} &nbsp;( </span>
              <span class="text-success">  A-${status_data.active_coin_count} &nbsp;</span>
              <span class="text-primary">  P-${status_data.pending_coin_count} &nbsp;</span>
              <span class="text-danger">  R-${status_data.running_coin_count} </span>
              <span> ) </span>
            </ul>
           <ul class="p-1 m-0 align-self-center fw-bold" >
              <span >SETS - ${set_counts} &nbsp;( </span>
              <span class="text-success">  A-${status_data.active_set_count} &nbsp;</span>
              <span class="text-primary">  P-${status_data.pending_set_count} &nbsp;</span>
              <span class="text-danger">  R-${status_data.running_set_count} </span>
              <span> ) </span>
            </ul>
     `

}

function renderPagination(data, page = 1) {

  totalRows = data.length
  const totalPages = Math.ceil(totalRows / rowsPerPage);
  const pagination = document.getElementById('pagination');
  pagination.innerHTML = '';

  for (let i = 1; i <= totalPages; i++) {
    const li = document.createElement('li');
    li.className = `page-item ${i === page ? 'active' : ''}`;
    li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
    li.addEventListener('click', function() {
      currentPage = i;
      renderTable(data, currentPage,current_status);
    });
    pagination.appendChild(li);
  }

}

function renderTable(data, page = 1,status) {
      const tableBody = document.getElementById('tableBody');
      tableBody.innerHTML = '';

      const start = (page - 1) * rowsPerPage;
      const end = start + rowsPerPage;
      const paginatedData = data.slice(start, end);
      // current_status=status
      if (status === "active") {
          action_column = ` 
              <div class="d-flex flex-row justify-content-around">
                <div class="icon-link icon-link-hover">
                    <i class="bi bi-trash  icon-link icon-link-hover" name="delete_active"></i>
                </div>
                <div class="icon-link icon-link-hover">
                  <i class="bi bi-arrow-left-right icon-link icon-link-hover" name="active-to-pending"></i>
                </div>
              </div>
            `
      } else if (status === "pending") {
          action_column = ` 
              <div class="d-flex flex-row justify-content-around">
                <div class="icon-link icon-link-hover">
                    <i class="bi bi-trash  icon-link icon-link-hover" name="delete"></i>
                </div>
                <div class="icon-link icon-link-hover">
                  <i class="bi bi-arrow-left-right icon-link icon-link-hover"  name="pending-to-active"></i>
                </div>
              </div>
            `
      } else {
          action_column = ` 
                <div class="d-flex flex-row justify-content-around ">
                  <div class="icon-link icon-link-hover">
                    <i class="bi bi-trash  icon-link icon-link-hover" name="delete"></i>
                  </div>
                  <div class="icon-link icon-link-hover">
                    <i class="bi bi-arrow-left-right icon-link icon-link-hover"  name="running-to-pending"></i>
                  </div>
                  <div class="icon-link icon-link-hover">
                    <i class="bi bi-info-circle icon-link icon-link-hover" name="info"></i>
                  </div>
                </div>
          `
      }

      let row_number=start
      paginatedData.forEach(row => {
          const tr = document.createElement('tr');
          tr.setAttribute('id', row.set_number);
          tr.setId
          row_number= row_number+1

          contract_address_icon_html= `
          <i class="bi bi-upc-scan icon-link icon-link-hover" onclick="funSolscanForWallet('${row.contract_adress}')"></i>
          `
          from_signature_icon_html = `
          <i class="bi bi-upc-scan icon-link icon-link-hover" onclick="funSolscanForSignature('${row.from_signature}')"></i>
          `
          to_signature_icon_html = `
              <i class="bi bi-upc-scan icon-link icon-link-hover" onclick="funSolscanForSignature('${row.to_signature}')"></i>
          `
          if (row.priority == "buy"){
              priority_html = ` <td class="text-success fw-bold">BUY</td>`
          }else{
              priority_html = ` <td class="text-danger fw-bold">SELL</td>`
          }


          tr.innerHTML = `
            <th scope="row">${row_number}</th>
            <td > 
                <div class="d-flex justify-content-around">
                    <div class="mr-3">
                        ${row.ticker}
                    </div>
                    <div>
                        ${contract_address_icon_html}
                    </div>
                </div>
            </td>
            ${priority_html}
            <td>${row.set_number}</td>
            <td>${row.description}</td>
            <td > 
                <div class="d-flex justify-content-around">
                    <div class="mr-3">
                        ${row.from_date}
                    </div>
                    <div>
                        ${from_signature_icon_html}
                    </div>
                </div>
            </td>
            <td > 
                <div class="d-flex justify-content-around">
                    <div class="mr-3">
                        ${row.to_date}
                    </div>
                    <div>
                        ${to_signature_icon_html}
                    </div>
                </div>
            </td>
            <td class="text-success fw-bold">${row.profit} %</td>
            <td>${row.txn_count}</td>
            <td>${row.valid_txn_count}</td>
            <td>${row.wallet_transfers_count}</td>
            <td>${row.uni_wallets_count}</td>
            <td class="text-success fw-bold">${row.buy_uni_wallet_count}</td>
            <td class="text-danger fw-bold">${row.sell_uni_wallet_count}</td>
            <td> 
                ${action_column}
            </td>
  
          `;
          tableBody.appendChild(tr);
          tr.addEventListener('click', function(event) {
                element_name=event.target.getAttribute('name')
                element_id=event.target.closest('tr').getAttribute('id')
                if(element_name=="delete"){
                    let confirmation = confirm("Do you want to DELETE ?");
                    if (!confirmation) {
                          event.preventDefault();
                          return;
                    }
                    showModal()
                }else if (element_name=="active-to-pending"||element_name=="pending-to-active"||element_name=="running-to-pending"){
                    let confirmation = confirm("Do you want to SHIFT ?");
                    if (!confirmation) {
                          event.preventDefault();
                          return;
                    }
                    showModal()
                }
                if (element_name=="info"){
                    action(element_name,element_id)
                }
          });
  
      });

      renderPagination(data,page)


    }
document.getElementById('searchInput').addEventListener('input', function(event) {
        const searchTerm = event.target.value.toLowerCase();
        if (searchTerm !== "") {
            filteredData = data_set.filter(row => row.ticker.toLowerCase().includes(searchTerm));
            renderTable(filteredData, 1, current_status);
        } else {
            renderTable(data_set, 1, current_status);
        }
      })



function checkFormData() {
        // Retrieve form values
        let wallet = $('#contractAddress').val();
        let fromDateInput = $('#fromDateInput').val();
        let fromHourInput = $('#fromHourInput').val();
        let fromMinuteInput = $('#fromMinuteInput').val();
        let fromSecondInput = $('#fromSecondInput').val();
        let toDateInput = $('#toDateInput').val();
        let toHourInput = $('#toHourInput').val();
        let toMinuteInput = $('#toMinuteInput').val();
        let toSecondInput = $('#toSecondInput').val();
        let coinName = $('#ticker').val();
        let peakValue = parseFloat($('#peakValue').val()); // Convert to number
        let lowValue = parseFloat($('#lowValue').val());   // Convert to number
        let discription =$('#discription').val();
        let priority_value =$('#radio').val();

        
        // Retrieve the selected radio button value
        let priority = $('input[name="radio"]:checked').val(); // Get the value of the checked radio button

        if (wallet.length!=44){
            alert("Incorrect solana wallet address (must be 44 characters)");
            return false

        }

        // Check for empty required fields
        if (wallet === "" || coinName === "" || discription==="") {
            alert("Empty inputs");
            return false
        }

        if (fromDateInput === "" || fromHourInput === "" || fromMinuteInput === "" || toDateInput === ""|| toHourInput === ""|| toMinuteInput === "") {
            alert("Date and time Empty");
            return false
        }

        if ( priority === undefined){
            alert("Priority must be selected");
            return false
        }
  

        // Compare datetime strings
        let fromDatetime = fromDateInput + 'T' + fromHourInput + ':' + fromMinuteInput + ':' + fromSecondInput;
        let toDatetime = toDateInput + 'T' + toHourInput + ':' + toMinuteInput + ':' + toSecondInput;
        
        if (fromDatetime > toDatetime) {
            alert("FROM Date and Time must be earlier than TO Date and Time.");
            return false;
        }
        

        // Confirm if peak and low values are both zero
        if (peakValue === 0 && lowValue === 0) {
              let confirmation = confirm("Both Peak and Low values are zero. Are you sure?");
              if (!confirmation) {
                      return false
              }
              let finalConfirmation = confirm(`Selected priority is ${priority}. Are you sure to continue?`);
              if (!finalConfirmation) {
                      return false
              }
        }else {
              // Validate peak and low values
              if ((peakValue <= 0 && lowValue <= 0) || (peakValue < lowValue) || (peakValue > lowValue && lowValue==0)) {
                  alert("Invalid Peak and low values");
                  return false
                    
              }
              
              // Confirm again if values are valid
              let finalConfirmation = confirm(`Selected priority is ${priority}. Are you sure to continue?`);
              if (!finalConfirmation) {
                  return false
              }

        }

        let finalConfirmation = confirm(` Please Check \n
            From -   ${fromDateInput}    ${fromHourInput.padStart(2, '0')} : ${fromMinuteInput.padStart(2, '0')} : ${fromSecondInput.padStart(2, '0')} \n
            To      -   ${toDateInput}    ${toHourInput.padStart(2, '0')} : ${toMinuteInput.padStart(2, '0')} : ${toSecondInput.padStart(2, '0')} \n\n Are you sure to continue?`);
        if (!finalConfirmation) {
            return false
        }

        return true
    
    }
  


function clickTableRow(element_name, element_id) {
  // Construct the URL with both parameters
      const url = `/table?action=${encodeURIComponent(element_name)}&element_id=${encodeURIComponent(element_id)}`;
      
      fetch(url, {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json'
          }
      })
      .then(response => response.json())
      .then(data => {
              moreInformation(data)
      })
      .catch(error => alert('Error fetching data:', error));
}

function moreInformation(data){
    console.log(data)
    if (data.action=="delete"){
      alert(data.status)
      setStatus(current_status)

    }else if (data.action=="info") {
        renderList(data)
    } else if(data.action=="pending-to-active"){
      alert(data.status)
      setStatus(current_status)
    }else if(data.action=="active-to-pending"){
      alert(data.status)
      setStatus(current_status)
    }else{
      alert("Unknown error (finder.js/moreInformation(data))" )
    }
    
}



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
function showListModel() {
  document.getElementById('listModel').classList.add('show');
  document.getElementById('listModel').style.display = 'block';
  document.body.classList.add('modal-open');
}

function hideListModal() {
  document.getElementById('listModel').classList.remove('show');
  document.getElementById('listModel').style.display = 'none';
  document.body.classList.remove('modal-open');
}




function renderList(data) {
  list=data.data[0]
  const listElement = document.getElementById('listElement');
  listElement.innerHTML = `
    <div class="modal-body">
          <div class="modal-item">
              <strong>CA          :</strong> ${list.contract_address}
          </div>
          <div class="modal-item">
              <strong>Ticker          :</strong> ${list.ticker}
          </div>
          <div class="modal-item">
              <strong>Description :</strong> ${list.description}
          </div>
          <div class="modal-item">
              <strong>Priority :</strong> ${list.priority}
          </div>
          <div class="modal-item">
              <strong>From Sig    :</strong> ${list.from_signature}
          </div>
          <div class="modal-item">
              <strong>To Sig      :</strong> ${list.to_signature}
          </div>
          <div class="modal-item">
              <strong>Current sig :</strong> ${list.current_signature}
          </div>
          <div class="modal-item">
              <strong>Low Value :</strong> ${list.low_value}
          </div>
          <div class="modal-item">
              <strong>Peak Value :</strong> ${list.peak_value}
          </div>
          <div class="modal-item">
              <strong>Status      :</strong> Partially succeeded
          </div>
    </div>
     `

    showListModel()
  }


document.getElementById('okButton').addEventListener('click', function() {
  const password = "isha@123"
  const name = document.getElementById('nameInput').value;
  if (name) {
      if (name == password){
          hideModal();
          action(element_name,element_id)
      }else{
          alert("Invalid Password")
      }
          
  }
});

document.getElementById('cancelButton').addEventListener('click', function() { 
    hideModal();
  
});

document.getElementById('okListButton').addEventListener('click', function() { 
  hideListModal();

});



document.getElementById('mergeButton').addEventListener('click', function(event) {
  // Get the values from the input fields
      let set1 = document.getElementById('set1').value;
      let set2 = document.getElementById('set2').value;

  // Check if both values are not empty
      if (set1.trim() !== "" && set2.trim() !== "") {
          merge(set1, set2);  // Call the merge function with the values
      } else {
          alert("Merge entries cannot be null or empty.");
      }
});

// document.getElementById('updateButton').addEventListener('click', function(event) {
//   update()
// });




document.addEventListener('DOMContentLoaded', function() {

    const navLinks = document.querySelectorAll('#navigation .nav-link');

    navLinks.forEach(function(link) {
      link.addEventListener('click', function() {
          // Remove 'active' class from all nav-link elements within #navigation
          navLinks.forEach(function(link) {
            link.classList.remove('active');
          });
          
          // Add 'active' class to the clicked element
          this.classList.add('active');
          
          // Use a custom data attribute to determine the status
          let status = this.getAttribute('data-status');
          
          if (status === "active") {
            current_status="active"
            setStatus("active");
          } else if (status === "pending") {
            current_status="pending"
            setStatus("pending");
          } else {
            current_status="running"
            setStatus("running");
            
          }
        });
    });
    
    setStatus(current_status);

});



document.addEventListener('DOMContentLoaded', () => {
  // Create a <style> element
  const style = document.createElement('style');
  style.type = 'text/css';

  // Define CSS rules as a string
  const css = `
      .spinner-overlay {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: rgba(255, 255, 255, 0.8); /* Light background to cover content */
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1050; /* Ensure it appears on top of other content */
      }
      
      .d-none {
          display: none;
      }
  `;

  // Add CSS rules to the <style> element
  style.appendChild(document.createTextNode(css));

  // Insert the <style> element into the <head> of the document
  document.head.appendChild(style);
});


document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form_data'); // Match form ID
  const spinner = document.getElementById('spinner');
  const searchButton = document.getElementById('searchButtonInFinder');
  const stopButton = document.getElementById('stopButton');

  let pollInterval;

  searchButton.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default form submission
    check =checkFormData()
    if (!check){
        return
    }

    // Show the spinner
    spinner.classList.remove('d-none');

    // Create FormData object from the form
    const formData = new FormData(form);

    // Convert FormData to a JSON object
    const data = {
        contractAddress: formData.get('contractAddress'),
        fromDate: formData.get('fromDateInput'),
        fromHour: parseInt(formData.get('fromHourInput'), 10),  // Convert to integer
        fromMinute: parseInt(formData.get('fromMinuteInput'), 10),  // Convert to integer
        fromSecond: parseInt(formData.get('fromSecondInput'), 10),  // Convert to integer
        toDate: formData.get('toDateInput'),
        toHour: parseInt(formData.get('toHourInput'), 10),  // Convert to integer
        toMinute: parseInt(formData.get('toMinuteInput'), 10),  // Convert to integer
        toSecond: parseInt(formData.get('toSecondInput'), 10),  // Convert to integer
        priority: formData.get('radio'),
        ticker: formData.get('ticker'),
        lowValue: formData.get('lowValue'),
        discription: formData.get('discription'),
        peakValue: formData.get('peakValue')
    };

    // Send data to the server
    fetch('/start-finding', {
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
        if (result[0]== true){
            console.log(result[1]);
            spinner.classList.add('d-none');  
            alert(result[1]);
        }else{
            console.log(result[1]);
            alert(result[1]); 
            spinner.classList.add('d-none'); 
        }

    })
    .catch(error => {
        console.error('Error:', error);
        spinner.classList.add('d-none'); // Hide the spinner
        alert('Error starting task.'); // Show error message
    });
  });


  stopButton.addEventListener('click', function(event) {

        let finalConfirmation = confirm(` Are you sure to end task?`);
        if (!finalConfirmation) {
                return false
        }
        fetch('/stop-finding', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if(data[0]){
                spinner.classList.add('d-none');
                console.log(data[1]);
                alert(data[1]);
            }else
                console.log(data[1]);
                alert(data[1]);
            // Alert with task stopping status
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error stopping the task.'); // Show error message
        });
  });
});
