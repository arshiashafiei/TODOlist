from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.password}')"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/succes" , methods=["POST"])
def succes():
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
    return render_template("succes.html")


@app.route("/dashboard", methods=["POST"])
def dashboard():
    email = request.form.get("email")
    userpass = request.form.get("password")
    if not email or not userpass:
        return render_template("failure.html")
    user_check = User.query.filter_by(email=email).first()
    if user_check == None:
        return render_template("failure.html")
    if not check_password_hash(user_check.password, userpass):
        return render_template("failure.html")
    return render_template("dashboard.html")