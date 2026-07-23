import os

import psycopg2
from flask import Flask, redirect, render_template, request, url_for

from password_policy import is_valid_password

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def user_exists(username, conn):
    with conn.cursor() as cur:
        cur.execute('SELECT 1 FROM "2402278" WHERE username = %s', (username,))
        return cur.fetchone() is not None


@app.route("/")
def home():
    return render_template("index.html", error=request.args.get("error"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    conn = get_connection()
    try:
        if not username or not is_valid_password(password, conn):
            return redirect(url_for("home", error="Password does not meet requirements"))
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO "2402278" (username, created_at) VALUES (%s, now())',
                (username,),
            )
        conn.commit()
    finally:
        conn.close()

    return render_template("welcome.html", username=username, password=password)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    conn = get_connection()
    try:
        valid = username and user_exists(username, conn) and is_valid_password(password, conn)
    finally:
        conn.close()

    if not valid:
        return redirect(url_for("home", error="Invalid username or password"))

    return render_template("welcome.html", username=username, password=password)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
