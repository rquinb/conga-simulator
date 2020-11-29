import numpy as np
from entities.game_entities import Cards, Deck, Game
from entities.players import ConservativeRandomRest

class GamesSimulator:

    def simulate_games(self, number_of_games, name_player_1, name_player_2):
        games = []
        for _ in range(number_of_games):
            games.append(self._simulate_game(name_player_1, name_player_2))
        return games

    def _simulate_game(self, name_player_1, name_player_2):
        # Starts a new game
        game = Game(players=[ConservativeRandomRest(name_player_1), ConservativeRandomRest(name_player_2)])
        while True:
            # Give cards
            deck = Deck()
            for i in range(len(game.players)):
                game.players[i].cards = Cards()
                for _ in range(7):
                    game.players[i].cards.receive_card(deck.retrieve_card())
                game.players[i].rest_value = game.players[i].value_of_current_hand()
            game, deck = self._simulate_round(game, deck)
            for index, player in enumerate(game.players):
                # If some player reaches 100, they lose the game
                if player.score >= 100:
                    winner_index = 0 if index == 1 else 1
                    game.winner = winner_index
                    break
            if game.winner is not None:
                break
        return game

    def _simulate_round(self, game, deck):
        current_player = 0
        while True:
            # Starts a new move
            current_player = 0 if current_player == 1 else 1
            game.players[current_player].played_dropped_card = False
            deck = game.players[current_player].make_move(deck)
            if game.players[current_player].has_cut:
                # When a player "cuts" a step-game has finished, scores are registered and then a check is
                # needed to figure out if some player reached the max amount of points (that means they lost)
                game.players[0].score += game.players[0].rest_value
                game.players[1].score += game.players[1].rest_value
                game.results.append(
                    {"player_1_points": game.players[0].score, "player_2_points": game.players[1].score})
                game.players[current_player].has_cut = False
                break
        return game, deck

    def compute_statistics(self,name_player_1, name_player_2, games):
        games_report = [game.report_results() for game in games]
        return GameStatistics(name_player_1, name_player_2, games_report).get_statistics()

class GameStatistics:
    def __init__(self, name_player_1, name_player_2, games_report):
        self.name_player_1 = name_player_1
        self.name_player_2 = name_player_2
        self.number_of_games = None
        self.mean_rounds_per_game = None
        self.max_rounds = None
        self.min_rounds = None
        self.rounds_histogram = None
        self.proportion_of_wins_player_1 = None
        self.proportion_of_wins_player_2 = None
        self.max_points_difference = None
        self.min_points_difference = None
        self._compute_statistics(games_report)

    def _compute_statistics(self, games_report):
        self.number_of_games = len(games_report)
        self.rounds_per_game = [len(game['score_evolution']) for game in games_report]
        self.mean_rounds_per_game = round(float(np.mean(self.rounds_per_game)),2)
        self.max_rounds = max(self.rounds_per_game)
        self.min_rounds = min(self.rounds_per_game)
        self.rounds_histogram = self._histogram_to_dict(np.histogram(self.rounds_per_game, bins=int(self.number_of_games * 0.1)))
        self.proportion_of_wins_player_1 = round(len([game for game in games_report if game["winner"] == self.name_player_1]) / self.number_of_games, 2)
        self.proportion_of_wins_player_2 = 1 - self.proportion_of_wins_player_1
        self.points_difference = [abs(game['score_evolution'][-1]['player_1_points'] - game['score_evolution'][-1]['player_2_points']) for game in games_report]
        self.max_points_difference = max(self.points_difference)
        self.min_points_difference = min(self.points_difference)
        self.games_report = games_report

    def get_statistics(self):
        return {key: value for key,value in self.__dict__.items() if not key.startswith("_")}

    def _histogram_to_dict(self, histogram):
        bins = []
        for i in range(len(list(histogram)[0])):
            bins.append({f'{round(histogram[1][i],2)}-{round(histogram[1][i+1],2)}': int(histogram[0][i])})
        return bins


