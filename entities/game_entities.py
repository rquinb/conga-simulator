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

    def _index_of(self, card):
        for index, current_card in enumerate(self._cards_list):
            if card ==  current_card:
                return index
        else:
            return None

    def get_copy(self):
        return Cards.from_list_of_cards(self._cards_list)

    def sort(self):
        self._cards_list.sort(key=lambda x: x.number)

    def receive_card(self, card):
        if isinstance(card, Card):
            self._cards_list.append(card)
        else:
            raise TypeError('Please provide a Card object')

    def drop_cards(self, cards=None):
        if cards:
            if not (isinstance(cards,Card) or isinstance(cards,Cards)):
                raise TypeError
            if isinstance(cards, Card):
                cards = Cards.from_list_of_cards([cards])
            deleted_cards = []
            for card in cards:
                if card in self._cards_list:
                    deleted_cards.append(self._cards_list.pop(self._index_of(card)))
            if not deleted_cards:
                raise game_exceptions.CardNotFound(f'Cards not found in list. Cannot drop')
            elif len(deleted_cards) == 1:
                return deleted_cards.pop()
            else:
                return Cards.from_list_of_cards(deleted_cards)
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


class CardGroup:
    COMMODIN_VALUE = 20
    ZERO_REST_VALUE = -10
    def __init__(self, games, rest):
        self.games = games
        self.rest = rest

    def value(self):
        value = 0
        if not self.rest:
            return self.ZERO_REST_VALUE
        for card in self.rest:
            value += card.number if card.number is not None else self.COMMODIN_VALUE
        return value


class Deck:
    def __init__(self):
        self.cards_in_deck = self._initialize_deck()
        self.dropped_cards = Cards()

    def _initialize_deck(self):
        cards = []
        # Adds all non-commpdin cards
        for number in range(1,MAX_NUMBER + 1):
            for kind in KINDS.keys():
                cards.append(Card(number, kind))
        cards = Cards.from_list_of_cards(cards)
        cards.shuffle_cards()
        return cards

    def retrieve_card(self):
        if not self.cards_in_deck:
            self.cards_in_deck = self._initialize_deck()
            self.dropped_cards = Cards()
        return self.cards_in_deck.drop_cards()

    def play_card(self, card):
        self.dropped_cards.receive_card(card)


class Player:
    def __init__(self, name, is_hand=False):
        self.cards = Cards()
        self.name = name
        self.is_hand = is_hand
        self.score = 0
        self.winner = False
        self.has_cut = False
        self.move = 0

    def add_points(self, points):
        self.score += points

    def remove_points(self, points):
        self.score -= points

    def cut(self):
        self.has_cut = True


class Game:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.deck = Deck()
        self.results = []
