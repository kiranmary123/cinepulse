from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import uuid
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = "cinemapulse-secret-key"

# ---------- AWS CONFIG ----------
REGION = "us-east-1"
ENDPOINT = "http://localhost:4566"  # Use AWS endpoint or LocalStack for testing

# DynamoDB Resource
dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION,
    endpoint_url=ENDPOINT,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# SNS Client
sns = boto3.client(
    "sns",
    region_name=REGION,
    endpoint_url=ENDPOINT,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# Tables
users_table = dynamodb.Table("Users")
feedback_table = dynamodb.Table("Feedbacks")

# SNS Topic ARN (replace with your topic ARN)
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:000000000000:UserLoginTopic"

# ---------- Admin Credentials ----------
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

# ---------- SNS Notification Helper ----------
def send_notification(subject, message):
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
    except ClientError as e:
        print(f"Error sending SNS notification: {e}")

# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Fetch user from DynamoDB
    res = users_table.get_item(Key={"username": username})
    if "Item" in res and res["Item"]["password"] == password:
        session["user"] = username

        # SNS notification for login
        send_notification(
            "User Login",
            f"User '{username}' has logged in successfully."
        )

        return redirect(url_for("dashboard"))

    return redirect(url_for("index"))

@app.route("/dashboard")
@user_login_required
def dashboard():
    return render_template("dashboard.html", user=session.get("user"))

@app.route("/feedback", methods=["GET", "POST"])
@user_login_required
def feedback():
    movies = [
        "Leo 2", "Kantara Chapter 1", "Game Changer",
        "Salaar Part 2", "Pushpa 2", "Jailer 2",
        "Kalki 2898 AD", "Indian 2", "Vikram 2"
    ]
    theatres = ["PVR", "INOX", "AGS", "SPI"]

    if request.method == "POST":
        feedback_table.put_item(
            Item={
                "id": str(uuid.uuid4()),
                "username": session["user"],
                "movie": request.form["movie"],
                "theatre": request.form["theatre"],
                "rating": request.form["rating"],
                "feedback": request.form["feedback"]
            }
        )
        return redirect(url_for("dashboard"))

    return render_template("feedback.html", movies=movies, theatres=theatres)

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
@admin_login_required
def admin_dashboard():
    res = feedback_table.scan()
    feedbacks = res.get("Items", [])
    return render_template("admin_dashboard.html", feedbacks=feedbacks)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ---------- Main ----------
if __name__ == "__main__":
    app.run(debug=True)
