import json, os
from flask import Flask
from flask import render_template

app = Flask(__name__)

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

def toetsvragen_10():
    vraag = toetsvragen()
    for vraag in toetsvragen():
        pagina = int(request.args.get("pagina", 1))
        per_pagina = 10
        if start is page 1:




if __name__ == '__main__':
    app.run(debug=True)