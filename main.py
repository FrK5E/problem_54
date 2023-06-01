from __future__ import annotations


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
        self.primary_sign = [100, "N/A"] # related to the ranking of highest artifact
        self.secondary_sign = 0 # related to the ranking of highest card outside of the primary articact 
        (tuples, secondary) = detect_tuples(hand)
        if is_royal_flush(hand): 
            self.primary_sign[0] = 0
            self.secondary_sign = []
        elif is_straight(hand) and is_flush(hand):
            hand1 = sort_cards(hand) 
            self.primary_sign[0] = 1 
            self.primary_sign[1] = values_rank[ hand1[-1][0] ]
        elif len(tuples)>0 and tuples[0][0] == 4: 
            #four of a kind
            self.primary_sign[0] = 2 
            self.primary_sign[1] = values_rank[ tuples[0][1]]
            self.secondary_sign = secondary
        elif len(tuples)==2 and tuples[0][0] == 3:
            #this implies full house
            self.primary_sign[0] = 3
            self.primary_sign[1] = values_rank[ tuples[0][1]]
            self.secondary_sign = values_rank[tuples[1][1]]  
        elif is_flush(hand): 
            self.primary_sign[0] = 4
            hand1 = sort_cards(hand)
            self.primary_sign[1] = values_rank[ hand1[-1][0]]
            self.secondary_sign = values_rank[ hand1[-2][0]]
        elif is_straight(hand):
            self.primary_sign[0] = 5
            hand1 = sort_cards(hand)
            self.primary_sign[1] = values_rank[ hand1[-1][0]]
        elif len(tuples)==1 and tuples[0][0]==3:
            self.primary_sign[0] = 6
            self.primary_sign[1] = values_rank[tuples[0][1]]
            self.secondary_sign = secondary
        elif len(tuples)==2 and tuples[0][0]==2 and tuples[1][0] == 2: 
            self.primary_sign[0] = 7
            self.primary_sign[1] = values_rank[tuples[0][1]]
            self.secondary_sign = values_rank[tuples[1][1]]
        elif len(tuples)==1 and tuples[0][0]==2:
            self.primary_sign[0] = 8
            self.primary_sign[1] = values_rank[tuples[0][1]]
            self.secondary_sign = secondary
        else: 
            hand1 = sort_cards(hand)
            self.primary_sign[0] = 9 
            self.primary_sign[1] = values_rank[hand1[-1][0]]
            self.secondary_sign = values_rank[ hand1[-2][0]]


    def stronger_than( self, other: Ranking ): 
        if  self.primary_sign[0] < other.primary_sign[0]: 
            return True
        elif self.primary_sign[0] == other.primary_sign[0]: 
            if self.primary_sign[1] > other.primary_sign[1]: 
                return True
            elif self.primary_sign[1] == other.primary_sign[1]: 
                return self.__stronger_secondary( other )

        return False 
    
    def getPrimarySign( self ): 
        return self.primary_sign[0]
    
    def __stronger_secondary( self, other: Ranking ): 
        if self.secondary_sign > other.secondary_sign: 
            return True
        elif self.secondary_sign == other.secondary_sign: 
            raise Exception( "same secondary sign, should not happen!")
        return False 



def validate_hand( hand: list[Card]):
    if not len(hand) == len(set(hand)): 
        raise Exception( "validation failed") 


def detect_tuples( hand: list[Card] ):
    validate_hand(hand)
    tuples = []
    singles = []
    trial = {}  
    for c in hand:
        key = c[0]
        if key not in trial:
            trial[key] = set()
        trial[key].add( c )
        
    for k in trial.keys(): 
        if len( trial[k])>1: 
            tuples.append( (len(trial[k]), k[0]) )     

    for k in trial.values():
        if len(k)==1: 
            singles.append( values_rank[list(k)[0][0]])

    tuples = sorted( tuples, key = lambda a: values_rank[a[1]], reverse=True )

    return ( sorted( tuples, key = lambda a: a[0], reverse=True ), sorted( singles, reverse=True ) )

def sort_cards( hand: list[Card] ) -> list[Card]: 
    return sorted( hand, key= lambda a: values_rank[a[0]]) 


def is_flush( hand: list[Card] ) -> bool:
    validate_hand(hand) 
    first_card_suite = hand[0][1]
    for ( i, c) in enumerate( hand[1:]):
        if c[1]!=first_card_suite: 
            return False  
    return True

def is_straight( hand: list[Card]) -> bool:
    validate_hand(hand)
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
        self.assertEqual( detect_tuples(hand=hand)[0], [(2,'2')]  )
        self.assertEqual( detect_tuples(hand=hand)[1], [values_rank['6'], values_rank['5'], values_rank['4']])
        hand = "2C 2S 4H 4C 4S".split()
        self.assertEqual( detect_tuples(hand=hand)[0], [(3,'4'), (2,'2')] )
        hand = "2C 2S 2H 2D 4S".split()
        self.assertEqual( detect_tuples(hand=hand)[0], [(4,'2')] )
        self.assertEqual( detect_tuples(hand=hand)[1], [values_rank['4']] )
        for k in ["2C 2S 3H 3D 4S", "3H 3D 4S 2C 2S" ]: 
            hand = k.split()
            self.assertEqual( detect_tuples(hand=hand)[0], [(2,'3'), (2,'2')] )
            self.assertEqual( detect_tuples(hand=hand)[1], [values_rank['4']] )


    def test_Ranking_1(self): 
        R1 = Ranking( "AH JH KH QH TH".split() ) #royal flush 
        R2 = Ranking( "4C 5C 6C 2C 3C".split() ) #straight 
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 0 )
        self.assertEqual( R2.getPrimarySign(), 1 )

        R1 = Ranking( "4C 5C 6C 7C 3C".split() ) #straight flush 
        R2 = Ranking( "4C 5C 6C 2C 3C".split() ) #straight flush
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 1 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )

        R1 = Ranking( "5C 5H 5S 5D 3C".split() ) #four fives
        R2 = Ranking( "4C 4H 4S 4D 3C".split() ) #four fours 
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 2 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )


        R1 = Ranking( "4C 4H 4S 4D 5C".split() ) #four fours and a five
        R2 = Ranking( "4C 4H 4S 4D 3C".split() ) #four fours and a three
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 2 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )


        R1 = Ranking( "5C 5H 5S 3D 3C".split() ) #full house
        R2 = Ranking( "4C 4H 4S 2D 2C".split() ) #full house
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 3 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )


        R1 = Ranking( "5C 5H 5S 6D 6C".split() ) #full house
        R2 = Ranking( "5C 5H 5S 3D 3C".split() ) #full house
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 3 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )


        R1 = Ranking( "2C 3C 6C 7C 9C".split() ) #flush
        R2 = Ranking( "2H 3H 6H 7H 8H".split() ) #flush
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 4 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )

        R1 = Ranking( "2C 3C 6C 8C 9C".split() ) #flush
        R2 = Ranking( "2H 3H 6H 7H 9H".split() ) #flush
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 4 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )

        R1 = Ranking( "4C 5H 6C 7S 3C".split() ) #straight 
        R2 = Ranking( "4D 5D 6C 2C 3C".split() ) #straight
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 5 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )

        R1 = Ranking( "4C 4H 4S 7S 3C".split() ) #three of a kind 
        R2 = Ranking( "3D 3H 3C 2C TC".split() ) 
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 6 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )

        R1 = Ranking( "4C 4H 4S 8S 3C".split() ) #three of a kind 
        R2 = Ranking( "4C 4H 4S 7S 3C".split() ) 
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 6 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )

        R1 = Ranking( "4C 4H 5S 5D 3C".split() ) #two pairs 
        R2 = Ranking( "4C 4H 2S 2D 3C".split() ) 
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 7 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )

        R1 = Ranking( "4C 4H 5S 5D 3C".split() ) #two pairs 
        R2 = Ranking( "3C 3H 5S 5D TC".split() ) 
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 7 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )

        R1 = Ranking( "4C 4H 5S 8D 3C".split() ) #one pair 
        R2 = Ranking( "3C 3H 5S 9D TC".split() ) 
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 8 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )

        R1 = Ranking( "4C 4H 5S 9D 3C".split() ) #one pair 
        R2 = Ranking( "4C 4H 5S 8D 3C".split() ) 
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 8 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )

        R1 = Ranking( "4C AH 5S 9D 3C".split() ) #high card 
        R2 = Ranking( "4C KH 5S 8D 3C".split() ) 
        self.assertEqual( R1.stronger_than(R2), True )
        self.assertEqual( R2.stronger_than(R1), False )
        self.assertEqual( R1.getPrimarySign(), 9 )
        self.assertEqual( R1.getPrimarySign(), R2.getPrimarySign() )

      


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

    hand1 = line[0:k].split()
    hand2 = line[k:].split()

    k1 = sort_cards( hand1 )
    k2 = sort_cards( hand2 )

    print( "hand1", hand1, "sorted_hand_1", k1 )
    print( "hand1", hand1, detect_tuples(hand1), "hand2", hand2, detect_tuples(hand2))
    

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