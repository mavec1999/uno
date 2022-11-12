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
1
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

def computer_ranked_cards(hand):
    
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

    hand = sorted(hand, key=lambda a: a["rank"], reverse=True)
    return hand
    

def pickup(deck, hand, discard_pile):
    if len(deck) == 0:
        deck = shuffle(discard_pile)
        discard_pile = []
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

def player_turn(deck, discard_pile, player_hand, pickup_counter):
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
    print(color.UNDERLINE+ "#      Card" + color.END)

    for i in range (len(player_hand)):
        if player_hand[i]["color"] == 'red':
            print(i, "    ", color.RED + print_cards(player_hand[i]) + color.END)
        elif player_hand[i]["color"] == 'green':
             print(i, "    ", color.GREEN + print_cards(player_hand[i]) + color.END)
        elif player_hand[i]["color"] == 'yellow':
             print(i, "    ", color.YELLOW + print_cards(player_hand[i]) + color.END)
        elif player_hand[i]["color"] == 'blue':
             print(i, "    ", color.BLUE + print_cards(player_hand[i]) + color.END)
        else:
            print(i, "    ", print_cards(player_hand[i]))
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
        action = int(input("What would you like to do? "))
        if action == 0:
            pickup(deck, player_hand, discard_pile)
            print("You pickup a new card")
            player_turn(deck, discard_pile, player_hand, 1)
            x = False
        elif action == 1:
            player_card = int(input("Which card would you like to play? "))  # multiple cards not supported

            if player_is_valid_card(discard_pile[0], player_hand[player_card]):
                discard_pile.insert(0, player_hand[player_card])
                if discard_pile[0]["color"] == "wild":
                    discard_pile[0]["color"] = input("Please choose color ").lower()
                player_hand.pop(player_card)
                x = False
            else:
                print("Cannot play that card")
        elif action == 2 and pickup_counter > 0:
            x = False
        else:
            print("Invalid selection")

def computer_turn(deck, discard_pile, computer_hand, which_computer):
    valid_cards = []
    valid_cards = computer_valid_card(computer_hand, discard_pile[0])
    valid_cards = computer_ranked_cards(valid_cards)

    if len(valid_cards) == 0:
        pickup(deck, computer_hand, discard_pile)
        print("Computer %s picks up" %which_computer)
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
        if discard_pile[0]["color"] == "wild":
            top_color = {"blue":0,"green":0,"yellow":0,"red":0, "wild":0}
            if len(computer_hand) == 1:
                return
            for i in range (len(computer_hand)):
                top_color[computer_hand[i]["color"]] += 1
            #sort by values
            sorted_tuples = sorted(top_color.items(),key=lambda x:x[1], reverse=True)
            sorted_colors = {k: v for k, v in sorted_tuples}
            #pick the most common color in the hand
            selected_color = list(sorted_colors.keys())[0]
            discard_pile[0]["color"] = selected_color
            print("Computer %s selects %s" %(which_computer, selected_color))
        x = computer_hand.index(valid_cards[0])
        computer_hand.pop(x)
    if len(computer_hand) == 1:
        print("Computer %s shouts Uno!" %which_computer)
def play_uno():
    print('Let\'s play Uno!')  # Press Ctrl+F8 to toggle the breakpoint.

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

    deal(deck,player_hand,computer1_hand, computer2_hand)
    discard_pile.append(deck[0])
    deck.pop(0)

    winner = True

    play_order = {0: "player", 1: "computer_1", 2: "computer_2"}

    while winner:
        if(play_order[0]) == "player":
            player_hand = sorted(player_hand, key=lambda a: a["ref_num"])
            player_turn(deck, discard_pile, player_hand, 0)
            if len(player_hand) == 0:
                    print("player wins!")
                    break
        elif(play_order[0]) == "computer_1":
            computer_turn(deck, discard_pile, computer1_hand, 1)
            if len(computer1_hand) == 0:
                    print("computer 1 wins!")
                    break
        elif(play_order[0]) == "computer_2":
            computer_turn(deck, discard_pile, computer2_hand, 2)
            if len(computer2_hand) == 0:
                    print("computer 2 wins!")
                    break

        new_order = {0: "", 1: "", 2: ""}

        if discard_pile[0]["action_1"] == "pickup":
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


        if discard_pile[0]["face"] == "skip":
            new_order[0] = play_order[2]
            new_order[1] = play_order[0]
            new_order[2] = play_order[1]
            play_order = new_order
        elif discard_pile[0]["face"] == "switch":
            new_order[0] = play_order[2]
            new_order[1] = play_order[1]
            new_order[2] = play_order[0]
            play_order = new_order
        else:
            new_order[0] = play_order[1]
            new_order[1] = play_order[2]
            new_order[2] = play_order[0]
            play_order = new_order
    for i in range (len(player_hand)):
        print(i, " ", player_hand[i])
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    play_uno()

