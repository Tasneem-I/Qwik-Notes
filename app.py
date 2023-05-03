from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
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

class User(UserMixin, db.Model):
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

db.init_app(app)
with app.app_context():
    db.create_all()

@login_manager.user_loader
def user_load(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        user = User(username=username, name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return render_template("login.html")
    else:
        return render_template("signup.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email = request.form.get("email")).first()
        if user.password == request.form.get("password"):
            login_user()
            return redirect(url_for("dashboard"))
    else:
        return render_template("login.html")
    

@app.route("/dashboard", methods= ["GET", "POST"])
def dash():
    return render_template("dashboard.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        user= current_user()
        todo = Todo(title = request.form.get("title"), content = request.form.get("content"), user_id = user.id)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("todos"))
    else:
        todos = Todo.query.filter_by(user_id = current_user.id)
        return render_template("todos.html", todos = todos)

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    task = Todo.query.filter_by(user_id = current_user.id, id = id)
    db.session.delete(id)
    db.session.commit()
    return render_template('todos.html')

if __name__ == "__main__":
    app.run(debug=True)
