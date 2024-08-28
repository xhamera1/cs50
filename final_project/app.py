import os

from decimal import Decimal
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required
import sqlite3
 


# Configure application
app = Flask(__name__)

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///budorent.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
@login_required
def home():
    return render_template("home.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("email"):
            return render_template("error.html", info="Must provide email")
        if not request.form.get("password"):
            return render_template("error.html", info="Must provide password")
        rows = db.execute("SELECT * FROM users WHERE email=?", request.form.get("email"))
        
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
                return render_template("error.html", info="invalid username and/or password")

        session["user_id"] = rows[0]["id"]
        return redirect("/home")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")



@app.route("/signup", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("signup.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        existing_user = db.execute(
            "SELECT email FROM users WHERE email = ?", email
        )
        if not email:
            return render_template("error.html", info="invalid email")
        elif existing_user:
            return render_template("error.html", info="email already taken")
        elif not password:
            return render_template("error.html", info="invalid email")
        elif not confirmation or (password != confirmation):
            return render_template("error.html", info="invalid confirmation")

        password_hash = generate_password_hash(
            password, method="pbkdf2", salt_length=16
        )

        try:
            result = db.execute(
                "INSERT INTO users (email, hash) VALUES (?, ?)", email, password_hash
            )
            if result:
                user_data = db.execute("SELECT id FROM users WHERE email = ?", email)
                if user_data:
                    return redirect("/login")
        except Exception as e:
            print(f"Database error: {e}")
            return render_template("error.html", info="registration error")











if __name__ == "__main__":
    app.run(debug=True)
