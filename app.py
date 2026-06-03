from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

# ---------- Config ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api_keys.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------- Model ----------
class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(100))
    api_key = db.Column(db.String(100), unique=True)

with app.app_context():
    db.create_all()

# ---------- Generate API Key ----------
@app.route("/generate-key", methods=["POST"])
def generate_key():

    data = request.get_json()

    key = str(uuid.uuid4())

    api_key = APIKey(
        owner=data["owner"],
        api_key=key
    )

    db.session.add(api_key)
    db.session.commit()

    return jsonify({
        "owner": data["owner"],
        "api_key": key
    })

# ---------- Auth Middleware ----------
def verify_api_key():

    key = request.headers.get("X-API-Key")

    if not key:
        return False

    api_key = APIKey.query.filter_by(
        api_key=key
    ).first()

    return api_key is not None

# ---------- Protected Route ----------
@app.route("/data")
def protected_data():

    if not verify_api_key():

        return jsonify({
            "message": "Invalid API Key"
        }), 401

    return jsonify({
        "message": "Protected data accessed"
    })

# ---------- List Keys ----------
@app.route("/keys")
def keys():

    all_keys = APIKey.query.all()

    return jsonify([
        {
            "owner": k.owner,
            "api_key": k.api_key
        }
        for k in all_keys
    ])

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
