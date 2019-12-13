from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from timehelper import Time
from helpers import apology, login_required
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

today = datetime.date.today()
# today = datetime.date(2019,12,9)
last_sunday = today - datetime.timedelta(days=today.weekday())
coming_saturday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
# print(today)
idx = (today.weekday()+1) % 7 # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
# print(idx)
sun = today - datetime.timedelta(idx)
mon = today - datetime.timedelta(idx-1)
tue = today - datetime.timedelta(idx-2)
wed = today - datetime.timedelta(idx-3)
thu = today - datetime.timedelta(idx-4)
fri = today - datetime.timedelta(idx-5)
sat = today - datetime.timedelta(idx-6)


# Configure application
app = Flask(__name__)
app.config[ 'DEBUG' ] = True

# Configure database

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cs50x:cs50x@localhost:8889/40hr'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Ensure responses aren't cached

class User( db.Model ):
  id = db.Column( db.Integer, primary_key = True )
  username = db.Column( db.String(100))
  password = db.Column( db.String(100))

  def __init__(self, username,password):
    self.username = username
    self.password = password

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():
    """Show user dashboard and current week"""
    days = [ sun,mon,tue,wed,thu,fri,sat ]
    timehead = ["DATE","IN DAY", "OUT LUNCH", "IN LUNCH", "OUT DAY", "TOTAL"]
    return render_template("index.html", days = days, timehead = timehead)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # hash the password and insert a new user in the database
        clave = generate_password_hash(request.form.get("password"), method='sha256')
        new_user_id = User(username=request.form.get("username"),password=clave)
        
        # unique username constraint violated?
        ####this is not working properly
        if not new_user_id:
            return apology("username taken", 400)

        # Remember which user has logged in and save it to db
        session["user_id"] = new_user_id
        db.session.add(new_user_id)
        db.session.commit()
        # Display a flash message
        flash("Registered!")

        # Redirect user to home page
        return redirect(url_for("user"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

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
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user.password, password): 
            flash('Please check your login details and try again.')
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session['user_id'] = user
        usuario = session['user_id']

        # Redirect user to home page
        return redirect(url_for("user", user=usuario))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("index"))

@app.route("/user")
@login_required
def user():
    """Show user dashboard""" 
    usuario = session['user_id']
    return render_template("user.html",user=usuario)

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

@app.context_processor
def inject_today_date():
    return {'today_date': datetime.date.today()}


if __name__ == "__main__":
  app.run()