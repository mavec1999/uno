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


def pickup(deck, hand):
    hand.append(deck[0])
    deck.pop(0)
    return

def player_turn(deck, discard_pile, player_hand):
    print("Top card", discard_pile[0])

    for i in range (len(player_hand)):
        print(i, " ", player_hand[i])

    x = True
    while x is True:
        print("0", "Pickup")
        print("1", "Play")
        action = int(input("What would you like to do?"))
        if action == 0:
            pickup(deck, player_hand)
            x = False
        elif action == 1:
            player_card = int(input("Which card would you like to play?"))  # multiple cards not supported

            if player_is_valid_card(discard_pile[0], player_hand[player_card]):
                discard_pile.insert(0, player_hand[player_card])
                if discard_pile[0]["color"] == "wild":
                    discard_pile[0]["color"] = input("please choose color")
                player_hand.pop(player_card)
                x = False
            else:
                print("Cannot play that card")
        else:
            print("Invalid selection")

def computer_turn(deck, discard_pile, computer_hand, which_computer):
    valid_cards = []
    valid_cards = computer_valid_card(computer_hand, discard_pile[0])

    if len(valid_cards) == 0:
        pickup(deck, computer_hand)
        print("Computer %s picks up" %which_computer)
    else:
        print("Computer %s plays" %which_computer, valid_cards[0])
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

    winner = True

    play_order = {0: "player", 1: "computer_1", 2: "computer_2"}

    while winner:
        if(play_order[0]) == "player":
            player_turn(deck, discard_pile, player_hand)
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
                    pickup(deck, player_hand)
            elif play_order[1] == "computer_1":
                print("Computer 1 picks up %s" %pickup_how_many)
                for i in range(pickup_how_many):
                    pickup(deck, computer1_hand)
            else:
                print("Computer 2 picks up %s" %pickup_how_many)
                for i in range(pickup_how_many):
                    pickup(deck, computer2_hand)


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

