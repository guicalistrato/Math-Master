import random

from flask import redirect, render_template, session
from functools import wraps

# Global variables
questions_number = 50

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", message=message, code=code)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def generate_test_id(question_list):
    # Get number of each question
    code = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(len(question_list)):
        if question_list[i] <= 26:
            code[i] = chr(question_list[i] + 64)

        else:
            code[i] = chr(question_list[i] + 70)

    for i in range(len(code)):
        print(f"{code[i]}", end="")

    code = ''.join(code)
    return code


def get_questions():
    question_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    log = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(10):
        while True:
            number = random.randint(1, questions_number)
            if number not in log:
                break
        log[i] = number
        question_list[i] = number
    question_list = sorted(question_list)
    return question_list
