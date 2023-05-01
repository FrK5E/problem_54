


def get_values_rank():
    values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    valuesR = {}
    for (i,v) in enumerate(values):
        valuesR[v] = i
    return valuesR


values_rank = get_values_rank()

Card = str

class Ranking: 
    def __init__(self, hand ): 
        self.primary_sign = 100
        tuples = detect_tuple(hand)
        if is_royal_flush(hand): 
            self.primary_sign = 0
            self.secondary_sign = []
        elif is_straight(hand) and is_flush(hand):
            hand1 = sort_cards(hand) 
            self.primary_sign = 1 
            self.secondary_sign = values_rank[ hand1[0][0] ]
        


def detect_tuple( hand: list[Card] ):
    result = []
    trial = {}  
    for c in hand:
        key = c[0]
        if key not in trial:
            trial[key] = set()
        trial[key].add( c )
        
    for k in trial.keys(): 
        if len( trial[k])>1: 
            result.append( (len(trial[k]), k[0]) )     

    return sorted( result, key = lambda a: a[0] )

def sort_cards( hand: list[Card] ) -> list[Card]: 
    return sorted( hand, key= lambda a: values_rank[a[0]]) 


def is_flush( hand: list[Card] ) -> bool: 
    first_card_suite = hand[0][1]
    for ( i, c) in enumerate( hand[1:]):
        if c[1]!=first_card_suite: 
            return False  
    return True

def is_straight( hand: list[Card]) -> bool:
    hand2 = sort_cards( hand ) 
    k = values_rank[hand2[0][0]]
    for (i,c) in enumerate( hand2[1:]):
        k1 = values_rank[c[0]]
        if k+i+1 != k1: 
            return False
    return True


def is_royal_flush( hand: list[Card]) -> bool: 
    hand2 = sort_cards(hand)
    return is_straight(hand2) and is_flush(hand2) and hand2[-1][0]=='A'


import sys
import unittest

class Tests(unittest.TestCase):

    def test_sort1(self):
        hand = "JC QS JH 2C 6S".split()
        hand1 = sort_cards( hand )
        self.assertEqual(hand1, "2C 6S JC JH QS".split())

    def test_is_flush(self):
        hand = "JC QS JH 2C 6S".split()
        self.assertEqual(is_flush(hand), False)
        hand = "JC QC 2C 7C 6C".split()
        self.assertEqual( is_flush(hand), True )

    def test_is_straight(self):
        hand = "2C 3S 4H 5C 6S".split()
        self.assertEqual( is_straight(hand=hand), True )
        hand = "4H 5C 6S 2C 3S".split()
        self.assertEqual( is_straight(hand=hand), True )
        hand = "2C 3S 4H 5C AS".split()
        self.assertEqual( is_straight(hand=hand), False )

    def test_is_royal_flush(self):
        hand = "2C 3S 4H 5C 6S".split()
        self.assertEqual( is_royal_flush(hand=hand), False )
        hand = "AH JH KH QH TH".split()
        self.assertEqual( is_royal_flush(hand=hand), True )

    def test_detect_tuple(self): 
        hand = "2C 2S 4H 5C 6S".split()
        self.assertEqual( detect_tuple(hand=hand), [(2,'2')]  )
        hand = "2C 2S 4H 4C 4S".split()
        self.assertEqual( detect_tuple(hand=hand), [(2,'2'), (3,'4')] )
      


#def get_rank( hand: str ): 
    # 1: high card
    # 2: one pair 
    # 3: two pairs 
    # 4: three of a kind 
    # 5: straight

def get_ranking( hand: list[Card]):
    return 0



def player_1_wins( line ): 
    suits = [ 'H', 'C', 'S', 'D'] # Hearts, Clubs, Spades, Diamonds
    values = [ '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    k = len(line) // 2

    list1 = line[0:k]
    list2 = line[k:]

    k1 = sort_cards( list1.split() )
    k2 = sort_cards( list2.split() )

    print( "hand1", list1, "sorted_hand_1", k1 )
    print( "hand1", list1, detect_tuple(list1), "hand2", list2, detect_tuple(list2))
    

    return 1

if __name__=="__main__":

    r = unittest.main( exit=False, failfast=True)
    if len(r.result.failures) or len(r.result.errors)>0: 
        sys.exit(1) 


    f = open('p054_poker.txt')
    lines = f.readlines()


    count = 0
    for l in lines[0:50]: 
        count = count + player_1_wins( l )


    print( count )