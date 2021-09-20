import pandas as pd
import random
import sklearn as sk




class deck:
    """
    Solitaire deck class
    """
    def __init__(self,a=1):
        types = 'Spade','Diamond','Hearts','Clover'
        numbers = 2,3,4,5,6,7,8,9,10,'J','Q','K','A'
        deck = list()
        for j in types:
            for i in numbers:
                deck.append([j,i])
        self.deck = deck * a
        self.len = len(deck)
        
    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self,t = 1):
        if t == 1:
            if self.len <= 0:
                print('Empty deck')
                return None
            else:
                card = self.deck[0]
                del self.deck[0]
                self.len = self.len -1
                return card
        else:
            return [self.draw() for i in range(t)]
        
    def reset(self):
        types = 'Spade','Diamond','Hearts','Clover'
        numbers = 2,3,4,5,6,7,8,9,10,'J','Q','K','A'
        deck = list()
        for j in types:
            for i in numbers:
                deck.append([j,i])
        self.deck = deck
        self.len = len(deck)
        
    def ready(self):
        self.reset()
        self.shuffle()
        
        
class Dealer:
    
    # We will mostly interact wiht only 1 class, which is this one
    
    """ Symbolizes the table """
    
    def __init__(self,players,deck = deck(4)):
        self.deck = deck
        self.hand = 0
        self.count_num = 0
        self.table =[]
        self.amount_players = len(players)
        self.start_deal(players)
        
    def start_deal(self,players):
        self.deck.shuffle()
        
        # Give all players 2 cards from deck
        
        for i in players:
            cards = self.deck.draw(2)
            self.table += cards
            i.set_hand(cards)
        
        # Give the dealer 2 cards
        cards = self.deck.draw(2)
        self.table += cards
        self.hand = cards
        self.count()
        
        
        
    def hit(self,player):
        # give a player a card
        card = self.deck.draw()
        self.table += card
        player.hit(card)
        
        
    def count(self):

        low = [2,3,4,5,6]
        mid = [7,8,9]
        high = [10,'King','Queen','Joker','Ace']
        value = 0
        for i in self.table:
            if i[1] in low:
                value += 1
            if i[1] in mid:
                value += 0
            if i[1] in high:
                value += -1
        self.count_num = value
        return value
    
    def turn(self,player):
        
        pass
            
            

    
class Player:
    
    def __init__(self):
        self.hand=[]
        
        
    def hit(self,card):
        self.hand += card
        
        
    def set_hand(self,cards):
        self.hand = cards
    
    
    def stay(self):
        return 'stay'
    
    def train(self,X,Y):
        pass

player1 = Player(pd.DataFrame())
player2 = Player(pd.DataFrame())

players = [player1,player2]


dealer = Dealer(players)
dealer.__dict__
    
        
deck = deck()

