
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import sqlite3
import os
import pickle
import numpy as np
import cv2
import tensorflow as tf
from werkzeug.utils import secure_filename
from sklearn.utils import class_weight
from weather.weather import get_weather_data  

app = Flask(__name__)
app.secret_key = "supersecretkey"


login_manager = LoginManager(app)
login_manager.login_view = "index"

IMG_SIZE = 150  
try:
    crop_model = pickle.load(open("model/model.pkl", "rb"))
    print("Crop model loaded successfully!")
except Exception as e:
    print("Error!", e)
    crop_model = None

try:
    soil_model = tf.keras.models.load_model("soil_classifier/soil_classifier.h5")
    soil_classes = ["alluvial", "black", "clay", "red"]
except Exception as e:
    print("Error loading soil classifier model:", e)
    soil_model = None
    soil_classes = []


def recommend_crops(soil_type):
    crops_dict = {
        "alluvial": ["Rice", "Sugarcane", "Wheat"],
        "black": ["Cotton", "Groundnut", "Sunflower"],
        "clay": ["Soybean", "Rice", "Maize"],
        "red": ["Pulses", "Groundnut", "Millets"]
    }
    return ", ".join(crops_dict.get(soil_type, []))

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        user = User()
        user.id = user_data[0]
        return user
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = None  
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            user = User()
            user.id = user_data[0]
            login_user(user)
            return redirect(url_for("home"))
        else:
            error_message = "Invalid username or password"  

    return render_template("login.html", error_message=error_message)

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/crop")
@login_required
def crop():
    return render_template("crop.html")

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    try:
        data = [float(request.form[key]) for key in 
                ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "ph", "Rainfall"]]

        print("🔹 Received Input:", data)

        if crop_model is None:
            print("Model not loaded!")
            return jsonify({"error": "Model not loaded!"})

        prediction = crop_model.predict([np.array(data)])[0]
        print("Prediction Output:", prediction)
        
        return jsonify({"prediction": prediction})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)})

@app.route("/soil", methods=["GET", "POST"])
@login_required
def soil():
    if request.method == "POST":
      
        if 'soilImage' not in request.files:
            return jsonify({"error": "No file part"})
        
        file = request.files['soilImage']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"})
        
        upload_folder = "uploads"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        image = cv2.imread(file_path)
        image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))  
        image = np.expand_dims(image, axis=0)  
        image = image / 255.0 

        predictions = soil_model.predict(image)
        
        print("🔹 Raw predictions:", predictions)

        confidence_threshold = 0.6
        if max(predictions[0]) < confidence_threshold:
            soil_type = "Uncertain"
        else:
            predicted_class = np.argmax(predictions, axis=1)[0] 
            soil_type = soil_classes[predicted_class]  

        print("🔹 Predicted class:", predicted_class, "Predicted soil type:", soil_type)

        recommended_crops = recommend_crops(soil_type)  

        return jsonify({
            "soil_type": soil_type,
            "recommended_crops": recommended_crops
        })
    
    return render_template("soil.html")

@app.route("/weather", methods=["GET", "POST"])
@login_required
def weather():
    weather_data = None  

    if request.method == "POST":
        try:
            city = request.form.get("city")
            if not city:
                return render_template("weather.html", error="City name is required")
            
            weather_data = get_weather_data(city)
            
            if weather_data.get("error"):
                return render_template("weather.html", error=weather_data["error"])
            
        except Exception as e:
            print("Error fetching weather data:", e)
            return render_template("weather.html", error="Failed to fetch weather data")

    return render_template("weather.html", weather_data=weather_data)

if __name__ == "__main__":
    app.run(debug=True)




