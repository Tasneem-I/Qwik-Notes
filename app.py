from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_session import Session
from sqlalchemy import func
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = 'jauh&y9ojlvgfrASRDTFY9Y'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable= False)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable = False)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable= False)
    content = db.Column(db.String(3000))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

db.init_app(app)
with app.app_context():
    db.create_all()