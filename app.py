from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey 

app = Flask(__name__)

from flask_debugtoolbar import DebugToolbarExtension

app.config['SECRET_KEY'] = "secret123"
debug = DebugToolbarExtension(app)

# responses = []


@app.route('/')
def home_page():
    """root page will show title, instructions, and button to start survey."""
    session.pop('responses', None)

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('home_page.html', title=title, instructions=instructions)

@app.route('/set-session', methods=["POST"])
def set_session():
    session["responses"] = []
    return redirect('/question/0',)



@app.route('/questions/<int:qid>')
def question_page(qid):
    """show the current question."""

    if 'responses' not in session:
        session['responses'] = []

    if len(session["responses"]) == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    
    if len(session["responses"]) != qid:
        """checking to see if user is out of order, send them to correct question"""
        flash ("trying to access question out of order!", "error")
        return redirect(f"/questions/{len(session['responses'])}")
    
    questions = satisfaction_survey.questions[qid]
    return render_template('question_page.html', questions=questions)



@app.route('/add_answer', methods=['POST'])
def add_answer():
    """add answers to responses list check if all questions have been answered and redirect to the appropriate page"""
    answer = request.form['answer']
    responses = session["responses"]

    responses.append(answer)
    session['responses'] = responses

    if len(session["responses"]) == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    else:
        return redirect(f"/questions/{len(session['responses'])}")



@app.route('/thankyou')
def thankyou_page():
    """Display thank you page"""

    title = satisfaction_survey.title
    return render_template('thankyou_page.html', title=title)