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

    user_id = session.get("user_id")
    rows = db.execute("SELECT * FROM wallet WHERE user_id=?", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)
    cash = usd(cash[0]['cash'])
    all = 0.0
    for row in rows:
        look = lookup(row['symbol'])
        row['price'] = look['price']
        row['total'] = row['amount']*row['price']
        all += row['total']
        row['total'] = usd(row['total'])
        row['price'] = usd(look['price'])
    all = usd(all)
    return render_template("index.html", cash=cash, rows = rows, all=all)


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
                "BUY",
                symbol,
                usd(round(price, 2)),
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
    user_id = session.get("user_id")
    rows = db.execute("SELECT * FROM transactions WHERE user_id=?", user_id)
    return render_template("history.html", rows=rows)


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
        symbol = request.form.get("symbol")

        if symbol is None:
            return apology("INVALID SYMBOL", 400)
        if not isinstance(symbol, str):
            return apology("INVALID SYMBOL", 400)
        symbol = symbol.strip()

        if not symbol:
            return apology("INVALID SYMBOL", 400)

        look = lookup(symbol)
        if not look:
            return apology("INVALID SYMBOL", 400)
        data = lookup(request.form.get("symbol"))
        value = usd(data['price'])
        if not data:
            return apology("INVALID SYMBOL", 400)
        return render_template("quoted.html", data=data, value=value)
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        existing_user = db.execute(
            "SELECT username FROM users WHERE username = ?", username
        )
        if username == "" or existing_user:
            return apology("Username is not available")
        elif password == "":
            return apology("MISSING PASSWORD")
        elif confirmation == "" or (password != confirmation):
            return apology("PASSWORDS DON'T MATCH")

        password_hash = generate_password_hash(
            password, method="pbkdf2", salt_length=16
        )

        result = db.execute(
            "INSERT INTO users(username, hash) VALUES (?, ?)", username, password_hash
        )

        if result:
            user_data = db.execute("SELECT id FROM users WHERE username = ?", username)
            if user_data:
                user_id = user_data[0]["id"]
                session["user_id"] = user_id

                return redirect("/")
        return apology("Registration failed")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session.get("user_id")
    rows = db.execute("SELECT * FROM wallet WHERE user_id=?", user_id)
    if request.method == "POST":
        if not request.form.get("shares") or not request.form.get("symbol"):
            return apology("You should choose shares or/and amount correctly", 400)

        shares = request.form.get("symbol")
        amount_tosell = int(request.form.get("shares"))
        if amount_tosell<=0:
            return apology("Must be a positive number")
        all_shares = db.execute("SELECT symbol FROM wallet WHERE user_id=?", user_id)
        symbol = [row['symbol'] for row in all_shares]
        if shares not in symbol:
            return apology("You do not have this shares")

        holding_shares = db.execute("SELECT * FROM wallet WHERE user_id=? and symbol=?",user_id,shares)
        holding_shares = int(holding_shares[0]["amount"])
        if holding_shares<amount_tosell:
            return apology("You do not have this amount of shares")

        look = lookup(shares)
        if not look:
            return apology("INVALID SYMBOL", 400)

        shares = look["symbol"]
        price = float(look["price"])
        db.execute("INSERT INTO transactions (user_id, operation, symbol, price, amount, date) VALUES (?, ?, ?, ?, ?, datetime('now'))",
                        user_id,
                        "SELL",
                        shares,
                        usd(round(price, 2)),
                        amount_tosell
                    )
        shares = request.form.get("symbol")
        old_amount = db.execute("SELECT * FROM wallet where user_id=? and symbol=?", user_id, shares)
        old_amount = int(old_amount[0]["amount"])
        new_amount = old_amount-amount_tosell
        if new_amount!=0:
            db.execute("UPDATE wallet SET amount=? WHERE user_id=? and symbol=?",new_amount,user_id,shares)
        else:
            db.execute("DELETE FROM wallet WHERE user_id=? and symbol=?", user_id, shares)

        cash_result = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        if not cash_result:
            return apology("USER NOT FOUND", 400)

        cash = float(cash_result[0]["cash"])

        total_amount = float(amount_tosell) * price
        new_cash = cash+total_amount
        db.execute(
                "UPDATE users SET cash = ROUND(?, 2) WHERE id = ?",
                new_cash,
                user_id
            )
        return redirect("/")
    else:
        return render_template("sell.html", rows=rows)


@app.route("/favorite", methods=["GET", "POST"])
@login_required
def favorite():
    user_id = session.get("user_id")
    if request.method == "POST":
        new_favorite = request.form.get("add")
        look = lookup(new_favorite)
        if not look:
            return apology("INVALID SYMBOL", 403)
        new_favorite = look["symbol"]
        db.execute("INSERT OR IGNORE INTO favorite (user_id, symbol) VALUES (?, ?)", user_id, new_favorite)
        return redirect("/favorite")
    else:
        rows = db.execute("SELECT symbol FROM favorite WHERE user_id=?", user_id)
        favorite_data = []
        for row in rows:
            symbol = row["symbol"]
            data = lookup(symbol)
            if data:
                favorite_data.append({
                    "symbol": data["symbol"],
                    "price": usd(data["price"]),
                    "high": usd(data["high"]),
                    "low": usd(data["low"]),
                    "volume": data["volume"]
                })
        return render_template("favorite.html", rows=favorite_data)



@app.route("/delete_favorite", methods=["POST"])
@login_required
def delete_favorite():
    user_id = session.get("user_id")
    symbol = request.form.get("symbol")
    db.execute("DELETE FROM favorite WHERE user_id = ? AND symbol = ?", user_id, symbol)
    return redirect("/favorite")




if __name__ == "__main__":
    app.run(debug=True)
