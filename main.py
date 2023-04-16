


def get_values_rank():
    values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    valuesR = {}
    for (i,v) in enumerate(values):
        valuesR[v] = i
    return valuesR


values_rank = get_values_rank()

Card = str

def detect_tuple( cards: list[Card] ):
    result = [] 
    for (i,c) in enumerate(cards[:-1]):
        n = 1
        for d in cards[i+1:]: 
            if c[0]==d[0]:
                n=n+1
        if n>1:
            result.append( (n, c[0] ))
    return result

def sort_cards( hand: list[Card] ) -> list[Card]: 
    return sorted( hand, key= lambda a: values_rank[a[0]]) 

def is_flush( hand: list[Card] ) -> bool: 
    first_card_suite = hand[0][1]
    for ( i, c) in enumerate( hand[1:]):
        if i[1]!=first_card_suite: 
            return False  
    return True

def is_straight( hand: list[Card]) -> bool: 
    k = values_rank[hand[0][0]]
    for (i,c) in enumerate( hand[1:]):
        k1 = values_rank[c[0]]
        if k+i+1 != k1: 
            return False
    return True




import sys
import unittest

class Tests(unittest.TestCase):

    def test_sort1(self):
        hand = "JC QS JH 2C 6S".split()
        hand1 = sort_cards( hand )
        self.assertEqual(hand1, "2C 6S JC JH QS".split())



#def get_rank( hand: str ): 
    # 1: high card
    # 2: one pair 
    # 3: two pairs 
    # 4: three of a kind 
    # 5: straight



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
    if len(r.result.failures)>0: 
        sys.exit(1) 


    f = open('p054_poker.txt')
    lines = f.readlines()


    count = 0
    for l in lines[0:50]: 
        count = count + player_1_wins( l )


    print( count )