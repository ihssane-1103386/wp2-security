from flask import Flask, request, render_template, redirect, url_for

from lib.gpt.bloom_taxonomy import get_bloom_category
from model_prompts import prompts_ophalen, prompt_details_ophalen, prompt_verwijderen
from indexeer_page_db_connection import prompt_lijst, prompt_ophalen_op_id
from urllib.parse import urlencode
import sqlite3

app = Flask(__name__)
DATABASE_FILE = "databases/database_toetsvragen.db"

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

@app.route("/")
def inlog():
    return render_template('inloggen.html')

# redacteuren uit de database halen
def get_redacteuren():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT display_name, login, is_admin FROM users")
    redacteuren = cursor.fetchall()
    conn.close()
    return redacteuren

@app.route('/redacteur')
def redacteur():
    redacteuren = get_redacteuren()
    return render_template('redacteur.html', redacteuren=redacteuren)

@app.route("/nr")
def nieuwe_redacteur():
    return render_template('nieuwe_redacteur.html')


@app.route('/indexeren', methods=["GET",'POST'])
def indexeren():
    prompts = prompt_lijst()
    questions_id = request.args.get('questions_id')

    if request.method == 'POST':
        vraag = request.form.get('vraag')
        prompt_id = request.form.get('keuze')
        return redirect(url_for('vraag_taxonomie_resultaat', vraag=vraag, prompt_id=prompt_id, questions_id=questions_id))


    if not questions_id:
        return "Geen questions_id meegegeven", 400

    try:
        conn = sqlite3.connect('databases/database_toetsvragen.db')
        cursor = conn.cursor()

        queries = load_queries('static/queries.sql')
        get_question = queries['get_question']
        # get_vak = queries['get_vak']

        cursor.execute(get_question, (questions_id,))
        # get_vak
        question = cursor.fetchone()

        if not question:
            return "Vraag niet gevonden", 404
        print(f"Opgehaalde vraagtekst: {question[0]}")

        return render_template('vraag_indexeren_naar_taxonomie.html',
                           vraag="placeholder",
                           vak="biologie",
                           onderwijsniveau="niveau 2",
                           leerjaar="leerjaar 1",
                           prompts=prompts,
                           questions_id=questions_id,
                           question=question[0])

    except Exception as e:
            print(f"Fout tijdens ophalen van vraag: {e}")
            return "Interne serverfout", 500
    finally:
            conn.close()

@app.route('/taxonomie_resultaat', methods=["GET","POST"])
def vraag_taxonomie_resultaat():
    prompt_id = request.args.get('prompt_id', 'bloom')
    prompt = prompt_ophalen_op_id(prompt_id)

    questions_id = request.args.get('questions_id')
    if not prompt:
        prompt = "Fallback Prompt"

    if not questions_id:
        return "Geen questions_id meegegeven", 400

    try:
        conn = sqlite3.connect('databases/database_toetsvragen.db')
        cursor = conn.cursor()

        queries = load_queries('static/queries.sql')
        get_question = queries['get_question']

        cursor.execute(get_question, (questions_id,))
        result = cursor.fetchone()

        if not result:
            return "Vraag niet gevonden", 404

        question = result[0]

        gpt_choice = "rac_test"
        ai_response = get_bloom_category(question, prompt, gpt_choice)

        if request.method == 'POST':
            taxonomie_bloom = request.form.get('taxonomie_bloom')
            update_taxonomie = queries['update_taxonomie']
            cursor.execute(update_taxonomie, (taxonomie_bloom, questions_id))
            conn.commit()
            return redirect(url_for('toetsvragen'))

        ai_niveau = ai_response.get("niveau", "geen antwoord")
        ai_uitleg = ai_response.get("uitleg", "geen antwoord")


        return render_template('vraag_indexeren_resultaat.html',
                               vraag=question,
                               vak="biologie",
                               onderwijsniveau="niveau 2",
                               leerjaar="leerjaar 1",
                               prompt=prompt[1],
                               ai_niveau=ai_niveau,
                               ai_uitleg=ai_uitleg,
                               questions_id=questions_id)
    except Exception as e:
        print(f"Fout tijdens ophalen van vraag: {e}")
        return "Interne serverfout", 500
    finally:
        conn.close()

@app.route("/toetsvragen", methods=["GET","POST"])
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
            ('toetsvragen.html',
                               vragen=question_page,
                               page=page,
                               next_page=next_page,
                               prev_page=prev_page,
                               total_pages=total_pages,
                               page_numbers=page_numbers,
                               show_first=show_first,
                               show_last=show_last,
                               search=search,
                               vak=vak,
                               taxonomie=taxonomie,
                               unieke_vakken=unieke_vakken))

    except Exception as e:
        print(f"Fout tijdens het verwerken van de vragen: {e}")
        return "Interne serverfout", 500
    finally:
        conn.close()

@app.route("/wijzig")
def wijzig():
    return render_template('wijzig_redacteuren.html')

@app.route("/ai_prompts")
def ai_prompts():
    prompts = prompts_ophalen()
    return render_template('ai_prompts.html', prompts=prompts)

@app.route("/prompt_details/<int:prompts_id>")
def prompt_details(prompts_id):
    prompt = prompt_details_ophalen(prompts_id)
    if prompt:
        return render_template('prompt_details.html', prompt=prompt)
    else:
        return "Prompt not found", 404

@app.route("/prompt_details/<int:prompts_id>/delete", methods=["POST"])
def delete_prompt_route(prompts_id):
    prompt_verwijderen(prompts_id)
    return redirect(url_for('ai_prompts'))

if __name__ == '__main__':
    app.run(debug=True)