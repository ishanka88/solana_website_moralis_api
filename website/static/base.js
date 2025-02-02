
function moralisApi(api_key){;
    const element = document.getElementById('api-key');
    api_key=api_key.data
    element.innerHTML= ` 
       <a class="nav-link text-dark icon-link icon-link-hover" aria-current="page" href="#"> API KEY - ${api_key.slice(0, 5)}.....${api_key.slice(-5)} </a>
    `
}

function findApi(action,api_key) {
    // Construct the URL with both parameters
        const url = `/api_value?action=${encodeURIComponent(action)}&api_key=${encodeURIComponent(api_key)}`;
        
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
                moralisApi(data)
        })
        .catch(error => alert('Error fetching data:', error));
  }

function showconfirmationModal(message) {
    message_element=document.getElementById('confirmationModLabeMessage')
    message_element.innerHTML = `
        <h5 class="modal-title" id="confirmationModLabelLabel">${message}</h5>

    `
    document.getElementById('confirmationModLabel').classList.add('show');
    document.getElementById('confirmationModLabel').style.display = 'block';
    document.body.classList.add('modal-open');
  }
  
function hideconfirmationModal() {
    document.getElementById('confirmationModLabel').classList.remove('show');
    document.getElementById('confirmationModLabel').style.display = 'none';
    document.body.classList.remove('modal-open');
  }

function hideFlashMessage() {
    document.getElementById('flashMessage').classList.remove('show');
    document.getElementById('flashMessage').style.display = 'none';
    document.body.classList.remove('modal-open');
  }

function showApiEnterModal() {
    document.getElementById('apiEnterModal').classList.add('show');
    document.getElementById('apiEnterModal').style.display = 'block';
    document.body.classList.add('modal-open');

    document.getElementById('ApiEnterCancelButton').addEventListener('click', function() { 
        hideApiEnterModal();
      
    });
    
    document.getElementById('ApiEnterOkButton').addEventListener('click', function() { 
        let api = document.getElementById('apiInput').value;
        if (api){
            findApi ("add",api)
        }else{
            alert("Empty Input")
        }

        hideApiEnterModal();

    
    });
    
  }
  
function hideApiEnterModal() {
    document.getElementById('apiEnterModal').classList.remove('show');
    document.getElementById('apiEnterModal').style.display = 'none';
    document.body.classList.remove('modal-open');

}

document.getElementById('getWebsiteTabs').addEventListener('click', function() {
    // Retrieve the value entered in the input field
    const contractAddress = document.getElementById('caTextBox').value;

    // Check if the contract address is not empty
    if (contractAddress) {
        // Construct URLs using the entered contract address (customize this as needed)
        const solscan_url = `https://solscan.io/token/${contractAddress}`;
        const rugcheck_url = `https://rugcheck.xyz/tokens/${contractAddress}`;
        const coinscan_url = `https://www.coinscan.com/solana/${contractAddress}`;
        const dexscreener_url = `https://dexscreener.com/solana/${contractAddress}`;
        const bubblemaps_url = `https://app.bubblemaps.io/sol/token/${contractAddress}`;
        const pumpFun_url = `https://pump.fun/coin/${contractAddress}`;


        // Open the new URLs in separate tabs
        window.open(solscan_url, '_blank');
        window.open(dexscreener_url, '_blank');
        window.open(coinscan_url, '_blank');
        window.open(bubblemaps_url, '_blank');
        window.open(pumpFun_url, '_blank');
        window.open(rugcheck_url, '_blank');

    } else {
        // If no contract address is entered, show an alert
        alert('Please enter a contract address');
    }
});



findApi("get", "isha")

const element = document.getElementById('api-key');
element.addEventListener('click', function() {
    showconfirmationModal("Do you want to change API KEY ?")
});

document.getElementById('confirmationModLabelYesButton').addEventListener('click', function() {
        hideconfirmationModal()
        showApiEnterModal()
  });

document.getElementById('confirmationModLabelCancelButton').addEventListener('click', function() { 
    hideconfirmationModal();
  
});

document.getElementById('flashCloseButton').addEventListener('click', function() { 
    hideFlashMessage();

});


