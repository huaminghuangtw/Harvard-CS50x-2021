import os
import requests
import urllib.parse

from flask import flash, redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def buy_kernel(db, form, user_id, from_homepage=False):
    if (from_homepage):
        symbol = list(form.to_dict(flat=False).keys())[1]
    else:
        symbol = form.get("symbol").upper()

    stock = lookup(symbol)

    if not symbol:
        if (from_homepage):
            return flash("Please enter a symbol", "danger")
        else:
            return apology("Please enter a symbol")
    elif not stock:
        if (from_homepage):
            return flash("Invalid symbol!", "danger")
        else:
            return apology("Invalid symbol!")

    try:
        if (from_homepage):
            shares_to_buy = int(request.form.get("quantity"))
        else:
            shares_to_buy = int(form.get("shares"))
    except:
        if (from_homepage):
            return flash("Shares must be an integer!", "danger")
        else:
            return apology("Shares must be an integer!")

    if (shares_to_buy <= 0):
        if (from_homepage):
            return flash("Shares must be a positive integer!", "danger")
        else:
            return apology("Shares must be a positive integer!")

    # db.execute will return a list of dictionaries, inside of which are keys and values representing a table's fields and cells, respectively
    current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    stock_name = stock["name"]
    stock_price = stock["price"]
    total_price = stock_price * shares_to_buy

    if (current_cash < total_price):
        if (from_homepage):
            return flash("Not enough cash!", "danger")
        else:
            return apology("Not enough cash!")
    else:
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash - total_price, user_id)
        db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)", \
                   user_id, stock_name, shares_to_buy, stock_price, "buy", symbol)

    session["messages"] = {"type": "Bought!", "symbol": symbol, "shares": shares_to_buy}


def sell_kernel(db, form, user_id, from_homepage=False):
    if (from_homepage):
        symbol = list(form.to_dict(flat=False).keys())[0]
        shares_to_sell = int(request.form.get("quantity"))
    else:
        symbol = form.get("symbol")
        shares_to_sell = int(form.get("shares"))

    if (shares_to_sell <= 0):
        if (from_homepage):
            return flash("Shares must be a positive interger!", "danger")
        else:
            return apology("Shares must be a positive integer!")

    stock_name = lookup(symbol)["name"]
    stock_price = lookup(symbol)["price"]
    shares_owned = db.execute("SELECT SUM(shares) as totalShares FROM transactions WHERE USER_ID = ? and SYMBOL = ? GROUP BY symbol", \
                              user_id, symbol)[0]["totalShares"]

    if (shares_owned < shares_to_sell):
        if (from_homepage):
            return flash("You don't have enough shares!", "danger")
        else:
            return apology("You don't have enough shares!")

    current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    income = shares_to_sell * stock_price
    db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + income, user_id)
    db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)", \
               user_id, stock_name, -shares_to_sell, stock_price, "sell", symbol)

    session["messages"] = {"type": "Sold!", "symbol": symbol, "shares": shares_to_sell}