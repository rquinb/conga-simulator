from entities.game_entities import Game
from entities.players import ConservativeMinRest
from entities.game_simulator import GamesSimulator, GameStatistics

class TestGameSimulation:

    def _simulate_game(self):
        player_1 = ConservativeMinRest(name='Jack')
        player_2 = ConservativeMinRest(name='Mary')
        games_simulator = GamesSimulator()
        return games_simulator.simulate_game(player_1, player_2)

    def test_simulation_of_game(self):
        game = self._simulate_game()
        assert isinstance(game,Game) and game.players[0].name == "Jack" and game.players[1].name == "Mary"

    def test_statistics_computation(self):
        game = self._simulate_game()
        game_statistics = GameStatistics(game.players[0].name, game.players[1].name, [game.report_results()])
        computed_statistics = game_statistics.get_statistics()
        assert not [value for key, value in computed_statistics.items() if value == None]

