from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def inlog():
    return render_template('inloggen.html')

@app.route('/redacteur')
def redacteur():
    return render_template('redacteur.html')

@app.route('/vraag_indexeren')
def vraag_indexeren():
    return render_template('vraag indexeren naar taxonomie.html')

if __name__ == '__main__':
    app.run()