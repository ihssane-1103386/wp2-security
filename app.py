import datetime
import logging

from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from lib.gpt.bloom_taxonomy import get_bloom_category
from model_prompts import prompts_ophalen, prompt_details_ophalen, prompt_verwijderen, prompt_toevoegen
from indexeer_page_db_connection import prompt_lijst, prompt_ophalen_op_id
from urllib.parse import urlencode
import sqlite3

app = Flask(__name__)
app.secret_key = 'error-not-found'
bcrypt = Bcrypt(app)

DATABASE_FILE = "databases/database_toetsvragen.db"

@app.context_processor
def inject_current_user():
    return {'current_user': session.get('current_user')}

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
def home_redirect():
    return redirect(url_for('inlog'))

@app.route("/inlog", methods=['GET', 'POST'])
def inlog():
    ingevulde_gebruikersnaam = ""
    ingevulde_wachtwoord = ""
    if request.method == 'POST':
        ingevulde_gebruikersnaam = request.form.get('username')
        ingevulde_wachtwoord = request.form.get('password')

        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        queries = load_queries('static/queries.sql')
        login_query = queries['login_query']

        cursor.execute(login_query,(ingevulde_gebruikersnaam, ))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[2], ingevulde_wachtwoord):
            # Zet de gebruiker in de sessie
            session['current_user'] = {
                'user_id': user[0],
                'username': user[1],
                'display_name': user[3],
                'is_admin': bool(user[5]),
                'password': user[2]
            }
            display_name = user[3]
            flash(f"Welkom {user[3]}! Je bent succesvol ingelogd!", "success")
            return redirect(url_for('toetsvragen'))
        else:
            flash("Onjuiste gebruikersnaam of wachtwoord. Probeer het opnieuw.", "error")
        return render_template('inloggen.html.jinja')
    return render_template('inloggen.html.jinja', ingevulde_gebruikersnaam = ingevulde_gebruikersnaam)


@app.route("/successvol_ingelogd")
def success():
    return render_template('successvol_ingelogd.html')

@app.route("/nieuwe_redacteur", methods=['GET', 'POST'])
def nieuwe_redacteur():
    gebruikersnaam = ""
    email = ""
    wachtwoord = ""
    if request.method == 'POST':
        gebruikersnaam = request.form.get('username')
        email = request.form.get('email')
        wachtwoord = request.form.get('password')
        is_admin = 1 if request.form.get('is_admin') == 'on' else 0
        date_created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        hashed_wachtwoord = bcrypt.generate_password_hash(wachtwoord).decode("utf-8")

        print(f"Gebruikersnaam: {gebruikersnaam}")
        print(f"Email: {email}")
        print(f"Wachtwoord (gehasht): {hashed_wachtwoord}")
        print(f"Is Admin: {is_admin}")

        if gebruikersnaam and hashed_wachtwoord and email:
            try:
                conn = sqlite3.connect('databases/database_toetsvragen.db')
                cursor = conn.cursor()

                queries = load_queries('static/queries.sql')
                insert_redacteur = queries['insert_redacteur']

                cursor.execute(insert_redacteur, (gebruikersnaam, hashed_wachtwoord, gebruikersnaam, date_created, is_admin))

                print(
                    f"Gebruikersnaam: {gebruikersnaam}, E-mail: {email}, Wachtwoord: {hashed_wachtwoord}, Is Admin: {is_admin}, Datum: {date_created}")

                conn.commit()
                conn.close()

                return render_template('successvol_ingelogd.html', message=f"{gebruikersnaam} is succesvol toegevoegd! Klik hieronder om verder te gaan!",
                                       link="http://127.0.0.1:5000/toetsvragen")

            except sqlite3.IntegrityError:
                flash("Fout: Deze gebruikersnaam of e-mail bestaat al!")
                return "Fout: Deze gebruikersnaam of e-mail bestaat al!", 400
            except Exception as e:
                return f"Er is een fout opgetreden: {e}"
    return render_template('nieuwe_redacteur.html')

# redacteuren uit de database halen
def get_redacteuren():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    queries = load_queries('static/queries.sql')
    get_redacteur = queries['get_redacteur']

    cursor.execute(get_redacteur)
    redacteuren = cursor.fetchall()
    conn.close()

    return redacteuren

@app.route('/redacteur')
def redacteur():
    current_user = session.get('current_user')
    print("Current User:", current_user)
    if not current_user:
        return redirect(url_for('inlog'))

    redacteuren = get_redacteuren()
    return render_template('redacteur.html.jinja', redacteuren=redacteuren, current_user=session.get('current_user'))


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
        get_vak = queries['get_vak']

        cursor.execute(get_question, (questions_id,))
        question = cursor.fetchone()

        if not question:
            return "Vraag niet gevonden", 404
        print(f"Opgehaalde vraagtekst: {question[0]}")

        cursor.execute(get_vak, (questions_id,))
        vak = cursor.fetchone()

        if not vak:
            vak = "Niet bekend"

        return render_template('vraag_indexeren_naar_taxonomie.html.jinja',
                               question=question[0],
                               vak=vak[0],
                               onderwijsniveau="niveau 2",
                               leerjaar="leerjaar 1",
                               prompts=prompts,
                               questions_id=questions_id,
                               )

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
        get_vak = queries['get_vak']

        cursor.execute(get_question, (questions_id,))
        result = cursor.fetchone()

        if not result:
            return "Vraag niet gevonden", 404

        question = result[0]
        cursor.execute(get_vak, (questions_id,))
        vak = cursor.fetchone()

        if not vak:
            vak = "Niet bekend"

        if request.method == 'POST':
            taxonomy_bloom = request.form.get('taxonomy_bloom')
            ai_response = session.get('ai_response')
            if ai_response:
                ai_niveau = ai_response.get("categorie", "geen antwoord")
                ai_uitleg = ai_response.get("uitleg", "geen antwoord")
                bloom_answer = f"Niveau: {ai_niveau}, Uitleg: {ai_uitleg}"
            else:
                bloom_answer = "Niveau: geen antwoord, Uitleg: geen antwoord"

            if taxonomy_bloom:
                update_taxonomie = queries['update_taxonomy']
                cursor.execute(update_taxonomie, (taxonomy_bloom, questions_id))

                update_bloom_answer = queries['update_bloom_answer']
                cursor.execute(update_bloom_answer, (bloom_answer, questions_id))

                print(f'{bloom_answer} opgeslagen?')

                logging.debug(f"taxonomy_bloom: {taxonomy_bloom}")
                logging.debug(f"bloom_answer: {bloom_answer}")

                conn.commit()
                return redirect(url_for('toetsvragen'))

        gpt_choice = "rac_test"
        ai_response = get_bloom_category(question, prompt, gpt_choice)
        session['ai_response'] = ai_response

        if ai_response:
            ai_niveau = ai_response.get("categorie", "Geen antwoord")
            ai_uitleg = ai_response.get("uitleg", "Geen antwoord")
        else:
            ai_niveau = "geen antwoord"
            ai_uitleg = "geen antwoord"

        bloom_answer = f"Niveau: {ai_niveau}, Uitleg: {ai_uitleg}"
        print(bloom_answer)

        return render_template('vraag_indexeren_resultaat.html.jinja',
                               question=question,
                               vak=vak[0],
                               onderwijsniveau="niveau 2",
                               leerjaar="leerjaar 1",
                               prompt=prompt,
                               ai_niveau=ai_niveau,
                               ai_uitleg=ai_uitleg,
                               questions_id=questions_id)

    except Exception as e:
        logging.error(f"Fout tijdens ophalen van vraag: {e}")
        return "Interne serverfout", 500
    finally:
        conn.close()

@app.route('/taxonomie_wijzigen', methods=["GET","POST"])
def vraag_taxonomie_wijzigen():
    questions_id = request.args.get('questions_id')

    if not questions_id:
        return "Geen questions_id meegegeven", 400

    try:
        conn = sqlite3.connect('databases/database_toetsvragen.db')
        cursor = conn.cursor()

        queries = load_queries('static/queries.sql')
        get_question = queries['get_question']
        get_vak = queries['get_vak']
        get_bloom_answer = queries['get_bloom_answer']

        cursor.execute(get_question, (questions_id,))
        question = cursor.fetchone()

        if not question:
            return "Vraag niet gevonden", 404
        print(f"Opgehaalde vraagtekst: {question[0]}")

        cursor.execute(get_vak, (questions_id,))
        vak = cursor.fetchone()

        if not vak:
            vak = "Niet bekend"

        cursor.execute(get_bloom_answer, (questions_id,))
        bloom_answer = cursor.fetchone()

        if not bloom_answer:
            bloom_answer = "Niet bekend"

        return render_template('vraag_taxonomie_wijzigen.html.jinja',
                               question=question[0],
                               vak=vak[0],
                               onderwijsniveau="niveau 2",
                               leerjaar="leerjaar 1",
                               bloom_answer=bloom_answer[0],
                               questions_id=questions_id, )

    except Exception as e:
        print(f"Fout tijdens het verwerken van de vragen: {e}")
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
            query += " AND taxonomy_bloom IS NULL"

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
            count_query += " AND taxonomy_bloom IS NULL"

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
            ('toetsvragen.html.jinja',
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

@app.route('/wijzig/<username>', methods=['GET', 'POST'])
def wijzig(username):
    current_user = session.get('current_user')
    if not current_user or (not current_user['is_admin'] and current_user['username'] != username):
        return "Toegang geweigerd", 403

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    queries = load_queries('static/queries.sql')
    redacteur_query = queries['redacteur_query']
    cursor.execute(redacteur_query, (username,))
    redacteur = cursor.fetchone()

    if not redacteur:
        conn.close()
        return "Redacteur niet gevonden", 404

    print("DEBUG: Redacteur:", redacteur)

    if request.method == 'POST':
        nieuwe_naam = request.form.get('display_name')
        wachtwoord = request.form.get('password')


        queries = load_queries('static/queries.sql')
        wijzig_redacteur_query = queries['wijzig_redacteur_query']

        cursor.execute(wijzig_redacteur_query,(nieuwe_naam, wachtwoord, username))
        conn.commit()
        conn.close()

        return redirect(url_for('redacteur'))

    conn.close()

    return render_template('wijzig_redacteuren.html.jinja', redacteur=redacteur)

@app.route('/update_redacteur/<int:user_id>', methods=['POST'])
def update_redacteur(user_id):
    current_user = session.get('current_user')

    if not current_user:
        return "Niet ingelogd", 403

    if not current_user['is_admin']:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        queries = load_queries('static/queries.sql')
        user_query = queries['get_user_by_id']
        cursor.execute(user_query, (user_id,))
        target_user = cursor.fetchone()
        conn.close()

        if not target_user or target_user[1] != current_user['username']:
            return "Toegang geweigerd", 403

    nieuwe_naam = request.form.get('name')
    nieuwe_email = request.form.get('email')
    nieuw_wachtwoord = request.form.get('password')

    if current_user['is_admin']:
        is_admin = 1 if request.form.get('is_admin') else 0
    else:
        is_admin = None

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    queries = load_queries('static/queries.sql')
    wijzig_redacteur_query = queries['wijzig_redacteur_query']

    if is_admin is not None:
        cursor.execute(wijzig_redacteur_query, (nieuwe_naam, nieuw_wachtwoord, nieuwe_email, is_admin, user_id))
    else:
        wijzig_redacteur_query = queries['wijzig_redacteur_without_admin']
        cursor.execute(wijzig_redacteur_query, (nieuwe_naam, nieuw_wachtwoord, nieuwe_email, user_id))

    conn.commit()
    conn.close()

    flash(f"Redacteur met ID {user_id} is bijgewerkt!", "success")

    return redirect(url_for('redacteur'))


@app.route('/delete_redacteur/<int:user_id>', methods=['POST'])
def delete_redacteur(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    queries = load_queries('static/queries.sql')
    delete_redacteur_query = queries['delete_redacteur_query']

    if not delete_redacteur_query:
        flash("De verwijder-query kon niet worden gevonden!", "error")
        return redirect(url_for('redacteur'))

    try:
        cursor.execute(delete_redacteur_query, (user_id,))
        conn.commit()
        flash(f"Redacteur met ID {user_id} is succesvol verwijderd!", "success")
    except sqlite3.OperationalError as e:
        flash(f"Er is een fout opgetreden: {e}", "error")
    finally:
        conn.close()

    return redirect(url_for('redacteur'))


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
    current_user = session.get('current_user')

    if not current_user.get('is_admin', False):
        return redirect(url_for('ai_prompts'))

    user_id = current_user.get('user_id')
    prompt_verwijderen(prompts_id)
    return redirect(url_for('ai_prompts'))


@app.route('/prompt_toevoegen', methods=['GET', 'POST'])
def nieuwe_prompt():

    current_user = session.get('current_user')

    if not current_user.get('is_admin', False):
        return redirect(url_for('ai_prompts'))

    user_id = current_user.get('user_id')

    if request.method == 'POST':
        prompt = request.form.get('prompt')
        prompt_details = request.form.get('prompt_details')

        try:
            prompt_toevoegen(user_id, prompt, prompt_details)
            return redirect(url_for('ai_prompts'))
        except Exception as e:
            logging.error(f"Fout tijdens het toevoegen van een nieuwe prompt: {e}")
            return "Interne serverfout", 500

    return render_template('prompt_toevoegen.html')


if __name__ == '__main__':
    app.run(debug=True)