import os

from decimal import Decimal
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
import sqlite3



# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        if not symbol:
            return apology("MISSING SYMBOL", 400)
        if not shares.isdigit():
            return apology("INVALID NUMBER OF SHARES", 400)
        
        shares = int(shares)

        look = lookup(symbol)
        if not look:
            return apology("INVALID SYMBOL", 400)
        
        symbol = look["symbol"]
        price = float(look["price"]) 

        user_id = session.get("user_id")
        cash_result = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        if not cash_result:
            return apology("USER NOT FOUND", 400)
        
        cash = float(cash_result[0]["cash"]) 

        total_amount = float(shares) * price

        if cash >= total_amount:
            new_cash = cash - total_amount
            db.execute(
                "INSERT INTO transactions (user_id, operation, symbol, price, amount, date) VALUES (?, ?, ?, ?, ?, datetime('now'))",
                user_id,
                "buy",
                symbol,
                round(price, 2), 
                shares
            )
            row = db.execute(
                "SELECT symbol FROM wallet WHERE user_id = ? AND symbol = ?",
                user_id,
                symbol
            )
            if len(row) == 0:
                db.execute(
                    "INSERT INTO wallet (user_id, symbol, amount) VALUES (?, ?, ?)",
                    user_id,
                    symbol,
                    shares
                )
            else:
                row = db.execute(
                    "SELECT amount FROM wallet WHERE user_id = ? AND symbol = ?",
                    user_id,
                    symbol
                )
                old_shares = row[0]["amount"]
                new_shares = old_shares + shares
                db.execute(
                    "UPDATE wallet SET amount = ? WHERE user_id = ? AND symbol = ?",
                    new_shares,
                    user_id,
                    symbol
                )
            db.execute(
                "UPDATE users SET cash = ROUND(?, 2) WHERE id = ?",
                new_cash,
                user_id
            )

            return redirect("/")
        else:
            return apology("CAN'T AFFORD", 400)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("INVALID SYMBOL", 403)
        data = lookup(request.form.get("symbol"))
        value = usd(data['price'])
        if not data:
            return apology("INVALID SYMBOL", 403)
        return render_template("quoted.html", data=data, value=value)
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username to register", 403)

        elif not request.form.get("password"):
            return apology("must provide password to register", 403)
        
        elif not request.form.get("confirmation"):
            return apology("must provide password again to register", 403)
        
        username = request.form.get("username")
        password1 = request.form.get("password")
        password2 = request.form.get("confirmation")

        hash_password = generate_password_hash(password1, 'pbkdf2', 16)

        if password1!=password2:
            return apology("passwords must be the same", 403)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?)", (username, hash_password))
        except sqlite3.IntegrityError:
            return apology("usename must be unique, try again", 403)
        else:
            return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


if __name__ == "__main__":
    app.run(debug=True)