from brownie import Ticket, accounts

def main():
    acc = accounts.load('0x5c0334D027A6273E33Ac177440B0624987F378D0')
    Ticket.deploy({'from': acc})
