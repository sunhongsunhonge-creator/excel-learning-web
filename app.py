from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "excel_secret_key"

TOTAL_QUIZZES = 6


# ---------------- DASHBOARD ---------------- #

@app.route("/")
def home():
    scores = session.get("scores", {})

    total_score = sum(scores.values())
    lessons_completed = len(scores)
    progress = int((lessons_completed / TOTAL_QUIZZES) * 100)

    return render_template(
        "dashboard.html",
        total_score=total_score,
        lessons_completed=lessons_completed,
        progress=progress
    )


# ---------------- LESSON ---------------- #

@app.route('/lesson1')
def lesson1():
    return render_template('lesson1.html')

@app.route('/lesson2')
def lesson2():
    return render_template('lesson2.html')

@app.route('/lesson3')
def lesson3():
    return render_template('lesson3.html')

@app.route('/lesson4')
def lesson4():
    return render_template('lesson4.html')

@app.route('/lesson5')
def lesson5():
    return render_template('lesson5.html')

@app.route('/lesson6')
def lesson6():
    return render_template('lesson6.html')


# ---------------- QUIZ 1 ---------------- #

@app.route("/quiz1", methods=["GET", "POST"])
def quiz1():
    score = None

    if request.method == "POST":
        score = 0

        answers = {
            "q1": "b",
            "q2": "cell",
            "q3": "letter",
            "q4": "number",
            "q5": "accounting"
        }

        for question, correct_answer in answers.items():
            if request.form.get(question) == correct_answer:
                score += 1

        scores = session.get("scores", {})
        scores["quiz1"] = score
        session["scores"] = scores

    return render_template("quiz1.html", score=score)


# ---------------- QUIZ 2-6 ---------------- #

def calculate_score(quiz_name, template_name):
    score = None

    if request.method == "POST":
        score = 0

        for i in range(1, 6):
            answer = request.form.get(f"q{i}")
            if answer:
                score += int(answer)

        scores = session.get("scores", {})
        scores[quiz_name] = score
        session["scores"] = scores

    return render_template(template_name, score=score)


@app.route("/quiz2", methods=["GET", "POST"])
def quiz2():
    return calculate_score("quiz2", "quiz2.html")


@app.route("/quiz3", methods=["GET", "POST"])
def quiz3():
    return calculate_score("quiz3", "quiz3.html")


@app.route("/quiz4", methods=["GET", "POST"])
def quiz4():
    return calculate_score("quiz4", "quiz4.html")


@app.route("/quiz5", methods=["GET", "POST"])
def quiz5():
    return calculate_score("quiz5", "quiz5.html")


@app.route("/quiz6", methods=["GET", "POST"])
def quiz6():
    return calculate_score("quiz6", "quiz6.html")


if __name__ == "__main__":
    app.run(debug=True)