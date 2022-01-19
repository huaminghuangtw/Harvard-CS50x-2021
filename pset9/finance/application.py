import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import *


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
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    if (request.method == "GET"):
        messages = session.get("messages", None)

        # Delete stocks with zero shares
        db.execute("DELETE FROM transactions \
                    WHERE symbol IN (SELECT symbol FROM transactions \
                    WHERE user_id = ? GROUP BY symbol HAVING TOTAL(shares) == 0)", \
                    user_id)

        stocks = db.execute("SELECT symbol, name, SUM(shares) as totalShares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        # db.execute will return a list of dictionaries, inside of which are keys and values representing a table's fields and cells, respectively
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash[0]["cash"]

        total = cash
        for stock in stocks:
            total += stock["price"] * stock["totalShares"]

        # Reset flashing message on homepage
        session["messages"] = None

        return render_template("index.html", stocks=stocks, cash=usd(cash), total=usd(total), usd_function=usd, messages=messages)
    else:
        if ("add_cash" in request.form):
            current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
            add_cash = request.form.get("add_cash")
            cash_added = int(add_cash)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + cash_added, user_id)
        else:
            stocks = db.execute("SELECT symbol, name, SUM(shares) as totalShares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
            for stock in stocks:
                transaction_type = request.form.get(stock["symbol"])
                if not transaction_type:
                    continue
                else:
                    if (transaction_type == "Sell"):
                        sell_kernel(db, request.form, user_id, from_homepage=True)
                    elif (transaction_type == "Buy"):
                        buy_kernel(db, request.form, user_id, from_homepage=True)
                    break

        return redirect("/")

# ---------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if (request.method == "POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Please provide username!", "danger")
            return redirect("/register")
        elif not password:
            flash("Please provide password!", "danger")
            return redirect("/register")
        elif not confirmation:
            flash("Please provide password confirmation!", "danger")
            return redirect("/register")

        if (password != confirmation):
            flash("Passwords do not match!", "danger")
            return redirect("/register")

        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            flash("Registration successful!", "success")
            return redirect("/")
        except:
            flash("Username has already been registered!", "danger")
            return redirect("/register")
    else:
        return render_template("register.html")

# ---------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id, but maintain flashed message if present
    if session.get("_flashes"):
        flashes = session.get("_flashes")
        session.clear()
        session["_flashes"] = flashes
    else:
        session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if (request.method == "POST"):

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username!", "danger")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password!", "danger")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if (len(rows) != 1) or (not check_password_hash(rows[0]["hash"], request.form.get("password"))):
            flash("Invalid username and/or password!", "danger")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = request.form.get("username")

        # Flash "Login successfully!" message
        flash("Login successfully!", "success")

        # Redirect user to homepage
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

    # Flash "You have been successfully logged out!" message
    flash("You have been successfully logged out!", "success")

    # Redirect user to login form
    return redirect("/login")

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
            flash("Please provide your current password!", "danger")
            return redirect("/changepwd")
        elif not new_password:
            flash("Please provide your new password!", "danger")
            return redirect("/changepwd")
        elif not confirmation:
            flash("Please provide new password confirmation!", "danger")
            return redirect("/changepwd")

        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        if (not check_password_hash(rows[0]["hash"], current_password)):
            flash("Your current password is incorrect!", "danger")
            return redirect("/changepwd")
        elif (new_password != confirmation):
            flash("New passwords do not match!", "danger")
            return redirect("/changepwd")
        elif (new_password == current_password):
            flash("Your new password cannot be the same as your current password!", "danger")
            return redirect("/changepwd")

        hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)

        flash("Successfully changed password!", "success")

        return redirect("/")
    else:
        username = session["username"]
        return render_template("changepwd.html", username=username)

# ---------------------------------------------
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    user_id = session["user_id"]
    if (request.method == "POST"):
        buy_kernel(db, request.form, user_id)
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
        sell_kernel(db, request.form, user_id)
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