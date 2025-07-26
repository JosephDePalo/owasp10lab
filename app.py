from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.secret_key = "73151537-033e-4ad1-8c71-5d14d57c6dc0"
db = SQLAlchemy(app)

ph = PasswordHasher()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __init__(self, username: str):
        self.username = username

    def set_password(self, password: str):
        self.password_hash = ph.hash(password)

    def check_password(self, password: str) -> bool:
        try:
            return ph.verify(self.password_hash, password)
        except Exception:
            return False


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return redirect(f"/dashboard/{user.id}")
        else:
            return "Invalid username or password", 401
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]

        if User.query.filter_by(username=username).first():
            flash("Username already taken")
            return redirect("/register")

        user = User(username=username)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Registration as '{username}' successful!")
            return redirect("/login")
        except Exception as e:
            return f"Error creating user: {e}", 500
    else:
        return render_template("register.html")


@app.route("/dashboard/<int:id>")
def dashboard(id: int):
    user = User.query.get_or_404(id)
    return render_template("dashboard.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
