import copy
from entities.game_entities import Game, Deck
from entities.players import PlayerBuilder
from entities.game_simulator import GamesSimulator, GameStatistics

class TestGameSimulation:
    REPRESENTATIVE_GAMES_AMOUNT = 500

    def _build_player(self, name):
        return PlayerBuilder().build_player(name)

    def _simulate_game(self):
        player_1 = self._build_player('Jack')
        player_2 = self._build_player('Mary')
        games_simulator = GamesSimulator()
        return games_simulator.simulate_game(player_1, player_2)

    def test_initial_cards_allocation(self):
        player_1 = self._build_player('Jack')
        player_2 = self._build_player('Mary')
        games_simulator = GamesSimulator()
        for _ in range(self.REPRESENTATIVE_GAMES_AMOUNT):
            deck = Deck()
            game = Game(players=[copy.deepcopy(player_1), copy.deepcopy(player_2)])
            game, deck = games_simulator._give_cards_to_players(game, deck)
            assert len(game.players[0].cards) == game.CARDS_IN_HAND and len(game.players[1].cards) == game.CARDS_IN_HAND

    def test_simulation_of_game(self):
        game = self._simulate_game()
        assert isinstance(game,Game) and game.players[0].name == "Jack" and game.players[1].name == "Mary"

    def test_statistics_computation(self):
        game = self._simulate_game()
        game_statistics = GameStatistics(game.players[0].name, game.players[1].name, [game.report_results()])
        computed_statistics = game_statistics.get_statistics()
        assert not [value for key, value in computed_statistics.items() if value == None]

