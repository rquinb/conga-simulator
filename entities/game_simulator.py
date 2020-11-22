from entities.game_entities import Deck, Game
from entities.players import ConservativeRandomRest

class GamesSimulator:

    @staticmethod
    def simulate_games(self, number_of_games):
        games = []
        for _ in range(number_of_games):
            game = Game()
            while True:
                deck = Deck()
                current_player = 0
                players = [ConservativeRandomRest('Matias'), ConservativeRandomRest('Jacque')]
                for i in range(len(players)):
                    for _ in range(7):
                        players[i].cards.receive_card(deck.retrieve_card())
                    players[i].rest_value = players[i].value_of_current_hand()
                while True:
                    played_dropped_card = False
                    current_player = 0 if current_player == 1 else 1
                    if deck.dropped_cards:
                        candidate_card = deck.dropped_cards.drop_cards()
                        analysis = players[current_player].analyze_card_impact_on_value(candidate_card)
                        if analysis.has_value_improved:
                            deck.play_card(players[current_player].play(candidate_card))
                            played_dropped_card = True
                        else:
                            deck.play_card(candidate_card)
                    if not played_dropped_card:
                        candidate_card = deck.retrieve_card()
                        analysis = players[current_player].analyze_card_impact_on_value(candidate_card)
                        if analysis.has_value_improved:
                            deck.play_card(players[current_player].play(candidate_card))
                        else:
                            deck.play_card(candidate_card)
                    if players[current_player].has_cut:
                        game.results.append(
                            {"player_1_points": players[0].rest_value, "player_2_points": players[1].rest_value})
                        break
                for index, player in enumerate(players):
                    if player.rest_value >= 100:
                        winner_index = 0 if index == 1 else 1
                        game.winner = players[winner_index].name
                        games.append(game)
                        break
        return games

