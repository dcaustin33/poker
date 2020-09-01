
import random
import numpy as np
import csv

class deck:
    def __init__(self): #basic initialization of a deck of cards
        self.suits = ['C', 'S', 'D', 'H']
        self.numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.card_deck = []
        self.board_cards = []
        
    def shuffle(self): #inserts each card into a list and then uses random shuffle to shuffle
        cards = []
        self.board_cards = []
        for suit in self.suits: 
            for number in self.numbers:
                card = suit + str(number)
                cards.append(card)
        random.shuffle(cards)
        self.card_deck = cards
        
    def deal_players(self, players = 9): #deals two cards to each of the parameterized players by popping off the deck
        players_cards = []
        self.shuffle() #calls shuffle function no downside if it has already been shuffled
        for i in range(players):
            players_cards.append([self.card_deck.pop()])
        for i in range(players):
            players_cards[i].append(self.card_deck.pop())
        return players_cards
    
    def flop(self): #deals the flop by popping a card
        for i in range(3):
            self.board_cards.append(self.card_deck.pop())
        return self.board_cards
        
    def turn(self):#see above
        self.board_cards.append(self.card_deck.pop())
        return self.board_cards
    
    def river(self):#see above
        self.board_cards.append(self.card_deck.pop())
        return self.board_cards
    
    def full_board_deal(self):#does allc at once
        for i in range(5):
            self.board_cards.append(self.card_deck.pop())
        return self.board_cards
    



class compare_poker: #class to classify hands and ultimately determine best hand
    def flush_sort(self, hand, board): #insertion sort descending by number and suit after already sorting by suit using .sort
        new = board + hand
        new.sort()#strings so sorts according to the first character then have to sort by number
        for element in range(1, len(new)): #insertion sort
            j = element - 1
            while (j >= 0 and int(new[j + 1][1:]) > int(new[j][1:])) and new[j + 1][0] == new[j][0]:
                first = new[j + 1]
                second = new[j]
                new[j] = first
                new [j + 1] = second
                j -= 1
        return new

    def number_sort(self, hand, board): #insertion sort but strictly for numbers
        first = hand + board
        new = []
        for element in first:
            new.append(int(element[1:]))#just takes the number
        for element in range(1, len(new)):
            j = element - 1
            while (j >= 0 and new[j + 1] > new[j]):
                first = new[j + 1]
                second = new[j]
                new[j] = first
                new [j + 1] = second
                j -= 1
        return new

    def straight_flush(self, hand1, board):#returns a list if true with the highest ranking otherwise just boolean
        #royal flush check not necessary as royal flush is simply the highest straight flush
        first_total = hand1 + board
        total = self.flush_sort(hand1, board)
        cards_row = 1
        suit = ''
        number = 0

        for element in total:
            if element[0] == suit and number - 1 == int(element[1:]):
                cards_row += 1
                number -= 1
            else:
                cards_row = 1
                suit = element[0]
                number = int(element[1:])
            if cards_row == 5:
                return [9, int(element[1:])]
            if cards_row == 4 and int(element[1:] == 2) and str(suit + '14') in total:
                return [9, int(element[1:])]

        return False
    
    def straight_flush_compare(self, rank1, rank2): #comparison if two hands both have a straight flush
        #checks who has the higher card
        if rank1[1] > rank2[1]: return 1
        if rank1[1] == rank2[1]: return 0
        if rank1[1] < rank2[1]: return -1

    def four_of_a_kind(self, hand1, board):#checks if there is a four of a kind
        total = self.number_sort(hand1, board)
        same_num = 1 #counts how many times same card in the hand
        prev_num = 0 #placeholder to hold which card is currently being counted
        highest_num = [] #list to find the highest kicker

        for element in total: #finds the best kicker
            if element not in highest_num: highest_num.append(element)

        for element in total:
            if element == prev_num: same_num += 1 # if same as placeholder increment
            else:  #otherwise reinitialize the prev num to the current number and go back to 1
                same_num = 1
                prev_num = element
            if same_num == 4: #if four of a kind will stop the loop and return
                if len(total) > 4:
                    if highest_num[0] == prev_num: #checks to implement the correct kicker
                        kicker = highest_num[1]
                    else: kicker = highest_num[0]
                else: kicker = 0
                    
                return [8, prev_num, kicker] #returns the relative strength, the number that has four of a kind and the kicker
        return False
    
    def four_of_a_kind_compare(self, rank1, rank2):#compares through first checking the number and then checks the kicker
        #returns -1 if rank2 wins or 1 if rank1 wins or 0 if there was a tie
        if rank1[1] > rank2[1]: 
            return 1
        if rank1[1] == rank2[1]:
            if rank1[2] > rank2[2]:
                return 1
            if rank1[2] == rank2[2]:
                return 0
            if rank1[2] < rank2[2]:
                return -1
        if rank1[1] < rank2[1]:
            return -1

    def full_house(self, hand1, board): #checks for a full house
        total = hand1 + board
        numbers = []
        for element in total: #strictly dependent on numbers so no need for suits
            numbers.append(int(element[1:]))

        three = [False, 0] #placeholder for if there is three of a kind anywhere and what number it is
        two = [False, 0]

        for num in numbers:
            if numbers.count(num) == 3: #uses .count to count if there is a three of a kind in numbers
                three = [True, num]
                numbers = list(filter(lambda a: a != num, numbers))#expunges the numbers used for first part of FH
                break

        for num in numbers:
            if numbers.count(num) >= 2:#similar to above but possible to have two three of a kinds so need >=
                two = [True, num]
                break
        if two[0] and three[0]:
            return [7, three[1], two[1]]
        return False
    
    def full_house_compare(self, rank1, rank2):
        if rank1[1] > rank2[1]: return 1 #compares the first three of a kind 
        if rank1[1] == rank2[1]: #if equal compares the second pair
            if rank1[2] > rank2[2]: return 1
            if rank1[2] == rank2[2]: return 0
            if rank1[2] < rank2[2]: return -1
        if rank1[1] < rank2[1]: return -1
    
        
    def flush(self, hand1, board): #checks for a flush
        total = self.flush_sort(hand1, board) #sorts by suit and number
        cards_row = 1
        suit = '' #placeholder to see if the resulting suits match
        cards_numbers = []
        for element in total:
            if element[0] == suit:
                cards_row += 1
                cards_numbers.append(int(element[1:]))#needs the number in case there are two flushes
            else:
                cards_row = 1
                suit = element[0]
                cards_numbers = []
                cards_numbers.append(int(element[1:]))
            if cards_row == 5:
                return [6, cards_numbers]
            
    def flush_compare(self, rank1, rank2):#simply compares the numbers of the flush in order 
        for i in range(5):
            if rank1[1][i] > rank2[1][i]: return 1
            if rank1[1][i] < rank2[1][i]: return -1
        return 0

    def straight(self, hand1, board): #checks for a straight number sort just returns the numbers
        
        total = self.number_sort(hand1, board)

        in_row = 1 #starts with 1 
        prev = 0 #placeholder for the previous number to see if the next is only 1 away
        
        for element in total:
            if element == prev: continue
            if element == prev - 1:
                in_row += 1
            else:
                in_row = 1
            prev = element
            if in_row == 5:
                return [5, element]
            if (in_row == 4 and element == 2) and 14 in total:
                return [5, 1]
        return False
    
    def straight_compare(self, rank1, rank2): #just compares the bottom card
        if rank1[1] > rank2[1]: return 1
        if rank1[1] == rank2[1]: return 0
        if rank1[1] < rank2[1]: return -1

    def three_of_a_kind(self, hand1, board): #checks for three of a kind
        
        total = self.number_sort(hand1, board)
        same_num = 1 #counts how many times same card in the hand
        prev_num = 0 #placeholder to hold which card is currently being counted
        highest_num = [] #list to find the highest kicker
        counter = 0
        for element in total:
            if total.count(element) == 3:
                total = list(filter(lambda a: a != element, total))
                return [4, element, total]
            
    def three_of_a_kind_compare(self, rank1, rank2): #compares through checking the three then each of the kickers
        if rank1[1] > rank2[1]: return 1
        if rank1[1] == rank2[1]:
            if len(rank1[2]) > 3:
                if rank1[2][0] > rank2[2][0]: return 1
                if rank1[2][0] == rank2[2][0]:
                    if len(rank1[2]) > 4:
                        if rank1[2][1] > rank2[2][1]: return 1
                        if rank1[2][1] == rank2[2][1]: return 0
                        if rank1[2][1] < rank2[2][1]: return -1
                    else: return 0
                if rank1[2][0] < rank2[2][0]: return -1
            else: return 0
                
        if rank1[1] < rank2[1]: return -1

    def two_pair(self, hand1, board):
        #checks for a two pair through similar method to FH above
        total = self.number_sort(hand1, board)
        number_pair1 = 0
        number_pair2 = 0
        for element in total:
            if total.count(element) == 2:
                number_pair1 = element
                total = list(filter(lambda a: a != element, total)) #expunges the one that have already used
                break
        for element in total:
            if total.count(element) == 2:
                number_pair2 = element
                total = list(filter(lambda a: a != element, total))#expunges so that you can find top kicker
                if len(total) == 0: total = [0] #for the case of ranking the board after the turn
                return [3, number_pair1, number_pair2, total[0]] 
    
    def two_pair_compare(self, rank1, rank2):#compares through top pair then second pair then kicker
        if rank1[1] > rank2[1]: return 1
        if rank1[1] == rank2[1]: 
            if rank1[2] > rank2[2]: return 1
            if rank1[2] == rank2[2]: 
                if rank1[3] > rank2[3]: return 1
                if rank1[3] == rank2[3]: return 0
                if rank1[3] < rank2[3]: return -1
            if rank1[2] < rank2[2]: return -1
        if rank1[1] < rank2[1]: return -1

    def pair(self, hand1, board):
        total = self.number_sort(hand1, board)
        pair = 0
        for num in total:
            if total.count(num) == 2:
                pair = num
                total = list(filter(lambda a: a != num, total))
                return [2, pair, total]
                break
        return False
    
    def pair_compare(self, rank1, rank2): #compares pair through pair and then the kickers
        if rank1[1] > rank2[1]: return 1
        if rank1[1] == rank2[1]: 
            if rank1[2][0] > rank2[2][0]: return 1
            if rank1[2][0] == rank2[2][0]: 
                if len(rank1[2]) > 3:
                    if rank1[2][1] > rank2[2][1]: return 1
                    if rank1[2][1] == rank2[2][1]: 
                        if len(rank1[2]) > 4:
                            if rank1[2][2] > rank2[2][2]: return 1
                            if rank1[2][2] == rank2[2][2]: return 0
                            if rank1[2][2] < rank2[2][2]: return -1
                        else: return 0
                    if rank1[2][1] < rank2[2][1]: return -1
                else: return 0
            if rank1[2][0] < rank2[2][0]: return -1
        if rank1[1] < rank2[1]: return -1

    def high_card(self, hand1, board): #returns the high card
        total = self.number_sort(hand1, board)
        numbers = []

        for element in total:
            numbers.append(element)

        return[1, numbers[0], numbers[1:]]
    
    def high_card_compare(self, rank1, rank2):#compares high cards
        for i in range(2):
            if rank1[1 + i] > rank2[1 + i]: return 1
            if rank1[1 + i] < rank2[1 + i]: return -1
        return 0
    
    def oesd(self, hand, board): #checks for an open ended straight through a similar method - just stops at 4
        total = self.number_sort(hand, board)

        in_row = 1
        prev = 0
        
        for element in total:
            if element == 14: continue #does not include an ace as that would not be an open ended straight
            if element == prev: continue
            if element == prev - 1:
                in_row += 1
            else:
                in_row = 1
            prev = element
            if in_row == 4:
                return [0]
        return False
    
    def flush_draw(self, hand, board): #checks for a flush draw
        total = self.flush_sort(hand, board)
        cards_row = 1
        suit = ''
        for element in total:
            if element[0] == suit:
                cards_row += 1
            else:
                cards_row = 1
                suit = element[0]
            if cards_row == 4:
                return [-1]
            
    def gut_shot_draw(self, hand, board): #checks for a gut shot straight meaning only 1 card would complete the straight
        total = self.number_sort(hand, board)
        
        in_row = 1
        prev = total[0]
        gut = 0
        gut_in_row = 0
        
        for element in total[1:]:
            if element == 14: 
                in_row = 1
                prev = 14
            if element == prev: continue
            if element == prev - 1:
                in_row += 1
            
            else:
                gut_in_row = in_row
                gut = prev-1 #keeps a number to see if this number could have completed the straight
                prev = element
                in_row = 1
            if element == gut - 1:
                gut -= 1
                gut_in_row  += 1
                
            if gut_in_row == 4: return [0] #just returns anything but false in order to check
            if in_row == 4:
                return [0]
            if in_row == 3 and (element == 11 or element == 2): 
                return [0]
            prev = element
        return False
    
    def straight_flush_draw(self, hand, board):
        first_total = hand + board
        total = self.flush_sort(hand, board)
        cards_row = 1
        suit = ''
        number = 0

        for element in total:
            if int(element[1:]) == 14: continue
            if element[0] == suit and number - 1 == int(element[1:]):
                cards_row += 1
                number -= 1
            else:
                cards_row = 1
                suit = element[0]
                number = int(element[1:])
            if cards_row == 4:
                return [0]

        return False
        
    
    def rank(self, hand, board): #ranks the hand through returning the top match
        if type(self.straight_flush(hand, board)) == list:
            return self.straight_flush(hand, board)
        
        if type(self.four_of_a_kind(hand, board)) == list:
            return self.four_of_a_kind(hand, board)
        
        if type(self.full_house(hand, board)) == list:
            return self.full_house(hand, board)
        
        if type(self.flush(hand, board)) == list:
            return self.flush(hand, board)
        
        if type(self.straight(hand, board)) == list:
            return self.straight(hand, board)
        
        if type(self.three_of_a_kind(hand, board)) == list:
            return self.three_of_a_kind(hand, board)
        
        if type(self.two_pair(hand, board)) == list:
            return self.two_pair(hand, board)
        
        if type(self.pair(hand, board)) == list:
            return self.pair(hand, board)
        
        if type(self.high_card(hand, board)) == list:
            return self.high_card(hand, board)
        
    def break_tie(self, rank1, rank2): #uses the compare to return who won
        if rank1[0] == 9:
            return self.straight_flush_compare(rank1, rank2)
        if rank1[0] == 8:
            return self.four_of_a_kind_compare(rank1, rank2)
        if rank1[0] == 7:
            return self.full_house_compare(rank1, rank2)
        if rank1[0] == 6:
            return self.flush_compare(rank1, rank2)
        if rank1[0] == 5:
            return self.straight_compare(rank1, rank2)
        if rank1[0] == 4:
            return self.three_of_a_kind_compare(rank1, rank2)
        if rank1[0] == 3:
            return self.two_pair_compare(rank1, rank2)
        if rank1[0] == 2:
            return self.pair_compare(rank1, rank2)
        if rank1[0] == 1:
            return self.high_card_compare(rank1, rank2)
    
    def winner(self, players_cards, board): #returns the winner seat number through checking rank
        winner = []
        hand_rank = [-5]
        winning_rank = 0
        counter = 0
        winning_hand = []
        
        for hand in players_cards: #iterates through all players cards
            
            if hand == board: current_rank = self.rank([], board)#for ease sometimes the board is included in the players cards
            else: current_rank = self.rank(hand, board)
                
            if current_rank[0] > hand_rank[0]: #if better rank than that hand is the current winner
                winner = [counter]
                hand_rank = current_rank
                winning_hand = hand
                
            elif current_rank[0] == hand_rank[0]: #if a tie breaks the tie
                if self.break_tie(hand_rank, current_rank) == -1:
                    hand_rank = current_rank
                    winner = [counter]
                    
                elif self.break_tie(hand_rank, current_rank) == 0: #has two winners if there 
                    winner.append(counter)
            counter += 1
        return [winner, hand_rank[0], winning_hand]
            




import csv
class simulation_odds:
    
    def __init__(self):

        self.deck = deck()
        self.compare_poke = compare_poker()
        
    def unsuited_full_prob(self, simulations):
        #initialize and create the dictionaries
        deck1 = self.deck
        compare = self.compare_poke
        unsuited = {}

        numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        
        counter = 0
        for i in numbers:
            for f in numbers[counter:]:
                unsuited[str(i) + ' ' + str(f)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            counter += 1
        same = 0
        count = 0
        for first in numbers: #iterates through all the possible unsuited pairs of cards to see what is the most likely outcome
            deck1.shuffle()
            first_card = 'D' + str(first) #adds diamonds to the first one as it does not matter what unsuited it is
            for second in numbers[count:]:
                second_card = 'C' + str(second) 
                for i in range(simulations): #range is the number of simulations to run
                    deck1.shuffle()
                    deck1.card_deck.remove(first_card)#removes the cards from the deck in order to avoid same dealing
                    deck1.card_deck.remove(second_card)
                    board = deck1.full_board_deal()
                    hand = [first_card, second_card]
                    hand = [hand, board]
                    winner = compare.winner(hand, board) #finds the rank of the winning hand
                    if len(winner[0]) > 1 or winner[0][0]== 1: 
                        unsuited[str(first) + ' ' + str(second)][-1] +=1
                        continue

                    unsuited[str(first) + ' ' + str(second)][winner[1] - 1] += 1

            count += 1
            print("unsuited_full", first)
        w = csv.writer(open("unsuited_full_prob.csv", "w"))
        for key, val in unsuited.items():
            newList = [x / simulations for x in val]
            key = [key]
            
            w.writerow(key + newList)
    
    def suited_full_prob(self, simulations):
        deck1 = self.deck
        compare = self.compare_poke
        suited = {}

        numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        
        counter = 1
        for i in numbers[:-1]:
            for f in numbers[counter:]:
                suited[str(i) + ' ' + str(f)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            counter += 1

        count = 0
        for first in numbers[:-1]: #iterates through all the possible unsuited pairs of cards to see what is the most likely outcome
            deck1.shuffle()
            first_card = 'D' + str(first) #adds diamonds to the first one as it does not matter what unsuited it is
            for second in numbers[count + 1:]:
                second_card = 'D' + str(second) 
                for i in range(simulations): #range is the number of simulations to run
                    deck1.shuffle()
                    deck1.card_deck.remove(first_card)#removes the cards from the deck in order to avoid same dealing
                    deck1.card_deck.remove(second_card)
                    board = deck1.full_board_deal()
                    hand = [first_card, second_card]
                    hand = [hand, board]
                    winner = compare.winner(hand, board) #finds the rank of the winning hand
                    if len(winner[0]) > 1 or winner[0][0]== 1: 
                        suited[str(first) + ' ' + str(second)][-1] +=1
                        continue

                    suited[str(first) + ' ' + str(second)][winner[1] - 1] += 1

            count += 1
            print("suited_full", first)
        w = csv.writer(open("suited_full_prob.csv", "w"))
        for key, val in suited.items():
            newList = [x / simulations for x in val]
            key = [key]
            
            w.writerow(key + newList)
    
    
    
    
    def unsuited_flop_prob(self, simulations):
        unsuited_flop = {}

        counter = 0
        numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        for i in numbers:
            for f in numbers[counter:]:
                unsuited_flop[str(i) + ' ' + str(f)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            counter += 1

        deck1 = self.deck
        compare = self.compare_poke

        
        count = 0
        for first in numbers: #iterates through all the possible unsuited pairs of cards to see what is the most likely outcome
            deck1.shuffle()
            first_card = 'D' + str(first) #adds diamonds to the first one as it does not matter what unsuited it is
            for second in numbers[count:]:
                second_card = 'C' + str(second) 
                for i in range(simulations): #range is the number of simulations to run
                    deck1.shuffle()
                    deck1.card_deck.remove(first_card)#removes the cards from the deck in order to avoid same dealing
                    deck1.card_deck.remove(second_card)
                    board = deck1.flop()
                    hand = [first_card, second_card]
                    hand = [hand, board]
                   
                    winner = compare.winner(hand, board) #finds the rank of the winning hand
                    if len(winner[0]) > 1 or winner[0][0]== 1: 
                        unsuited_flop[str(first) + ' ' + str(second)][-1] +=1
                        continue
                        
                    if type(compare.oesd(hand[0], board)) == list and (winner[1] != 9 and winner[1] != 5): 
                        unsuited_flop[str(first) + ' ' + str(second)][-2] += 1
                    if type(compare.flush_draw(hand[0], board)) == list and (winner[1] != 9 and winner[1] != 6): 
                        unsuited_flop[str(first) + ' ' + str(second)][-3] += 1


                    unsuited_flop[str(first) + ' ' + str(second)][winner[1] - 1] += 1

            count += 1
            
        w = csv.writer(open("unsuited_flop_prob.csv", "w"))
        for key, val in unsuited_flop.items():
            newList = [x / simulations for x in val]
            key = [key]
            
            w.writerow(key + newList)
            
            
    def suited_flop_prob(self, simulations):
        suited_flop = {}

        counter = 1
        numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        for i in numbers[:-1]:
            for f in numbers[counter:]:
                suited_flop[str(i) + ' ' + str(f)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            counter += 1

        deck1 = self.deck
        compare = self.compare_poke

        
        count = 1
        for first in numbers[:-1]: #iterates through all the possible unsuited pairs of cards to see what is the most likely outcome
            deck1.shuffle()
            first_card = 'D' + str(first) #adds diamonds to the first one as it does not matter what unsuited it is
            for second in numbers[count:]:
                second_card = 'D' + str(second) 
                for i in range(simulations): #range is the number of simulations to run
                    deck1.shuffle()
                    deck1.card_deck.remove(first_card)#removes the cards from the deck in order to avoid same dealing
                    deck1.card_deck.remove(second_card)
                    board = deck1.flop()
                    hand = [first_card, second_card]
                    hand = [hand, board]
                    winner = compare.winner(hand, board) #finds the rank of the winning hand

                        
                    if type(compare.oesd(hand[0], board)) == list and (winner[1] != 9 and winner[1] != 5): 
                        suited_flop[str(first) + ' ' + str(second)][-2] += 1
                    if type(compare.flush_draw(hand[0]), board) == list and (winner[1] != 9 and winner[1] != 6): 
                        suited_flop[str(first) + ' ' + str(second)][-3] += 1
                    if len(winner[0]) > 1 or winner[0][0]== 1: 
                        suited_flop[str(first) + ' ' + str(second)][-1] +=1
                        continue

                    

                    suited_flop[str(first) + ' ' + str(second)][winner[1] - 1] += 1

            count += 1
            
        w = csv.writer(open("suited_flop_prob.csv", "w"))
        for key, val in suited_flop.items():
            newList = [x / simulations for x in val]
            key = [key]
            
            w.writerow(key + newList)
            
    def unsuited_turn_prob(self, simulations):
        unsuited_turn = {}

        counter = 0
        numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        for i in numbers:
            for f in numbers[counter:]:
                unsuited_turn[str(i) + ' ' + str(f)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            counter += 1

        deck1 = self.deck
        compare = self.compare_poke

        
        count = 0
        for first in numbers: #iterates through all the possible unsuited pairs of cards to see what is the most likely outcome
            deck1.shuffle()
            first_card = 'D' + str(first) #adds diamonds to the first one as it does not matter what unsuited it is
            for second in numbers[count:]:
                second_card = 'C' + str(second) 
                for i in range(simulations): #range is the number of simulations to run
                    deck1.shuffle()
                    deck1.card_deck.remove(first_card)#removes the cards from the deck in order to avoid same dealing
                    deck1.card_deck.remove(second_card)
                    board = deck1.flop()
                    board = deck1.turn()
                    hand = [first_card, second_card]
                    hand = [hand, board]
                    winner = compare.winner(hand, board) #finds the rank of the winning hand
                    if len(winner[0]) > 1 or winner[0][0]== 1: 
                        unsuited_turn[str(first) + ' ' + str(second)][-1] +=1
                        continue
                    if compare.oesd(hand[0], board) == list and (winner[1] != 9 and winner[1] != 5): 
                        unsuited_turn[str(first) + ' ' + str(second)][-2] += 1
                    if compare.flush_draw(hand[0], board) == list and (winner[1] != 9 and winner[1] != 6): 
                        unsuited_turn[str(first) + ' ' + str(second)][-3] += 1

                    unsuited_turn[str(first) + ' ' + str(second)][winner[1] - 1] += 1

            count += 1
            
        w = csv.writer(open("unsuited_turn_prob.csv", "w"))
        for key, val in unsuited_turn.items():
            newList = [x / simulations for x in val]
            w.writerow([key, newList])
            
            
    def suited_turn_prob(self, simulations):
        suited_turn = {}

        counter = 1
        numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        for i in numbers[:-1]:
            for f in numbers[counter:]:
                suited_turn[str(i) + ' ' + str(f)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            counter += 1

        deck1 = self.deck
        compare = self.compare_poke

        
        count = 1
        for first in numbers[:-1]: #iterates through all the possible unsuited pairs of cards to see what is the most likely outcome
            deck1.shuffle()
            first_card = 'D' + str(first) #adds diamonds to the first one as it does not matter what unsuited it is
            for second in numbers[count:]:
                second_card = 'D' + str(second) 
                for i in range(simulations): #range is the number of simulations to run
                    deck1.shuffle()
                    deck1.card_deck.remove(first_card)#removes the cards from the deck in order to avoid same dealing
                    deck1.card_deck.remove(second_card)
                    board = deck1.flop()
                    board = deck1.turn()
                    hand = [first_card, second_card]
                    hand = [hand, board]
                    winner = compare.winner(hand, board) #finds the rank of the winning hand

                    if len(winner[0]) > 1 or winner[0][0]== 1: 
                        suited_turn[str(first) + ' ' + str(second)][-1] +=1
                        continue
                        
                    if compare.oesd(hand[0], board) == list and (winner[1] != 9 and winner[1] != 5): 
                        suited_turn[str(first) + ' ' + str(second)][-2] += 1
                    if compare.flush_draw(hand[0], board) == list and (winner[1] != 9 and winner[1] != 6): 
                        suited_turn[str(first) + ' ' + str(second)][-3] += 1

                    

                    suited_turn[str(first) + ' ' + str(second)][winner[1] - 1] += 1

            count += 1
            
        w = csv.writer(open("suited_turn_prob.csv", "w"))
        for key, val in suited_turn.items():
            newList = [x / simulations for x in val]
            w.writerow([key, newList])
            
    def compare_hands(self, hand1, hand2, simulations): #compares two hands to see in the end which comes out on top more
        deck1 = self.deck
        compare = self.compare_poke
        hand1_win = 0 #counter for how many times hand1 wins
        for i in range(simulations):
            deck1.shuffle()
            total = hand1 + hand2
            for i in total: #removes the cards in the hands then deals and compares
                deck1.card_deck.remove(i)
            board = deck1.full_board_deal()
            winner = compare.winner([hand1, hand2], board)
            if winner[0] == [0]: hand1_win += 1
        print("The likelihood of hand1 winning this is " + str(hand1_win / simulations))
    
    
    def best_hand_suited(self, simulations): #finds the probability of heads up win for suited cards
        combinations = {}

        counter = 1
        numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        for i in numbers[:-1]:
            for f in numbers[counter:]:
                combinations[str(i) + ' ' + str(f)] = 0 #has all the combinations of possible suited cards
            counter += 1

        deck1 = self.deck
        compare = self.compare_poke
        
        hand1_win = 0
        for i in combinations: #for each combination runs the required number of simulations
            hand1_win = 0
            for num in range(simulations): 
                deck1.shuffle()
                numbers = i.split(' ')
                cards = ['D' + str(numbers[0]), 'D' + str(numbers[1])]
                deck1.card_deck.remove(cards[0])
                deck1.card_deck.remove(cards[1])
                opponent_hand = deck1.deal_players(1)[0] #deals the opponent 
                players_hands = [cards, opponent_hand]
                board = deck1.full_board_deal() #deals the board then compares
                winner = compare.winner(players_hands, board)
                if winner[0] == [0]: hand1_win += 1
            combinations[i] = hand1_win / simulations
        w = csv.writer(open("suited_best_hand_prob.csv", "w"))
        for key, val in combinations.items():
            w.writerow([key, val])
            
    def best_hand_unsuited(self, simulations):#finds the probability of heads up win for unsuited cards
        combinations = {}

        counter = 0
        numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        for i in numbers:
            for f in numbers[counter:]:
                combinations[str(i) + ' ' + str(f)] = 0 #has all the combinations of possible unsuited cards
            counter += 1

        deck1 = self.deck
        compare = self.compare_poke
        
        hand1_win = 0
        for i in combinations:
            hand1_win = 0
            for num in range(simulations): #for each combination runs the required number of simulations
                deck1.shuffle()
                numbers = i.split(' ')
                cards = ['D' + str(numbers[0]), 'C' + str(numbers[1])]
                deck1.card_deck.remove(cards[0])
                deck1.card_deck.remove(cards[1])
                opponent_hand = deck1.deal_players(1)[0]
                players_hands = [cards, opponent_hand]
                board = deck1.full_board_deal()
                winner = compare.winner(players_hands, board)
                if winner[0] == [0]: hand1_win += 1
            combinations[i] = hand1_win / simulations
        w = csv.writer(open("unsuited_best_hand_prob.csv", "w"))
        for key, val in combinations.items():
            w.writerow([key, val])
        





