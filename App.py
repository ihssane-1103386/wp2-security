from flask import Flask, request
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    print(request.args.get("test"))
    print(request.args.get("Lastname"))
    print(request.args.get("Age"))
    print(request.args.get("Birthdate"))
    print(request.args.get("email"))
    print(request.args.get("Password"))
    return render_template('hello_world.html')


if __name__ == '__main__':
    app.run()