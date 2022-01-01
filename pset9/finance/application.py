import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# ---------------------------------------------
@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    stocks = db.execute("SELECT symbol, name, SUM(shares) as totalShares, price FROM transactions WHERE user_id = ? GROUP BY symbol",
                        user_id)
    # db.execute will return a list of dictionaries, inside of which are keys and values representing a table’s fields and cells, respectively
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash[0]["cash"]

    total = cash
    for stock in stocks:
        total += stock["price"] * stock["totalShares"]

    return render_template("index.html", stocks=stocks, cash=usd(cash), total=usd(total), usd_function=usd)

# ---------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if (request.method == "POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please provide username")
        elif not password:
            return apology("Please provide password")
        elif not confirmation:
            return apology("Please provide password confirmation")

        if (password != confirmation):
            return apology("Passwords do not match!")

        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            return redirect("/")
        except:
            return apology("Username has already been registered!")
    else:
        return render_template("register.html")

# ---------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if (request.method == "POST"):

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if (len(rows) != 1) or (not check_password_hash(rows[0]["hash"], request.form.get("password"))):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# ---------------------------------------------
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# ---------------------------------------------
@app.route("/changepwd", methods=["GET", "POST"])
@login_required
def changepwd():
    """Change password"""
    if (request.method == "POST"):
        user_id = session["user_id"]
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not current_password:
            return apology("Please provide your current password")
        elif not new_password:
            return apology("Please provide your new password")
        elif not confirmation:
            return apology("Please provide new password confirmation")

        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        if (not check_password_hash(rows[0]["hash"], current_password)):
            return apology("Your current password is incorrect!")
        elif (new_password != confirmation):
            return apology("New passwords do not match!")
        elif (new_password == current_password):
            return apology("Your new password cannot be the same as your current password!")

        hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)

        return redirect("/")
    else:
        return render_template("changepwd.html")

# ---------------------------------------------
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if (request.method == "POST"):
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        if not symbol:
            return apology("Please enter a symbol")
        elif not stock:
            return apology("Invalid symbol!")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Shares must be an integer!")

        if (shares <= 0):
            return apology("Shares must be a positive integer!")

        user_id = session["user_id"]
        # db.execute will return a list of dictionaries, inside of which are keys and values representing a table’s fields and cells, respectively
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash[0]["cash"]
        stock_name = stock["name"]
        stock_price = stock["price"]
        total_price = stock_price * shares

        if (cash < total_price):
            return apology("Not enough cash!")
        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_price, user_id)
            db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)",
                       user_id, stock_name, shares, stock_price, "buy", symbol)

        return redirect("/")
    else:
        return render_template("buy.html")

# ---------------------------------------------
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if (request.method == "POST"):
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if (shares <= 0):
            return apology("Shares must be a positive integer!")

        stock_name = lookup(symbol)["name"]
        stock_price = lookup(symbol)["price"]
        shares_owned = db.execute("SELECT shares FROM transactions WHERE USER_ID = ? and SYMBOL = ? GROUP BY symbol",
                                  user_id, symbol)[0]["shares"]

        if (shares_owned < shares):
            return apology("You don't have enough shares!")

        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        income = shares * stock_price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + income, user_id)
        db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)",
                   user_id, stock_name, -shares, stock_price, "sell", symbol)

        return redirect("/")
    else:
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        return render_template("sell.html", symbols=symbols)

# ---------------------------------------------
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT type, symbol, price, shares, time FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions=transactions, usd_function=usd)

# ---------------------------------------------
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if (request.method == "POST"):
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        if not symbol:
            return apology("Please enter a symbol")

        if not stock:
            return apology("Invalid symbol!")

        return render_template("quoted.html", stock=stock, usd_function=usd)

    else:
        return render_template("quote.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)