import json, os, jinja2
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

@app.route("/")
def toetsvragen():
    json_path = os.path.join(app.root_path, 'static', 'assets', 'json files', 'questions_extract.json')

    try:
        with open(json_path, 'r') as f:
            vragen = json.load(f)
    except Exception as e:
        print(f"Fout bij het openen van het JSON-bestand: {e}")
        vragen = []
    return render_template("toetsvragen.html", vragen=vragen)

if __name__ == '__main__':
    app.run(debug=True)