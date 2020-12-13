from entities.game_entities import Cards, Deck


class TestDeck:

    def test_retrieving_card(self):
        deck = Deck()
        card_to_retrieve = deck.cards_in_deck[-1]
        retrieved_card = deck.retrieve_card()
        assert retrieved_card == card_to_retrieve and len(deck.cards_in_deck) == 47

    def test_retrieving_card_when_no_card_left(self):
        deck = Deck()
        deck.cards_in_deck = Cards()
        deck.retrieve_card()
        assert len(deck.cards_in_deck) == 47

    def test_play_card(self):
        deck = Deck()
        cards_in_deck_before_playing = len(deck.cards_in_deck)
        cards_played_before_playing = len(deck.dropped_cards)
        card_to_play = deck.retrieve_card()
        deck.play_card(card_to_play)
        cards_in_deck_after_playing = len(deck.cards_in_deck)
        cards_played_after_playing = len(deck.dropped_cards)
        assert cards_in_deck_before_playing - cards_in_deck_after_playing == 1 and cards_played_after_playing - cards_played_before_playing == 1
