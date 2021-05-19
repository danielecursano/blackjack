from web3 import Web3
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
net = 'ropsten'
url = config[net]['url']
dealer = config[net]['dealer']
contractAddress = config[net]['contract']
private_key = os.environ['PRIVATE_KEY']
abi = [    {      "inputs": [],      "stateMutability": "nonpayable",      "type": "constructor"    },    {      "inputs": [],      "name": "buy",      "outputs": [],      "stateMutability": "payable",      "type": "function"    },    {      "inputs": [        {          "internalType": "address",          "name": "",          "type": "address"        }      ],      "name": "db",      "outputs": [        {          "internalType": "bool",          "name": "",          "type": "bool"        }      ],      "stateMutability": "view",      "type": "function"    },    {      "inputs": [        {          "internalType": "address",          "name": "player",          "type": "address"        }      ],      "name": "retire",      "outputs": [        {          "internalType": "bool",          "name": "",          "type": "bool"        }      ],      "stateMutability": "nonpayable",      "type": "function"    }  ]

w3 = Web3(Web3.HTTPProvider(url))


contract = w3.eth.contract(address=contractAddress, abi=abi)

def checkpass(addr):
    result = contract.functions.retire(addr).call({'from': dealer})

    # Once the function gets called to get boolean if true
    # the player will play and will be sent a transaction to the contact in 
    # order to retire the pass (setting bool to false)

    if result:
        unsigned_txn = contract.functions.retire(addr).buildTransaction({'nonce': w3.eth.get_transaction_count(dealer)})
        signed_txn = w3.eth.account.sign_transaction(unsigned_txn, private_key=private_key)
        w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return result

def pay(addr):
    # if transaction is valid in case of win this function is used
    # to send the player the amount of ether he used doubled
    try:
        transaction = {
            'to': addr,
            'from': dealer,
            'value': w3.toWei(0.009, 'ether'),
            'gas': 200000,
            'gasPrice': 234567821,
            'nonce': w3.eth.get_transaction_count(dealer)
        }
        signed = w3.eth.account.sign_transaction(transaction, private_key)
        w3.eth.send_raw_transaction(signed.rawTransaction)
        return True
    except ValueError:
        # Nonsense try-exception due to the fact this is a personal project
        # As there was an error if the dealer had a pending transaction
        # he couldn't send any rewards
        return False

