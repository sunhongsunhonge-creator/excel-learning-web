from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("dashboard.html")

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

@app.route("/quiz1")
def quiz1():
    return render_template("quiz1.html")

@app.route("/quiz2")
def quiz2():
    return render_template("quiz2.html")

@app.route("/quiz3")
def quiz3():
    return render_template("quiz3.html")

@app.route("/quiz4")
def quiz4():
    return render_template("quiz4.html")

@app.route("/quiz5")
def quiz5():
    return render_template("quiz5.html")

@app.route("/quiz6")
def quiz6():
    return render_template("quiz6.html")

import os
if __name__ == "__main__":
    app.run()   