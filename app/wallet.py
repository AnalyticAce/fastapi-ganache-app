from web3 import Web3

GANACHE_URL = "http://127.0.0.1:8545"

web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if web3.is_connected():
    print("Connected to Ganache")
else:
    print("Could not connect to Ganache")

def generate_wallet():
    wallet = web3.eth.account.create()
    print("Wallet address", wallet.address)
    print("Wallet private key", wallet.key.hex())
    return wallet

def get_balance(address):
    balance = web3.eth.get_balance(address)
    eth_balance = web3.from_wei(balance, "ether")
    return eth_balance, balance

def send_transaction(sender, receiver, private_key, amount):
    nonce = web3.eth.get_transaction_count(sender)
    tx = {
        'nonce': nonce,
        'to': receiver,
        'value': web3.to_wei(amount, "ether"),
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
    }
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print("Transaction sent", tx_hash.hex())
    return tx_hash.hex()