# MATH MASTER

#### Description: 
A simple web application focused in math learning, using Flask.

# Introduction
## Before Development
After a lot of time thinking, I opted to do a web-based application using JavaScript, Python, and SQL, because, even though Finance was very challenging, I liked the implementation and seeing it complete was very rewarding.

With that in mind, it was time to choose what my application would be about. I initially thought about making a CPF (Cadastro de Pessoas Físicas, Brazil's taxpayer registry) analyser/generator, but after thinking that it might be too simple, I changed my mind to create a website about something I love but many people hate and/or struggle with: Math.

## Design Choices
The first thing I did after deciding what my program would be about was to decide what I would put in it. I started by creating the directory and making the regular flask folders and files. I copied the login(), logout() and register() functions I used in Finance as they would serve a similar purpose in my new program. I also defined the functions index(), text() and history(), but didn't put anything in them.

After this little setup, I took a look in the layout.html and styles.css files from Finance and based the layout.html and styles.css files I used in my program from them, making some changes to adapt better. By looking at the final version of my website's homepage, the similarities are clear, but also are the differences. After this, I designed my own icon in Paint, then converted it to .ico (a file type I did not even know existed). It is quite a simple one, but it represents well my website (a calculator), and most of these web icons are also very simple.

# Coding

## test() and test_home()
Now, after the copy & paste and style part done, it was time to actually start implementing my program. The first route I coded was test(), that in the beginning was supposed to be only one route, but I splitted it in two, test() and test_home(). I made that decision because otherwise it would feel disorganized and harder to undertand. To implement them, I made use of two helper functions I code in helpers.py, get_questions() and generate_test_id(), that respectively would get 10 numbers between 1 and 50 and generate an alphabetical ID based on these numbers.

## Making the Questions
With that, I had a way to generate question numbers and even an ID based on them, but I didn't have the actual questions. So I turned to ChatGPT and asked it to generate 10 questions from 5 different topics that are very common in Brazilian exams: functions, geometry, trigonometry, proportion and financial math. After revising them, I put them in a .csv file and asked for its helps once again, now for it to make a python program that would put this database in my project.db file. With that done, now I had a working database with 50 questions from various math subjects.

## Continuing with test() and test_home()
The rest of the implementation of the functions was pretty straigh forward, but I struggled a bit with the HTML files. The test homepage was easy to make, but doing the dynamically generated test HTML was quite challenging. I opted for using radio buttons as each question had only one right answers. I also opted to permit the user to not answer a question, but it would be counted as wrong. I spent some time perfecting the design until I got to this:
```
             <!-- Question X --->
            "<h3>Question 1</h3>
            <h6>{{ test[0].question_text }}</h6>
            <div class="mb-3">
                <p>
                    <input type="radio" name="question_1" id="q1_a" value="a">
                    <label for="q1_a">a) {{ test[0].a }}</label>
                </p>
                <p>
                    <input type="radio" name="question_1" id="q1_b" value="b">
                    <label for="q1_b">b) {{ test[0].b }}</label>
                </p>
                <p>
                    <input type="radio" name="question_1" id="q1_c" value="c">
                    <label for="q1_c">c) {{ test[0].c }}</label>
                </p>
                <p>
                    <input type="radio" name="question_1" id="q1_d" value="d">
                    <label for="q1_d">d) {{ test[0].d }}</label>
                </p>"
```
Then I asked for ChatGPT to repeat it for the 10 questions that would be per test. To finish it I just put a submit button. With that, I just had to receive the answers the user submitted, compare it with the correct answers, check which ones they got right and wrong, see the subjects of the questions they missed and output it to a results.html file. This piece of code illustrates a good part of the process:

```
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
```
## History
Implementantion of history was quite simple, as I already put the information in a history table in the tests() function, using some SQL statements and the tables "users", "questions" and "tests". This line of codes shows the insertion process I used:
```
        db.execute("INSERT INTO history (user, correct_answers, test_id, time) VALUES (?, ?, ?, ?)",
                   user, questions_correct, test_id, time)
```
## forum() & learn() and its derivatives
Both of these functions weren't planned at the start of development as stated in the beggining of this text, but I decided to include them to make the website feel more alive.

### learn()
As it just uses GET method, implementing learn() was quite simple. I chose to make multiple routes derivated from learn, like /geometry and /financial_math, as it made the understanding and flow of the code very simple, and if in the future I wished to add more subjects to this website (e.g.: statistics) it would be pretty simple. Here is the (very simple) implementation of learn and all its derivate routes in app.py:

```
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
```
### forum()
forum() was the last funcion/route added to the website. I was unsure if I should implement it as I would be the only to use the website, but I did it anyway. To test it, I created another profile in my website and could see its post from my "personal" one, as it can be seen in the video I posted. The implementation was made easier as I decided to create a table to store the post and its informations, called forum, that was accessed with db.execute to insert and output information to the template.

# Conclusion
MathMaker was quite challenging to create but was very rewarding, and became my favorite problem set from CS50, probably because of the emotional value. I think I designed it in a way that would make it very easy to do updates and expand its features in the future, and it could prove to be a useful website for students if released someday.
