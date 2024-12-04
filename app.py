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

if __name__ == '__main__':
    app.run()