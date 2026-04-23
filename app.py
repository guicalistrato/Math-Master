# Borrowing first lines of code from finance's app.py
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, generate_test_id, get_questions

# Configure application
app = Flask(__name__)


@app.template_filter('index')
def index(sequence, i):
    return sequence[i]


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Global variables
questions_number = 50


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Starting actual new code
# Index


@app.route("/")
@login_required
def index():
    """Show Home Page"""
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = name[0]['username']

    return render_template("index.html", username=username)

# Home dos Tests
@app.get("/test_home")
@login_required
def test_home_get():
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = name[0]['username']
    return render_template("test_home.html", username=username)

@app.post("/test_home")
@login_required
def test_home_post():
    """Redirect to Test Home Page"""
    # User reached route via POST (as by submitting a form via POST)
    # Get questions number
    questions = get_questions()

    # Generate test ID
    test_id = generate_test_id(questions)

    # Get questions
    for i in range(10):
        a = db.execute("SELECT a FROM questions WHERE number = ?", questions[i])[0]["a"]
        b = db.execute("SELECT b FROM questions WHERE number = ?", questions[i])[0]["b"]
        c = db.execute("SELECT c FROM questions WHERE number = ?", questions[i])[0]["c"]
        d = db.execute("SELECT d FROM questions WHERE number = ?", questions[i])[0]["d"]
        question_text = db.execute("SELECT question FROM questions WHERE number = ?", questions[i])[
            0]["question"]
        answer = db.execute("SELECT answer FROM questions WHERE number = ?",
                            questions[i])[0]["answer"]
        difficulty = db.execute("SELECT difficulty FROM questions WHERE number = ?", questions[i])[
            0]["difficulty"]
        db.execute(
            "INSERT INTO tests (test_id, question_number, question_text, a, b, c, d, answer, difficulty, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", test_id, questions[
                i], question_text, a, b, c, d, answer, difficulty, datetime.now()
        )

    # Render the test
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = name[0]['username']
    test = db.execute("SELECT * FROM tests WHERE test_id = ?", test_id)
    return render_template("test.html", test=test, username=username)

# testes em si
@app.get("/test")
@login_required
def test_get():
    return render_template("/")

@app.post("/test")
@login_required
def test_post():
    """Create a Test and show results"""
    # User reached route via POST (as by submitting a form via POST)
    """Display the test"""
    # Get Test ID
    test_id = db.execute("SELECT test_id FROM tests ORDER BY time DESC LIMIT 1")[0]["test_id"]

    # List questions' subjects
    sub = db.execute("SELECT subject FROM questions WHERE number IN (SELECT question_number FROM tests WHERE test_id = ?)",
                        test_id)
    subject = []
    for i in range(10):
        subject.append(sub[i]["subject"])

    # Get Correct Answers
    correct_answers = []
    for i in range(10):
        correct_answers.append(db.execute(
            "SELECT answer FROM tests WHERE test_id = ?", test_id)[i]["answer"])

    # Get User Answers (ChatGPT helped)
    user_answers = [request.form.get(f"question_{i}") for i in range(1, 11)]

    # Check
    correctness = []
    review = []
    questions_correct = 0
    for i in range(10):
        if correct_answers[i] == user_answers[i]:
            correctness.append("correct")
            questions_correct += 1
        else:
            correctness.append("incorrect")
            if sub[i]["subject"] not in review:
                review.append(sub[i]["subject"])

    # Custom Message
    if questions_correct < 5:
        message = "Oops! Better luck next time!"
    elif questions_correct in [5, 6]:
        message = "You're almost there. Don't give up!"
    elif questions_correct in [7, 8, 9]:
        message = "Very nice! Your math skills are impressive"
    else:
        message = "Amazing! You did a fantastic job!"

    # Add to history
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    user = name[0]['username']
    time = db.execute("SELECT time FROM tests WHERE test_id = ?", test_id)
    time = time[0]['time']

    db.execute("INSERT INTO history (user, correct_answers, test_id, time) VALUES (?, ?, ?, ?)",
                user, questions_correct, test_id, time)

    # Render Results
    questions = [(i)for i in range(1, 11)]
    return render_template("results.html", questions=questions, user_answers=user_answers, correct_answers=correct_answers, correctness=correctness, questions_correct=questions_correct, message=message, subject=subject, review=review)
    
# rota do forum
@app.get("/forum")
@login_required
def forum_get():
    # Get values from database
    posts = db.execute("SELECT * FROM forum ORDER BY time DESC")
    return render_template("forum.html", posts=posts)

@app.post("/forum")
@login_required
def forum_post():
    # Get Post Informations
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    user = name[0]['username']
    post = request.form.get("post")
    time = datetime.now()

    # Insert Post into forum table
    db.execute("INSERT INTO forum (user, post, time) VALUES (?, ?, ?)", user, post, time)

    # Get values from database
    posts = db.execute("SELECT * FROM forum")

    return render_template("forum.html", posts=posts)

# History
@app.route("/history")
@login_required
def history():
    """Show a history of all the tests the user has taken, as well as their evolution"""
    # Get info
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = name[0]['username']
    info = db.execute("SELECT * FROM history WHERE user = ?", username)
    # Render index page
    return render_template("history.html", info=info)

@app.route("/learn")
@login_required
def learn():
    """Redirect to Learn page"""
    return render_template("learn.html")

@app.route("/functions")
@login_required
def functions():
    """Redirect to Functions page"""
    return render_template("functions.html")

@app.route("/geometry")
@login_required
def geometry():
    """Redirect to Geometry page"""
    return render_template("geometry.html")

@app.route("/trigonometry")
@login_required
def trigonometry():
    """Redirect to Trigonometry page"""
    return render_template("trigonometry.html")

@app.route("/proportion")
@login_required
def proportion():
    """Redirect to Proportion page"""
    return render_template("proportion.html")

@app.route("/financial_math")
@login_required
def financial_math():
    """Redirect to Financial Math page"""
    return render_template("financial_math.html")

# Login
@app.get("/login")
def login_get():
    session.clear()
    return render_template("login.html")

@app.post("/login")
def login_post():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 403)

    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 403)

    # Query database for username
    rows = db.execute(
        "SELECT * FROM users WHERE username = ?", request.form.get("username")
    )

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(
        rows[0]["hash"], request.form.get("password")
    ):
        return apology("invalid username and/or password", 403)

    # Remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # Redirect user to home page
    return redirect("/")

# Register
@app.get("/register")
def register_get():
    return render_template("register.html")

@app.post("/register")
def register_post():
    """Register user"""

    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 400)

    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 400)

    # Ensure confimation was submitted
    elif not request.form.get("confirmation"):
        return apology("must confirm password", 400)

    # Check if password and confirmation are equal
    if request.form.get("password") != request.form.get("confirmation"):
        return apology("passwords do not match", 400)

    # Check if username is already taken
    rows = db.execute(
        "SELECT * FROM users WHERE username = ?", request.form.get("username")
    )
    if len(rows) != 0:
        return apology("username already taken", 400)

    # Add user to the table
    db.execute(
        "INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password"))
    )

    nrows = db.execute(
        "SELECT * FROM users WHERE username = ?", request.form.get("username")
    )

    # Remember which user has logged in
    session["user_id"] = nrows[0]["id"]

    # Redirect user to home page
    return redirect("/")

# Logout
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
