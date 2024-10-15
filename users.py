from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import secrets
import blogs as blog_db
import logging

def create_account(username, password):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user:
        print("user found")
        return False

    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password) RETURNING id")
        result = db.session.execute(sql, {"username":username, "password":hash_value})
        user_id = result.fetchone()[0]
        db.session.commit()

        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        session["id"] = user_id
        
        return True
    except:
        print("error creating account")
        return False
    

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        return False
    
    if check_password_hash(user.password, password):
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        session["id"] = user.id
        return True
    return False

def logout():
    del session["username"]
    del session["csrf_token"]
    del session["id"]

def delete_account():
    try:
        user_id = session["id"]

        sql = text("SELECT id FROM blogs WHERE user_id = :user_id")
        blogs = db.session.execute(sql, {"user_id": user_id}).fetchall()

        for blog in blogs:
            blog_db.delete_blog(blog.id)

        sql = text("DELETE FROM likes WHERE user_id = :user_id")
        db.session.execute(sql, {"user_id": user_id})

        sql = text("DELETE FROM users WHERE id = :user_id")
        db.session.execute(sql, {"user_id": user_id})

        db.session.commit()
        return True

    except Exception as e:
        logging.error(f"Error deleting account for user {user_id}: {e}")
        return False