from flask import Flask, render_template, request

app = Flask(__name__)

# ---------------- HOME / DASHBOARD ---------------- #

@app.route("/")
def home():
    return render_template("dashboard.html",
                           total_score=120,
                           lessons_completed=6,
                           progress=75)

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


# ---------------- QUIZ 1 (แบบเทียบคำตอบข้อความ) ---------------- #

@app.route("/quiz1", methods=["GET", "POST"])
def quiz1():
    result = None
    explanation = None

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

        if score >= 3:
            result = f"คุณได้ {score} / 5 คะแนน ผ่านเกณฑ์ 👍"
        else:
            result = f"คุณได้ {score} / 5 คะแนน ยังไม่ผ่าน ❌"

        explanation = "เกณฑ์ผ่านคือ 3 คะแนนขึ้นไป"

    return render_template("quiz1.html",
                           result=result,
                           explanation=explanation)


# ---------------- QUIZ 2-6 (แบบ value = 1 / 0) ---------------- #

def calculate_score(template_name):
    score = None

    if request.method == "POST":
        score = 0
        for i in range(1, 6):
            answer = request.form.get(f"q{i}")
            if answer:
                score += int(answer)

    return render_template(template_name, score=score)


@app.route("/quiz2", methods=["GET", "POST"])
def quiz2():
    return calculate_score("quiz2.html")


@app.route("/quiz3", methods=["GET", "POST"])
def quiz3():
    return calculate_score("quiz3.html")


@app.route("/quiz4", methods=["GET", "POST"])
def quiz4():
    return calculate_score("quiz4.html")


@app.route("/quiz5", methods=["GET", "POST"])
def quiz5():
    return calculate_score("quiz5.html")


@app.route("/quiz6", methods=["GET", "POST"])
def quiz6():
    return calculate_score("quiz6.html")


if __name__ == "__main__":
    app.run()