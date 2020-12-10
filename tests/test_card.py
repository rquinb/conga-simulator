import game_exceptions
from entities.game_entities import Card


class TestCard:

    def test_valid_card(self):
        try:
            Card(number=12, kind="B")
            has_rised_exception = False
        except Exception:
            has_rised_exception = True
        assert not has_rised_exception

    def test_invalid_card_number(self):
        try:
            Card(number=13, kind="B")
            has_rised_invalid_number_exception = False
        except game_exceptions.InvalidCardNumber:
            has_rised_invalid_number_exception = True
        except Exception:
            has_rised_invalid_number_exception = False
        assert has_rised_invalid_number_exception

    def test_invalid_card_kind(self):
        try:
            Card(number=1, kind="H")
            has_rised_invalid_kind_exception = False
        except game_exceptions.InvalidCardKind:
            has_rised_invalid_kind_exception = True
        except Exception:
            has_rised_invalid_kind_exception = False
        assert has_rised_invalid_kind_exception

    def test_string_representation(self):
        card = Card(number=10, kind="O")
        string_representation = card.to_string()
        assert string_representation == "10 de oro"

    def test_dictionary_conversion(self):
        card = Card(number=8, kind="E")
        dict_representation = card.to_dict()
        assert type(dict_representation) == dict

    def test_equality_detection(self):
        card_a = Card(number=7, kind="C")
        card_b = Card(number=7, kind="C")
        assert card_a == card_b

    def test_inequality_detection(self):
        card_a = Card(number=6, kind="E")
        card_b = Card(number=6, kind="C")
        assert card_a != card_b