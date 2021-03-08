from brownie import Ticket, accounts
import pytest

#Tests data: (dealer index, player index, amount of transaction and result of event getTicke)

tests = [(
    1,
    2,
    1.0045e18,
    False 
    ),
(
    0,
    1,
    0.0045e18,
    True
)]

@pytest.mark.parametrize("dealer, player, value, result", tests)
def test_event(dealer, player, value, result):
    player = accounts[player]
    dealer = accounts[dealer]
    balance = player.balance()
    contract = player.deploy(Ticket)
    contract.buy(dealer, {'value': value})
    recipe = contract.retire({'from': dealer})
    assert recipe.events['getTicket'][0][0]['checkTicket'] == result

