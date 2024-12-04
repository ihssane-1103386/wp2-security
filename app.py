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

@app.route("/indexeren")
def indexeren():
    return render_template('vraag indexeren naar taxonomie.html')

@app.route("/wijzig")
def wijzig():
    return render_template('wijzig_redacteuren.html')

if __name__ == '__main__':
    app.run()