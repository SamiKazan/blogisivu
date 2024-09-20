from app import app
from flask import render_template, request, redirect
import users
import blogs

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

#returns crate_blog page
#creates blog and returns blogpage
@app.route("/create_blog", methods=["GET", "POST"])
def create_blog():
    if request.method == 'GET':
        return render_template("create_blog.html")

    if request.method == 'POST':
        genre = request.form["genre"]
        title = request.form["title"]
        content = request.form["content"]

        if not title or not content:
            return render_template("create_blog.html", error="Title and content are required")
        if len(title) > 100:
            return render_template("create_blog.html", error="Title is too long (max 100 characters)")
        if len(content) > 5000:
            return render_template("create_blog.html", error="Content is too long (max 5000 characters)")
        
        if blogs.create_blog(genre, title, content):
            return redirect("/all_blogs")
        return render_template("create_blog.html", error="Error creating blog")


@app.route("/all_blogs")
def all_blogs():
    all_blogs = blogs.get_all_blogs()
    return render_template("all_blogs.html", blogs=all_blogs)


@app.route("/profile/<int:id>")
def profile(id):
    pass