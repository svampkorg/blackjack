import random
from os import system

from .art import logo
from .arthandling import cards_to_art
from .blackjack_types import Card, Deck, Hand, deck
from .gamelogic import Standing, get_hand_value, get_standing


def draw_logo():

    system("clear")

    print(logo)
    print(f"Player wallet: ${ state.player_wallet }, (enter ? for rules)")


def draw_rules():

    draw_logo()

    print("\nThe rules are as follow:\n")
    print(
        "Get as close to 21 as possible by either stand, or hit (Hit means draw a card)."
    )
    print("Ace counts as 11, unless your total pass 21, in which case it counts as 1.")
    print("2 through 9 counts as is.")
    print("10, Jackal, Queen and King all count as 10.\n")
    print("A hand over 21 is considered a bust, a loss.\n")
    print(
        "Total of 21 equals Jackpot, a win. Unless dealer also has Jackpot, in which case dealer wins."
    )
    print("Dealer must draw at a hand < 16, and stand at 17 or above.\n")
    print("Jackpot payoff is 3/2 and a regular win is 1/1.\n")
    print("Press any key to continue.")


def random_card_from(available_cards: Deck) -> Card:

    color = random.choice(list(available_cards.keys()))
    value = random.choice(list(available_cards[color]))

    return Card(color, value)


def available_deck(currently_dealed: Deck) -> Deck:

    full_deck = deck.copy()

    for color in currently_dealed:
        full_deck[color] = [
            card_value
            for card_value in full_deck[color]
            if card_value not in currently_dealed[color]
        ]

    return full_deck


def add_card_to_deck(current_deck: Deck, card: Card) -> Deck:

    new_deck = current_deck.copy()

    if card.color not in new_deck:
        new_deck.update({card.color: []})

    new_deck[card.color].append(card.value)

    return new_deck


def deal_cards(
    available_cards: Deck, currently_dealt: Deck, nr_to_deal: int
) -> tuple[list[Card | None], Deck]:

    new_cards: list[Card | None] = []

    for _ in range(nr_to_deal):
        new_card = random_card_from(available_cards)
        currently_dealt = add_card_to_deck(currently_dealt, new_card)
        new_cards.append(new_card)

    return new_cards, currently_dealt


class GameState:

    currently_dealt: Deck
    player_hand: Hand
    dealer_hand: Hand
    player_wallet: int
    player_bet: int

    def __init__(self):

        self.player_wallet = 25
        self.player_bet = 0
        self.shuffle()

    def shuffle(self):

        self.currently_dealt = {}
        self.player_hand = []
        self.dealer_hand = []

    def initial_deal(self):

        # NOTE: Player
        available_cards = available_deck(self.currently_dealt)
        new_player_cards, self.currently_dealt = deal_cards(
            available_cards, self.currently_dealt, 2
        )
        self.player_hand.extend(new_player_cards)

        # NOTE: Dealer
        available_cards = available_deck(self.currently_dealt)
        new_dealer_cards, self.currently_dealt = deal_cards(
            available_cards, self.currently_dealt, 2
        )
        self.dealer_hand.extend(new_dealer_cards)

    def dealer_hand_value(self) -> int:

        return get_hand_value(self.dealer_hand)

    def player_hand_value(self) -> int:

        return get_hand_value(self.player_hand)

    def standing(self) -> Standing:

        return get_standing(self.player_hand_value(), self.dealer_hand_value())

    def hit_player(self):

        available_cards = available_deck(state.currently_dealt)
        new_player_cards, state.currently_dealt = deal_cards(
            available_cards, state.currently_dealt, 1
        )
        state.player_hand.extend(new_player_cards)

    def hit_dealer(self):

        available_cards = available_deck(state.currently_dealt)
        new_dealer_cards, state.currently_dealt = deal_cards(
            available_cards, state.currently_dealt, 1
        )
        state.dealer_hand.extend(new_dealer_cards)

    def bet(self):

        keep_asking = True

        while keep_asking:

            amount = input("First, place a bet $")

            if amount == "?":
                draw_rules()
                input()
                draw_logo()
                continue

            if not amount.isdigit():
                continue

            amount = int(amount)

            if amount > self.player_wallet:
                continue
            else:
                keep_asking = False
                self.player_bet = int(amount)
                self.player_wallet = self.player_wallet - int(amount)

        draw_logo()

    def maybe_payout(self):

        multiple = 0

        if self.standing() == Standing.Draw:
            multiple = 0
        elif self.standing() == Standing.PlayerBlackjack:
            multiple = 1.5
        elif self.player_won():
            multiple = 1
        else:
            return

        self.player_wallet += self.player_bet + round(self.player_bet * multiple)

    def player_won(self) -> bool:

        match self.standing():
            case Standing.Player:
                return True
            case Standing.DealerBust:
                return True
            case Standing.PlayerBlackjack:
                return True
            case _:
                return False

    def draw_board(self, conceal_dealer: bool = True):

        if conceal_dealer:
            draw_logo()
            print(
                f"Your hand:\n{ cards_to_art(self.player_hand) }Value: { self.player_hand_value() }\n"
            )
            print(f"Dealer's hand:\n{ cards_to_art([self.dealer_hand[0], None]) }")
        else:
            draw_logo()
            print(
                f"Your hand:\n{ cards_to_art(self.player_hand) }Value: { self.player_hand_value() }\n"
            )
            print(
                f"Dealer's hand:\n{ cards_to_art(self.dealer_hand) }Value: { self.dealer_hand_value() }\n"
            )


state = GameState()
