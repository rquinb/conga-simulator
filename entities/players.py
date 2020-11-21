from entities.game_entities import Player
from entities.card_processors import CardsGrouper

class ConservativeRandomRest(Player):
    def __init__(self, name):
        super().__init__(name)