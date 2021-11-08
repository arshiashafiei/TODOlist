from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        userpass = request.form.get("password")
        user_check = User.query.filter_by(email=email).first()
        if not email or not userpass or user_check == None or not check_password_hash(user_check.password, userpass):
            return render_template("failure.html")
        session["email"] = email
        return redirect("/dashboard")
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        hash = generate_password_hash(password)
        user_check = User.query.filter_by(email=email).first()
        if not email or not password or not name or user_check != None:
            return render_template("failure.html")
        u = User(name=name, email=email, password=hash)
        db.session.add(u)
        db.session.commit()
        return render_template("login.html", name=name)
    return render_template("signup.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect("/")
