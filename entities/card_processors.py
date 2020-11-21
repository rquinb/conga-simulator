import game_exceptions
from entities.game_entities import Card


class GamesDetector:
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
            consecutive_cards = []
            last_card = Card()
            sorted_cards = hand.sort_cards(kind_groups[kind])
            for index, card in enumerate(sorted_cards):
                if not last_card.number:
                    last_card = card
                    consecutive_cards.append(last_card)
                elif card.number - last_card.number == 1:
                    last_card = card
                    consecutive_cards.append(card)
                    if  index == len(sorted_cards) - 1 and len(consecutive_cards) >= self.MIN_EQUAL_CARD_NUMBER_FOR_GAME:
                        cards_with_ladder.append(consecutive_cards)
                else:
                    if len(consecutive_cards) >= self.MIN_EQUAL_CARD_NUMBER_FOR_GAME:
                        cards_with_ladder.append(consecutive_cards)
                    last_card = card
                    consecutive_cards = [last_card]

        return cards_with_ladder

class CardsGrouper:
    def __init__(self):
        self.games_detector = GamesDetector()

    def group_by_game(self, hand):
        pass
