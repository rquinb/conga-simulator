import random
import game_exceptions
from collections import Sequence

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
        return f"{self.number} de {KINDS.get(self.kind)}" if not self.commodin else "Comodin"

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return self.to_string()

    def __eq__(self, other_card):
        return self.number == other_card.number and self.kind == other_card.kind


class Cards(Sequence):
    def __init__(self):
        self._cards_list = []

    def __len__(self):
        return len(self._cards_list)

    def __getitem__(self, index):
        return self._cards_list[index]

    @staticmethod
    def from_list_of_cards(cards_list):
        cards = Cards()
        for card in cards_list:
            cards.receive_card(card)
        return cards

    def sort(self):
        self._cards_list.sort(key=lambda x: x.number)

    def receive_card(self, card):
        if isinstance(card, Card):
            self._cards_list.append(card)
        else:
            raise TypeError('Please provide a Card object')

    def drop_card(self, card=None):
        if card:
            for index, current_card in enumerate(self._cards_list):
                if current_card == card:
                    return self._cards_list.pop(index)
            raise game_exceptions.CardNotFound(f'Card: {card} was not found in list. Cannot drop')
        elif self._cards_list:
            return self._cards_list.pop()
        else:
            raise game_exceptions.EmptyListOfCards('Card list is empty. Cannot remove more cards')

    def group_by_kind(self):
        kind_groups = {}
        for kind in {card.kind for card in self._cards_list}:
            kind_groups[kind] = Cards.from_list_of_cards([card for card in self._cards_list if card.kind == kind])
        return kind_groups

    def shuffle_cards(self):
        random.shuffle(self._cards_list)


class Hand:
    CARD_LIMIT = 7
    def __init__(self, is_hand=False):
        self.cards = Cards()
        self.games = []
        self.cards_combinations = []
        self.is_hand = is_hand


    def receive_card(self, card):
        if len(self.cards) < self.CARD_LIMIT or (len(self.cards) < self.CARD_LIMIT + 1 and self.is_hand):
            self.cards.receive_card(card)
        else:
            raise game_exceptions.CardLimitException

    def drop_card(self, card):
        return self.cards.drop_card(card)


class Deck:
    def __init__(self):
        self.cards = self._initialize_deck()

    def _initialize_deck(self):
        cards = []
        # Adds all non-commpdin cards
        for number in range(1,MAX_NUMBER + 1):
            for kind in KINDS.keys():
                cards.append(Card(number, kind))
        # Adds commodines
        for _ in range(MAX_COMMODINES):
            cards.append(Card(commodin=True))
        cards = Cards.from_list_of_cards(cards)
        cards.shuffle_cards()
        return cards

    def retrieve_card(self):
        if not self.cards:
            self.cards = self._initialize_deck()
        return self.cards.drop_card()

    def create_hand(self, is_hand=False):
        hand = Hand(is_hand=is_hand)
        while True:
            try:
                hand.receive_card(self.retrieve_card())
            except game_exceptions.CardLimitException:
                break
        return hand


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = None
        self.score = 0
        self.winner = False

    def assign_hand(self, hand):
        self.hand = hand

    def add_points(self, points):
        self.score += points

    def remove_points(self, points):
        self.score -= points


class Game:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.deck = Deck()
        self.results = []


