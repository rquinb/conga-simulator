import random
from collections.abc import Sequence
import game_exceptions



class Card:
    def __init__(self, number=None, kind=None, commodin=False):
        self.number = self._set_number(number) if number else number
        self.kind = self._set_kind(kind) if kind else kind
        self.commodin = commodin

    @staticmethod
    def _set_number(number):
        if number <= Cards.MAX_NUMBER:
            return number
        raise game_exceptions.InvalidCardNumber(f"Please provide a number less than or equal to {Cards.MAX_NUMBER}")

    @staticmethod
    def _set_kind(kind):
        if kind in Cards.KINDS.keys():
            return kind
        raise game_exceptions.InvalidCardKind(f"Please provide a valid kind: It should be one of {Cards.KINDS}")

    def to_string(self):
        return f"{self.number} de {Cards.KINDS.get(self.kind)}" if not self.commodin else "Comodin"

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return self.to_string()

    def __eq__(self, other_card):
        return self.number == other_card.number and self.kind == other_card.kind

    def __hash__(self):
        return hash(self.to_string())


class Cards(Sequence):
    KINDS = {"E": "espada", "O": "oro", "B": "basto", "C": "copa"}
    MAX_NUMBER = 12
    MAX_COMMODINES = 2

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
            if card == current_card:
                return index
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
            if not isinstance(cards, (Card, Cards)):
                raise TypeError
            if isinstance(cards, Card):
                cards = Cards.from_list_of_cards([cards])
            cards_to_delete = []
            for card in cards:
                if card in self._cards_list:
                    cards_to_delete.append(card)
                else:
                    raise game_exceptions.CardNotFound(f'Card: {card} not found in list. Cannot drop cards')
            deleted_cards = [self._cards_list.pop(self._index_of(card)) for card in cards_to_delete]
            if len(deleted_cards) == 1:
                return deleted_cards.pop()
            return Cards.from_list_of_cards(deleted_cards)
        if self._cards_list:
            return self._cards_list.pop()
        raise game_exceptions.EmptyListOfCards('Card list is empty. Cannot remove more cards')

    def group_by_kind(self):
        kind_groups = {}
        for kind in {card.kind for card in self._cards_list}:
            kind_groups[kind] = Cards.from_list_of_cards([card for card in self._cards_list if card.kind == kind])
        return kind_groups

    def shuffle_cards(self):
        random.shuffle(self._cards_list)

    def __eq__(self, other):
        set_cards = set(self)
        set_other_cards = set(other)
        return set_cards == set_other_cards


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

    def drop_card_from_group(self, card):
        if card in self.rest:
            return self.rest.drop_cards(card)
        for game in self.games:
            if card in game:
                return game.drop_cards(card)
        return None

    def _has_cut_in_zero(self):
        return not self.rest

    def _has_conga(self):
        return len(self.games) == 1 and not self.rest

    def find_type_of_cut(self):
        if self._has_conga():
            return "conga_cut"
        if self._has_cut_in_zero():
            return "zero_cut"
        return "normal_cut"


class Deck:
    def __init__(self):
        self.cards_in_deck = self._initialize_deck()
        self.dropped_cards = Cards()

    @staticmethod
    def _initialize_deck():
        cards = []
        # Adds all non-commpdin cards
        for number in range(1, Cards.MAX_NUMBER + 1):
            for kind in Cards.KINDS:
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


class Game:
    MAX_SCORE = 100
    CARDS_IN_HAND = 7
    CUT_TYPES = ['no_cut', 'normal_cut', "zero_cut", 'conga_cut']

    def __init__(self, players):
        self.players = players
        self.winner = None
        self.deck = Deck()
        self.results = []

    def report_results(self):
        return {"score_evolution": self.results,
                "winner": self.players[self.winner].name}


class Cut:
    def __init__(self, value, kind):
        self.value = value
        self.kind = kind

    def to_dict(self):
        return self.__dict__
