from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "cinemapulse-secret-key"

# Temporary in-memory storage
feedbacks = []

# Credentials
USER_USERNAME = "kiran"
USER_PASSWORD = "cinema"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ---------- Decorators ----------
def user_login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return wrapper

def admin_login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapper

# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if (
        request.form["username"] == USER_USERNAME
        and request.form["password"] == USER_PASSWORD
    ):
        session["user"] = USER_USERNAME
        return redirect(url_for("dashboard"))
    return redirect(url_for("index"))

@app.route("/dashboard")
@user_login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/feedback", methods=["GET", "POST"])
@user_login_required
def feedback():

    movies = [
        "Leo 2",
        "Kantara Chapter 1",
        "Game Changer",
        "Salaar Part 2",
        "Pushpa 2",
        "Jailer 2",
        "Kalki 2898 AD",
        "Indian 2",
        "Vikram 2"
    ]

    theatres = ["PVR", "INOX", "AGS", "SPI"]

    if request.method == "POST":
        feedbacks.append({
            "movie": request.form["movie"],
            "theatre": request.form["theatre"],
            "rating": request.form["rating"],
            "feedback": request.form["feedback"]
        })
        return redirect(url_for("dashboard"))

    return render_template(
        "feedback.html",
        movies=movies,
        theatres=theatres
    )

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if (
            request.form["username"] == ADMIN_USERNAME
            and request.form["password"] == ADMIN_PASSWORD
        ):
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
@admin_login_required
def admin_dashboard():
    return render_template("admin_dashboard.html", feedbacks=feedbacks)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
