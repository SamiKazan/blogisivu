from flask import session
from sqlalchemy.sql import text
from db import db
import logging

#inserts new blog into blogs table
def create_blog(genre, title, content):
    try:
        sql = text("INSERT INTO blogs (user_id, title, genre, content, uploaded_at) VALUES (:user_id, :title, :genre, :content, NOW())")
        
        db.session.execute(sql, {
            "user_id": session["id"],
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