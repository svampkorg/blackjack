type Deck = dict[str, list[int]]

type Hand = list[Card|None]

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    color:str
    value:int

    def __str__(self) -> str:
        return self.color + ":" + str(self.value)

            
deck: Deck = {
        "󰣎": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "󰣑": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "󰣐": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        "󰣏": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
}
