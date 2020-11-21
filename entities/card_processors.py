from entities.game_entities import Card, Cards, CardGroup


class GamesDetector:
    MIN_EQUAL_CARD_NUMBER_FOR_GAME = 3
    def __init__(self):
        pass

    def cards_with_same_number(self, cards):
        same_number_cards = []
        available_cards = cards
        while available_cards:
            next_card = available_cards[0]
            equal_cards = Cards.from_list_of_cards([card for card in available_cards if card.number == next_card.number])
            if len(equal_cards) >= self.MIN_EQUAL_CARD_NUMBER_FOR_GAME:
                same_number_cards.append(equal_cards)
            # Delete processed cards from available cards
            available_cards = Cards.from_list_of_cards([card for card in available_cards if card not in equal_cards])
        return same_number_cards

    def cards_with_ladder(self, cards):
        kind_groups = cards.group_by_kind()
        cards_with_ladder = []
        for kind in kind_groups.keys():
            consecutive_cards = []
            last_card = Card()
            kind_groups[kind].sort()
            for index, card in enumerate(kind_groups[kind]):
                if not last_card.number:
                    last_card = card
                    consecutive_cards.append(last_card)
                elif card.number - last_card.number == 1:
                    last_card = card
                    consecutive_cards.append(card)
                    if  index == len(kind_groups[kind]) - 1 and len(consecutive_cards) >= self.MIN_EQUAL_CARD_NUMBER_FOR_GAME:
                        cards_with_ladder.append(Cards.from_list_of_cards(consecutive_cards))
                else:
                    if len(consecutive_cards) >= self.MIN_EQUAL_CARD_NUMBER_FOR_GAME:
                        cards_with_ladder.append(Cards.from_list_of_cards(consecutive_cards))
                    last_card = card
                    consecutive_cards = [last_card]

        return cards_with_ladder

class CardsGrouper:
    def __init__(self):
        self.games_detector = GamesDetector()

    def group_by_games_found(self, cards):
        games = []
        rest = Cards()
        same_number = self.games_detector.cards_with_same_number(cards)
        # Remove "same number games" cards from collection
        for same_number_cards in same_number:
             games.append(cards.drop_cards(same_number_cards))
        ladders = self.games_detector.cards_with_ladder(cards)
        # Remove "ladder" cards from collection
        for ladder in ladders:
            games.append(cards.drop_cards(ladder))
        # Add ungrouped rest of cards to groupes list
        card_group = CardGroup(games=games, rest=cards)
        return card_group
