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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # create query from database to display on index page
    rows = db.execute("SELECT * FROM users_stocks WHERE user_id = :user",
                      user=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user",
                      user=session["user_id"])[0]['cash']

    total = cash
    #create list for each row of stocks the user has
    stocks = []
    for element, row in enumerate(rows):
        stock_info = lookup(row['symbol'])

        stocks.append(list((stock_info['symbol'], stock_info['name'], row['amount'], stock_info['price'],
                            stock_info['price'] * row['amount'], 2)))

        total += stocks[element][4]

    return render_template("index.html", stocks=stocks, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Checking if stock symbol exists
        if not lookup(request.form.get("symbol")):
            return apology("Unable to find stock.")

        elif request.form.get("symbol") is None:
            return apology("Missing symbol.")

        elif not request.form.get("shares").isdigit():
            return apology("You cannot purchase partial shares.", 400)

        symbol = lookup(request.form.get("symbol"))['symbol']   # This looks up the value of symbols in the form called symbol
        amount = int(request.form.get("shares"))    # amount of shares bought

        # Calculating cost of buying shares

        share_price = lookup(symbol)['price']
        cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])
        cash = cash[0]["cash"]
        remaining_cash = cash - (share_price * float(amount))

        # Verify if user has enough money to buy
        if remaining_cash < 0:
            return apology("Sorry, you do not have enough money to complete the transaction.")

        # if enough money
        # Check to see if user has bought stocks before
        # Create a table with .schema for user_stocks before hand
        check = db.execute("SELECT amount FROM users_stocks WHERE user_id = :user AND symbol = :symbol",
                            user=session["user_id"], symbol=symbol)

        # If no stocks of the same company bought before
        # insert into table
        if not check:
            db.execute("INSERT INTO users_stocks(user_id, symbol, amount) VALUES (:user, :symbol, :amount)",
                        user=session["user_id"], symbol=symbol, amount=amount)
            # ADD TO HISTORY TABLE
            db.execute("INSERT INTO transactions (user_id, symbol, amount, value) VALUES (:user, :symbol, :amount, :value)",
                       user=session["user_id"], symbol=symbol, amount=amount, value= (share_price))

        # if stocks bought before and exist
        # update amount into the table
        else:
            # ADD TO HISTORY TABLE
            db.execute("INSERT INTO transactions (user_id, symbol, amount, value) VALUES (:user, :symbol, :amount, :value)",
                       user=session["user_id"], symbol=symbol, amount=amount, value= (share_price))

            amount += check[0]['amount']    # adds new amounts of shares into the amount column of the check table

            db.execute("UPDATE users_stocks SET amount = :amount WHERE user_id = :user AND symbol=:symbol",
                        user=session["user_id"], symbol=symbol, amount=amount)

        #deduct user's cash
        db.execute("UPDATE users SET cash=:cash WHERE id=:user",
                   cash=remaining_cash, user=session["user_id"])




        #Redirect user to index
        flash("Stocks bought!" , 'success')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""


    #show database for transactions
    rows = db.execute("SELECT * FROM transactions WHERE user_id= :user",
                      user=session["user_id"])

    #create list called transactions to extract data from database into a table
    transactions = []
    for row in rows:
        stock_info = lookup(row['symbol'])

        #add the info into the empty list called transactions
        transactions.append(list((stock_info['symbol'], stock_info['name'], row['amount'], row['value'], row['date'])))

    #redirect user to history page

    return render_template("history.html", transactions=transactions)

@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():
    """To topup money into user's account"""
    if request.method == "POST":

        if request.form.get("amount") is None:
            return apology("Please enter a valid amount.")
        else:
            cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])
            cash = cash[0]["cash"]
            amount= int(request.form.get("amount"))


        db.execute("INSERT INTO topups (user_id, cash, new_amount, total_cash) VALUES (:user, :cash, :amount, :total_cash)",
               user=session["user_id"], cash=cash, amount=amount, total_cash= amount + cash)

        #update total cash
        db.execute("UPDATE users SET cash=:cash WHERE id= :user", cash=(amount+cash), user=session["user_id"])

        #redirect user to topup page
        flash("Topup success!", 'success')
        return redirect("/")

        return render_template("topup.html")
    else:


        return render_template("topup.html")


@app.route("/topuphistory")
@login_required
def topuphistory():
    tprows=db.execute("SELECT * FROM topups WHERE user_id=:user", user=session["user_id"])

    topups=[]

    for rows in tprows:
        topups.append(list((rows['cash'], rows['new_amount'], rows['total_cash'], rows['date'])))

    return render_template("topuphistory.html", topups=topups)

@app.route("/pfinance", methods=["GET", "POST"])
@login_required
def pfinance():
    if request.method == "POST":

        if not request.form.get("pfinance"):
            return apology("Please enter the name of the account.", 403)

        elif not request.form.get("type"):
            return apology("Please select the type of the account.", 403)

        elif not request.form.get("amount"):
            return apology("Please enter the amount of the account", 403)
        else:
            accname= request.form.get("pfinance")
            acctype= request.form.get("type")
            accamount= round(int(request.form.get("amount")), 2)

            #afterwards, we update the pfinance table with the amounts from the accounts.
            db.execute("INSERT INTO pfinance (user_id, type, name, amount) VALUES (:user, :actype, :acname, :acamount)",
                       user=session["user_id"], actype=acctype, acname=accname, acamount=accamount)

        #redirect user to topup page
        flash("Payment added!", 'success')

        return render_template("personalfinance.html")
    else:

        return render_template("personalfinance.html")

@app.route("/pfinancetable")
@login_required
def pfinancetable():
    pfinancerows= db.execute("SELECT * FROM pfinance WHERE user_id=:user", user=session["user_id"])

    phistory=[]

    for rows in pfinancerows:
        phistory.append(list((rows['type'], rows['name'], rows['amount'], rows['date'])))

    return render_template("pfinancetable.html", phistory=phistory)

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
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

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
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        stocksymbol = lookup(request.form.get("symbol"))

        # If invalid symbol entered
        if not stocksymbol:
            return apology("Unable to find stock.")

        # Otherwise display result
        return render_template("quoted.html", stocksymbol=stocksymbol)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirm password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure passwords match(confirm password)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Sorry, the passwords do not match", 400)

        # Ensure username does not exist
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        if len(rows) == 0:
            db.execute("INSERT INTO users(username, hash) VALUES (:username, :hashp)",
                       username=request.form.get("username"), hashp=generate_password_hash(request.form.get("confirmation")))

        # Remember user log in
        else:
            return apology("Username has already been taken", 400)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol = lookup(request.form.get("symbol"))['symbol']   # This looks up the value of symbols in the form called symbol
        amount = int(request.form.get("shares"))    # amount of shares bought

        # Checking to see if enough shares exist to sell

        share_price = lookup(symbol)['price']

        current_share = db.execute("SELECT amount FROM users_stocks WHERE user_id = :user AND symbol = :symbol",
                                   symbol=symbol, user=session["user_id"])[0]['amount']
        remaining_share = current_share - amount

        value = share_price
        if remaining_share == 0:
            db.execute("DELETE FROM users_stocks WHERE user_id = :user AND symbol = :symbol",
                        user=session["user_id"], symbol=symbol)

        # if invalid amount of stocks
        elif remaining_share < 0:
            return apology("Sorry, you do not have enough stocks.")

        # if valid stocks, we update the users_stocks table with new values
        else:
            db.execute("UPDATE users_stocks SET amount = :amount WHERE user_id = :user AND symbol = :symbol",
                       symbol=symbol, user=session["user_id"], amount=remaining_share)

        # update user's cash
        cash = db.execute("SELECT cash FROM users where id = :user", user=session["user_id"])[0]['cash']
        cash_aftersales=cash + (share_price * amount)

        db.execute("UPDATE users SET cash = :cash WHERE id= :user", cash=cash_aftersales, user=session['user_id'])


        # ADD TO HISTORY TABLE
        db.execute("INSERT INTO transactions(user_id, symbol, amount, value) VALUES (:user, :symbol, :amount, :value)",
                   user=session['user_id'], symbol=symbol, amount=-amount, value=value)


        #Redirect user to index
        flash("Stocks sold!" , 'success')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        rows = db.execute("SELECT symbol, amount FROM users_stocks WHERE user_id = :user",
                          user=session["user_id"])

        stocks =  {}
        for row in rows:
            stocks[row['symbol']] = row['amount']
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
