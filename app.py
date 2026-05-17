import io
from flask import Flask, request, jsonify, render_template, session, send_file, redirect, url_for
import pyotp
import qrcode
import io
import os
import stripe

app17 = Flask(__name__)

# session kulcshoz kötelező
app17.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# -------- LOGIN --------
# -------- LOGIN --------
@app17.route("/login", methods=["POST"])
def login():

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if len(username) < 4 or len(password) < 4:
        return jsonify({"message": "Too short credentials"}), 400

    if not any(c in "%!@#$" for c in password):
        return jsonify({"message": "Password must contain special character"}), 400

    # login successful
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
        return redirect(url_for("index17"))

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
    app17.run(host="0.0.0.0", port=24000)