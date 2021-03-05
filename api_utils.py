from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/4ef94712ce884095ad5a2404003f36e5'))
dealer = '0x997515C1CA7a0F2cCf670d215765B1bAf11FeCD7'
with open('/home/daniele/Documenti/bc/test', 'r') as file:
    key = file.read()

key = key.split('\n')[1]

def pay(addr, txHash):
    if verify_transaction(txHash, addr):
        transaction = {
            'to': addr,
            'from': dealer,
            'value': w3.toWei(0.09, 'ether'),
            'gas': 200000,
            'gasPrice': 234567821,
            'nonce': w3.eth.get_transaction_count(dealer)
        }
        signed = w3.eth.account.sign_transaction(transaction, key)
        w3.eth.send_raw_transaction(signed.rawTransaction)
        return True
    return False

def verify_transaction(txHash, addr):
    transaction = w3.eth.get_transaction(txHash)
    try:
        if transaction['from'] == addr and transaction['to'] == dealer:
            if w3.fromWei(transaction['value'], 'ether') > 0.0044:
                return True
        return False
    except:
        return False
