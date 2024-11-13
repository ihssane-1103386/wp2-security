from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def test_file():
    print(request.args.get("firstname"))
    return render_template('Test.html')


if __name__ == '__main__':
    app.run()