import flask
from entities import Card, Hand, Deck, Game


app = flask.Flask(__name__)

@app.route('/')
def home_page():
    return "conga-simulator v0.0.1"

@app.route('/deck', methods=['GET'])
def get_deck():
    deck = Deck()
    return flask.jsonify({"cards": [card.to_string() for card in deck.cards]})

@app.route('/games-detection', methods=['GET'])
def detect_games():
    game = Game()
    hand = Hand()
    hand.receive_card(Card(1, "C"))
    hand.receive_card(Card(2, "C"))
    hand.receive_card(Card(3, "C"))
    hand.receive_card(Card(7, "E"))
    hand.receive_card(Card(9, "E"))
    hand.receive_card(Card(7, "O"))
    hand.receive_card(Card(5, "B"))
    same = []
    ladder = []
    for found_game in game.cards_with_same_number(hand):
        same.append([card.to_string() for card in found_game])
    for found_game in game.cards_with_ladder(hand):
        ladder.append([card.to_string() for card in found_game])
    return flask.jsonify({"games":{"same_number":same, "ladder": ladder}})


if __name__ == '__main__':
    app.run(debug=True)
