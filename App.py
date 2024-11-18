from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def test_file():
    print(request.args.get("firstname"))
    return render_template('Test.html')

def toetsvragen():
    print(request.args.get("naam zoeken in json file"))
    print(request.args.get("categorie zoeken in json file"))
    print(request.args.get("resultaten zoeken met/zonder taxonomie"))
    return render_template('toetsvragen.html')

if __name__ == '__main__':
    app.run()