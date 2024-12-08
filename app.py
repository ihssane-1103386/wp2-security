from flask import Flask, request
from flask import render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
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
    return render_template('vraag indexeren naar taxonomie.html')

@app.route("/wijzig")
def wijzig():
    return render_template('wijzig_redacteuren.html')

@app.route("/ai_prompts")
def ai_prompts():
    conn = sqlite3.connect('databases/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            prompts.prompts_id, 
            prompts.prompt, 
            users.display_name AS user_display_name, 
            prompts.questions_count, 
            prompts.questions_correct
        FROM 
            prompts
        JOIN 
            users ON prompts.user_id = users.user_id
    ''')
    prompts = cursor.fetchall()

    conn.close()

    return render_template('ai_prompts.html', prompts=prompts)

@app.route("/prompt_details/<int:prompts_id>")
def prompt_details(prompts_id):
    conn = sqlite3.connect('databases/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            prompts.prompt, 
            prompts.prompt_details, 
            users.display_name AS user_display_name, 
            prompts.questions_count, 
            prompts.questions_correct, 
            prompts.questions_incorrect, 
            prompts.date_created
        FROM 
            prompts
        JOIN 
            users ON prompts.user_id = users.user_id
        WHERE 
            prompts.prompts_id = ?
    ''', (prompts_id,))
    prompt = cursor.fetchone()

    conn.close()

    if prompt:
        return render_template('prompt_details.html', prompt=prompt)
    else:
        return "Prompt not found", 404



if __name__ == '__main__':
    app.run()