import os
import requests

from flask import Flask, session
from flask import Flask, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods = ["POST"])
def singin():

    usuario = request.form.get("username")
    password = request.form.get("password")

    usuid = db.execute("SELECT * FROM credential WHERE usuario = :usuario",{"usuario":usuario}).fetchone()
    
    match = usuid[1]
    user_id = usuid[0]



    if password==match:

        return render_template("session.html",username=user_id)

    else:
        error = "Contraseña Incorrecta"
        return render_template ("index.html",error=error)
    
    if usuario=="" or password=="":
        error = "Please fill all the fields"
        return render_template ("index.html", error=error)

@app.route("/session", methods=["GET","POST"])
def session():

    isbn = request.form.get("isbn")
    title = request.form.get("isbn")
    author = request.form.get("isbn")
    
    infor = db.execute("SELECT * FROM books WHERE isbn ILIKE :isbn OR title ILIKE :isbn OR author ILIKE :isbn ",{"isbn":"%" +isbn+ "%","isbn":"%" +title+ "%","isbn":"%" +author+ "%"}).fetchall()

    return render_template("session.html",infor=infor)

@app.route("/details", methods=["GET","POST"])
def details():

    isbn = request.form.get("isbne")

    bdata = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "3FnYpHAxIdxiyCY6f1Ekw", "isbns": isbn})
    grvw = res.json()
    rvw_avg = grvw["books"][0]["average_rating"]
    
    return render_template("books.html", bdata=bdata,rvw_avg=rvw_avg)

@app.route("/registration")
def register():
    return render_template("register.html")

@app.route("/registration", methods = ["POST"])
def registration():

    usuario = request.form.get("regname")
    password = request.form.get("regpass")
    cpassword = request.form.get("cregpass")
    
    if usuario=="" or password=="" or cpassword=="":
        error = 'Please type all fields'
        return render_template("register.html",error=error)
    elif password==cpassword:
        result = db.execute("SELECT * FROM credential WHERE usuario = :usuario",{"usuario":usuario}).fetchone()
        if result is None:
            db.execute("INSERT INTO credential (usuario, password) VALUES (:usuario, :password)",{"usuario": usuario,"password": password})
            db.commit()
            return render_template("register.html")
        else:
            error = "User already exist"
            return render_template("register.html",error=error)
    else:
        error = 'Both password should match'
        return render_template("register.html",error=error)


