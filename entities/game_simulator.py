import numpy as np
from entities.game_entities import Cards, Deck, Game
from entities.players import ConservativeMinRest

class GamesSimulator:

    def simulate_games(self, number_of_games, name_player_1, name_player_2):
        games = []
        for _ in range(number_of_games):
            games.append(self._simulate_game(name_player_1, name_player_2))
        return games

    def _simulate_game(self, name_player_1, name_player_2):
        # Starts a new game
        game = Game(players=[ConservativeMinRest(name_player_1), ConservativeMinRest(name_player_2)])
        while True:
            # Give cards
            deck = Deck()
            for i in range(len(game.players)):
                game.players[i].cards = Cards()
                for _ in range(game.CARDS_IN_HAND):
                    game.players[i].cards.receive_card(deck.retrieve_card())
                game.players[i].rest_value = game.players[i].value_of_current_hand()
            game, deck, cut_info = self._simulate_round(game, deck)
            for index, player in enumerate(game.players):
                # If some player reaches 100, they lose the game. The game also ends when I player has Conga
                if cut_info['cut_kind'] == "conga_cut":
                    winner_index = cut_info['player']
                    game.winner = winner_index
                    break
                if player.score >= game.MAX_SCORE:
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
            if game.players[current_player].has_cut():
                # When a player "cuts" a step-game has finished, scores are registered and then a check is
                # needed to figure out if some player reached the max amount of points (that means they lost)
                game.players[0].score += game.players[0].rest_value
                game.players[1].score += game.players[1].rest_value
                game.results.append(
                    {"player_1":{
                        "points":game.players[0].score,
                        "cut": game.players[0].cut.kind if game.players[0].cut else None
                        },
                    "player_2":{
                        "points": game.players[1].score,
                        "cut": game.players[1].cut.kind if game.players[1].cut else None
                        }
                    }
                )
                cut_info = {"player": current_player, "cut_kind": game.players[current_player].cut.kind}
                game.players[current_player].cut = None
                break
        return game, deck, cut_info

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
        self.player_1_cuts = None
        self.player_2_cuts = None
        self._compute_statistics(games_report)

    def _compute_statistics(self, games_report):
        self.number_of_games = len(games_report)
        self.rounds_per_game = [len(game['score_evolution']) for game in games_report]
        self.mean_rounds_per_game = round(float(np.mean(self.rounds_per_game)),2)
        self.max_rounds = max(self.rounds_per_game)
        self.min_rounds = min(self.rounds_per_game)
        self.rounds_histogram = self._histogram_to_dict(np.histogram(self.rounds_per_game, bins="sqrt"))
        self.proportion_of_wins_player_1 = round(len([game for game in games_report if game["winner"] == self.name_player_1]) / self.number_of_games, 2)
        self.proportion_of_wins_player_2 = round(1 - self.proportion_of_wins_player_1, 2)
        self.points_difference = [abs(game['score_evolution'][-1]['player_1']['points'] - game['score_evolution'][-1]['player_2']['points']) for game in games_report]
        self.max_points_difference = max(self.points_difference)
        self.min_points_difference = min(self.points_difference)
        self.player_1_cuts = self._cuts_report(games_report, "player_1")
        self.player_2_cuts = self._cuts_report(games_report, "player_2")
        self.games_report = games_report

    def get_statistics(self):
        return {key: value for key,value in self.__dict__.items() if not key.startswith("_")}

    def _histogram_to_dict(self, histogram):
        bins = []
        for i in range(len(list(histogram)[0])):
            bins.append({f'{round(histogram[1][i],2)}-{round(histogram[1][i+1],2)}': int(histogram[0][i])})
        return bins

    def _cuts_report(self, games_report, player_number):
        cuts = {key: 0 for key in Game.CUT_TYPES}
        for game in games_report:
            for round in game['score_evolution']:
                if not round[player_number]['cut']:
                    cuts['no_cut'] += 1
                else:
                    cuts[round[player_number]['cut']] += 1
        return cuts


