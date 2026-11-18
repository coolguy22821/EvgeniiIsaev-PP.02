from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from notification_service import send_registration_notification

DB_PATH = Path(__file__).resolve().parent / "registrations.db"
app = Flask(__name__)
app.secret_key = "change-this-secret-key"

def db():
    con=sqlite3.connect(DB_PATH); con.row_factory=sqlite3.Row; return con

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL,
        group_name TEXT NOT NULL, email TEXT NOT NULL, competition_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        con.execute("""CREATE TABLE IF NOT EXISTS notification_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT, registration_id INTEGER NOT NULL,
        group_name TEXT NOT NULL, status TEXT NOT NULL, details TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

@app.route("/")
def index(): return render_template("index.html")

@app.route("/register",methods=["POST"])
def register():
    values=[request.form.get(k,"").strip() for k in
            ("full_name","group_name","email","competition_name")]
    if not all(values):
        flash("Пожалуйста, заполните все поля.","error"); return redirect(url_for("index"))
    if "@" not in values[2] or "." not in values[2].split("@")[-1]:
        flash("Укажите корректный адрес электронной почты.","error")
        return redirect(url_for("index"))
    with db() as con:
        cur=con.execute("INSERT INTO registrations(full_name,group_name,email,competition_name) VALUES(?,?,?,?)",values)
        rid=cur.lastrowid
    result=send_registration_notification({"registration_id":rid,"full_name":values[0],
        "group_name":values[1],"competition_name":values[3]})
    with db() as con:
        con.execute("INSERT INTO notification_log(registration_id,group_name,status,details) VALUES(?,?,?,?)",
                    (rid,values[1],result["status"],result["details"]))
    flash("Заявка успешно зарегистрирована!","success")
    return redirect(url_for("index"))

@app.route("/registrations")
def registrations():
    with db() as con: rows=con.execute("SELECT * FROM registrations ORDER BY created_at DESC").fetchall()
    return render_template("registrations.html",registrations=rows)

@app.route("/notifications")
def notifications():
    with db() as con:
        rows=con.execute("""SELECT notification_log.*, registrations.full_name,
        registrations.competition_name FROM notification_log JOIN registrations
        ON registrations.id=notification_log.registration_id
        ORDER BY notification_log.created_at DESC""").fetchall()
    return render_template("notifications.html",notifications=rows)

if __name__=="__main__":
    init_db(); app.run(debug=True)
