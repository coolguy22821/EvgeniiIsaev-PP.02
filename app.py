from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from max_bot import notify_class_representatives

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "registrations.db"

app = Flask(__name__)
app.secret_key = "change-this-secret-key"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                group_name TEXT NOT NULL,
                email TEXT NOT NULL,
                competition_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    full_name = request.form.get("full_name", "").strip()
    group_name = request.form.get("group_name", "").strip()
    email = request.form.get("email", "").strip()
    competition_name = request.form.get("competition_name", "").strip()

    if not all([full_name, group_name, email, competition_name]):
        flash("Пожалуйста, заполните все поля.", "error")
        return redirect(url_for("index"))

    if "@" not in email or "." not in email.split("@")[-1]:
        flash("Укажите корректный адрес электронной почты.", "error")
        return redirect(url_for("index"))

    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO registrations
            (full_name, group_name, email, competition_name)
            VALUES (?, ?, ?, ?)
        """, (full_name, group_name, email, competition_name))
        registration_id = cursor.lastrowid

    # На первой неделе используется безопасный режим-заглушка.
    # Реальная отправка появится после подключения официального MAX API.
    notify_class_representatives({
        "registration_id": registration_id,
        "full_name": full_name,
        "group_name": group_name,
        "competition_name": competition_name
    })

    flash("Заявка успешно зарегистрирована!", "success")
    return redirect(url_for("index"))


@app.route("/registrations", methods=["GET"])
def registrations():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM registrations ORDER BY created_at DESC"
        ).fetchall()
    return render_template("registrations.html", registrations=rows)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
