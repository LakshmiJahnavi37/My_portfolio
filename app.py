from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "contacts.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            interests TEXT,
            bio TEXT
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("My portfolio.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    gender = request.form.get("gender")
    interests = ", ".join(request.form.getlist("interests"))
    bio = request.form.get("bio")

    print(name, email, gender, interests, bio)  # DEBUG LINE

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (name, email, gender, interests, bio) VALUES (?, ?, ?, ?, ?)",
        (name, email, gender, interests, bio)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("thankyou"))

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


if __name__ == "__main__":
    init_db()         
    app.run(debug=True)
