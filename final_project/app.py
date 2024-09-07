import os

from decimal import Decimal
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date
from helpers import login_required
import sqlite3
 


# Configure application
app = Flask(__name__)

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def to_usd(rows):
    for row in rows:
        row['price_daily'] = usd(row['price_daily'])
    return rows

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



@app.route("/rentequipment", methods=["GET", "POST"])
def rentequipment():
    rows = db.execute("SELECT * FROM equipment")
    rows1 = to_usd(rows)
    return render_template("rentequipment.html", rows = rows1)



@app.route("/rentequipmentloged", methods=["GET", "POST"])
def rentequipmentloged():
    rows = db.execute("SELECT * FROM equipment")
    rows1 = to_usd(rows)
    return render_template("rentequipmentloged.html", rows = rows1)



"""must change situation where available==0"""
@app.route("/yourprofil")
@login_required
def yourprofil():
    user_id = session["user_id"]
    date_today = date.today()
    items_currently = db.execute("SELECT * FROM renting JOIN equipment ON renting.item_id=equipment.item_id WHERE user_id=? AND renting.back_date>=?", user_id, date_today)
    items_past = db.execute("SELECT * FROM renting JOIN equipment ON renting.item_id=equipment.item_id WHERE user_id=? AND renting.back_date<?", user_id, date_today)
    return render_template("yourprofil.html", items_currently=items_currently, items_past=items_past)

@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    if "cart" not in session:
        session["cart"] = []

    user_id = session["user_id"]
    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            item_id = request.form.get("item_id")
            if item_id in session["cart"]:
                return redirect("/rentequipmentloged")  
            if item_id:
                session["cart"].append(item_id)
            return redirect("/rentequipmentloged")  

        elif action == "remove":
            item_id_delete = request.form.get("item_id_delete")
            if item_id_delete and item_id_delete in session["cart"]:
                session["cart"].remove(item_id_delete)
            return redirect("/cart")  
        elif action == "reserve":
            rent_date = date.today()
            back_date_str = request.form.get("back_date")

            try:
                back_date = datetime.strptime(back_date_str, '%Y-%m-%d').date()
            except ValueError:
                return "Invalid date format. Please use YYYY-MM-DD.", 400
            days_difference = (back_date - rent_date).days + 1
            cart = db.execute("SELECT * FROM equipment WHERE item_id IN (?)", session["cart"])
            total_price_daily = 0.0
            for item in cart:
                total_price_daily = total_price_daily + item["price_daily"]
            total_price = days_difference * total_price_daily
            total_price_daily = usd(total_price_daily)
            total_price = usd(total_price)
            cart = to_usd(cart)
            for item in cart:
                db.execute("INSERT INTO renting (user_id, item_id, rent_date, back_date) VALUES (?, ?, ?, ?)", 
                user_id, item["item_id"], rent_date, back_date)
                result = db.execute("SELECT * FROM equipment WHERE item_id=(?)", item["item_id"])
                if result:
                    current_available = result[0]["available"]
                    new_available = current_available - 1
                    db.execute("UPDATE equipment SET available=(?) WHERE item_id=(?)", new_available, item["item_id"])
                    session["cart"].clear()

            return render_template("thankyou.html", cart=cart, back_date=back_date, rent_date=rent_date, total_price=total_price, days_difference = days_difference, total_price_daily=total_price_daily) 


    items = db.execute("SELECT * FROM equipment WHERE item_id IN (?)", session["cart"])
    items = to_usd(items)
    return render_template("cart.html", items=items)




@app.route("/thankyou", methods=["GET", "POST"])
@login_required
def thankyou():
    return render_template("thankyou.html")


@app.route("/ourstores", methods=["GET", "POST"])
def ourstores():
    return render_template("ourstores.html")



@app.route("/aboutus", methods=["GET", "POST"])
def aboutus():
    return render_template("aboutus.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")



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
