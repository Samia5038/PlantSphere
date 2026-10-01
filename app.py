
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from soil_model import classify_soil_image, load_soil_model as load_or_train_soil_model
from weather.weather import get_weather_data


BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DATABASE_PATH = INSTANCE_DIR / "users.db"
MODEL_PATH = INSTANCE_DIR / "crop_model.joblib"
DATA_PATH = BASE_DIR / "Crop_recommendation.csv"
UPLOAD_DIR = INSTANCE_DIR / "uploads"
SOIL_MODEL_PATH = INSTANCE_DIR / "soil_model.joblib"
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
FEATURE_COLUMNS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
FORM_FIELDS = ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "ph", "Rainfall"]
soil_model_payload = None

INSTANCE_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("PLANTSPHERE_SECRET_KEY", "local-plantsphere-session-key")
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please sign in to open the agriculture tools."
login_manager.login_message_category = "info"


@contextmanager
def connect_database():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    with connect_database() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )


initialize_database()


class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    with connect_database() as connection:
        row = connection.execute(
            "SELECT id, username FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    return User(row["id"], row["username"]) if row else None


def load_or_train_crop_model():
    if MODEL_PATH.exists():
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            MODEL_PATH.unlink(missing_ok=True)

    if not DATA_PATH.exists():
        raise FileNotFoundError("Crop_recommendation.csv is missing.")

    dataset = pd.read_csv(DATA_PATH)
    if not set(FEATURE_COLUMNS + ["label"]).issubset(dataset.columns):
        raise ValueError("Crop dataset is missing one or more expected columns.")

    model = RandomForestClassifier(n_estimators=140, random_state=42, n_jobs=-1)
    model.fit(dataset[FEATURE_COLUMNS], dataset["label"])
    joblib.dump(model, MODEL_PATH)
    return model


def recommend_crops(soil_type):
    crops = {
        "alluvial": ["Rice", "Sugarcane", "Wheat"],
        "black": ["Cotton", "Groundnut", "Sunflower"],
        "clay": ["Soybean", "Rice", "Maize"],
        "red": ["Pulses", "Groundnut", "Millets"],
    }
    return crops.get(soil_type, [])


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if len(username) < 3 or len(username) > 30:
            flash("Username must be between 3 and 30 characters.", "error")
        elif len(password) < 8:
            flash("Use a password with at least 8 characters.", "error")
        else:
            try:
                with connect_database() as connection:
                    connection.execute(
                        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                        (username, generate_password_hash(password)),
                    )
                flash("Account created. Sign in to continue.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("That username is already registered.", "error")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        with connect_database() as connection:
            row = connection.execute(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,),
            ).fetchone()
        if row and check_password_hash(row["password_hash"], password):
            login_user(User(row["id"], row["username"]))
            return redirect(url_for("home"))
        flash("Username or password was not recognized.", "error")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/home")
@login_required
def home():
    return render_template("home.html")


@app.route("/crop")
@login_required
def crop():
    return render_template("crop.html")


@app.route("/predict", methods=["POST"])
@login_required
def predict():
    try:
        values = [float(request.form[field]) for field in FORM_FIELDS]
        nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall = values
        if min(nitrogen, phosphorus, potassium, rainfall) < 0:
            raise ValueError("Nutrients and rainfall cannot be negative.")
        if not -10 <= temperature <= 60 or not 0 <= humidity <= 100 or not 0 <= ph <= 14:
            raise ValueError("Check the temperature, humidity, and pH values.")

        model = load_or_train_crop_model()
        features = pd.DataFrame([values], columns=FEATURE_COLUMNS)
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = float(np.max(probabilities))
        return jsonify({"prediction": str(prediction), "confidence": round(confidence * 100)})
    except (KeyError, TypeError, ValueError) as error:
        return jsonify({"error": str(error) or "Enter valid values for every field."}), 400
    except Exception as error:
        app.logger.exception("Crop prediction failed")
        return jsonify({"error": "Prediction could not be completed: {}".format(error)}), 503


@app.route("/soil", methods=["GET", "POST"])
@login_required
def soil():
    global soil_model_payload
    if request.method == "POST":
        upload = request.files.get("soilImage")
        if upload is None or not upload.filename:
            return jsonify({"error": "Choose a soil image first."}), 400
        filename = secure_filename(upload.filename)
        extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            return jsonify({"error": "Upload a PNG, JPG, JPEG, or WEBP image."}), 400
        try:
            image = Image.open(upload.stream)
            image.verify()
            upload.stream.seek(0)
            image = Image.open(upload.stream)
            if soil_model_payload is None:
                soil_model_payload = load_or_train_soil_model(SOIL_MODEL_PATH)
            result = classify_soil_image(image, soil_model_payload)
        except Exception:
            app.logger.exception("Soil image classification failed")
            return jsonify({"error": "The selected file is not a readable image."}), 400

        return jsonify({
            "soil_type": result["soil_type"].title(),
            "confidence": round(result["confidence"] * 100),
            "test_accuracy": round(result["test_accuracy"] * 100, 1),
            "recommended_crops": recommend_crops(result["soil_type"]),
            "note": "Model confidence is not a guarantee; confirm soil properties with a local soil test.",
        })

    return render_template("soil.html")


@app.route("/weather", methods=["GET", "POST"])
@login_required
def weather():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            flash("Enter a town or city name.", "error")
        else:
            weather_data = get_weather_data(city)
            if weather_data.get("error"):
                flash(weather_data["error"], "error")
                weather_data = None
    return render_template("weather.html", weather_data=weather_data)


@app.errorhandler(413)
def upload_too_large(_error):
    if request.path == url_for("soil"):
        return jsonify({"error": "Image must be smaller than 8 MB."}), 413
    return "Request is too large.", 413


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)




