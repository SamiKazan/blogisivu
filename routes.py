from app import app
from flask import render_template, request, redirect
import users

#returns to main page
@app.route("/")
def index():
    return render_template("index.html")

#returns to create_account page
#returns to main page if account is created
@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == 'GET':
        return render_template("create_account.html")
    
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        if len(username) < 3 or len(username) > 20:
            return render_template("create_account.html", error="Invalid username (must be between 3-50 charecters)")
        
        if len(password) > 50:
            return render_template("create_account.html", error="Invalid password (too long)")
        
        if users.create_account(username, password):
            return redirect("/")
        return render_template("create_account.html", error="Username is already taken")


#returns to login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        if users.login(username, password):
            return redirect("/")
        return render_template("login.html", error="Invalid username or password")

#logs out user and returns to main page
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")