from entities.game_entities import Card, Cards
from entities.card_processors import GamesDetector

class TestGameDetection:

    def _initialize_hand(self, style=None):
        if not hasattr(self, 'games_detector'):
            self.games_detector = GamesDetector()
        hand = Cards()
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

    def _cards_are_consecutive(self, ladder):
        previous_card = None
        cards_are_consecutive = False
        for card in ladder:
            if previous_card is None:
                previous_card = card
            elif card.number - previous_card.number != 1:
                cards_are_consecutive = False
                break
            else:
                previous_card = card
                cards_are_consecutive = True
        return cards_are_consecutive

    def _has_sufficient_cards_with_same_number(self, cards):
        first_card = cards[0]
        same_number_cards = [card for card in cards if card.number == first_card.number]
        return len(same_number_cards) >= self.games_detector.MIN_EQUAL_CARD_NUMBER_FOR_GAME

    def test_two_same_number_game_detection(self):
        hand = self._initialize_hand("two_same_number_game_no_ladder")
        same = self.games_detector.cards_with_same_number(hand)
        first_game_has_sufficient_cards = self._has_sufficient_cards_with_same_number(same[0])
        second_game_has_sufficient_cards = self._has_sufficient_cards_with_same_number(same[1])
        assert first_game_has_sufficient_cards and second_game_has_sufficient_cards

    def test_detection_of_game_absence(self):
        hand = self._initialize_hand("no_game")
        same = self.games_detector.cards_with_same_number(hand)
        ladder = self.games_detector.cards_with_ladder(hand)
        assert not same and not ladder

    def test_detection_of_ladder(self):
        hand = self._initialize_hand("no_same_number_game_one_ladder")
        ladder = self.games_detector.cards_with_ladder(hand)
        assert self._cards_are_consecutive(ladder[0])

    def test_ladder_and_same_card_games_detection_in_same_hand(self):
        hand = self._initialize_hand('one_same_number_game_one_ladder')
        same = self.games_detector.cards_with_same_number(hand)
        ladder = self.games_detector.cards_with_ladder(hand)
        same_card_game_has_sufficient_cards = self._has_sufficient_cards_with_same_number(same[0])
        all_ladder_game_cards_are_consecutive = self._cards_are_consecutive(ladder[0])
        assert same_card_game_has_sufficient_cards and all_ladder_game_cards_are_consecutive



