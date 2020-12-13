import os
import datetime
import flask
import psycopg2.extensions
from psycopg2.extras import RealDictCursor
from http import HTTPStatus
from celery import Celery
from flask_cors import CORS
from entities import repositories
from entities.game_entities import Deck
from entities.game_simulator import GamesSimulator
from entities.players import PlayerBuilder

app = flask.Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
CORS(app, expose_headers=['Location'])
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

USER = os.getenv('USERNAME', 'user')
PASSWORD = os.getenv('PASSWORD', 'pass')
HOST = os.getenv('HOST', 'database')
PORT = os.getenv('PORT')
psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
db_connection = repositories.DatabaseConnection(max_wait_seconds=15).connect_to_db(user=USER,
                                                                                   password=PASSWORD,
                                                                                   host=HOST,
                                                                                   port=PORT,
                                                                                   database="simulator",
                                                                                   cursor_factory=RealDictCursor)
simulations_repository = repositories.SimulationsRepository(db_connection)


@app.route('/deck', methods=['GET'])
def get_deck():
    deck = Deck()
    return flask.jsonify({"cards": [card.to_string() for card in deck.cards_in_deck]})


@app.route('/games-simulations/<simulation_id>', methods=['GET'])
def get_simulation(simulation_id):
    simulation = simulations_repository.get_simulation(simulation_id)
    return flask.jsonify(simulation), HTTPStatus.OK


@app.route('/games-simulations', methods=['GET'])
def get_simulations():
    simulations = simulations_repository.get_simulations()
    return flask.jsonify({'result': simulations}), HTTPStatus.OK


@app.route('/games-simulations', methods=['POST'])
def make_simulation():
    request_body = flask.request.get_json()
    number_of_games = request_body['numberOfGames']
    player_1_data = request_body['player1']
    player_2_data = request_body['player2']
    task = simulate_games.delay(number_of_games, player_1_data, player_2_data)
    return flask.jsonify({}), HTTPStatus.ACCEPTED, {'Location': flask.url_for('get_task_status', task_id=task.id)}


@app.route('/games-simulations/task/<task_id>')
def get_task_status(task_id):
    task = simulate_games.AsyncResult(task_id)
    status = {'state': task.state, 'current_simulation': 0, 'total': 0}
    if task.state != 'PENDING' and task.state != 'FAILURE':
        status['state'] = task.state
        status['current_simulation'] = task.info.get('current_simulation', 0)
        status['total'] = task.info.get('total', 1)
        if 'result' in task.info:
            status['result'] = task.info['result']

    return flask.jsonify(status)


@celery.task(bind=True)
def simulate_games(self, number_of_games, player_1_data, player_2_data):
    player_1 = PlayerBuilder().build_player(name=player_1_data['name'],
                                            agent_type=player_1_data['agentType'],
                                            accepted_cards_range=player_1_data['acceptedCardsRange'],
                                            max_rest_for_cutting=player_1_data['maxRestBeforeCutting'])
    player_2 = PlayerBuilder().build_player(name=player_2_data['name'],
                                            agent_type=player_2_data['agentType'],
                                            accepted_cards_range=player_2_data['acceptedCardsRange'],
                                            max_rest_for_cutting=player_2_data['maxRestBeforeCutting'])
    games_simulator = GamesSimulator()
    games = []
    for i in range(number_of_games):
        games.append(games_simulator.simulate_game(player_1, player_2))
        self.update_state(state='SIMULATING_GAMES', meta={'current_simulation': i + 1, 'total': number_of_games})
    games_statistics = games_simulator.compute_statistics(player_1.name, player_2.name, games)
    simulations_repository.save_simulation(simulation_id=self.request.id.__str__(),
                                           created_time=datetime.datetime.utcnow(),
                                           total_games=games_statistics['number_of_games'],
                                           mean_rounds_per_game=games_statistics['mean_rounds_per_game'],
                                           details=games_statistics)
    return {'current_simulation': number_of_games, 'total': number_of_games, 'result': games_statistics}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
