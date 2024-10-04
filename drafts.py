from flask import session
from sqlalchemy.sql import text
from db import db
import logging

#inserts new blog into blogs table
def create_draft(genre, title, content):
    try:
        sql = text("INSERT INTO drafts (user_id, title, genre, content, created_at) VALUES (:user_id, :title, :genre, :content, NOW())")
        
        db.session.execute(sql, {
            "user_id": session["id"],
            "title": title,
            "genre": genre,
            "content": content
        })
        db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Error saving draft blog: {e}")
        return False
    

def own_drafts():
    try:
        user_id = session.get("id")
        if not user_id:
            logging.error("User not logged in")
            return []

        sql = text("SELECT * FROM drafts WHERE user_id = :user_id")
        result = db.session.execute(sql, {"user_id": user_id})
        blogs = result.fetchall()
        return blogs
    
    except Exception as e:
        logging.error(f"Error fetching drafts: {e}")
        return []
    
def delete_draft(draft_id):
    try:
        # Check if blog exists and get the user_id
        sql = text("SELECT user_id FROM drafts WHERE id = :draft_id")
        result = db.session.execute(sql, {"draft_id": draft_id}).fetchone()

        user_id = result[0]

        # Check if the current user is the owner of the draft
        if user_id != session["id"]:
            return False

        # Delete the draft
        sql = text("DELETE FROM drafts WHERE id = :draft_id")
        db.session.execute(sql, {"draft_id": draft_id})
        db.session.commit()
        return True

    except Exception as e:
        logging.error(f"Error deleting blog {draft_id}: {e}")
        return False