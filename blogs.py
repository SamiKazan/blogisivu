from flask import session
from sqlalchemy.sql import text
from db import db
import logging

#inserts new blog into blogs table
def create_blog(genre, title, content):
    try:
        sql = text("INSERT INTO blogs (user_id, username, title, genre, content, uploaded_at) VALUES (:user_id, :username, :title, :genre, :content, NOW())")
        
        db.session.execute(sql, {
            "user_id": session["id"],
            "username": session["username"],
            "title": title,
            "genre": genre,
            "content": content
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
        sql = text("SELECT content, username, sent_at FROM comments WHERE blog_id = :blog_id")
        result = db.session.execute(sql, {"blog_id": blog_id})
        comments = result.fetchall()
        return comments
    
    except Exception as e:
        logging.error(f"Error fetching comments for blog {blog_id}: {e}")
        return []