# poker
Compilation of different poker classes that can be used for simulations or anything related to poker.

Class: deck
  Functions:
    shuffle: 
      Takes no arguments - shuffles the deck and assigns the shuffled deck to the property card_deck. No return
      
    deal_players: 
      Takes one argument, players automatically set to 9. Returns a nested list of all hole cards for given amount of players
      
    flop:
      No arguments - return 3 cards used on the flop
      
    turn:
      No arguments - returns the 1 card on the turn
      
    river:
      No arguments - returns the last card on the river
      
    full_board_deal:
      No argument - returns a full board deal 5 cards
      
      
      
Class: compare_poker
  Functions:
    flush_sort:
      takes arguments hand and board both in list - returns the amount of cards given sorted first by suit then by number in descending order - uses custom quicksort
    
    number_sort:
      takes arguments hand and board both in lists - returns the amount of cards given sorted only by number with no suit attached
    
    straight_flush:
      takes arguments hand and board both in lists - returns a list of the rank which is the highest at 9 and the last card which can be used for ties
      Has a compare function that can take the return values from two straight flushes and outputs 1 if the first given is a higher, 0 if tie and -1 if second is higher
    
    four_of_a_kind:
      takes arguments hand and board both in lists - returns a list of the rank if true, the number of the four of a kind and the kicker
      Has a compare function that can take the return values from two four of a kinds and outputs 1 if the first given is a higher, 0 if tie and -1 if second is higher
    
    full_house:
      takes arguments hand and board both in lists - returns a list of the rank, which number was three of a kind and which number was two of a kind
      Has a compare function that can take the return values from two full houses and outputs 1 if the first given is a higher, 0 if tie and -1 if second is higher
    
    flush:
      takes arguments hand and board both in lists - returns a list of the rank and the highest cards in order in the flush for ties
      Has a compare function that can take the return values from two flushes and outputs 1 if the first given is a higher, 0 if tie and -1 if second is higher
    
    straight:
      takes arguments hand and board both in lists - returns a list of the rank and the last card which can be used for ties
      Has a compare function that can take the return values from two straights and outputs 1 if the first given is a higher, 0 if tie and -1 if second is higher
    
    three_of_a_kind:
      takes arguments hand and board both in lists - returns a list of the rank, the number of the three of a kind, and then the two highest next cards
      Has a compare function that can take the return values from two three of a kinds and outputs 1 if the first given is a higher, 0 if tie and -1 if second is higher
    
    two_pair:
      takes arguments hand and board both in lists - returns a list of the rank, the number of first pair, number of second pair and the kicker
      Has a compare function that can take the return values from two straight flushes and outputs 1 if the first given is a higher, 0 if tie and -1 if second is higher
    
    pair:
      takes arguments hand and board both in lists - returns a list of the rank, the number of the pair, and then a list of all the remaining cards to be used for kicker comparison
      Has a compare function that can take the return values from two straight flushes and outputs 1 if the first given is a higher, 0 if tie and -1 if second is higher
    
    high_card:
      takes arguments hand and board both in lists - returns a list of the rank, the high card, and then a list of the remaining cards
      Has a compare function that can take the return values from two straight flushes and outputs 1 if the first given is a higher, 0 if tie and -1 if second is higher
    
    rank:
      takes arguments hand and board both in lists - returns the highest possible rank in a list
    
    break_tie:
      takes arguments of the outputs of the above functions that have equal rank - uses the compare functions to return 1 if the first given is higher, 0 if tie and -1 if second is higher
    
    winner:
      takes arguments nested lists of players hands and the board - return the number of the winner, 0 indexed, the rank of the hand, and the actual cards


Class: simulation_odds
  Functions:
    unsuited_full_prob:
      takes number of simulations as an argument - writes to a csv the number of times each rank was hit with high card at the beginning for unsuited combinations
    
    suited_full_prob:
      takes number of simulations as an argument - writes to a csv the number of times each rank was hit with high card at the beginning for suited combinations
    
    unsuited_flop_prob:
      takes number of simulations as an argument - writes to a csv the number of times each rank was hit at the flop with high card at the beginning for unsuited combinations, with flush draw, OESD and how many times the board is the highest possible at the end
    
    suited_flop_prob:
      takes number of simulations as an argument - writes to a csv the number of times each rank was hit at the flop with high card at the beginning for unsuited combinations, with flush draw, OESD and how many times the board is the highest possible at the end
    
    unsuited_turn_prob:
      takes number of simulations as an argument - writes to a csv the number of times each rank was hit at the turn with high card at the beginning for unsuited combinations, with flush draw, OESD and how many times the board is the highest possible at the end
    
    suited_flop_prob:
      takes number of simulations as an argument - writes to a csv the number of times each rank was hit at the flop with high card at the beginning for unsuited combinations, with flush draw, OESD and how many times the board is the highest possible at the end
    
    compare_hands:
      takes arguments hand1, hand2 and simulations - prints out how likely it is that hand1 would win this hand based on the number of simulations
    
    best_hand_suited:
      takes arguments number of simulations - writes to a csv that for each combination how likely it is that you win the hand with this pair of cards
    
    best_hand_unsuited:
      takes arguments number of simulations - writes to a csv that for each combination how likely it is that you win the hand with this pair of cards






    
    
    
    
