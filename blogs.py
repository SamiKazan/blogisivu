from flask import session
from sqlalchemy.sql import text
from db import db
import logging
from utils import sanitizer

#inserts new blog into blogs table
def create_blog(title, content):
    try:
        safe_content = sanitizer.sanitize_and_convert_newlines(content)
        sql = text("INSERT INTO blogs (user_id, username, title, content, uploaded_at) VALUES (:user_id, :username, :title, :content, NOW())")
        
        db.session.execute(sql, {
            "user_id": session["id"],
            "username": session["username"],
            "title": title,
            "content": safe_content
        })
        db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Error creating blog: {e}")
        return False


def get_all_blogs():
    try:
        sql = text("SELECT * FROM blogs")
        result = db.session.execute(sql)
        blogs = result.fetchall()
        return blogs
    except Exception as e:
        logging.error(f"Error fetching blogs: {e}")
        return []


def get_blog_by_id(id):
    try:
        sql = text("SELECT * from blogs WHERE id =:id")
        result = db.session.execute(sql, {"id": id})
        blog = result.fetchone()
        return blog
    except Exception as e:
        logging.error(f"Error fetching blog by id: {e}")
        return None


def own_blogs():
    try:
        user_id = session.get("id")
        if not user_id:
            logging.error("User not logged in")
            return []

        sql = text("SELECT * FROM blogs WHERE user_id = :user_id")
        result = db.session.execute(sql, {"user_id": user_id})
        blogs = result.fetchall()
        return blogs
    except Exception as e:
        logging.error(f"Error fetching own blogs: {e}")
        return []
    

def comment_blog(content, blog_id):
    try:
        sql = text("INSERT INTO comments (user_id, username, blog_id, content, sent_at) VALUES (:user_id, :username, :blog_id, :content, NOW())")

        db.session.execute(sql, {
            "user_id": session["id"],
            "username": session["username"],
            "blog_id": blog_id,
            "content": content
        })
        db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Error commenting on blog:{e}")
        return
    

def get_comments(blog_id):
    try:
        sql = text("SELECT id, content, username, user_id, sent_at FROM comments WHERE blog_id = :blog_id")
        result = db.session.execute(sql, {"blog_id": blog_id})
        comments = result.fetchall()
        return comments
    
    except Exception as e:
        logging.error(f"Error fetching comments for blog {blog_id}: {e}")
        return []
    

def like_blog(blog_id):
    user_id = session["id"]
    try:
        #check if user already liked blog
        sql_check = text("SELECT COUNT(*) FROM likes WHERE user_id = :user_id AND blog_id = :blog_id")
        result = db.session.execute(sql_check, {"user_id": user_id, "blog_id": blog_id}).scalar()
        if result > 0:
            return False

        sql = text("INSERT INTO likes (user_id, blog_id) VALUES (:user_id, :blog_id)")

        db.session.execute(sql, {
            "user_id": session["id"],
            "blog_id": blog_id,
        })
        db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Error liking on blog:{e}")
        return
    

def get_likes(blog_id):
    try:
        sql = text("SELECT COUNT(user_id) FROM likes WHERE blog_id = :blog_id")
        result = db.session.execute(sql, {"blog_id": blog_id})
        likes = result.fetchone()
        return likes[0]
    
    except Exception as e:
        logging.error(f"Error fetching comments for blog {blog_id}: {e}")
        return []
    
def delete_comment(comment_id):
    try:
        # Check if the comment exists and get the user_id
        sql = text("SELECT user_id FROM comments WHERE id = :comment_id")
        result = db.session.execute(sql, {"comment_id": comment_id}).fetchone()

        user_id = result[0]

        # Check if the current user is the owner of the comment
        if user_id != session["id"]:
            return False

        # Delete the comment
        sql = text("DELETE FROM comments WHERE id = :comment_id")
        db.session.execute(sql, {"comment_id": comment_id})
        db.session.commit()
        return True

    except Exception as e:
        logging.error(f"Error deleting comment {comment_id}: {e}")
        return False


def delete_blog(blog_id):
    try:
        # Check if blog exists and get the user_id
        sql = text("SELECT user_id FROM blogs WHERE id = :blog_id")
        result = db.session.execute(sql, {"blog_id": blog_id}).fetchone()

        user_id = result[0]

        # Check if the current user is the owner of the blog
        if user_id != session["id"]:
            return False
        
        # Delete all comments associated with the blog
        sql = text("DELETE FROM comments WHERE blog_id = :blog_id")
        db.session.execute(sql, {"blog_id": blog_id})

        # Delete all likes associated with the blog
        sql = text("DELETE FROM likes WHERE blog_id = :blog_id")
        db.session.execute(sql, {"blog_id": blog_id})

        # Delete the blog
        sql = text("DELETE FROM blogs WHERE id = :blog_id")
        db.session.execute(sql, {"blog_id": blog_id})
        db.session.commit()
        return True

    except Exception as e:
        logging.error(f"Error deleting blog {blog_id}: {e}")
        return False
        

def delete_account():
    try:
        user_id = session["id"]

        sql = text("SELECT * FROM blogs WHERE user_id = :user_id")
        blogs = db.session.execute(sql, {"user_id": user_id}).fetchall()

        for i in blogs:
            delete_blog(i.id)

        sql = text("DELETE FROM likes WHERE id = :user_id")
        db.session.execute(sql, {"user_id": user_id})

        sql = text("DELETE FROM users WHERE id = :user_id")
        db.session.execute(sql, {"user_id": user_id})



        db.session.commit()
        return True

    except Exception as e:
        logging.error(f"Error deleting account for user {user_id}: {e}")
        return False
    

def get_most_liked_blog():
    try:
        sql = text("""
            SELECT b.*, COUNT(l.user_id) as like_count
            FROM blogs b
            LEFT JOIN likes l ON b.id = l.blog_id
            GROUP BY b.id
            ORDER BY like_count DESC
            LIMIT 1
        """)
        result = db.session.execute(sql)
        blog = result.fetchone()
        return blog
    except Exception as e:
        logging.error(f"Error fetching most liked blog: {e}")
        return None


def liked_blogs():
    try:
        user_id = session["id"]

        sql = text("""
            SELECT b.*
            FROM blogs b
            JOIN likes l ON b.id = l.blog_id
            WHERE l.user_id = :user_id
        """)
        result = db.session.execute(sql, {"user_id": user_id})
        blogs = result.fetchall()
        return blogs

    except Exception as e:
        logging.error(f"Error fetching liked blogs: {e}")
        return None