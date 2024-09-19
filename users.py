from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import secrets

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
        print("error")
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