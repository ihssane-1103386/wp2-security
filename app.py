from flask import Flask, request, render_template, redirect, url_for
from db_prompt_data import prompts_ophalen, prompt_details_ophalen, prompt_verwijderen

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
    return render_template('vraag_indexeren_resultaat.html')

@app.route("/indexeren")
def indexeren():
    return render_template('vraag_indexeren_naar_taxonomie.html')

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
    app.run()