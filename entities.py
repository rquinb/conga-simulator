import game_exceptions

class Card:
    def __init__(self, number=None, kind=None, commodin=False):
        self.number = number
        self.kind = kind
        self.commodin=commodin

    def __eq__(self, other_card):
        return self.number == other_card.number and self.kind == other_card.kind


class Hand:
    CARD_LIMIT = 7
    def __init__(self, is_hand=False):
        self.cards = []
        self.games = []
        self.is_hand = is_hand

    def receive_card(self, card):
        if len(self.cards) < 7 or (len(self.cards) < 8 and self.is_hand):
            self.cards.append(card)
        else:
            raise game_exceptions.CardLimitException

    def drop_card(self, card):
        for index, current_card in enumerate(self.cards):
            if current_card == card:
                self.cards.pop(index)

