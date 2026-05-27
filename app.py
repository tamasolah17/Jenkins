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



app17 = Flask(__name__)

app17.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

# ✅ DATABASE CONFIG (THIS WAS MISSING)
app17.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app17.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app17)
migrate = Migrate(app17, db)


stripe.api_key = "sk_test_51SYGVPEg9EarudRIP7y58GzMmAIi08AaJwC7Kcin1CPC188ZLjVqkGCvKGzRk1jUdrprcVJNhJbq4uzgyh3RrGdI00crPRc5MO"


# -------- LOGIN --------
# -------- LOGIN --------
@app17.route("/login", methods=["POST"])
def login():

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")

    if len(username) < 4 or len(password) < 4:
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

            success_url="http://54.211.101.220/success",
            cancel_url="http://54.211.101.220/cancel",
        )

        return redirect(checkout_session.url)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------- 2FA SETUP (QR) --------
@app17.route("/2fa/setup")
def setup_2fa():
    if not session.get("authenticated"):
        return jsonify({"message": "Not logged in"}), 401

    secret = pyotp.random_base32()
    session["2fa_secret"] = secret

    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(
        name="user",
        issuer_name="FlaskApp"
    )

    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)

    return send_file(buf, mimetype="image/png")

@app17.route("/2fa")
def twofa():
    if not session.get("authenticated"):
        return redirect(url_for("index"))

    return render_template("2fa.html")
# -------- 2FA VERIFY --------
@app17.route("/2fa/verify", methods=["POST"])
def verify_2fa():
    code = request.form.get("code", "")
    secret = session.get("2fa_secret")

    if not secret:
        return jsonify({"message": "2FA not initialized"}), 400

    totp = pyotp.TOTP(secret)

    if totp.verify(code):
        session["2fa_passed"] = True
        return jsonify({"message": "2FA success"})
    else:
        return jsonify({"message": "Invalid code"}), 400

# -------- STRIPE SUCCESS --------
@app17.route("/success")
def success():

    # after successful payment continue to 2FA
    return redirect(url_for("twofa"))


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


if __name__ == "__main__":
    with app17.app_context():
        db.create_all()
    print(os.path.abspath("app.db"))
    app17.run(host="0.0.0.0", port=9000)