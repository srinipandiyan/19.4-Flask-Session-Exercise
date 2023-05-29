from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "insert-secret-token"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def launch_page():
    return render_template("start_survey.html")

@app.route("/survey-start", methods=['POST'])
def redirect_to_survey():
    session["responses"] = []
    return redirect("/questions/0")

@app.route("/questions/<int:idx>")
def display_question(idx):
    responses = session.get("responses")

    if(idx != len(responses)):
        res_len = len(responses)
        flash("Invalid question. Complete the survey in order.")
        return redirect(f"/questions/{res_len}")
    
    question = survey.questions[idx]
    return render_template("question.html", question_num=idx, question=question)

@app.route("/response", methods=["POST"])
def handle_responses():
    choice = request.form['response']
    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/completion")
    else:
        res_len = len(responses)
        return redirect(f"/questions/{res_len}")
    
@app.route("/completion")
def survey_complete():
    return render_template("completion.html")