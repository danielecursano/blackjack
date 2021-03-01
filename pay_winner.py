from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/id_testing'))
dealer = '0x997515C1CA7a0F2cCf670d215765B1bAf11FeCD7'
key = 'private_key'

def pay(addr):
    transaction = {
        'to': addr,
        'from': dealer,
        'value': w3.toWei(0.01, 'ether'),
        'gas': 200000,
        'gasPrice': 234567821,
        'nonce': w3.eth.get_transaction_count(dealer)
}
    signed = w3.eth.account.sign_transaction(transaction, key)
    w3.eth.send_raw_transaction(signed.rawTransaction)
    return True


