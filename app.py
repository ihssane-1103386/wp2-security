import sqlite3
from flask import Flask, request
from flask import render_template
from urllib.parse import urlencode

app = Flask(__name__)

def load_queries(path):
    queries = {}
    query_name = None
    parameters = []

    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            print(f"Processing line: {line}")
            if line.startswith('-- [') and line.endswith(']'):
                if query_name and parameters:
                    queries[query_name] = ' '.join(parameters).rstrip(';')
                query_name = line[4:-1]
                parameters = []
            elif query_name:
                if line:
                    parameters.append(line)

        if query_name and parameters:
            queries[query_name] = ' '.join(parameters).rstrip(';')

    return queries

@app.route("/", endpoint="toetsvragen")
def toetsvragen():
    try:
        conn = sqlite3.connect('databases/database_toetsvragen.db')
        cursor = conn.cursor()

        queries = load_queries('static/queries.sql')

        normal_query = queries['normal_query']
        count_query = queries['count_query']
        vak_query = queries['vak_query']

        # This is for searching in toetsvragen
        search = request.args.get("search", '').strip()
        vak = request.args.get("vak", '').strip()
        taxonomie = request.args.get("taxonomie", '')

        # This is for the page numbers
        page = int(request.args.get('page', 1))
        per_page = 10
        start = (page - 1) * per_page

        query = normal_query.replace("SELECT", "SELECT questions_id")
        parameters = []

        if search:
            query += " AND question LIKE ?"
            parameters.append(f"%{search}%")

        if vak:
            query += " AND vak = ?"
            parameters.append(vak)

        if taxonomie:
            query += " AND taxonomy_bloom IS NOT NULL"

        query += " LIMIT ? OFFSET ?"
        parameters.extend([per_page, start])

        cursor.execute(query, parameters)
        question_page = cursor.fetchall()

        count_parameters = []

        if search:
            count_query += " AND question LIKE ?"
            count_parameters.append(f"%{search}%")
        if vak:
            count_query += " AND vak = ?"
            count_parameters.append(vak)
        if taxonomie:
            count_query += " AND taxonomy_bloom IS NOT NULL"

        cursor.execute(count_query, count_parameters)
        total_questions = cursor.fetchone()[0]

        total_pages = (total_questions + per_page - 1) // per_page
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        show_first = page > 1
        show_last = page < total_pages

        base_params = {
            "search": search,
            "vak": vak,
            "taxonomie": taxonomie
        }

        page_numbers = []
        for i in range(1, total_pages + 1):
            base_params["page"] = i
            page_numbers.append(f"?{urlencode(base_params)}")

        cursor.execute(vak_query)
        unieke_vakken = [row[0] for row in cursor.fetchall()]

        return (render_template
            ('toetsvragen.html', vragen=question_page, page=page, next_page=next_page, prev_page=prev_page, total_pages=total_pages, page_numbers=page_numbers, show_first=show_first, show_last=show_last, search=search, vak=vak, taxonomie=taxonomie,unieke_vakken=unieke_vakken))

    except Exception as e:
        print(f"Fout tijdens het verwerken van de vragen: {e}")
        return "Interne serverfout", 500
    finally:
        conn.close()

@app.route("/inloggen")
def inlog():
    return render_template('inloggen.html')

@app.route('/redacteur')
def redacteur():
    return render_template('redacteur.html')

@app.route("/nr")
def nieuwe_redacteur():
    return render_template('nieuwe_redacteur.html')

@app.route('/taxonomie_resultaat')
def vraag_taxonomie_resultaat():
    questions_id = request.args.get('questions_id')
    if not questions_id:
        return "Geen questions_id meegegeven", 400

    try:
        conn = sqlite3.connect('databases/database_toetsvragen.db')
        cursor = conn.cursor()

        queries = load_queries('static/queries.sql')
        get_question = queries['get_question']

        cursor.execute(get_question, (questions_id,))
        question = cursor.fetchone()

        if not question:
            return "Vraag niet gevonden", 404

        return render_template('vraag indexeren resultaat.html', questions_id=questions_id, question=question[0])

    except Exception as e:
            print(f"Fout tijdens ophalen van vraag: {e}")
            return "Interne serverfout", 500
    finally:
            conn.close()

@app.route("/indexeren")
def indexeren():
    questions_id = request.args.get('questions_id')
    if not questions_id:
        return "Geen questions_id meegegeven", 400

    try:
        conn = sqlite3.connect('databases/database_toetsvragen.db')
        cursor = conn.cursor()

        queries = load_queries('static/queries.sql')
        get_question = queries['get_question']

        print(f"Gebruikte questions_id: {questions_id}")
        cursor.execute(get_question, (questions_id,))
        question = cursor.fetchone()
        print(f"Opgehaalde vraag: {question}")

        if not question:
            return "Vraag niet gevonden", 404
        print(f"Opgehaalde vraagtekst: {question[0]}")

        return render_template('vraag indexeren naar taxonomie.html', questions_id=questions_id, question=question[0])

    except Exception as e:
            print(f"Fout tijdens ophalen van vraag: {e}")
            return "Interne serverfout", 500
    finally:
            conn.close()

@app.route("/wijzig")
def wijzig():
    return render_template('wijzig_redacteuren.html')

if __name__ == '__main__':
    app.run()