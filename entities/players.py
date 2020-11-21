from entities.game_entities import Player
from entities.card_processors import CardsGrouper

class ValueImpactAnalysis:
    def __init__(self, rest_value, less_valuable_card, has_value_improved):
        self.rest_value = rest_value
        self.less_valuable_card = less_valuable_card
        self.has_value_improved = has_value_improved


class ConservativeRandomRest(Player):
    def __init__(self, name, is_hand=False):
        super().__init__(name, is_hand)
        self.rest_value = self.value_of_current_hand()

    def value_of_current_hand(self):
        cards_gruper = CardsGrouper()
        return cards_gruper.group_by_games_found(self.cards).value()

    def analyze_card_impact_on_value(self, card):
        max_card = None
        cards_to_value = self.cards.get_copy()
        cards_to_value.receive_card(card)
        cards_grouper = CardsGrouper()
        card_group = cards_grouper.group_by_games_found(cards_to_value)
        for card in card_group.rest:
            if not max_card:
                max_card = card
            elif card.number > max_card.number:
                max_card = card
        card_group.rest.drop_cards(max_card)
        rest_value = card_group.value()
        return ValueImpactAnalysis(rest_value=rest_value,
                                   less_valuable_card=max_card,
                                   has_value_improved=rest_value < self.rest_value )

    def play(self, card):
        value_analysis = self.analyze_card_impact_on_value(card)
        self.rest_value = value_analysis.rest_value
        if self.rest_value < 10:
            self.cut()
        return self.cards.drop_cards(value_analysis.less_valuable_card)
