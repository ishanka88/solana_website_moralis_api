
// Function to update the UI with the credential file name
function credentials(credential_file_name) {
    const element = document.getElementById('credential_file_name');
    credential_file_name = credential_file_name.data;  // Assuming data contains the file name
    element.innerHTML = ` 
       <a class="nav-link text-dark icon-link icon-link-hover" aria-current="page" href="#"> CREDENTIAL - ${credential_file_name} </a>
    `;
}

// Function to send the credential file to the backend
function findCredential(action, credential_file_name) {
    // Construct the URL with both parameters
    const url = `/credential_value`;

    // Fetch the data from the server
    fetch(url, {
        method: 'POST',  // Use POST to send file data
        headers: {
            'Content-Type': 'application/json',  // Ensure the data is sent as JSON
        },
        body: JSON.stringify({
            action: action,
            file_name: credential_file_name.name,
            file_data: credential_file_name.content  // Sending the file content
        })
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        credentials(data);  // Update the UI with the response
    })
    .catch(error => alert('Error fetching data:', error));
}

// Show confirmation modal before changing the credential file
function showconfirmationModal(message) {
    const message_element = document.getElementById('confirmationModLabeMessage');
    message_element.innerHTML = `
        <h5 class="modal-title" id="confirmationModLabelLabel">${message}</h5>
    `;
    document.getElementById('confirmationModLabel').classList.add('show');
    document.getElementById('confirmationModLabel').style.display = 'block';
    document.body.classList.add('modal-open');
}

// Hide confirmation modal
function hideconfirmationModal() {
    document.getElementById('confirmationModLabel').classList.remove('show');
    document.getElementById('confirmationModLabel').style.display = 'none';
    document.body.classList.remove('modal-open');
}

// Hide flash message
function hideFlashMessage() {
    document.getElementById('flashMessage').classList.remove('show');
    document.getElementById('flashMessage').style.display = 'none';
    document.body.classList.remove('modal-open');
}

// Show the API modal to enter a new credential file
function showApiEnterModal() {
    document.getElementById('credentialEnterModal').classList.add('show');
    document.getElementById('credentialEnterModal').style.display = 'block';
    document.body.classList.add('modal-open');

    // Close the modal when clicking cancel
    document.getElementById('CredentialEnterCancelButton').addEventListener('click', function() { 
        credentialEnterModal();
    });

    // Handle form submission (when file is selected)
    document.getElementById('CredentialEnterSubmitButton').addEventListener('click', function() { 
        let confirmation = confirm("Do you want to change the credential file?");
        if (!confirmation) {
            window.location.reload(true);
            return;
        }
        
        const fileInput = document.getElementById('credentialFileInput');
        const file = fileInput.files[0];  // Only take the first file

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const fileContent = e.target.result;  // Get the content of the file as a string

                // Prepare the data to send to the backend
                const data = {
                    action: 'add',
                    file_name: file.name,
                    file_data: fileContent  // Send the file content as text
                };
                credentialEnterModal();

                fetch('/credential_value', {
                    method: 'POST',  // Use POST instead of GET
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)  // Send as JSON
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    alert(data.message)
                    credentials(data);  // Update the UI with the response
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error uploading file!');
                });
            };

            reader.readAsText(file);  // Read the file as text (since it's JSON)
        } else {
            alert("Please select a file.");
        }
    });

}

// Hide the credential input modal
function credentialEnterModal() {
    document.getElementById('credentialEnterModal').classList.remove('show');
    document.getElementById('credentialEnterModal').style.display = 'none';
    document.body.classList.remove('modal-open');
}

// Initialize page and check if a credential is already set
findCredential("get", "isha");

const element = document.getElementById('credential_file_name');
element.addEventListener('click', function() {
    showconfirmationModal("Do you want to change the credential file?");
});

// Handle confirmation actions for changing credential
document.getElementById('confirmationModLabelYesButton').addEventListener('click', function() {
    hideconfirmationModal();
    showApiEnterModal();  // Show the modal for uploading a new file
});

document.getElementById('confirmationModLabelCancelButton').addEventListener('click', function() { 
    hideconfirmationModal();
});

document.getElementById('flashCloseButton').addEventListener('click', function() { 
    hideFlashMessage();
});


// function credentials(credentil_file_name){;
//     const element = document.getElementById('credential_file_name');
//     credentil_file_name=credentil_file_name.data
//     element.innerHTML= ` 
//        <a class="nav-link text-dark icon-link icon-link-hover" aria-current="page" href="#"> CREDENTIAL - ${credentil_file_name} </a>
//     `
// }







// function findCredential(action,credential_file_name) {
//     // Construct the URL with both parameters
//         const url = `/credential_value?action=${encodeURIComponent(action)}&credential_file_name=${encodeURIComponent(credential_file_name)}`;
        
//         fetch(url, {
//             method: 'GET',
//             headers: {
//                 'Content-Type': 'application/json'
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//                 credentials(data)
//         })
//         .catch(error => alert('Error fetching data:', error));
//   }

// function showconfirmationModal(message) {
//     message_element=document.getElementById('confirmationModLabeMessage')
//     message_element.innerHTML = `
//         <h5 class="modal-title" id="confirmationModLabelLabel">${message}</h5>

//     `
//     document.getElementById('confirmationModLabel').classList.add('show');
//     document.getElementById('confirmationModLabel').style.display = 'block';
//     document.body.classList.add('modal-open');
//   }
  
// function hideconfirmationModal() {
//     document.getElementById('confirmationModLabel').classList.remove('show');
//     document.getElementById('confirmationModLabel').style.display = 'none';
//     document.body.classList.remove('modal-open');
//   }

// function hideFlashMessage() {
//     document.getElementById('flashMessage').classList.remove('show');
//     document.getElementById('flashMessage').style.display = 'none';
//     document.body.classList.remove('modal-open');
//   }

// function showApiEnterModal() {
//     document.getElementById('credentialEnterModal').classList.add('show');
//     document.getElementById('credentialEnterModal').style.display = 'block';
//     document.body.classList.add('modal-open');

//     document.getElementById('CredentialEnterCancelButton').addEventListener('click', function() { 
//         credentialEnterModal();
      
//     });
    
//     document.getElementById('CredentialEnterSubmitButton').addEventListener('click', function() { 
//         let confirmation = confirm("Do you want to Change Credentila file ?");
//         if (!confirmation) {
//           window.location.reload(true);
//           return;
//         }
//         const file = document.getElementById('credentialFileInput').files[0];

//         if (file){
//             findCredential ("add",file)
//         }else{
//             alert("Empty Input")
//         }

//         credentialEnterModal();

    
//     });
    
//   }
  
// function credentialEnterModal() {
//     document.getElementById('credentialEnterModal').classList.remove('show');
//     document.getElementById('credentialEnterModal').style.display = 'none';
//     document.body.classList.remove('modal-open');

// }


// findCredential("get", "isha")

// const element = document.getElementById('credential_file_name');
// element.addEventListener('click', function() {
//     showconfirmationModal("Do you want to change Credential file ?")
// });

// document.getElementById('confirmationModLabelYesButton').addEventListener('click', function() {
//         hideconfirmationModal()
//         showApiEnterModal()
//   });

// document.getElementById('confirmationModLabelCancelButton').addEventListener('click', function() { 
//     hideconfirmationModal();
  
// });

// document.getElementById('flashCloseButton').addEventListener('click', function() { 
//     hideFlashMessage();

// });

