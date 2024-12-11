import sqlite3
from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/", endpoint="toetsvragen")
def toetsvragen():
    try:
        conn = sqlite3.connect('databases/database_toetsvragen.db')
        cursor = conn.cursor()

        # This is for searching in toetsvragen
        search = request.args.get("search", '').strip()
        vak = request.args.get("vak", '').strip()
        taxonomie = request.args.get("taxonomie", '')

        # This is for the page numbers
        page = int(request.args.get('page', 1))
        per_page = 10
        start = (page - 1) * per_page

        query = "SELECT question, vak, date_created, taxonomy_bloom FROM questions WHERE 1=1"
        parameters = []

        # Iets met previous page als de website ververst bij het zoeken?
        # De zoekresultaten gelden per 10, ik wil alle vragen en het behouden, totdat er ververst wordt?

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

        count_query = "SELECT COUNT(*) FROM questions WHERE 1=1"
        count_parameters = []  # Specifiek voor count_query
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

        if total_pages <= 10:
            page_numbers = list(range(1, total_pages + 1))
        else:
            if page <= 5:
                page_numbers = list(range(1, 6)) + ['...'] + [total_pages]
            elif page >= total_pages - 4:
                page_numbers = [1, '...'] + list(range(total_pages - 4, total_pages + 1))
            else:
                page_numbers = [1, '...'] + list(range(page - 2, page + 3)) + ['...'] + [total_pages]

        cursor.execute("SELECT DISTINCT vak FROM questions")
        unieke_vakken = [row[0] for row in cursor.fetchall()]

        # Doorgeven van question_id nummer naar indexeren/wijzigen
        # Question_query = "SELECT question_id FROM questions"
        # request.args.get('question_id')

        return (render_template
            ('toetsvragen.html', vragen=question_page, page=page, next_page=next_page, prev_page=prev_page, total_pages=total_pages, page_numbers=page_numbers, show_first=show_first, show_last=show_last, search=search, vak=vak, taxonomie=taxonomie,unieke_vakken=unieke_vakken))

    except Exception as e:
        print(f"Fout tijdens het verwerken van de vragen: {e}")
        return "Interne serverfout", 500

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
    return render_template('vraag indexeren resultaat.html')

@app.route("/indexeren")
def indexeren():
    question_id = request.args.get('question_id')

    conn = sqlite3.connect('databases/database_toetsvragen.db')
    cursor = conn.cursor()

    cursor.execute("SELECT question_id, question FROM questions WHERE question_id", (question_id,))
    question = cursor.fetchone()

    return render_template('vraag indexeren naar taxonomie.html', question=question)

@app.route("/wijzig")
def wijzig():
    return render_template('wijzig_redacteuren.html')

if __name__ == '__main__':
    app.run()