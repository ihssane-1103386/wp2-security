import json, os
from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# @app.route("/")
# def toetsvragen():
#     json_path = os.path.join(app.root_path, 'static', 'assets', 'json files', 'questions_extract.json')

    # try:
    #     with open(json_path, 'r') as f:
    #         vragen = json.load(f)
    # except Exception as e:
    #     print(f"Fout bij het openen van het JSON-bestand: {e}")
    #     vragen = []
    # return render_template("toetsvragen.html", vragen=vragen)

    # with open(json_path, "r") as f:
    #     return json.load(f)

# @app.route("/")
# def toetsvragen_10():
#     vragen = toetsvragen()
#
#     page = int(request.args.get('page', 1))
#     per_page = 10
#     start = (page - 1) * per_page
#     end = start + per_page
#     vragen_pagina = vragen[start:end]
#
#     next_page = page + 1 if end < len(vragen) else None
#     prev_page = page - 1 if start > 0 else None
#
#     return render_template('toetsvragen.html',
#                            vragen=vragen_pagina,
#                            page=page,
#                            next_page=next_page,
#                            prev_page=prev_page)

@app.route("/", endpoint="toetsvragen")
def toetsvragen():
    try:
        with open('static/assets/json files/questions_extract.json') as f:
          vragen = json.load(f)

          page = int(request.args.get('page', 1))

          per_page = 10
          start = (page - 1) * per_page
          end = start + per_page

          vragen_pagina = vragen[start:end]

          next_page = page + 1 if end < len(vragen) else None
          prev_page = page - 1 if start > 0 else None

          total_pages = (len(vragen) + per_page - 1) // per_page

        return render_template('toetsvragen.html', vragen=vragen_pagina,
                               page=page, next_page=next_page, prev_page=prev_page, total_pages=total_pages)
    except Exception as e:
        print(f"Fout tijdens het verwerken van de vragen: {e}")
        return "Interne serverfout", 500

if __name__ == '__main__':
    app.run(debug=True)