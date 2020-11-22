import flask
from entities.game_entities import Deck

app = flask.Flask(__name__)

@app.route('/deck', methods=['GET'])
def get_deck():
    deck = Deck()
    return flask.jsonify({"cards": [card.to_string() for card in deck.cards]})

if __name__ == '__main__':
    app.run()
