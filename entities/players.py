import numpy as np
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
        self.rest_value = None

    def value_of_current_hand(self):
        cards_grouper = CardsGrouper()
        return cards_grouper.group_by_games_found(self.cards).value()

    def _analyze_card_impact_on_value(self, card):
        max_card = None
        cards_to_value = self.cards.get_copy()
        cards_to_value.receive_card(card)
        cards_grouper = CardsGrouper()
        card_group = cards_grouper.group_by_games_found(cards_to_value)
        for card_in_group in card_group.rest:
            if not max_card:
                max_card = card_in_group
            elif card_in_group.number > max_card.number:
                max_card = card_in_group
        if max_card is None:
            longest_game_index = np.argmax([len(game) for game in card_group.games])
            max_card = card_group.games[longest_game_index][-1]
        card_group.drop_card_from_group(max_card)
        rest_value = card_group.value()
        return ValueImpactAnalysis(rest_value=rest_value,
                                   less_valuable_card=max_card,
                                   has_value_improved=rest_value < self.rest_value )

    def _play(self, card):
        value_analysis = self._analyze_card_impact_on_value(card)
        self.rest_value = value_analysis.rest_value
        self.cards.receive_card(card)
        if self.rest_value < 10:
            self.cut()
        return self.cards.drop_cards(value_analysis.less_valuable_card)

    def make_move(self, deck):
        if deck.dropped_cards:
            candidate_card = deck.dropped_cards.drop_cards()
            analysis = self._analyze_card_impact_on_value(candidate_card)
            if analysis.has_value_improved:
                deck.play_card(self._play(candidate_card))
                self.played_dropped_card = True
            else:
                deck.play_card(candidate_card)
        if not self.played_dropped_card:
            candidate_card = deck.retrieve_card()
            analysis = self._analyze_card_impact_on_value(candidate_card)
            if analysis.has_value_improved:
                deck.play_card(self._play(candidate_card))
            else:
                deck.play_card(candidate_card)
        return deck
