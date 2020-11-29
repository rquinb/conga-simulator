import flask
from flask_cors import CORS
from entities.game_entities import Deck
from entities.game_simulator import GamesSimulator

app = flask.Flask(__name__)
CORS(app)

@app.route('/deck', methods=['GET'])
def get_deck():
    deck = Deck()
    return flask.jsonify({"cards": [card.to_string() for card in deck.cards_in_deck]})

@app.route('/games-simulation', methods=['GET'])
def get_simulation():
    number_of_games = int(flask.request.args.get('number-of-games'))
    player_1_name = flask.request.args.get('player-1')
    player_2_name = flask.request.args.get('player-2')
    games_simulator = GamesSimulator()
    games = games_simulator.simulate_games(number_of_games, player_1_name, player_2_name)
    return flask.jsonify({"games": [game.report_results() for game in games]})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
