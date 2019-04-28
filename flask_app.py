from flask import Flask, flash, redirect, render_template, request, session, abort
import flask
import get_random_phrase

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('GC_CC.html')


@app.route("/api/get_text/", methods=['POST'])
def get_text():
    data = flask.request.data
    data = data.decode("utf-8")
    return flask.jsonify(get_random_phrase.query_this(data))
    #return flask.jsonify("Random")

if __name__ == "__main__":
    app.run(debug=True)