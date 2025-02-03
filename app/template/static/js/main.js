async function generateWallet() {
    try {
        const response = await fetch('/api/generate-wallet/', { method: 'POST' });
        const wallet = await response.json();
        
        document.getElementById('wallet-result').innerHTML = `
            <p>Address: <strong>${wallet.address}</strong></p>
            <p>Private Key: <input type="password" value="${wallet.private_key}" 
                class="form-control" readonly></p>
            <div class="alert alert-warning mt-2">
                ⚠️ Save this private key securely!
            </div>
        `;
    } catch (error) {
        alert('Error generating wallet: ' + error);
    }
}

async function getBalance() {
    const address = document.getElementById('address').value;
    if (!address) return alert('Please enter an address');
    
    try {
        const response = await fetch(`/api/balance/${address}`);
        const balance = await response.json();
        
        document.getElementById('balance-result').innerHTML = `
            <p>ETH Balance: <strong>${balance.eth_balance}</strong></p>
            ${balance.balance ? `<p>USD Value: $${balance.balance}</p>` : ''}
        `;
    } catch (error) {
        alert('Error fetching balance: ' + error);
    }
}

async function sendTransaction() {
    const transactionData = {
        sender: document.getElementById('sender').value,
        receiver: document.getElementById('receiver').value,
        private_key: document.getElementById('privateKey').value,
        amount: parseFloat(document.getElementById('amount').value)
    };
    console.log('Transaction Data:', transactionData);
    try {
        const response = await fetch('/api/send-transaction/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(transactionData)
        });
        
        const result = await response.json();
        
        document.getElementById('transaction-result').innerHTML = `
            <div class="alert alert-success">
                Transaction successful! Hash: ${result.transaction_hash}
            </div>
        `;
    } catch (error) {
        document.getElementById('transaction-result').innerHTML = `
            <div class="alert alert-danger">
                Error: ${error.message}
            </div>
        `;
    }
}