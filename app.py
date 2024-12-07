import sqlite3
from flask import Flask, request
from flask import render_template

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
    vraag_id = request.args.get('vraag_id')
    conn = sqlite3.connect('databases/database_toetsvragen.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = ?", (vraag_id,))
    question = cursor.fetchone()
    return render_template('vraag indexeren naar taxonomie.html', question=question)

@app.route("/taxonomie_wijzigen")
def taxonomie_wijzigen():
    vraag_id = request.args.get('vraag_id')
    conn = sqlite3.connect('databases/database_toetsvragen.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = ?", (vraag_id,))
    question = cursor.fetchone()

    return render_template('vraag geïndexeerd wijzigen.html', question=question)

@app.route("/wijzig")
def wijzig():
    return render_template('wijzig_redacteuren.html')

if __name__ == '__main__':
    app.run()