from app import app
from flask import render_template, request, redirect, session, abort
import users
import blogs
import drafts


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
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        genre = request.form["genre"]
        title = request.form["title"]
        content = request.form["content"]
        action = request.form["action"]

        if not title or not content:
            return render_template("create_blog.html", error="Title and content are required")
        if len(title) > 100:
            return render_template("create_blog.html", error="Title is too long (max 100 characters)")
        if len(content) > 5000:
            return render_template("create_blog.html", error="Content is too long (max 5000 characters)")
        
        if action == "blog":
            if blogs.create_blog(genre, title, content):
                return redirect("/my_blogs")
            
        if action == "draft":
            if drafts.create_draft(genre, title, content):
                return redirect("my_drafts")
            
        return render_template("create_blog.html", error="Error creating blog")


#returns all blogs page
@app.route("/all_blogs")
def all_blogs():
    all_blogs = blogs.get_all_blogs()
    return render_template("all_blogs.html", blogs=all_blogs)


#returns spesific blog
@app.route("/blog/<int:id>")
def blog(id):
    blog_data = blogs.get_blog_by_id(id)
    comment_data = blogs.get_comments(id)
    likes_data = blogs.get_likes(id)
    current_user = session["id"]

    if blog_data:
        return render_template("blog.html", blog=blog_data, comments=comment_data, 
                               likes=likes_data, current_user=current_user)
    else:
        return render_template("index.html", error="Blog not found")

#returns users' blogs
@app.route("/my_blogs")
def my_blogs():
    own_blogs = blogs.own_blogs()
    current_user = session["id"]
    return render_template("my_blogs.html", blogs=own_blogs, current_user=current_user)

#returns user profile
@app.route("/profile")
def profile():
    own_blogs = blogs.own_blogs()
    current_user = session["id"]

    return render_template("profile.html", blogs=own_blogs, current_user=current_user)


#comment on specific blog
@app.route("/comment_blog", methods=["POST"])
def comment_blog():
    blog_id = request.form["blog_id"]
    comment = request.form["comment"]

    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

    if blogs.comment_blog(comment, blog_id):
        return redirect(f"/blog/{blog_id}")
    return "Failed to comment"


#like specific blog
@app.route("/like_blog", methods=["POST"])
def like_blog():
    blog_id = request.form["blog_id"]

    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

    if blogs.like_blog(blog_id):
        return redirect(f"/blog/{blog_id}")
    
    blog_data = blogs.get_blog_by_id(blog_id)
    comment_data = blogs.get_comments(blog_id)
    likes_data = blogs.get_likes(blog_id)
    current_user = session["id"]
    
    return render_template("blog.html", blog=blog_data, comments=comment_data, likes=likes_data, 
                           error="You have already liked this blog", current_user=current_user)


#deletes comment from blog
@app.route("/delete_comment", methods=["POST"])
def delete_comment():
    comment_id = request.form["comment_id"]
    blog_id = request.form["blog_id"]
    
    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
    
    if blogs.delete_comment(comment_id):
        return redirect(f"/blog/{blog_id}")
    return "Failed to delete comment", 400
    

#delete users' blog
@app.route("/delete_blog", methods=["POST"])
def delete_blog():
    blog_id = request.form["blog_id"]
    
    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
    
    if blogs.delete_blog(blog_id):
        return redirect(f"/my_blogs")
    return "Failed to delete blog", 400


#deletes users' account
@app.route("/delete_account", methods=["POST"])
def delete_account():
    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

    if blogs.delete_account():
        logout()
    return "Failed to delete account", 400

#returns users' drafts
@app.route("/my_drafts")
def my_drafts():
    own_drafts = drafts.own_drafts()
    current_user = session["id"]
    return render_template("my_drafts.html", drafts=own_drafts, current_user=current_user)


#delete users' drafts
@app.route("/delete_draft", methods=["POST"])
def delete_draft():
    draft_id = request.form["draft_id"]
    
    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
    
    if drafts.delete_draft(draft_id):
        return redirect(f"/my_drafts")
    return "Failed to delete draft", 400


