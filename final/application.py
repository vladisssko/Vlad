import os
import datetime
import smtplib
import myEnvVal

import cgi, cgitb

import json
from io import BytesIO



EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")


@app.route("/")
def index():
    """Show the homepage"""

    return render_template("home.html")

@app.route("/home")
def about():
    """Show the homepage"""

    return render_template("home.html")

@app.route("/schedule", methods=["GET", "POST"])
@login_required
def schedule():
    if request.method == "POST":
        comunication = request.form.get("radio-98")
        day_pref = request.form.getlist("checkbox-465")
        time_pref = request.form.getlist("checkbox-246")
        text = request.form.get("textarea-398")
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#inserting to database

        db.execute("INSERT INTO appointment (id, comunication, day_pref, time_pref, text, time ) VALUES (:id, :comunication, :day_pref, :time_pref, :text, :time )", id = session["user_id"] , comunication= comunication, day_pref=day_pref  , time_pref=time_pref  , text=text, time=time)

        print(comunication , day_pref , time_pref, text )
        return render_template("confirmation.html")

    else:
        return render_template("schedule.html")

@app.route("/mail", methods=["GET", "POST"])
def mails():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD )

        subject = 'Check out Bronx as a puppy!'
        body = 'how about getting beer at 6am'

        msg = f'Subject: {subject} \n \n {body}'
        server.sendmail(EMAIL_ADDRESS, 'tomasmolcan25@icloud.com', msg )

        print(name, email, subject, message)

    else:
        return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
# Query database for username
        message4 = "Incorrect username or password, please try again"
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", message = message4 )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        print(session["user_id"] )

        if session["user_id"]==33:
            return redirect("p_app")


        else:
            # Redirect user to home page
            message5 = "You have successfully logged in :)"
            return render_template("home.html", message=message5)

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password1 = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256')
        confirmpassword = request.form.get("confirmpassword")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        number = request.form.get("number")
        message = "Please make sure all the fields are entered correctly"
        message1 = "User already exists, please try again."
        message2 = "Password confirmation doesn't match password, please try again."
        message3 = "You have successfully registered and logged in :)"

        # Ensure username was submitted
        if (not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmpassword")
            or not request.form.get("firstname") or not request.form.get("lastname")
            or not request.form.get("email") or not request.form.get("number") ):
            return render_template("register.html", message=message, username = username, password=password ,confirmpassword=confirmpassword,firstname=firstname, lastname=lastname,email=email,number=number   )

        elif  request.form.get("password") != confirmpassword :
            return render_template("register.html", message=message2, username = username, password=password ,confirmpassword=confirmpassword,firstname=firstname, lastname=lastname,email=email,number=number  )

        else:
            rows = db.execute("SELECT * FROM users")
            for row in rows:
                if username == row["username"]:
                    return render_template("register.html", message=message1, username = username, password=password ,confirmpassword=confirmpassword,firstname=firstname, lastname=lastname,email=email,number=number  )
            else:
                db.execute("INSERT INTO users (username, hash, first_name, last_name, email, tel_number ) VALUES(:username, :hash, :first_name, :last_name, :email, :tel_number)", username = username, hash=password1 ,first_name=firstname, last_name=lastname,email=email,tel_number=number)
                rowz = db.execute("SELECT * FROM users WHERE username = :username", username=username )

                session["user_id"] = rowz[0]["id"]
                return render_template("home.html", message=message3)

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        return render_template("register.html")

@app.route("/myrequests" )
@login_required
def myrequests():

    table = db.execute("SELECT * FROM appointment WHERE id = :id ORDER BY time DESC;", id = session["user_id"])
    return render_template("myrequests.html", table=table)

@app.route("/tips" )
def tips():
    return render_template("tips.html")

@app.route("/logout" )
def logout():
    session.clear()
    return render_template("home.html")

@app.route("/p_app", methods = ["GET", "POST"])
@login_required
def p_app ():
    if request.method == "GET":
        active = db.execute("SELECT * FROM users JOIN appointment ON users.id = appointment.id WHERE handeled = 'false' ; ")
        return render_template("p_app.html", active=active )



    else:
        global data
        data = request.form.get('Data')

       # jsdata = request.form['Data']

        print(data)

    return redirect("/details")




@app.route("/details", methods = ["GET", "POST"])
@login_required
def details ():
    if request.method == "GET":
        showDetails = db.execute("SELECT * FROM users JOIN appointment ON users.id = appointment.id WHERE tel_number = :tel_number ",tel_number = data)
        return render_template("details.html", showDetails=showDetails)
    else:
        db.execute("UPDATE appointment SET handeled= 'true'  WHERE id IN  (SELECT id FROM users  WHERE tel_number = :tel_number);",tel_number = data)
        return redirect("/p_app")

@app.route("/h_app", methods = ["GET", "POST"])
@login_required
def h_app ():
    if request.method == "GET":
        handeled = db.execute("SELECT * FROM users JOIN appointment ON users.id = appointment.id WHERE handeled = 'true' ; ")
        return render_template("h_app.html",handeled=handeled)
    else:
        db.execute("DELETE FROM appointment WHERE handeled = 'true' ; ")
        message = "Handeled appoitment requests have been succesfully deleted from list."
        return render_template("/h_app.html", message = message)