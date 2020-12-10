from entities.game_entities import Card, Cards
from entities.card_processors import CardsGrouper

class TestCardGroup:

    def _get_cards_group(self, cards):
        cards_grouper = CardsGrouper()
        return cards_grouper.group_by_games_found(cards)

    def test_value_computation_when_zero_rest(self):
        cards = Cards.from_list_of_cards([Card(4, 'E'), Card(6, 'B'), Card(3, 'E'), Card(5, 'E'),
                                          Card(6, 'C'), Card(6, 'E'), Card(6, 'O')])
        grouped_cards = self._get_cards_group(cards)
        assert grouped_cards.value() == -10

    def test_value_computation_when_there_is_rest(self):
        cards = Cards.from_list_of_cards([Card(4, 'E'), Card(6, 'B'), Card(4, 'O'), Card(5, 'E'),
                                          Card(6, 'C'), Card(6, 'E'), Card(6, 'O')])
        grouped_cards = self._get_cards_group(cards)
        assert grouped_cards.value() == 13

    def test_detection_of_zero_cut(self):
        cards = Cards.from_list_of_cards([Card(4, 'E'), Card(6, 'B'), Card(3, 'E'), Card(5, 'E'),
                                          Card(6, 'C'), Card(6, 'E'), Card(6, 'O')])
        grouped_cards = self._get_cards_group(cards)
        assert grouped_cards.find_type_of_cut() == "zero_cut"

    def test_detection_of_conga_cut(self):
        cards = Cards.from_list_of_cards([Card(4, 'E'), Card(2, 'E'), Card(3, 'E'), Card(5, 'E'),
                                          Card(7, 'E'), Card(6, 'E'), Card(8, 'E')])
        grouped_cards = self._get_cards_group(cards)
        assert grouped_cards.find_type_of_cut() == 'conga_cut'

    def test_detection_of_normal_cut(self):
        cards = Cards.from_list_of_cards([Card(4, 'E'), Card(6, 'B'), Card(3, 'E'), Card(5, 'E'),
                                          Card(6, 'C'), Card(6, 'E'), Card(8, 'O')])
        grouped_cards = self._get_cards_group(cards)
        assert grouped_cards.find_type_of_cut() == "normal_cut"