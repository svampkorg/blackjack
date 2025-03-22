from enum import Enum
from .blackjack_types import Hand

class Standing(Enum):

    Player = 1
    Dealer = 2
    PlayerBlackjack = 3
    DealerBlackjack = 4
    PlayerBust = 5
    DealerBust = 6
    Draw = 7

def get_hand_value(hand: Hand) -> int:

    value = 0

    for card in hand:
        if not card:
            continue
        if card.value - 10 > 0:
            value += 10
        elif card.value == 1:
            if (value + 11) > 21:
                value += 1
            else:
                value += 11
        else:
            value += card.value

    return value

def get_standing(player: int, dealer: int):

    if player > 21:
        return Standing.PlayerBust
    elif dealer > 21:
        return Standing.DealerBust
    if dealer == 21:
        return Standing.DealerBlackjack
    elif player == 21:
        return Standing.PlayerBlackjack
    elif player == dealer:
        return Standing.Draw
    elif player > dealer:
        return Standing.Player
    else: 
        return Standing.Dealer

def print_standing(standing: Standing):

    match standing:
        case Standing.Draw:
            print("It's a draw! Nobody wins! ¯\\_(ツ)_/¯")
        case Standing.PlayerBlackjack:
            print("You win on Blackjack! ⊂(◉‿◉)つ")
        case Standing.DealerBlackjack:
            print("Dealer wins on Blackjack! (´סּ︵סּ`)")
        case Standing.Player:
            print("You Win! ᕕ( ᐛ )ᕗ")
        case Standing.Dealer:
            print("Dealer Wins! (ⱺ ʖ̯ⱺ)")
        case Standing.DealerBust:
            print("Dealer is Bust! You Win! (͠≖ ͜ʖ͠≖) hehe")
        case Standing.PlayerBust:
            print("You are Bust! Dealer wins! ୧༼ಠ益ಠ༽୨")
