from app import app
from flask import render_template, request

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_account")
def create_account():
    return render_template("create_account.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")