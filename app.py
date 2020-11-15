import flask


app = flask.Flask(__name__)

@app.route('/')
def home_page():
    return "conga-simulator v0.0.1"

if __name__ == '__main__':
    app.run(debug=True)
