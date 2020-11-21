from entities.game_entities import Card, Hand
from entities.card_processors import GamesDetector

class TestGameDetection:

    def _initialize_hand(self, style=None):
        hand = Hand()
        if style == "one_same_number_game_one_ladder":
            hand.receive_card(Card(1, "O"))
            hand.receive_card(Card(1, "B"))
            hand.receive_card(Card(1, "C"))
            hand.receive_card(Card(3, "O"))
            hand.receive_card(Card(4, "O"))
            hand.receive_card(Card(5, "O"))
            hand.receive_card(Card(9, "O"))
        elif style == "two_same_number_game_no_ladder":
            hand.receive_card(Card(1, "O"))
            hand.receive_card(Card(1, "B"))
            hand.receive_card(Card(1, "C"))
            hand.receive_card(Card(3, "E"))
            hand.receive_card(Card(3, "O"))
            hand.receive_card(Card(3, "C"))
            hand.receive_card(Card(9, "O"))
        elif style == "no_same_number_game_one_ladder":
            hand.receive_card(Card(1, "O"))
            hand.receive_card(Card(2, "B"))
            hand.receive_card(Card(4, "C"))
            hand.receive_card(Card(5, "E"))
            hand.receive_card(Card(6, "E"))
            hand.receive_card(Card(7, "E"))
            hand.receive_card(Card(8, "E"))
        elif style == "no_game":
            hand.receive_card(Card(1, "O"))
            hand.receive_card(Card(2, "B"))
            hand.receive_card(Card(4, "C"))
            hand.receive_card(Card(5, "E"))
            hand.receive_card(Card(6, "E"))
            hand.receive_card(Card(10, "E"))
            hand.receive_card(Card(11, "C"))
        return hand

    def test_two_same_number_game_detection(self):
        game_detector = GamesDetector()
        hand = self._initialize_hand("two_same_number_game_no_ladder")
        same = game_detector.cards_with_same_number(hand)
        for game in same:
            first_card = game[0]
            same_number_cards = [card for card in game if card.number == first_card.number]
            assert len(same_number_cards) >= game.MIN_EQUAL_CARD_NUMBER_FOR_GAME

    def test_correct_detection_of_both_same_number_games(self):
        game_detector = GamesDetector()
        hand = self._initialize_hand("two_same_number_game_no_ladder")
        same = game_detector.cards_with_same_number(hand)
        assert len(same) == 2

