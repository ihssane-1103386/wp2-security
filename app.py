from flask import Flask, request, render_template, redirect, url_for
from db_prompt_data import prompts_ophalen, prompt_details_ophalen, prompt_verwijderen
from indexeer_page_db_connection import prompt_lijst
import sqlite3

app = Flask(__name__)
DATABASE_FILE = "databases/database.db"

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

@app.route('/taxonomie_resultaat')
def vraag_taxonomie_resultaat():
    return render_template('vraag_indexeren_resultaat.html',
                            vraag = "placeholder",
                            vak = "biologie",
                            onderwijsniveau = "niveau 2",
                            leerjaar = "leerjaar 1",
                            prompt = "bloom")
@app.route('/indexeren')
def indexeren():
    prompts= prompt_lijst()
    return render_template('vraag_indexeren_naar_taxonomie.html',
                           vraag= "placeholder",
                           vak="biologie",
                           onderwijsniveau="niveau 2",
                           leerjaar="leerjaar 1",
                           prompts=prompts)

@app.route("/toetsvragen")
def toetsvragen():
    try:
        conn = sqlite3.connect('databases/database_toetsvragen.db')
        cursor = conn.cursor()

        page = int(request.args.get('page', 1))

        per_page = 10
        start = (page - 1) * per_page
        end = start + per_page

        cursor.execute("SELECT question, vak, date_created, taxonomy_bloom FROM questions LIMIT ? OFFSET ?", (per_page,start))
        question_page = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM questions")
        total_questions = cursor.fetchone()[0]
        total_pages = (total_questions + per_page - 1) // per_page

        next_page = page + 1 if end < total_questions else None
        prev_page = page - 1 if start > 0 else None

        show_first = page > 5
        show_last = page < total_questions - 5
        if total_pages <= 10:
            page_numbers = list(range(1, 11))
        else:
            if page <= 5:
                page_numbers = list(range(1, 6)) + ['...'] + [total_pages]
            elif page >= total_pages - 4:
                page_numbers = [1, '...'] + list(range(total_pages - 4, total_pages + 1))
            else:
                page_numbers = [1, '...'] + list(range(page - 2, page + 3)) + ['...'] + [total_pages]

        return render_template('toetsvragen.html', vragen=question_page,
                               page=page, next_page=next_page, prev_page=prev_page, total_pages=total_pages, page_numbers=page_numbers, show_first=show_first, show_last=show_last)

    except Exception as e:
        print(f"Fout tijdens het verwerken van de vragen: {e}")
        return "Interne serverfout", 500


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