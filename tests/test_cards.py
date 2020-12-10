import game_exceptions
from entities.game_entities import Card, Cards


class TestCards:

    def test_building_cards_from_list(self):
        all_card_items_belong_to_cards = True
        list_of_cards = [Card(10,"B"), Card(5,"E"), Card(12, "C")]
        cards = Cards.from_list_of_cards(list_of_cards)
        for index, card in enumerate(cards):
            if card != list_of_cards[index]:
                all_card_items_belong_to_cards = False
        assert isinstance(cards, Cards) and all_card_items_belong_to_cards

    def test_sorting(self):
        correctly_sorted = True
        list_of_cards = [Card(11, "B"), Card(4, "E"), Card(7, "C")]
        cards = Cards.from_list_of_cards(list_of_cards)
        cards.sort()
        for index, card in enumerate(cards):
            if (index == 0 and card != list_of_cards[1]) or (index == 1 and card != list_of_cards[2]) or (index == 2 and card != list_of_cards[0]):
                correctly_sorted = False
                break
        assert correctly_sorted

    def test_receiving_valid_card(self):
        cards = Cards()
        number_of_cards_before_receiving_card = len(cards)
        valid_card = Card(4, "O")
        cards.receive_card(valid_card)
        number_of_cards_after_receiving_card = len(cards)
        assert cards[0] == valid_card and number_of_cards_after_receiving_card - number_of_cards_before_receiving_card == 1

    def test_receiving_a_non_card_element(self):
        cards = Cards()
        number_of_cards_before_receiving_card = len(cards)
        invalid_card = "string"
        try:
            cards.receive_card(invalid_card)
            has_rised_type_error = False
        except TypeError:
            has_rised_type_error = True
        except Exception:
            has_rised_type_error = False
        number_of_cards_after_receiving_card = len(cards)
        assert has_rised_type_error and number_of_cards_after_receiving_card == number_of_cards_before_receiving_card

    def test_dropping_a_card_that_exists_in_cards(self):
        card_to_drop = Card(1, "E")
        list_of_cards = [Card(3, "E"), card_to_drop , Card(8, "O")]
        cards = Cards.from_list_of_cards(list_of_cards)
        number_of_cards_before_dropping_card = len(cards)
        dropped_card = cards.drop_cards(card_to_drop)
        number_of_cards_after_dropping_card = len(cards)
        assert dropped_card == card_to_drop and number_of_cards_before_dropping_card - number_of_cards_after_dropping_card == 1

    def test_dropping_a_card_that_does_not_exists_in_cards(self):
        card_to_drop = Card(11, "E")
        list_of_cards = [Card(3, "E"), Card(3,"B") , Card(8, "O")]
        cards = Cards.from_list_of_cards(list_of_cards)
        number_of_cards_before_dropping_card = len(cards)
        try:
            cards.drop_cards(card_to_drop)
            has_raised_card_not_found_exception = False
        except game_exceptions.CardNotFound:
            has_raised_card_not_found_exception = True
        except Exception:
            has_raised_card_not_found_exception = False
        number_of_cards_after_dropping_card = len(cards)
        assert has_raised_card_not_found_exception and number_of_cards_before_dropping_card == number_of_cards_after_dropping_card

    def test_dropping_last_card_when_cards_exist(self):
        list_of_cards = [Card(2, "E"), Card(1,"B") , Card(12, "O")]
        cards = Cards.from_list_of_cards(list_of_cards)
        number_of_cards_before_dropping_card = len(cards)
        dropped_card = cards.drop_cards()
        number_of_cards_after_dropping_card = len(cards)
        assert dropped_card == list_of_cards[-1] and number_of_cards_before_dropping_card - number_of_cards_after_dropping_card == 1

    def test_dropping_last_card_when_no_card_in_cards(self):
        cards = Cards()
        number_of_cards_before_dropping_card = len(cards)
        try:
            cards.drop_cards()
            has_raised_empty_list_of_cards_exception = False
        except game_exceptions.EmptyListOfCards:
            has_raised_empty_list_of_cards_exception = True
        except Exception:
            has_raised_empty_list_of_cards_exception = False
        number_of_cards_after_dropping_card = len(cards)
        assert has_raised_empty_list_of_cards_exception and number_of_cards_before_dropping_card == number_of_cards_after_dropping_card

    def test_dropping_cards_that_exists_in_cards(self):
        list_of_cards_to_drop = [Card(1, "E"), Card(4,"O")]
        cards_to_drop = Cards.from_list_of_cards(list_of_cards_to_drop)
        list_of_cards = [Card(3, "E"), Card(8, "O")] + list_of_cards_to_drop
        cards = Cards.from_list_of_cards(list_of_cards)
        number_of_cards_before_dropping_card = len(cards)
        dropped_cards = cards.drop_cards(cards_to_drop)
        number_of_cards_after_dropping_card = len(cards)
        assert dropped_cards == cards_to_drop and number_of_cards_before_dropping_card - number_of_cards_after_dropping_card == len(cards_to_drop)

    def test_dropping_cards_that_do_not_exist_in_cards(self):
        list_of_cards_to_drop = [Card(3, "E"), Card(5,"O")]
        cards_to_drop = Cards.from_list_of_cards(list_of_cards_to_drop)
        list_of_cards = [Card(3, "E"), Card(9, "O")]
        cards = Cards.from_list_of_cards(list_of_cards)
        number_of_cards_before_dropping_card = len(cards)
        try:
            cards.drop_cards(cards_to_drop)
            has_raised_card_not_found_exception = False
        except game_exceptions.CardNotFound:
            has_raised_card_not_found_exception = True
        except Exception:
            has_raised_card_not_found_exception = False
        number_of_cards_after_dropping_card = len(cards)
        assert has_raised_card_not_found_exception and number_of_cards_before_dropping_card == number_of_cards_after_dropping_card

    def test_group_by_kind(self):
        ten_of_basto = Card(10, 'B')
        nine_of_gold = Card(9, 'O')
        six_of_cup = Card(6, 'C')
        four_of_basto = Card(4,'B')
        twelve_of_gold = Card(12,'O')
        eleven_of_gold = Card(11, 'O')
        cards = Cards.from_list_of_cards([ten_of_basto, nine_of_gold, six_of_cup , four_of_basto, twelve_of_gold, eleven_of_gold])
        kind_groups = cards.group_by_kind()
        for kind in ['B', 'O', 'C']:
            if kind == "B":
                cards_were_correctly_grouped = ten_of_basto in kind_groups[kind] and four_of_basto in kind_groups[kind] \
                                               and len(kind_groups[kind]) == 2
            elif kind == "O":
                cards_were_correctly_grouped = twelve_of_gold in kind_groups[kind] and eleven_of_gold in kind_groups[kind] \
                                               and nine_of_gold in kind_groups[kind] and len(kind_groups[kind]) == 3
            elif kind == "C":
                cards_were_correctly_grouped = six_of_cup in kind_groups[kind] and len(kind_groups[kind]) == 1
            else:
                cards_were_correctly_grouped = False
        assert cards_were_correctly_grouped

    def test_equality_detection(self):
        list_of_cards = [Card(10,'O'), Card(3,'C')]
        reversed_list_of_cards = list_of_cards.copy()
        reversed_list_of_cards.reverse()
        cards_a = Cards.from_list_of_cards(list_of_cards)
        cards_b = Cards.from_list_of_cards(reversed_list_of_cards)
        assert cards_a == cards_b

    def test_inequality_detection(self):
        list_of_cards_a = [Card(10,'O'), Card(3,'C')]
        list_of_cards_b = [Card(10,'O'), Card(4,'C')]
        cards_a = Cards.from_list_of_cards(list_of_cards_a)
        cards_b = Cards.from_list_of_cards(list_of_cards_b)
        assert cards_a != cards_b


