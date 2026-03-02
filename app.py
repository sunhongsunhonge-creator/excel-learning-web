from flask import Flask, render_template, request, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "excel_secret_key"

TOTAL_QUIZZES = 6

# ---------------- DATABASE ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------------- USER MODEL ----------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="user")

# ---------------- SCORE MODEL ----------------
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lesson = db.Column(db.String(50))
    score = db.Column(db.Integer) 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- AUTH ----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ---------------- ADMIN ----------------
@app.route('/admin')
@login_required
def admin():
    if current_user.role != "admin":
        return redirect(url_for('home'))

    users = User.query.all()
    return render_template('admin.html', users=users)

# ---------------- DASHBOARD ----------------
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

# ---------------- LESSON ----------------
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

# ---------------- QUIZ 1 ----------------
@app.route("/quiz1", methods=["GET", "POST"])
def quiz1():
    questions = {
        "q1": {"correct_answer": "b","correct_text": "Spreadsheet","explanation": "Excel เป็นโปรแกรมประเภท Spreadsheet"},
        "q2": {"correct_answer": "cell","correct_text": "Cell","explanation": "Cell คือจุดตัดของแถวและคอลัมน์"},
        "q3": {"correct_answer": "letter","correct_text": "ตัวอักษร (A, B, C...)","explanation": "คอลัมน์แสดงเป็นตัวอักษร"},
        "q4": {"correct_answer": "number","correct_text": "ตัวเลข (1, 2, 3...)","explanation": "แถวแสดงเป็นตัวเลข"},
        "q5": {"correct_answer": "accounting","correct_text": "งานบัญชี / คำนวณข้อมูล","explanation": "Excel นิยมใช้ในงานบัญชี"}
    }

    score = None
    results = []

    if request.method == "POST":
        score = 0
        for key, data in questions.items():
            user_answer = request.form.get(key)
            is_correct = user_answer == data["correct_answer"]

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

# ---------------- QUIZ HANDLER ----------------
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

@app.route("/quiz2", methods=["GET", "POST"])
def quiz2():
    questions = {
        "q1":{"answer":"1","correct_text":"Save หรือ Save As","explanation":"ใช้บันทึกไฟล์"},
        "q2":{"answer":"1","correct_text":"Ctrl + S","explanation":"ปุ่มลัดบันทึก"},
        "q3":{"answer":"1","correct_text":"Delete","explanation":"ลบข้อมูล"},
        "q4":{"answer":"1","correct_text":"Copy","explanation":"คัดลอก"},
        "q5":{"answer":"1","correct_text":"Paste","explanation":"วางข้อมูล"}
    }
    return handle_quiz("quiz2","quiz2.html",questions)

@app.route("/quiz3", methods=["GET", "POST"])
def quiz3():
    questions = {
        "q1":{"answer":"equal","correct_text":"=","explanation":"สูตรต้องเริ่มด้วย ="},
        "q2":{"answer":"sum","correct_text":"SUM","explanation":"หาผลรวม"},
        "q3":{"answer":"avg","correct_text":"AVERAGE","explanation":"หาค่าเฉลี่ย"},
        "q4":{"answer":"min","correct_text":"MIN","explanation":"ค่าต่ำสุด"},
        "q5":{"answer":"sum","correct_text":"SUM(A1:A5)","explanation":"รวมค่า"}
    }
    return handle_quiz("quiz3","quiz3.html",questions)

@app.route("/quiz4", methods=["GET", "POST"])
def quiz4():
    questions = {
        "q1":{"answer":"if_logic","correct_text":"ตรวจสอบเงื่อนไข","explanation":"IF ใช้ตรวจสอบ"},
        "q2":{"answer":"correct_structure","correct_text":"โครงสร้าง IF","explanation":"IF(เงื่อนไข,จริง,เท็จ)"},
        "q3":{"answer":"fail","correct_text":"ไม่ผ่าน","explanation":"40 < 50"},
        "q4":{"answer":"nested","correct_text":"Nested IF","explanation":"หลายเงื่อนไข"},
        "q5":{"answer":"zero","correct_text":"0","explanation":"ไม่ถึงเป้า"}
    }
    return handle_quiz("quiz4","quiz4.html",questions)

@app.route("/quiz5", methods=["GET", "POST"])
def quiz5():
    questions = {
        "q1":{"answer":"trend","correct_text":"เห็นแนวโน้ม","explanation":"กราฟช่วยวิเคราะห์"},
        "q2":{"answer":"line","correct_text":"Line Chart","explanation":"แนวโน้มเวลา"},
        "q3":{"answer":"select","correct_text":"เลือกข้อมูล","explanation":"ต้องเลือกก่อน"},
        "q4":{"answer":"label","correct_text":"Data Labels","explanation":"แสดงค่า"},
        "q5":{"answer":"pie","correct_text":"Pie Chart","explanation":"แสดงสัดส่วน"}
    }
    return handle_quiz("quiz5","quiz5.html",questions)

@app.route("/quiz6", methods=["GET", "POST"])
def quiz6():
    questions = {
        "q1":{"answer":"home","correct_text":"Home","explanation":"จัดรูปแบบ"},
        "q2":{"answer":"percentage","correct_text":"Percentage","explanation":"แสดง %"},
        "q3":{"answer":"format_only","correct_text":"เปลี่ยนรูปแบบ","explanation":"ไม่กระทบค่า"},
        "q4":{"answer":"page_layout","correct_text":"Page Layout","explanation":"ตั้งค่าหน้า"},
        "q5":{"answer":"file_print","correct_text":"File → Print","explanation":"สั่งพิมพ์"}
    }
    return handle_quiz("quiz6","quiz6.html",questions)

# ---------------- CREATE DB ----------------
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)