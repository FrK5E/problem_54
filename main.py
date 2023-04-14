


def detect_tuple( hand: str ):
    items = hand.split() 
    result = []
    for (i,c) in enumerate(items[:-1]):
        n = 0
        for d in items[i+1:]: 
            if c[0]==d[0]:
                n=n+1
        if n>0:
            result.append( (n, c[0] ))
    return result


                


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

    hand1 = line[0:k]
    hand2 = line[k:]

    print( "hand1", hand1, detect_tuple(hand1), "hand2", hand2, detect_tuple(hand2))
    

    return 1


f = open('p054_poker.txt')
lines = f.readlines()


count = 0
for l in lines[0:50]: 
    count = count + player_1_wins( l )


print( count )