import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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


@app.route("/")
@login_required
def index():
    return render_template("index.html")



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

        db.execute("INSERT INTO trips (user_id, destination, start_date, end_date) VALUES (:user_id, :destination, :start_date, :end_date)",
        user_id=session["user_id"], destination=destination, start_date=start_date, end_date=end_date)

        return render_template("index.html")

    else:
        return render_template("create.html")






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