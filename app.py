import flask
from flask_cors import CORS
from entities.game_entities import Deck
from entities.game_simulator import GamesSimulator
from entities.players import PlayerBuilder

app = flask.Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route('/deck', methods=['GET'])
def get_deck():
    deck = Deck()
    return flask.jsonify({"cards": [card.to_string() for card in deck.cards_in_deck]})

@app.route('/games-simulation', methods=['POST'])
def make_simulation():
    request_body = flask.request.get_json()
    number_of_games = request_body['numberOfGames']
    player_1_data = request_body['player1']
    player_2_data = request_body['player2']
    player_1 = PlayerBuilder().build_player(name=player_1_data['name'],
                                            agent_type=player_1_data['agentType'],
                                            accepted_cards_range=player_1_data['acceptedCardsRange'],
                                            max_rest_for_cutting=player_1_data['maxRestBeforeCutting'])

    player_2 = PlayerBuilder().build_player(name=player_2_data['name'],
                                            agent_type=player_2_data['agentType'],
                                             accepted_cards_range=player_2_data['acceptedCardsRange'],
                                            max_rest_for_cutting=player_2_data['maxRestBeforeCutting'])
    games_simulator = GamesSimulator()
    games = games_simulator.simulate_games(number_of_games, player_1, player_2)
    games_statistics = games_simulator.compute_statistics(player_1.name, player_2.name, games)
    return flask.jsonify({"games": games_statistics})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
