from entities.game_entities import Card, Cards
from entities.card_processors import CardsGrouper

class TestCardsGrouper:

    def test_detection_of_one_ladder_and_one_same_number_game_with_rest(self):
        cards = Cards.from_list_of_cards([Card(1, 'O'), Card(6, 'B'), Card(3, 'O'), Card(2, 'O'),
                                          Card(6, 'C'), Card(6, 'E'), Card(10, 'O')])
        cards_grouper = CardsGrouper()
        grouped_cards = cards_grouper.group_by_games_found(cards)
        assert len(grouped_cards.games) == 2 and grouped_cards.rest

    def test_detection_of_one_ladder_and_no_other_game(self):
        cards = Cards.from_list_of_cards([Card(4, 'E'), Card(7, 'B'), Card(3, 'E'), Card(5, 'E'),
                                          Card(6, 'C'), Card(6, 'E'), Card(11, 'O')])
        cards_grouper = CardsGrouper()
        grouped_cards = cards_grouper.group_by_games_found(cards)
        assert len(grouped_cards.games) == 1 and grouped_cards.rest

    def test_detection_of_one_same_number_and_no_other_game(self):
        cards = Cards.from_list_of_cards([Card(4, 'E'), Card(7, 'B'), Card(3, 'E'), Card(6, 'E'),
                                          Card(6, 'C'), Card(6, 'B'), Card(6, 'O')])
        cards_grouper = CardsGrouper()
        grouped_cards = cards_grouper.group_by_games_found(cards)
        assert len(grouped_cards.games) == 1 and grouped_cards.rest

