""" KPOP Next Big Sound - Web Application for Social Metrics of KPOP Artists"""
""" Official Final Project of Team TEN BILLION POINTS for BreederDAO Hackathon 2022"""

import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd, num, form, sort_smi, sort_nbs, sort_cmb, get

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
app.jinja_env.filters["num"] = num
app.jinja_env.filters["form"] = form

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///accounts.db")
dbs = SQL("sqlite:///nbs.db")


@app.route("/")
@login_required
def home():
    """Redirect to index"""
    return redirect("index.html")


@app.route("/index")
@login_required
def index():
    """Show summary of chart"""

    sort = request.args.get("sort", "else")
    exe = sort_nbs(sort)

    socials = dbs.execute(exe)

    return render_template("index.html", socials=socials, num=num, form=form, sort=sort)


@app.route("/smi", methods=["GET", "POST"])
@login_required
def smi():
    """Social Metrics Index"""

    # POST: Quote web page with lookup values
    if request.method == "POST":
        pass

    # GET: Direct the user to the buy web page with method post
    else:
        sort = request.args.get("sort", "else")
        exe = sort_smi(sort)
        socials = dbs.execute(exe)
        return render_template("smi.html", socials=socials, num=num, form=form, sort=sort)
        

@app.route("/cmb", methods=["GET", "POST"])
@login_required
def cmb():
    """Social Metrics Index"""

    # POST: Quote web page with lookup values
    if request.method == "POST":
        pass

    # GET: Direct the user to the buy web page with method post
    else:
        sort = request.args.get("sort", "else")
        exe = sort_cmb(sort)
        socials = dbs.execute(exe)
        return render_template("cmb.html", socials=socials, num=num, form=form, sort=sort)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Search for artist's stats"""
    
    if request.method == "POST":
        artist = request.form.get("artist")
        chart = request.form.get("chart")
        month = request.form.get("month")
        
        
        if not artist:
            return apology("Please select an artist")
        elif not chart:
            return apology("Please select a chart")
        elif chart in ["smi", "cmb"] and not month:
            return apology("Please select a month")
            
        if chart == "ind":
            month = "total"
            
        exe = get(artist, chart, month)
        if month == "total":
            info = dbs.execute(exe)[0][chart]
        else:
            info = dbs.execute(exe)[0][month]
        
        months = {
            "jan": "January",
            "feb": "February",
            "mar": "March",
            "apr": "April",
            "may": "May",
            "jun": "June",
            "jul": "July",
            "aug": "August",
            "sep": "September",
            "oct": "October",
            "nov_dec": "November-December",
            "total": "Total",
        }
        
        charts = {
            "smi": "Social Metrics Index",
            "cmb": "Combined Chart Cumulative Points",
            "ind": "Summary Index",
        }
        
        return render_template("searched.html", info=info, artist=artist, chart=chart, month=month, usd=usd, num=num, months=months, charts=charts)
    
    else:
        artists = dbs.execute("SELECT artist FROM nbs ORDER BY artist")
        return render_template("search.html", artists=artists, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/index")


@app.route("/about")
@login_required
def about():

    # POST: Quote web page with lookup values
    if request.method == "POST":

        # Fetch symbol input from user
        symbol = request.form.get("symbol")

        # Check if there is provided symbol
        if not symbol:
            return apology("Symbol not found")

        # Lookup for the symbol and get the values
        quote = lookup(symbol)

        # Check if the symbol is valid
        if not quote:
            return apology("Invalid symbol")

    # GET: Direct the user to the quote web page with method post
    else:
        return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Fetch data from registration page
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Hash te password provided
        hash = generate_password_hash(password)

        # Ensure username was submitted
        if not username:
            return apology("Please provide username")

        # Ensure password was submitted and the confirmation matches the password
        elif not password or password != confirmation:
            return apology("Please provide password and confirm it")

        try:
            # Query database to insert username and hashed password
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            return redirect("/index")
        except:
            # Notify that the username is already registered
            return apology("You're already registered!")

        # Redirect user to home page
        return redirect("/index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/changePass", methods=["GET", "POST"])
@login_required
def changePass():
    """ Change Password """

    if request.method == "POST":

        # Fetch user id
        user_id = session["user_id"]

        # Get the provided old and new passwords
        old_pass = request.form.get("old_pass")
        new_pass = request.form.get("new_pass")

        # Get the user's current password and check if the old password is correct
        old_hash = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        if not check_password_hash(old_hash[0]["hash"], old_pass):
            return apology("Incorrect password")

        # Update the new password
        new_hash = generate_password_hash(new_pass)
        db.execute("UPDATE users SET hash = ?", new_hash)

        # Log out the user
        session.clear()

        return redirect("/index")
    else:
        return render_template("change_pass.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
