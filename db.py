from flask_sqlalchemy import SQLAlchemy
from app import app
import psycopg2
from os import getenv

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)

from models import User, Blog, Like, Comment, Draft

with app.app_context():
    db.create_all()