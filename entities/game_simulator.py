from entities.game_entities import Cards, Deck, Game
from entities.players import ConservativeRandomRest

class GamesSimulator:

    def simulate_games(self, number_of_games, name_player_1, name_player_2):
        games = []
        for _ in range(number_of_games):
            games.append(self.simulate_game(name_player_1, name_player_2))
        return games

    def simulate_game(self, name_player_1, name_player_2):
        # Starts a new game
        game = Game()
        players = [ConservativeRandomRest(name_player_1), ConservativeRandomRest(name_player_2)]
        while True:
            # Give cards
            deck = Deck()
            current_player = 0
            for i in range(len(players)):
                players[i].cards = Cards()
                for _ in range(7):
                    players[i].cards.receive_card(deck.retrieve_card())
                players[i].rest_value = players[i].value_of_current_hand()
            while True:
                # Starts a new move
                current_player = 0 if current_player == 1 else 1
                players[current_player].played_dropped_card = False
                deck = players[current_player].make_move(deck)
                if players[current_player].has_cut:
                    # When a player "cuts" a step-game has finished, scores are registered and then a check is
                    # needed to figure out if some player reached the max amount of points (that means they lost)
                    players[0].score += players[0].rest_value
                    players[1].score += players[1].rest_value
                    game.results.append(
                        {"player_1_points": players[0].score, "player_2_points": players[1].score})
                    players[current_player].has_cut = False
                    break
            for index, player in enumerate(players):
                # If some player reaches 100, they lose the game
                if player.score >= 100:
                    winner_index = 0 if index == 1 else 1
                    game.winner = players[winner_index].name
                    break
            if game.winner:
                break
        return game

