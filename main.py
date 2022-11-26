import xlrd
import random

def shuffle(deck):
    random.shuffle(deck)
    return deck

def deal(deck, p1, p2, p3):
    cards_in_hand = 7
    for card in range(7):
        p1.append(deck[0])
        deck.pop(0)
        p2.append(deck[0])
        deck.pop(0)
        p3.append(deck[0])
        deck.pop(0)
    return

def player_is_valid_card(top_card, hand):
    if hand["color"] == "wild":
        return True
    elif top_card["color"] == "wild":
        return True
    elif top_card["color"] == hand["color"]:
        return True
    elif top_card["face"] == hand["face"]:
        return True
    return False

def computer_valid_card(hand, top_card):
    valid_cards = []
    if top_card["color"] == "wild":
        valid_cards = hand
        return valid_cards
    else:
        for i in range(len(hand)):
            if hand[i]["color"] == "wild":
                valid_cards.append(hand[i])
                continue
            elif top_card["color"] == hand[i]["color"]:
                valid_cards.append(hand[i])
                continue
            elif top_card["face"] == hand[i]["face"]:
                valid_cards.append(hand[i])
                continue
        return valid_cards

def computer_ranked_cards(hand, next_player, previous_player, uno_condition):
    
    #maximum defensiveness if both players have Uno. Play pickup cards or play nothing
    if uno_condition[next_player] == True and uno_condition[previous_player] == True:
        emergency_hand = []
        for i in range(len(hand)):
            if hand[i]["action_1"] == "pickup":
                emergency_hand.append(hand[i])
        return emergency_hand

    #strongly prefer defensive cards if next player has shouted uno
    if uno_condition[next_player] == True and uno_condition[previous_player] != True:
        for i in range (len(hand)):
            if hand[i]["action_1"] == "pickup" or hand[i]["face"] == "skip" or hand[i]["face"] == "switch":
                hand[i]["rank"] += 108 #only 108 cards in the deck, so this ensures top rank regardless of other factors
    elif uno_condition[previous_player] == True:
        for i in range(len(hand)):
            if hand[i]["face"] == "skip" or hand[i]["face"] == "switch":
                hand[i]["rank"] -= 108 #do not switch or skip back to the player that just shouted Uno!

    #tend to play most common color cards
    top_color = {"blue":0,"green":0,"yellow":0,"red":0, "wild":0}
    for i in range (len(hand)):
        top_color[hand[i]["color"]] += 1
    for i in range (len(hand)):
        if hand[i]["color"] == "blue":
            hand[i]["rank"] += top_color["blue"]
        elif hand[i]["color"] == "green":
            hand[i]["rank"] += top_color["green"]
        elif hand[i]["color"] == "yellow":
            hand[i]["rank"] += top_color["yellow"]
        elif hand[i]["color"] == "red":
            hand[i]["rank"] += top_color["red"]
    
    #tend to avoid playing non-pickup 2 cards
    for i in range (len(hand)):
        if hand[i]["face"] == 2 and hand[i]["action_1"] != "pickup":
            hand[i]["rank"] -= 1
    
    #tend to favor playing 0 cards
    for i in range (len(hand)):
        if hand[i]["face"] == 0:
            hand[i]["rank"] += 1

    #tend to prefer playing multi-cards
    for i in range (len(hand)-1):
        for j in range (i, len(hand)-1):
            if hand[i]["ref_num"] == hand[j]["twin"]:
                hand[i]["rank"] +=1
                hand[j]["rank"] +=1

    hand = sorted(hand, key=lambda a: a["rank"], reverse=True)
    return hand
    

def pickup(deck, hand, discard_pile):
    #first checks if there are any cards left in the deck.
    #if not, the discard pile becomes the new deck
    if len(deck) == 0:
        #saves the top card of the discard pile, while shuffling the rest
        last_played_card = discard_pile[0]
        discard_pile.pop(0)
        deck = shuffle(discard_pile)
        discard_pile = last_played_card
    hand.append(deck[0])
    deck.pop(0)
    return

def print_cards(card):
    clean_card = card["color"]
    if type(card["face"]) is float:
        clean_card = clean_card + " " + str(int(card["face"]))
    elif type(card["face"]) is str:
        clean_card = clean_card + " " + card["face"]
    
    if card["action_1"] != "none":
        clean_card = clean_card + " " + card["action_1"]
    
    return clean_card.title()

def selection_validator(cards_to_play, player_hand):
    if 0 >= len(cards_to_play) or len(cards_to_play) > 2:
        print("You must select at least 1 card but not more than 2 to play")
        return False
    elif len(cards_to_play) == 2:
        if 0 > cards_to_play[0] or cards_to_play[0] >= len(player_hand) or 0 > cards_to_play[1] or cards_to_play[1] >= len(player_hand):
            print("The selection you have made is out of range")
            return False
        elif player_hand[cards_to_play[0]]["twin"] != player_hand[cards_to_play[1]]["ref_num"]:
            print("Only cards matched by color AND number may be multiplayed")
            return False
    else:
        if 0 > cards_to_play[0] or cards_to_play[0] >= len(player_hand):
            print("The selection you have made is out of range")
            return False

    return True

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def player_turn(deck, discard_pile, player_hand, pickup_counter, round, uno_condition):
    
    if discard_pile[0]["color"] == 'red':
        print("The top card is", color.RED + print_cards(discard_pile[0])+ color.END)
    elif discard_pile[0]["color"] == 'green':
        print("The top card is", color.GREEN + print_cards(discard_pile[0])+ color.END)
    elif discard_pile[0]["color"] == 'yellow':
            print("The top card is", color.YELLOW + print_cards(discard_pile[0])+ color.END)
    elif discard_pile[0]["color"] == 'blue':
            print("The top card is", color.BLUE + print_cards(discard_pile[0])+ color.END)
    else:
        print("The top card is", print_cards(discard_pile[0]))
    
    print()
    print("Your hand")
    print(color.UNDERLINE+ "#        Card" + color.END)

    for i in range (len(player_hand)):
        if player_hand[i]["color"] == 'red':
            print(i, '\t', color.RED + print_cards(player_hand[i]) + color.END)
        elif player_hand[i]["color"] == 'green':
             print(i, '\t', color.GREEN + print_cards(player_hand[i]) + color.END)
        elif player_hand[i]["color"] == 'yellow':
             print(i, '\t', color.YELLOW + print_cards(player_hand[i]) + color.END)
        elif player_hand[i]["color"] == 'blue':
             print(i, '\t', color.BLUE + print_cards(player_hand[i]) + color.END)
        else:
            print(i, '\t', print_cards(player_hand[i]))
    x = True
    while x is True:
        print()
        print("Please Select Action")
        if pickup_counter == 0:
            print("0", "Pickup")
            print("1", "Play")
        else:
            print("1", "Play")
            print("2", "End turn")
        
        try:
            action = int(input("What would you like to do? "))
        except ValueError:
            print("Invalid selection")
        else:
            if action == 0:
                pickup(deck, player_hand, discard_pile)
                print("You pickup a new card")
                player_turn(deck, discard_pile, player_hand, 1, round, uno_condition)
                x = False
            elif action == 1:
                #multi-card now supported
                cards_to_play = []
                
                try:
                    cards_to_play = [int(item) for item in input("Which card(s) would you like to play? ").split()]
                except:
                    print("""Invalid selection.\nPlease select a card number from those listed above.\nFor multi-play, please enter up to two card numbers separated by a space""")
                else:
                    if selection_validator(cards_to_play, player_hand): #checks that only 1 or 2 cards matching cards are selected
                        if player_is_valid_card(discard_pile[0], player_hand[cards_to_play[0]]): #checks that those cards are legal
                            
                            if len(cards_to_play) == 1: #single play
                                discard_pile.insert(0, player_hand[cards_to_play[0]])
                                discard_pile[0]["played_round"] = round
                                player_hand.pop(cards_to_play[0])
                            else: #multiplay
                                discard_pile.insert(0, player_hand[cards_to_play[0]])
                                discard_pile[0]["played_round"] = round
                                discard_pile.insert(0, player_hand[cards_to_play[1]])
                                discard_pile[0]["played_round"] = round
                                
                                #pop the latter card first so as to not mess up the indexing
                                if cards_to_play[0] > cards_to_play [1]:
                                    player_hand.pop(cards_to_play[0])
                                    player_hand.pop(cards_to_play[1])
                                else:
                                    player_hand.pop(cards_to_play[1])
                                    player_hand.pop(cards_to_play[0])

                            if discard_pile[0]["color"] == "wild":
                                valid_colors = ["blue", "green", "yellow", "red"]
                                
                                new_color = ""

                                while new_color not in valid_colors:
                                    try:
                                        new_color = input("Please choose color ").lower()
                                    except ValueError:
                                        print("You must type-in red, green, yellow, or blue only")
                                
                                discard_pile[0]["color"] = new_color
                            
                            if discard_pile[0]["color"] == 'red':
                                print("You play", color.RED + print_cards(discard_pile[0]) + color.END)
                            elif discard_pile[0]["color"] == 'green':
                                print("You play", color.GREEN + print_cards(discard_pile[0]) + color.END)
                            elif discard_pile[0]["color"] == 'yellow':
                                print("You play", color.YELLOW + print_cards(discard_pile[0]) + color.END)
                            elif discard_pile[0]["color"] == 'blue':
                                print("You play", color.BLUE + print_cards(discard_pile[0]) + color.END)
                                
                            x = False #exits the while loop. allows continuation to checking the uno condition
                        
                        else:
                            print("Cannot play that card")
                    else:
                        print("""Invalid selection.\nPlease select a card number from those listed above.\nFor multi-play, please enter up to two card numbers separated by a space""")
            elif action == 2 and pickup_counter > 0:
                x = False
    
    if len(player_hand) == 1 and uno_condition["player"] == False:
        uno_condition["player"] = True
        print("You shout Uno!")
    elif len(player_hand) == 1 and uno_condition["player"] == False:
        uno_condition["player"] = True
    else:
        uno_condition["player"] = False

def computer_turn(deck, discard_pile, computer_hand, which_computer, pickup_counter, round, next_player, uno_condition, previous_player):
    valid_cards = []
    valid_cards = computer_valid_card(computer_hand, discard_pile[0]) #identifies whic cards are valid
    valid_cards = computer_ranked_cards(valid_cards, next_player, previous_player, uno_condition) #ranks the valid cards, if any

    if len(valid_cards) == 0 and pickup_counter == 0:
        pickup(deck, computer_hand, discard_pile)
        print("Computer %s picks up" %which_computer)
        pickup_counter = 1
        computer_turn(deck, discard_pile, computer_hand, which_computer, pickup_counter, round, next_player, uno_condition, previous_player)
    elif len(valid_cards) > 0:
        if len(valid_cards) > 1 and valid_cards[0]["twin"] == valid_cards[1]["ref_num"]:
            print("Computer %s makes a" %which_computer, color.BOLD + "multi-play!" + color.END)

            if valid_cards[0]["color"] == 'red':
                print("Computer %s plays two" %which_computer, color.RED + print_cards(valid_cards[0])+"s" + color.END)
            elif valid_cards[0]["color"] == 'green':
                print("Computer %s plays two" %which_computer, color.GREEN + print_cards(valid_cards[0])+"s" + color.END)
            elif valid_cards[0]["color"] == 'yellow':
                print("Computer %s plays two" %which_computer, color.YELLOW + print_cards(valid_cards[0])+"s" + color.END)
            elif valid_cards[0]["color"] == 'blue':
                print("Computer %s plays two" %which_computer, color.BLUE + print_cards(valid_cards[0])+"s" + color.END)
            else:
                print("Computer %s plays two" %which_computer, print_cards(valid_cards[0])+"s")

            discard_pile.insert(0, valid_cards[0])
            discard_pile[0]["played_round"] = round
            discard_pile.insert(0, valid_cards[1])
            discard_pile[0]["played_round"] = round
            x = computer_hand.index(valid_cards[0])
            y = computer_hand.index(valid_cards[1])
            
            #pops the latter card to avoid messing up the indexing
            if x > y:
                computer_hand.pop(x)
                computer_hand.pop(y)
            else:
                computer_hand.pop(y)
                computer_hand.pop(x)
        else:
            if valid_cards[0]["color"] == 'red':
                print("Computer %s plays" %which_computer, color.RED + print_cards(valid_cards[0]) + color.END)
            elif valid_cards[0]["color"] == 'green':
                print("Computer %s plays" %which_computer, color.GREEN + print_cards(valid_cards[0]) + color.END)
            elif valid_cards[0]["color"] == 'yellow':
                print("Computer %s plays" %which_computer, color.YELLOW + print_cards(valid_cards[0]) + color.END)
            elif valid_cards[0]["color"] == 'blue':
                print("Computer %s plays" %which_computer, color.BLUE + print_cards(valid_cards[0]) + color.END)
            else:
                print("Computer %s plays" %which_computer, print_cards(valid_cards[0]))

            discard_pile.insert(0, valid_cards[0])
            discard_pile[0]["played_round"] = round
            x = computer_hand.index(valid_cards[0])
            computer_hand.pop(x)

        #if computer plays a wild card, the computer selects the most common color left in its hand
        if discard_pile[0]["color"] == "wild":
            top_color = {"blue":0,"green":0,"yellow":0,"red":0, "wild":0}
            if len(computer_hand) < 1:
                return
            for i in range (len(computer_hand)):
                top_color[computer_hand[i]["color"]] += 1
            
            #sort by values
            sorted_tuples = sorted(top_color.items(),key=lambda x:x[1], reverse=True)
            sorted_colors = {k: v for k, v in sorted_tuples}
            
            #pick the most common color in the hand
            selected_color = list(sorted_colors.keys())[0]

            #if the computer selects Wild because it has more than one wild card, select different color at random
            if selected_color == "wild" and len(computer_hand) > 1:
                color_list = ["blue", "green", "yellow", "red"]
                selected_color = random.choice(color_list)

            discard_pile[0]["color"] = selected_color
            print("Computer %s selects %s" %(which_computer, selected_color))
        
    if len(computer_hand) == 1:
        #this check prevents the computer from shouting Uno twice when playing after pickup
        if which_computer == 1 and uno_condition["computer_1"] == False:
            uno_condition["computer_1"] = True
            print("Computer %s shouts Uno!" %which_computer)
        elif which_computer == 2 and uno_condition["computer_2"] == False:
            uno_condition["computer_2"] = True
            print("Computer %s shouts Uno!" %which_computer)
        elif which_computer == 1 and uno_condition["computer_1"] == True:
            uno_condition["computer_1"] = True
        elif which_computer == 2 and uno_condition["computer_2"] == True:
            uno_condition["computer_2"] = True
    else:
        if which_computer == 1:
            uno_condition["computer_1"] = False
        else:
            uno_condition["computer_2"] = False

def play_uno():
    print('Let\'s play Uno!')

    workbook = xlrd.open_workbook('deck.xls')
    workbook = xlrd.open_workbook('deck.xls', on_demand = True)
    worksheet = workbook.sheet_by_index(0)

    first_row = []
    for col in range(worksheet.ncols):
        first_row.append(worksheet.cell_value(0,col))

    deck = []

    for row in range(1, worksheet.nrows):
        card = {}
        for col in range(worksheet.ncols):
            card[first_row[col]]=worksheet.cell_value(row,col)
        deck.append(card)

    shuffle(deck)

    discard_pile = []
    player_hand = []
    computer1_hand = []
    computer2_hand = []

    #round variable keeps track of which round each card is played. 
    #it's used to confirm that actions only get applied once, and only in the next round
    round = 0

    deal(deck,player_hand,computer1_hand, computer2_hand)
    discard_pile.append(deck[0])
    deck.pop(0)

    winner = True

    play_order = {0: "player", 1: "computer_1", 2: "computer_2"}
    uno_condition = {"player": False, "computer_1": False, "computer_2": False}

    while winner:
        next_player = play_order[1]
        previous_player = play_order[2]
        if(play_order[0]) == "player":
            player_hand = sorted(player_hand, key=lambda a: a["ref_num"])
            player_turn(deck, discard_pile, player_hand, 0, round, uno_condition)
            if len(player_hand) == 0:
                    print("player wins!")
                    break
        elif(play_order[0]) == "computer_1":
            computer_turn(deck, discard_pile, computer1_hand, 1, 0, round, next_player, uno_condition, previous_player)
            if len(computer1_hand) == 0:
                    print("computer 1 wins!")
                    break
        elif(play_order[0]) == "computer_2":
            computer_turn(deck, discard_pile, computer2_hand, 2, 0, round, next_player, uno_condition, previous_player)
            if len(computer2_hand) == 0:
                    print("computer 2 wins!")
                    break

        new_order = {0: "", 1: "", 2: ""}

        #makes the next player in the play order pickup, except if the round variable says not to
        if discard_pile[0]["action_1"] == "pickup" and discard_pile[0]["played_round"] == round:
            
            pickup_how_many = int(discard_pile[0]["face"])
            
            if play_order[1] == "player":
                print(play_order[0] + " makes you pickup %s" %pickup_how_many)
                for i in range(pickup_how_many):
                    pickup(deck, player_hand, discard_pile)
            elif play_order[1] == "computer_1":
                print("Computer 1 picks up %s" %pickup_how_many)
                for i in range(pickup_how_many):
                    pickup(deck, computer1_hand, discard_pile)
            else:
                print("Computer 2 picks up %s" %pickup_how_many)
                for i in range(pickup_how_many):
                    pickup(deck, computer2_hand, discard_pile)
            
            #this essentially checks if there was a multi-play of pickup cards. if there was,
            #both discard_pile[0] and discard_pile[1] will have the same value for "round_played"
            #which will also match the current value for 'round'
            if len(discard_pile) > 1:
                if discard_pile[1]["action_1"] == "pickup" and discard_pile[1]["played_round"] == round:
                    pickup_how_many = int(discard_pile[1]["face"])
                    if play_order[1] == "player":
                        print(play_order[0] + " makes you pickup another %s" %pickup_how_many)
                        for i in range(pickup_how_many):
                            pickup(deck, player_hand, discard_pile)
                    elif play_order[1] == "computer_1":
                        print("Computer 1 picks up another %s" %pickup_how_many)
                        for i in range(pickup_how_many):
                            pickup(deck, computer1_hand, discard_pile)
                    else:
                        print("Computer 2 picks up another %s" %pickup_how_many)
                        for i in range(pickup_how_many):
                            pickup(deck, computer2_hand, discard_pile)

        #sets the play order. for skip/switch cards, will first confirm the round they were played.
        #since all cards are initialized to have a '-1' value for round, and the round variable 
        #itself is initialized to '0', skip/switch cannot affect play if they are the first
        #top card in the discard pile when play begins 
        if discard_pile[0]["face"] == "skip" and discard_pile[0]["played_round"] == round:
            new_order[0] = play_order[2]
            new_order[1] = play_order[0]
            new_order[2] = play_order[1]
            play_order = new_order
        elif discard_pile[0]["face"] == "switch" and discard_pile[0]["played_round"] == round: 
            new_order[0] = play_order[2]
            new_order[1] = play_order[1]
            new_order[2] = play_order[0]
            play_order = new_order
        else:
            new_order[0] = play_order[1]
            new_order[1] = play_order[2]
            new_order[2] = play_order[0]
            play_order = new_order

        round += 1

if __name__ == '__main__':
    play_uno()

