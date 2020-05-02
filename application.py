import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    total_money = 0

    all_symbols = db.execute ("SELECT symbol FROM purchase WHERE user_id = :u_id  GROUP BY symbol;", u_id = session['user_id'])
    actual_cash = db.execute ("SELECT cash FROM users WHERE id = :id ;", id = session["user_id"])
    if all_symbols != []:
        stocks = []

        for i in all_symbols:
            data = lookup( i['symbol'] )
            stock = db.execute("SELECT SUM(shares) FROM purchase WHERE user_id = :id AND symbol = :symbol;", id = session["user_id"], symbol = data['symbol'] )

            if stock[0]['SUM(shares)'] == 0:
                continue

            else:
                info = {}
                info['name'] = data['name']
                info['symbol'] = data['symbol']
                info['price'] = data['price']
                info['shares'] = stock[0]['SUM(shares)']
                info['total'] = info['shares'] * info['price']
                stocks.append(info)

        for j in range(len(stocks)):
            total_money += stocks[j]['total']

        total_money += actual_cash[0]['cash']
        print(actual_cash[0]['cash'])


        return render_template("home.html",  stocks = stocks, actual_cash = round(actual_cash[0]['cash'], 2) , total_money = round(total_money,2) )

    else:
        current_cash = db.execute ("SELECT cash FROM users WHERE id = :id ;", id = session["user_id"])
        return render_template("home.html",   actual_cash = round(actual_cash[0]['cash'], 2) , total_money = actual_cash[0]['cash'])

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("insert symbol and try again", 403)
        else:
            symbol = request.form.get("symbol")
            buy = lookup(symbol)
            user_cash = db.execute("SELECT cash FROM users WHERE id = (:id)", id = session["user_id"])
            number = request.form.get("shares")
            total_amount = buy["price"] * int(number)
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            remaining_cash = user_cash[0]['cash'] - float(total_amount)

            if buy == None:
                return apology("symbol not found, try again", 403)
            elif not request.form.get("shares"):
                return apology("insert number of shares", 403)
#checking if user can afford transaction
            elif total_amount  < user_cash[0]['cash']:
#inserting in to the table "purchase" all the values
                db.execute("INSERT INTO purchase (user_id, symbol, name, shares, price,time, price1) VALUES (:user_id , :symbol , :name , :shares , :price , :time, :price1)", user_id = session["user_id"], symbol = symbol.upper(), name = buy["name"], shares = number, price = str(round(total_amount, 2)) , time = time, price1 = buy["price"] )
                db.execute("UPDATE users SET cash = :cash WHERE id = :id ", cash = remaining_cash , id = session["user_id"] )

                return redirect("/")
            else:
                return apology("not enought money for transaction", 403)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    table = db.execute("SELECT * FROM purchase WHERE user_id = :id ;", id = session["user_id"])

    return render_template("history.html", table = table )


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
            return apology("provide symbol", 403)
        else:
            symbol = request.form.get("symbol")

            quote = lookup(symbol)

            if quote == None:
                return apology("symbol not found, try again", 403)

            else:
                return render_template("quoted.html", name=quote["name"], symbol = symbol, price = quote["price"]   )
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password was submitted
        elif not request.form.get("password2"):
            return apology("must provide confirmation password", 403)

        elif   request.form.get("password") != request.form.get("password2") :
            return apology("passwords need to match", 403)

        name = request.form.get("username")
        password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256')
        rows = db.execute("SELECT * FROM users")
        for row in rows:
            if name == row["username"]:
                return apology("username already exists", 403)
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username = name, hash = password)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":

        all_symbols = db.execute ("SELECT symbol FROM purchase WHERE user_id = :u_id  GROUP BY symbol;", u_id = session['user_id'])

        return render_template("sell.html", symbol = all_symbols)

    else:
        shares = (request.form.get("shares") )
        symbol = request.form.get("symbol")
        stock1 = db.execute("SELECT SUM(shares) FROM purchase WHERE user_id = :id AND symbol = :symbol;", id = session["user_id"], symbol = symbol )

        if int(shares) > stock1[0]['SUM(shares)']:
            return apology("insert correct number of shares you can afford", 403)
        elif int(shares) <= 0:
            return apology("insert correct number of shares you can afford", 403)

        else:
            plus_price = lookup(symbol)["price"] * int(shares)
            cash = db.execute("SELECT cash FROM users WHERE id = :id;", id = session["user_id"],  )
            current_cash = cash[0]['cash'] + plus_price
            shares1 = db.execute ("SELECT SUM(shares) from purchase WHERE user_id = :id AND symbol = :symbol;", id = session["user_id"], symbol = symbol )
            total_shares = shares1[0]['SUM(shares)'] - float(shares)

            name = lookup(symbol)
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.execute("UPDATE users SET cash = :cash WHERE id = :id ", cash = current_cash , id = session["user_id"] )
            db.execute("INSERT INTO purchase (user_id, symbol, name, shares, price,time, price1) VALUES (:user_id , :symbol , :name , :shares , :price , :time, :price1)", user_id = session["user_id"], symbol = symbol.upper(), name = name["name"], shares = -int(shares), price = -float(name["price"]) , time = time, price1= lookup(symbol)["price"])

            return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
