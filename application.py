import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


from helpers import apology, login_required, lookup, exchange_rate, format


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

# # Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///travel.db")

# # Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "GET":
        trips = db.execute("SELECT trip_id, destination, start_date, end_date, image_url, alt_description FROM trips WHERE user_id = :user_id ORDER BY start_date ASC", user_id=session["user_id"])
        print(trips[0]["image_url"])


        return render_template("index.html", trips=trips)

    else:
        trip_id = request.form.get("trip_id")

        rows = db.execute("SELECT destination, start_date, end_date, trip_id from trips WHERE trip_id=:trip_id", trip_id = trip_id)

        trip_to_edit = (rows[0])


        return render_template("edit.html", trip = trip_to_edit)




@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":

        new_destination = request.form.get("destination")
        new_start_date = request.form.get("start_date")
        new_end_date = request.form.get("end_date")
        trip_id = request.form.get("trip_id")

        print(trip_id)

        db.execute("UPDATE trips SET destination = :new_destination, start_date = :new_start_date, end_date = :new_end_date WHERE trip_id = :trip_id", new_destination = new_destination, new_start_date = new_start_date, new_end_date = new_end_date, trip_id = trip_id)

        return render_template("edit-complete.html")

    else:
        return render_template("index.html")


#Check date format format
def date_check(month, day):
    if month > 12:
        return 1

    if month == 2:
        if day > 29:
            return 1
    elif month == 4 or month == 6 or month == 9 or month == 11:
        if day > 30:
            return 1
    else:
        if day > 31:
            return 1
    return 0



@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    #User inputs in new trip information
    if request.method == "POST":

        destination = request.form.get("destination")
        if not destination:
            return apology("Please input a destination")

        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        start_month = int(start_date[5:7])
        start_day = int(start_date[8:10])

        if date_check(start_month, start_day) == 1:
            return apology("Please input valid date")

        end_month = int(end_date[5:7])
        end_day = int(end_date[8:10])

        ####error check end month and day

        image = lookup(destination)
        image_url = (image["urls"]["regular"])
        alt_description = (image["alt_description"])
        print(alt_description)




        db.execute("INSERT INTO trips (user_id, destination, start_date, end_date, image_url, alt_description) VALUES (:user_id, :destination, :start_date, :end_date, :image_url, :alt_description)",
        user_id=session["user_id"], destination=destination, start_date=start_date, end_date=end_date, image_url=image_url, alt_description=alt_description)

        return redirect("/")

    else:
        return render_template("create.html")

# @app.route("/edit", methods=["GET", "POST"])
# @login_required
# def edit():

#     # if request.method == "POST":

#     # else:
#     #     trip = db.execute("SELECT destination, start_date, end_date FROM trips WHERE trip_id=:id", id =)

@app.route("/exchange", methods=["GET", "POST"])
@login_required
def exchange():

    if request.method == "POST":

        #Parse form inputs
        start_currency = request.form.get("start_currency").upper()
        end_currency = request.form.get("end_currency").upper()
        amount = request.form.get("amount")

        #Make api call
        response = exchange_rate(start_currency, end_currency)

        #Get the exchange rate from the result
        rate = list((response["rates"].values()))

        #Multiply the exchange rate by the amount (start_currency is the base, amount multiplied by rate for end_currency)
        final_amount = (rate[0] * float(amount))

        final_amount_2dp = "%.2f" % final_amount

        return render_template("exchange-post.html", start_currency = start_currency, end_currency = end_currency, amount = amount, final_amount = final_amount_2dp)

    else:
        return render_template("exchange.html")


# @app.route("/history")
# @login_required
# def history():




@app.route("/register", methods=["GET", "POST"])

def register():
    """Register user"""

    #User reached route via POST
    if request.method == "POST":

        #User entered username
        if not request.form.get("username"):
            return apology("must provide username")

        #User entered password
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password")

        #Confirm password matches
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password must match")

        #Hash the password
        hash = generate_password_hash(request.form.get("password"))

        #Insert user into database
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=hash)

        if not result:
            return apology("username already exists")
        else:
            return apology("registration complete", 200)

        #Remember user
        session["user_id"] = result

        return redirect("/")

    #User reached route via GET
    else:
        return render_template("register.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username_to_check = request.args.get("username")
    if len(username_to_check) < 1:
        return jsonify(False)

    current_users = db.execute("SELECT username FROM users")

    for user in current_users:
        if user["username"] == username_to_check:
            return jsonify(False)
        else:
            return jsonify(True)




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


# @app.route("/exchange", methods=["GET", "POST"])
# @login_required
# def quote():



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)