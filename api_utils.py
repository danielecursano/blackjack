from web3 import Web3
import os

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/4ef94712ce884095ad5a2404003f36e5'))
dealer = '0x997515C1CA7a0F2cCf670d215765B1bAf11FeCD7'
db = 'receiptDB'

contractAddress = '0xeBEee8BBF68887666059a4F86B1Fed12c8BB58b2'
key = os.environ['PRIVATE_KEY']


def pay(addr, txHash):
    """
    if transaction is valid in case of win this function is used
    to send the player the amount of ether he used doubled
    """
    if verify_transaction(txHash, addr):
        transaction = {
            'to': addr,
            'from': dealer,
            'value': w3.toWei(0.009, 'ether'),
            'gas': 200000,
            'gasPrice': 234567821,
            'nonce': w3.eth.get_transaction_count(dealer)
        }
        signed = w3.eth.account.sign_transaction(transaction, key)
        w3.eth.send_raw_transaction(signed.rawTransaction)
        return True
    return False

def verify_transaction(txHash, addr):
    """
    The transaction made by the user is been verified getting sender and recipient
    and the value of transaction
    """
    if read_hashes(txHash):
        return False
    transaction = w3.eth.get_transaction(txHash)    
    append_hash(txHash)
    try:
        if transaction['to'] == contractAddress and transaction['value'] == 4500000000000000:
            return True
        return False
    except:
        return False

def append_hash(txHash):
    with open(db, 'a') as file:
        file.write(txHash+'\n')

def read_hashes(txHash):
    with open(db, 'r') as file:
        data = file.read().split('\n')

    if txHash in data:
        return True
    return False
