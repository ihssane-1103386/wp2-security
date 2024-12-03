import json, sqlite3
from flask import Flask
from flask import render_template, request
import json

app = Flask(__name__)

@app.route("/", endpoint="toetsvragen")
def toetsvragen():
    try:
        conn = sqlite3.connect('databases/database_toetsvragen.db')
        cursor = conn.cursor()

        page = int(request.args.get('page', 1))

        per_page = 10
        start = (page - 1) * per_page
        end = start + per_page

        cursor.execute("SELECT question, vak, date_created FROM questions LIMIT ? OFFSET ?", (per_page,start))
        vragen_pagina = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM questions")
        total_vragen = cursor.fetchone()[0]
        total_pages = (total_vragen + per_page - 1) // per_page

        next_page = page + 1 if end < total_vragen else None
        prev_page = page - 1 if start > 0 else None

        return render_template('toetsvragen.html', vragen=vragen_pagina,
                               page=page, next_page=next_page, prev_page=prev_page, total_pages=total_pages)
    except Exception as e:
        print(f"Fout tijdens het verwerken van de vragen: {e}")
        return "Interne serverfout", 500

if __name__ == '__main__':
    app.run(debug=True)