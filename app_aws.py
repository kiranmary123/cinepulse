from flask import Flask, request, redirect, url_for, session
from functools import wraps
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = "cinemapulse-secret-key"

# ---------- AWS CONFIG ----------
REGION = "us-east-1"

dynamodb = boto3.resource("dynamodb", region_name=REGION)
sns = boto3.client("sns", region_name=REGION)

# ---------- DynamoDB Tables ----------
users_table = dynamodb.Table("Users")
admin_users_table = dynamodb.Table("AdminUsers")
projects_table = dynamodb.Table("Projects")
enrollments_table = dynamodb.Table("Enrollments")

# ---------- SNS Topic ARN ----------
# Will be injected by test_app_aws.py
SNS_TOPIC_ARN = None


def send_notification(subject, message):
    if not SNS_TOPIC_ARN:
        return
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
    except ClientError as e:
        print(e)


# ---------- Admin Credentials ----------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ---------- Login Required Decorator ----------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


# ---------- Routes ----------
@app.route("/")
def index():
    return "✅ CinePulse is running successfully!"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (
            request.form.get("username") == ADMIN_USERNAME
            and request.form.get("password") == ADMIN_PASSWORD
        ):
            session["username"] = ADMIN_USERNAME
            send_notification("Admin Login", "Admin logged in successfully")
            return redirect(url_for("dashboard"))

        return "❌ Invalid credentials", 401

    return """
        <h2>Login</h2>
        <form method="post">
            <input name="username" placeholder="username"><br><br>
            <input name="password" type="password" placeholder="password"><br><br>
            <button type="submit">Login</button>
        </form>
    """


@app.route("/dashboard")
@login_required
def dashboard():
    return "🎉 Welcome to CinePulse Dashboard"


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
