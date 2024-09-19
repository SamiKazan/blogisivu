from flask_sqlalchemy import SQLAlchemy
from app import app
import psycopg2

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"

db = SQLAlchemy(app)