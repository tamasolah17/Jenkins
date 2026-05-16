import io
from flask import Flask, request, jsonify, render_template, session, send_file, redirect, url_for
import pyotp
import qrcode

app17 = Flask(__name__)

# session kulcshoz kötelező
app17.secret_key = "dev-secret-change-me"


# -------- LOGIN --------
@app17.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if len(username) < 4 or len(password) < 4:
        return jsonify({"message": "Too short credentials"}), 400

    if not any(c in "%!@#$" for c in password):
        return jsonify({"message": "Password must contain special character"}), 400

    # login OK -> 2FA indítás
    session["authenticated"] = True
    return jsonify({"message": "Login OK, go to /2fa/setup"})


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


# -------- PROTECTED ROUTE EXAMPLE --------
@app17.route("/")
def index():
    if not session.get("2fa_passed"):
        return jsonify({"message": "2FA required"}), 401

    return render_template("index17.html")


if __name__ == "__main__":
    app17.run(host="0.0.0.0", port=24000)