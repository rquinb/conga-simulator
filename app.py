import flask
import entities


app = flask.Flask(__name__)

@app.route('/')
def home_page():
    return "conga-simulator v0.0.1"

@app.route('/deck', methods=['GET'])
def get_deck():
    deck = entities.Deck()
    return flask.jsonify({"cards": [card.to_string() for card in deck.cards]})

if __name__ == '__main__':
    app.run(debug=True)
