import io
from flask import Flask, request, jsonify, render_template, session, send_file, redirect, url_for
import pyotp
import qrcode
import io
import os
import stripe
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, LoginLog
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram, Gauge
from flask_mail import Mail, Message
from email_service import send_welcome_email





app17 = Flask(__name__)
metrics = PrometheusMetrics(app17)
app17.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

# ✅ DATABASE CONFIG (THIS WAS MISSING)
app17.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app17.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app17)
migrate = Migrate(app17, db)
with app17.app_context():
    db.create_all()


stripe.api_key = "sk_test_51SYGVPEg9EarudRIP7y58GzMmAIi08AaJwC7Kcin1CPC188ZLjVqkGCvKGzRk1jUdrprcVJNhJbq4uzgyh3RrGdI00crPRc5MO"

login_success = Counter(
    "login_success_total",
    "Successful logins"
)

login_failed = Counter(
    "login_failed_total",
    "Failed logins"
)

email_sent = Counter(
    "email_sent_total",
    "Successfully sent emails"
)

email_failed = Counter(
    "email_failed_total",
    "Failed email deliveries"
)

# LOGIN ATTEMPTS
login_attempts = Counter(
    "login_attempts_total",
    "Total login attempts"
)

# FAILED LOGINS
failed_logins = Counter(
    "failed_logins_total",
    "Failed login attempts"
)

# STRIPE FAILURES
stripe_failures = Counter(
    "stripe_failures_total",
    "Stripe payment failures"
)
stripe_finished = Counter(
    "stripe_finishes_total",
    "Stripe payment finish"
)

# LOGIN LATENCY
login_latency = Histogram(
    "login_latency_seconds",
    "Login request latency"
)

# ACTIVE SESSIONS
active_sessions = Gauge(
    "active_sessions",
    "Currently active sessions"
)

# DB QUERY TIME
db_query_duration = Histogram(
    "db_query_duration_seconds",
    "Database query duration"
)
# -------- LOGIN --------
# -------- LOGIN --------
@app17.route("/login", methods=["POST"])
def login():

  with login_latency.time():
    login_attempts.inc()


    username = request.form.get("username", "")
    password = request.form.get("password", "")
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")

    if len(username) < 4 or len(password) < 4:
        login_failed.inc()
        log = LoginLog(
            username=username,
            ip_address=ip,
            user_agent=user_agent,
            successful=False
        )

        db.session.add(log)
        db.session.commit()

        return jsonify({"message": "Too short credentials"}), 400

    if not any(c in "%!@#$" for c in password):

        log = LoginLog(
            username=username,
            ip_address=ip,
            user_agent=user_agent,
            successful=False
        )

        db.session.add(log)
        db.session.commit()

        return jsonify({"message": "Password must contain special character"}), 400



    # login successful
    # check if user already exists
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    # hash password
    from werkzeug.security import generate_password_hash

    hashed_password = generate_password_hash(password)

    # create user
    new_user = User(
        username=username,
        password=hashed_password
    )

    # save to database
    db.session.add(new_user)
    db.session.commit()

    # session login
    session["authenticated"] = True

    try:

        checkout_session = stripe.checkout.Session.create(

            payment_method_types=["card"],

            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Premium Access",
                        },
                        "unit_amount": 500,
                    },
                    "quantity": 1,
                }
            ],

            mode="payment",

            success_url="http://app.automationclinics.com/success",
            cancel_url="http://app.automationclinics.com/cancel",
        )
        stripe_finished.inc()
        return redirect(checkout_session.url)

    except Exception as e:
        stripe_failures.inc()
        return jsonify({"error": str(e)}), 500





@app17.route("/stripe/webhook", methods=["POST"])
def stripe_webhook():

    payload = request.data

    event = stripe.Event.construct_from(
        request.json,
        stripe.api_key
    )

    if event["type"] == "checkout.session.completed":

        customer_email = (
            event["data"]["object"]
            .get("customer_details", {})
            .get("email")
        )

        try:
            send_welcome_email(customer_email)
            email_sent.inc()

        except Exception:
            email_failed.inc()

    return "", 200
# -------- 2FA SETUP (QR) --------


# -------- STRIPE SUCCESS --------



# -------- STRIPE CANCEL --------
@app17.route("/cancel")
def cancel():
    return "Payment Cancelled"
# -------- PROTECTED ROUTE EXAMPLE --------
@app17.route("/")
def index():


    if app17.config.get("TESTING"):
        return render_template("index17.html")
    return render_template("index17.html")

@app17.route("/health")
def health():
    return {"status": "UP"}, 200
if __name__ == "__main__":
    with app17.app_context():
        db.create_all()
    print(os.path.abspath("app.db"))
    print("lol1")
    app17.run(host="0.0.0.0", port=9000)