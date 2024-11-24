import json
from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route("/")
# def inlog():
#     return render_template('inloggen.html')
#
# @app.route('/redacteur')
# def redacteur():
#     return render_template('redacteur.html')

@app.route("/toetsvragen")
def toetsvragen():
    with open("static/assets/json files/questions_extract.json") as f:
        vragen = json.load(f)
    return render_template("toetsvragen.html", vragen=vragen)

if __name__ == '__main__':
    app.run(debug=True)