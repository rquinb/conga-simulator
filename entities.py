import random
import game_exceptions

KINDS = {"E":"espada", "O": "oro", "B": "basto", "C": "copa"}
MAX_NUMBER = 12
MAX_COMMODINES = 2

class Card:
    def __init__(self, number=None, kind=None, commodin=False):
        self.number = self._set_number(number) if number else number
        self.kind = self._set_kind(kind) if kind else kind
        self.commodin= commodin

    def _set_number(self, number):
        if number <= MAX_NUMBER:
            return number
        else:
            raise game_exceptions.InvalidCardNumber(f"Please provide a number less than or equal to {MAX_NUMBER}")

    def _set_kind(self, kind):
        if kind in KINDS.keys():
            return kind
        else:
            raise game_exceptions.InvalidCardKind(f"Please provide a valid kind: It should be one of {KINDS}")

    def to_string(self):
        return f"{self.number} de {KINDS.get(self.kind)}" if not self.commodin else "Commodin"

    def __str__(self):
        return self.to_string()

    def __eq__(self, other_card):
        return self.number == other_card.number and self.kind == other_card.kind



class Hand:
    CARD_LIMIT = 7
    def __init__(self, is_hand=False):
        self.cards = []
        self.games = []
        self.is_hand = is_hand

    def receive_card(self, card):
        if len(self.cards) < self.CARD_LIMIT or (len(self.cards) < self.CARD_LIMIT + 1 and self.is_hand):
            self.cards.append(card)
        else:
            raise game_exceptions.CardLimitException

    def drop_card(self, card):
        for index, current_card in enumerate(self.cards):
            if current_card == card:
                return self.cards.pop(index)
        return None


class Deck:
    def __init__(self):
        self.cards = self._initialize_deck()

    def _initialize_deck(self):
        cards = []
        # Adds all non-commpdin cards
        for number in range(1,MAX_NUMBER + 1):
            for kind in KINDS.keys():
                cards.append(Card(number, kind))
        # Adds commodins
        for _ in range(MAX_COMMODINES):
            cards.append(Card(commodin=True))
        self._shuffle_cards(cards)
        return cards

    @staticmethod
    def _shuffle_cards(cards):
        random.shuffle(cards)

    def shuffle_deck(self):
        self._shuffle_cards(self.cards)