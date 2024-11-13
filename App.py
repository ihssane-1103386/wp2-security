from flask import Flask, request
from flask import render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def test_file():  # put application's code here
    print(request.args.get("voorbeeld"))
    return render_template('/templates/Test.html')


if __name__ == '__main__':
    app.run()