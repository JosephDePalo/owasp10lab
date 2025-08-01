import subprocess
from hashlib import sha256
import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    make_response,
)
from flask_sqlalchemy import SQLAlchemy
import jwt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.secret_key = "73151537-033e-4ad1-8c71-5d14d57c6dc0"
db = SQLAlchemy(app)


def generate_jwt(identity):
    payload = {
        "id": identity,
        "iat": datetime.datetime.now(),
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=30),
    }
    return jwt.encode(payload, key=None, algorithm="none")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __init__(self, username: str):
        self.username = username

    def set_password(self, password: str):
        self.password_hash = sha256(password.encode("utf-8")).hexdigest()

    def check_password(self, password: str) -> bool:
        hash_to_test = sha256(password.encode("utf-8")).hexdigest()
        return hash_to_test == self.password_hash


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
            resp = make_response(redirect(f"/dashboard/{user.id}"))
            token = generate_jwt(user.id)
            resp.set_cookie("access_token", token)
            return resp
        else:
            flash("Invalid credentials!")
            return render_template("login.html")
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


@app.route("/dashboard/<int:id>", methods=["GET", "POST"])
def dashboard(id: int):
    user = User.query.get_or_404(id)

    token = request.cookies.get("access_token")
    if not token:
        return "No access_token provided.", 401
    token_payload = jwt.decode(token, options={"verify_signature": False})
    if token_payload.get("id", -1) != id:
        return "Unauthorized", 401

    if request.method == "POST":
        if id == 1:
            cmd = request.form["Command"]
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True
            )
            flash(result.stdout)
            flash(result.stderr)
            return render_template("admin_dashboard.html", user=user)

    if id == 1:
        return render_template("admin_dashboard.html", user=user)
    return render_template("dashboard.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
