from flask import Flask, render_template, request, session
import os

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

    questions = {
        "q1": {
            "correct_answer": "b",
            "correct_text": "Spreadsheet",
            "explanation": "Excel เป็นโปรแกรมประเภท Spreadsheet"
        },
        "q2": {
            "correct_answer": "cell",
            "correct_text": "Cell",
            "explanation": "Cell คือจุดตัดของแถวและคอลัมน์"
        },
        "q3": {
            "correct_answer": "letter",
            "correct_text": "ตัวอักษร (A, B, C...)",
            "explanation": "คอลัมน์แสดงเป็นตัวอักษร"
        },
        "q4": {
            "correct_answer": "number",
            "correct_text": "ตัวเลข (1, 2, 3...)",
            "explanation": "แถวแสดงเป็นตัวเลข"
        },
        "q5": {
            "correct_answer": "accounting",
            "correct_text": "งานบัญชี / คำนวณข้อมูล",
            "explanation": "Excel นิยมใช้ในงานบัญชี"
        }
    }

    score = None
    results = []

    if request.method == "POST":
        score = 0

        for key, data in questions.items():
            user_answer = request.form.get(key)
            is_correct = user_answer == data["answer"]

            if is_correct:
                score += 1

            results.append({
                "question": key,
                "is_correct": is_correct,
                "correct_text": data["correct_text"],
                "explanation": data["explanation"]
            })

        scores = session.get("scores", {})
        scores["quiz1"] = score
        session["scores"] = scores

    return render_template("quiz1.html", score=score, results=results)

# ---------------- QUIZ 2 ---------------- #

@app.route("/quiz2", methods=["GET", "POST"])
def quiz2():

    questions = {
        "q1": {
            "answer": "1",
            "correct_text": "Save หรือ Save As",
            "explanation": "คำสั่ง Save และ Save As ใช้สำหรับบันทึกไฟล์"
        },
        "q2": {
            "answer": "1",
            "correct_text": "Ctrl + S",
            "explanation": "Ctrl + S เป็นปุ่มลัดบันทึกไฟล์"
        },
        "q3": {
            "answer": "1",
            "correct_text": "Delete",
            "explanation": "Delete ใช้ลบข้อมูล"
        },
        "q4": {
            "answer": "1",
            "correct_text": "Copy",
            "explanation": "Copy ใช้คัดลอกข้อมูล"
        },
        "q5": {
            "answer": "1",
            "correct_text": "Paste",
            "explanation": "Paste ใช้วางข้อมูล"
        }
    }

    score = None
    results = []

    if request.method == "POST":
        score = 0

        for key, data in questions.items():
            user_answer = request.form.get(key)
            is_correct = user_answer == data["answer"]

            if is_correct:
                score += 1

            results.append({
                "question": key,
                "is_correct": is_correct,
                "correct_text": data["correct_text"],
                "explanation": data["explanation"]
            })

        scores = session.get("scores", {})
        scores["quiz2"] = score
        session["scores"] = scores

    return render_template("quiz2.html", score=score, results=results)


# ---------------- QUIZ 3-6 ---------------- #

def handle_quiz(quiz_name, template_name, questions):

    score = None
    results = []

    if request.method == "POST":
        score = 0

        for key, data in questions.items():
            user_answer = request.form.get(key)
            is_correct = user_answer == data["answer"]

            if is_correct:
                score += 1

            results.append({
                "question": key,
                "is_correct": is_correct,
                "correct_text": data["correct_text"],
                "explanation": data["explanation"]
            })

        scores = session.get("scores", {})
        scores[quiz_name] = score
        session["scores"] = scores

    return render_template(template_name, score=score, results=results)


@app.route("/quiz3", methods=["GET", "POST"])
def quiz3():
    questions = {
        "q1": {"answer": "equal", "correct_text": "=", "explanation": "สูตรต้องเริ่มด้วย ="},
        "q2": {"answer": "sum", "correct_text": "SUM", "explanation": "SUM ใช้หาผลรวม"},
        "q3": {"answer": "avg", "correct_text": "AVERAGE", "explanation": "AVERAGE ใช้หาค่าเฉลี่ย"},
        "q4": {"answer": "min", "correct_text": "MIN", "explanation": "MIN ใช้หาค่าต่ำสุด"},
        "q5": {"answer": "sum", "correct_text": "SUM(A1:A5)", "explanation": "รวมค่าตั้งแต่ A1-A5"},
    }
    return handle_quiz("quiz3", "quiz3.html", questions)


@app.route("/quiz4", methods=["GET", "POST"])
def quiz4():
    questions = {
        "q1": {"answer": "if_logic", "correct_text": "ตรวจสอบเงื่อนไข", "explanation": "IF ใช้ตรวจสอบเงื่อนไข"},
        "q2": {"answer": "correct_structure", "correct_text": "โครงสร้าง IF", "explanation": "IF(เงื่อนไข,จริง,เท็จ)"},
        "q3": {"answer": "fail", "correct_text": "ไม่ผ่าน", "explanation": "40 < 50"},
        "q4": {"answer": "nested", "correct_text": "Nested IF", "explanation": "ใช้หลายเงื่อนไข"},
        "q5": {"answer": "zero", "correct_text": "0", "explanation": "ไม่ถึงเป้าได้ 0"},
    }
    return handle_quiz("quiz4", "quiz4.html", questions)


@app.route("/quiz5", methods=["GET", "POST"])
def quiz5():

    questions = {
        "q1": {
            "answer": "trend",
            "correct_text": "ช่วยให้ข้อมูลเข้าใจง่ายและเห็นแนวโน้มชัดเจน",
            "explanation": "กราฟช่วยให้เห็นแนวโน้มและเข้าใจข้อมูลได้ง่ายขึ้น"
        },
        "q2": {
            "answer": "line",
            "correct_text": "Line Chart",
            "explanation": "Line Chart เหมาะสำหรับแสดงแนวโน้มตามช่วงเวลา"
        },
        "q3": {
            "answer": "select",
            "correct_text": "เลือกช่วงข้อมูลที่ต้องการ",
            "explanation": "ต้องเลือกข้อมูลก่อนจึงจะสร้างกราฟได้"
        },
        "q4": {
            "answer": "label",
            "correct_text": "Data Labels",
            "explanation": "Data Labels ใช้แสดงค่าตัวเลขบนกราฟ"
        },
        "q5": {
            "answer": "pie",
            "correct_text": "Pie Chart",
            "explanation": "Pie Chart เหมาะสำหรับแสดงสัดส่วนของข้อมูล"
        }
    }

    return handle_quiz("quiz5", "quiz5.html", questions)


@app.route("/quiz6", methods=["GET", "POST"])
def quiz6():
    questions = {
        "q1": {"answer": "home", "correct_text": "Home", "explanation": "จัดรูปแบบอยู่ใน Home"},
        "q2": {"answer": "percentage", "correct_text": "Percentage", "explanation": "ใช้แสดง %"},
        "q3": {"answer": "format_only", "correct_text": "เปลี่ยนรูปแบบเท่านั้น", "explanation": "ไม่กระทบค่าคำนวณ"},
        "q4": {"answer": "page_layout", "correct_text": "Page Layout", "explanation": "ตั้งค่าหน้ากระดาษ"},
        "q5": {"answer": "file_print", "correct_text": "File → Print", "explanation": "สั่งพิมพ์จาก File"},
    }
    return handle_quiz("quiz6", "quiz6.html", questions)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)