from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/dashboard", methods=["POST"])
def dashboard():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return render_template("failure.html")
    return render_template("dashboard.html")