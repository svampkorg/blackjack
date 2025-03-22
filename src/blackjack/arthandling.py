from .blackjack_types import Card


def value_to_sign(value: int) -> str:

    match value:
        case 13:
            return "K"
        case 12:
            return "Q"
        case 11:
            return "J"
        case 1:
            return "A"
        case _:
            return str(value)


def card_art(card: Card) -> list[str]:

    card_parts: list[str] = []
    card_parts.append(f"╭───╮")
    card_parts.append(
        f"│{value_to_sign(card.value)}{" " if card.value == 10 else "  "}│"
    )
    card_parts.append(f"│ {card.color} │")
    card_parts.append(
        f"│{" " if card.value == 10 else "  "}{value_to_sign(card.value)}│"
    )
    card_parts.append(f"╰───╯")

    return card_parts


def facedown_card_art() -> list[str]:

    card_parts: list[str] = []
    card_parts.append("╭───╮")
    card_parts.append("│?  │")
    card_parts.append("│ ? │")
    card_parts.append("│  ?│")
    card_parts.append("╰───╯")

    return card_parts


def cards_to_art(cards: list[Card | None]):

    cards_arts: list[list[str]] = []
    full_art_len = len(facedown_card_art()) if not cards[0] else len(card_art(cards[0]))

    for card in cards:
        if not card:
            cards_arts.append(facedown_card_art())
        else:
            cards_arts.append(card_art(card))

    nr_of_cards = len(cards_arts)
    art_string = ""

    for art_index in range(full_art_len):
        for card_index in range(nr_of_cards):
            art_string += cards_arts[card_index][art_index]

        art_string += "\n"

    return art_string
