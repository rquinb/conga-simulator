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
        return f"{self.number} de {KINDS.get(self.kind)}" if not self.commodin else "Comodin"

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

    def sort_cards(self, cards):
        cards.sort(key=lambda x: x.number)
        return cards

    def group_cards_by_kind(self, cards):
        kind_groups = {}
        for kind in {card.kind for card in cards}:
            kind_groups[kind] = [card for card in cards if card.kind == kind]
        return kind_groups

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


class Game:
    MIN_EQUAL_CARD_NUMBER_FOR_GAME = 3
    def __init__(self):
        pass

    def cards_with_same_number(self, hand):
        same_number_cards = []
        available_cards = hand.cards
        while available_cards:
            next_card = available_cards[0]
            equal_cards = [card for card in available_cards if card.number == next_card.number]
            if len(equal_cards) >= self.MIN_EQUAL_CARD_NUMBER_FOR_GAME:
                same_number_cards.append(equal_cards)
            # Delete processed cards from available list
            available_cards = [card for card in available_cards if card not in equal_cards]
        return same_number_cards

    def cards_with_ladder(self, hand):
        kind_groups = hand.group_cards_by_kind(hand.cards)
        cards_with_ladder = []
        for kind in kind_groups.keys():
            consecutive_numbers = 0
            last_card = Card()
            consecutive_cards = []
            sorted_cards = hand.sort_cards(kind_groups[kind])
            for index, card in enumerate(sorted_cards):
                if not last_card.number:
                    last_card = card
                    consecutive_cards.append(last_card)
                    consecutive_numbers += 1
                elif card.number - last_card.number == 1:
                    last_card = card
                    consecutive_numbers += 1
                    consecutive_cards.append(card)
                else:
                    last_card = card
                    consecutive_cards = [last_card]
                    consecutive_numbers = 1
                if len(consecutive_cards) >= self.MIN_EQUAL_CARD_NUMBER_FOR_GAME:
                    cards_with_ladder.append(consecutive_cards)
        return cards_with_ladder







