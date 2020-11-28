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