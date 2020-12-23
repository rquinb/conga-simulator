import copy
import numpy as np
from entities.game_entities import Cards, Game, Move, Cut
from entities.card_processors import CardsGrouper


class PlayerBuilder:

    def build_player(self, name, agent_type="conservative_chooser", accepted_cards_range=None,
                     max_rest_for_cutting=None):
        if agent_type == "conservative_chooser":
            constructor_params = {'name': name}
            if accepted_cards_range:
                if len(accepted_cards_range) == 2:
                    constructor_params["min_card_number_accepted"] = accepted_cards_range[0]
                    constructor_params["max_card_number_accepted"] = accepted_cards_range[1]
            if max_rest_for_cutting:
                constructor_params["max_rest_for_cutting"] = max_rest_for_cutting
            return self._build_conservative_chooser(**constructor_params)
        raise ValueError(f'Invalid agent type: "{agent_type}" is not an existent agent_type')

    @staticmethod
    def _build_conservative_chooser(name, min_card_number_accepted=1, max_card_number_accepted=12,
                                    max_rest_for_cutting=10):
        return ConservativeMinRest(name=name,
                                   min_card_number_accepted=min_card_number_accepted,
                                   max_card_number_accepted=max_card_number_accepted,
                                   max_rest_for_cutting=max_rest_for_cutting)


class ValueImpactAnalysis:
    def __init__(self, rest_value, less_valuable_card, has_value_improved, potential_cut_type):
        self.rest_value = rest_value
        self.less_valuable_card = less_valuable_card
        self.has_value_improved = has_value_improved
        self.potential_cut_type = potential_cut_type


class Player:
    def __init__(self, name):
        self.cards = Cards()
        self.name = name
        self.winner = False
        self.cut = None
        self.played_dropped_card = False
        self.rest_value = None

    def value_of_current_hand(self):
        cards_grouper = CardsGrouper()
        return cards_grouper.group_by_games_found(copy.deepcopy(self.cards)).value()

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
        potential_cut_type = card_group.find_type_of_cut()
        return ValueImpactAnalysis(rest_value=rest_value,
                                   less_valuable_card=max_card,
                                   potential_cut_type=potential_cut_type,
                                   has_value_improved=rest_value < self.rest_value)

    def play_cut(self, cut_type):
        self.cut = Cut(value=True, kind=cut_type)

    def has_cut(self):
        return self.cut.value if self.cut else False


class ConservativeMinRest(Player):
    def __init__(self, name, max_rest_for_cutting=10, max_card_number_accepted=12, min_card_number_accepted=1):
        super().__init__(name)
        self.max_rest_for_cutting = max_rest_for_cutting
        self.max_card_number_accepted = max_card_number_accepted
        self.min_card_number_accepted = min_card_number_accepted

    def _play(self, card, score):
        value_analysis = self._analyze_card_impact_on_value(card)
        self.rest_value = value_analysis.rest_value
        self.cards.receive_card(card)
        if self.rest_value < self.max_rest_for_cutting and score.get_score(self.name) + self.rest_value < Game.MAX_SCORE:
            self.play_cut(value_analysis.potential_cut_type)
        return self.cards.drop_cards(value_analysis.less_valuable_card)

    def make_move(self, deck, score):
        retrieved_card = None
        card_to_play = None
        if deck.dropped_cards:
            candidate_card = deck.dropped_cards.drop_cards()
            is_between_acceptable_number_range = self.min_card_number_accepted <= candidate_card.number <= self.max_card_number_accepted
            analysis = self._analyze_card_impact_on_value(candidate_card)
            retrieved_card = candidate_card
            if analysis.has_value_improved and is_between_acceptable_number_range:
                card_to_play = self._play(retrieved_card, score)
                self.played_dropped_card = True
                deck.play_card(retrieved_card)
            else:
                card_to_play = candidate_card
                deck.play_card(retrieved_card)
        if not self.played_dropped_card:
            candidate_card = deck.retrieve_card()
            is_between_acceptable_number_range = self.min_card_number_accepted <= candidate_card.number <= self.max_card_number_accepted
            analysis = self._analyze_card_impact_on_value(candidate_card)
            retrieved_card = candidate_card
            if analysis.has_value_improved and is_between_acceptable_number_range:
                card_to_play = self._play(retrieved_card, score)
                deck.play_card(retrieved_card)
            else:
                card_to_play = candidate_card
                deck.play_card(retrieved_card)
        return deck, Move(player_name=self.name,
                          retrieved_card=retrieved_card,
                          played_card=card_to_play,
                          cut=self.cut,
                          hand=self.cards.get_copy())
