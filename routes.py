from app import app
from flask import render_template, request, redirect, session, abort
import users
import blogs
import drafts


#returns to main page
@app.route("/")
def index():
    most_liked_blog = blogs.get_most_liked_blog()
    return render_template("index.html", most_liked_blog=most_liked_blog)


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
            return render_template("create_account.html", error="Invalid username (must be between 3-20 charecters)")
        
        if len(password) > 50:
            return render_template("create_account.html", error="Password must be less than 50 characters")
        
        if len(password) < 5:
            return render_template("create_account.html", error="Password must be atleast 5 characters long")
        
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

        title = request.form["title"]
        content = request.form["content"]
        action = request.form["action"]

        if not title or not content:
            return render_template("create_blog.html", error="Title and content are required")
        if len(title) > 40:
            return render_template("create_blog.html", error="Title is too long (max 100 characters)")
        if len(content) > 4000:
            return render_template("create_blog.html", error="Content is too long (max 5000 characters)")
        
        if action == "post blog":
            if blogs.create_blog(title, content):
                return redirect("/my_blogs")
            
        if action == "create draft":
            if drafts.create_draft(title, content):
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

    #vois lisää että kommentti on max 100 merkkiä ja oikee returni jos failaa
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

    if users.delete_account():
        session.clear()
        return redirect("/")
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


#returns spesific draft
@app.route("/my_drafts/<int:id>")
def draft(id):
    try:
        draft_data = drafts.get_draft_by_id(id)
        current_user = session["id"]
        print(draft_data, "draft")

        if draft_data:
            return render_template("edit_draft.html", draft=draft_data, current_user=current_user)
        else:
            return render_template("index.html", error="Draft not found")
    except Exception as e:
        return render_template("index.html", error="An error occurred while fetching the draft")
    

#edits draft and returns my_drafts
@app.route("/edit_draft", methods=["POST"])
def edit_draft():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    title = request.form["title"]
    content = request.form["content"]
    draft_id = request.form["draft_id"]

    if not title or not content:
        return render_template("create_blog.html", error="Title and content are required")
    if len(title) > 40:
        return render_template("create_blog.html", error="Title is too long (max 100 characters)")
    if len(content) > 4000:
        return render_template("create_blog.html", error="Content is too long (max 5000 characters)")
    
    if drafts.edit_draft(title, content, draft_id):
        return redirect("my_drafts")
        
    return render_template("create_blog.html", error="Error editing blog")

@app.route("/post_draft/<int:id>", methods=["POST"])
def post_draft(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    draft_data = drafts.get_draft_by_id(id)

    if blogs.create_blog(draft_data.title, draft_data.content):
        drafts.delete_draft(id)
        own_blogs = blogs.own_blogs()
        current_user = session["id"]
        return render_template("my_blogs.html", blogs=own_blogs, current_user=current_user)
        
    return render_template("my_drafts", error="Error creating blog from draft")


@app.route("/liked_blogs", methods=["GET"])
def liked_blogs():
    liked_blogs = blogs.liked_blogs()
    current_user = session["id"]

    if blogs.liked_blogs():
        return render_template("liked_blogs.html", blogs=liked_blogs, current_user=current_user)
    
    return render_template("liked_blogs.html", blogs=[], current_user=current_user)