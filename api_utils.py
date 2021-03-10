from web3 import Web3
import os
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
url = config['cheapeth']['url']
dealer = config['cheapeth']['dealer']
contractAddress = config['cheapeth']['contract']

w3 = Web3(Web3.HTTPProvider(url))
db = 'receiptDB'
key = os.environ['PRIVATE_KEY']


def pay(addr, txHash):
    """
    if transaction is valid in case of win this function is used
    to send the player the amount of ether he used doubled
    """
    try:
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
    except ValueError:
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
        print(txHash, data, data.index(txHash))
        return True
    return False
