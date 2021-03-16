import random

class Player:
    """
    class used for player and dealer in blackjack

    @prop value to get the sum of cards in self.cards list
    as card A can be 1 or 11
    """
    def __init__(self):
        self.cards = []

    @property
    def value(self):
        try:
            return sum(self.cards)
        except:
            if 'A' in self.cards:
                for i in range(len(self.cards)):
                    if self.cards[i] == 'A':
                        self.cards[i] = 11
                        if self.value>21:
                            self.cards[i] = 1
            return sum(self.cards)

class BlackJack:
    """
    Attributes: addr = address of the player used to give prize in case of win
                txHash = receipt of transaction made by user to play a game
                deck = 2 deck of 52 card
    """
    def __init__(self, addr, txHash):
        self.address = addr
        self.txHash = txHash
        self.dealer = Player()
        self.players = Player()
        self.cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.deck = {10: 32, 'A': 8, 9: 8, 8: 8, 7: 8, 6: 6, 5: 8, 4: 8, 3: 8, 2: 8} 

    def extract(self):
        """ 
        function to extract card from the deck and check if possible
        method useless as once the game is finished the deck is restored
        """
        card_ext = random.choice(self.cards)
        while self.deck[card_ext] == 0:
            card_ext = random.choice(self.cards)

        self.deck[card_ext] += -1
        return card_ext

    def start_game(self):
        """
        player and dealer are given 2 cards each 
        then the game can start asking the player
        if he wants a card or pass
        """
        self.players.cards = []
        self.dealer.cards = []
        for _ in range(2):
            self.dealer.cards.append(self.extract())
            self.players.cards.append(self.extract())
        return self.dealer.cards, self.players.cards

    def verify(self, finish=0):
        status_dealer = True
        status_player = True

        if self.players.value > 21:
            status_player = False
        if finish == 0:
            return status_player, self.dealer.cards, self.players.cards
        if finish == 1:
            while self.dealer.value < 17:
                self.dealer.cards.append(self.extract())
            if self.dealer.value > 21: 
                if status_player:
                    result = 'WIN'
                    return result, self.dealer.cards, self.players.cards
            if self.players.value > self.dealer.value:
                result = 'WIN'
            if self.players.value == self.dealer.value:
                result = 'DRAW'
            if self.players.value < self.dealer.value:
                result = 'LOSE'
            return result, self.dealer.cards, self.players.cards

        

               
