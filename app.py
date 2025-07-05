
# from flask import Flask, render_template, request, jsonify
# import pickle
# import numpy as np
# import pandas as pd
# from weather.weather import get_weather_data

# app = Flask(__name__)

# # Load trained model
# model = pickle.load(open("model/model.pkl", "rb"))

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         # Get input data from the form
#         data = [float(request.form[key]) for key in request.form]
#         final_input = np.array(data).reshape(1, -1)
        
#         # Make prediction using the loaded model
#         prediction = model.predict(final_input)
#         return jsonify({"prediction": prediction[0]})
    
#     except Exception as e:
#         return jsonify({"error": str(e)})


# @app.route("/weather", methods=["POST"])
# def weather():
#     city = request.form["city"]
#     weather_data = get_weather_data(city)
#     return jsonify(weather_data)

# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# import sqlite3
# import pickle
# import numpy as np
# from weather.weather import get_weather_data  # our weather helper
# # (Make sure you set your API key in weather/weather.py)

# app = Flask(__name__)
# app.secret_key = "supersecretkey"

# # Setup Flask-Login
# login_manager = LoginManager()
# login_manager.login_view = "index"
# login_manager.init_app(app)

# # Load the trained crop prediction model
# model = pickle.load(open("model/model.pkl", "rb"))

# # ---------------------------
# # User Authentication Classes & Functions
# # ---------------------------
# class User(UserMixin):
#     pass

# @login_manager.user_loader
# def load_user(user_id):
#     conn = sqlite3.connect("database/users.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
#     user_data = cursor.fetchone()
#     conn.close()
#     if user_data:
#         user = User()
#         user.id = user_data[0]
#         user.username = user_data[1]
#         return user
#     return None

# # ---------------------------
# # Routes
# # ---------------------------

# # Login & Signup Page
# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/signup", methods=["POST"])
# def signup():
#     username = request.form["username"]
#     password = request.form["password"]
#     conn = sqlite3.connect("database/users.db")
#     cursor = conn.cursor()
#     try:
#         cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#         conn.commit()
#     except sqlite3.IntegrityError:
#         conn.close()
#         return "Username already exists."
#     conn.close()
#     return redirect(url_for("index"))

# @app.route("/login", methods=["POST"])
# def login():
#     username = request.form["username"]
#     password = request.form["password"]
#     conn = sqlite3.connect("database/users.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
#     user_data = cursor.fetchone()
#     conn.close()
#     if user_data:
#         user = User()
#         user.id = user_data[0]
#         login_user(user)
#         return redirect(url_for("home"))
#     return "Invalid credentials"

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("index"))

# # Dashboard (after login)
# @app.route("/home")
# @login_required
# def home():
#     return render_template("home.html")

# # Weather Forecast Page
# @app.route("/weather", methods=["GET", "POST"])
# @login_required
# def weather():
#     if request.method == "POST":
#         city = request.form["city"]
#         weather_data = get_weather_data(city)
#         return jsonify(weather_data)
#     return render_template("weather.html")

# # Crop Recommendation (Prediction) Page
# @app.route("/predict", methods=["POST"])
# @login_required
# def predict():
#     try:
#         # Expecting 7 fields: Nitrogen, Phosphorus, Potassium, Temperature, Humidity, ph, Rainfall
#         data = [float(request.form[key]) for key in ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "ph", "Rainfall"]]
#         prediction = model.predict([np.array(data)])[0]
#         return jsonify({"prediction": prediction})
#     except Exception as e:
#         return jsonify({"error": str(e)})

# @app.route("/crop")
# @login_required
# def crop():
#     return render_template("crop.html")

# # Soil Recommendation Page (For now, simply render the page; you'll need to implement image upload and processing)
# @app.route("/soil", methods=["GET", "POST"])
# @login_required
# def soil():
#     if request.method == "POST":
#         # Implement soil image processing here
#         # For now, just return a dummy recommendation
#         return jsonify({"recommendation": "Recommended crops for your soil: Wheat, Rice"})
#     return render_template("soil.html")

# if __name__ == "__main__":
#     app.run(debug=True)








# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# import sqlite3
# import pickle
# import numpy as np
# from weather.weather import get_weather_data  # Ensure the weather helper is set correctly

# app = Flask(__name__)
# app.secret_key = "supersecretkey"

# # Setup Flask-Login
# login_manager = LoginManager()
# login_manager.login_view = "index"
# login_manager.init_app(app)

# # Load the trained crop prediction model
# model = pickle.load(open("model/model.pkl", "rb"))

# # ---------------------------
# # User Authentication Classes & Functions
# # ---------------------------
# class User(UserMixin):
#     pass

# @login_manager.user_loader
# def load_user(user_id):
#     conn = sqlite3.connect("database/users.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
#     user_data = cursor.fetchone()
#     conn.close()
#     if user_data:
#         user = User()
#         user.id = user_data[0]
#         user.username = user_data[1]
#         return user
#     return None

# # ---------------------------
# # Routes
# # ---------------------------

# # Home page
# @app.route("/")
# def index():
#     return render_template("index.html")

# # # Signup route
# # @app.route("/signup", methods=["POST"])
# # def signup():
# #     username = request.form["username"]
# #     password = request.form["password"]
# #     conn = sqlite3.connect("database/users.db")
# #     cursor = conn.cursor()
# #     try:
# #         cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
# #         conn.commit()
# #     except sqlite3.IntegrityError:
# #         conn.close()
# #         return "Username already exists."
# #     conn.close()
# #     return redirect(url_for("index"))

# # # Login route
# # @app.route("/login", methods=["POST"])
# # def login():
# #     username = request.form["username"]
# #     password = request.form["password"]
# #     conn = sqlite3.connect("database/users.db")
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
# #     user_data = cursor.fetchone()
# #     conn.close()
# #     if user_data:
# #         user = User()
# #         user.id = user_data[0]
# #         login_user(user)
# #         return redirect(url_for("home"))
# #     return "Invalid credentials"





# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
#         user_data = cursor.fetchone()
#         conn.close()
#         if user_data:
#             user = User()
#             user.id = user_data[0]
#             login_user(user)
#             return redirect(url_for("home"))
#         return "Invalid credentials"
#     return render_template("login.html")  # This renders the login page for GET requests

# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         try:
#             cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#             conn.commit()
#         except sqlite3.IntegrityError:
#             conn.close()
#             return "Username already exists."
#         conn.close()
#         return redirect(url_for("index"))
#     return render_template("signup.html")  # This renders the signup page for GET requests

# # Logout route
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("index"))

# # Dashboard page (after login)
# @app.route("/home")
# @login_required
# def home():
#     return render_template("home.html")

# # Weather forecast page
# @app.route("/weather", methods=["GET", "POST"])
# @login_required
# def weather():
#     if request.method == "POST":
#         city = request.form["city"]
#         weather_data = get_weather_data(city)  # Ensure this function returns valid data
#         return jsonify(weather_data)
#     return render_template("weather.html")

# # Crop recommendation (prediction) page
# @app.route("/predict", methods=["POST"])
# @login_required
# def predict():
#     try:
#         # Expecting 7 fields: Nitrogen, Phosphorus, Potassium, Temperature, Humidity, ph, Rainfall
#         data = [float(request.form[key]) for key in ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "ph", "Rainfall"]]
#         prediction = model.predict([np.array(data)])[0]
#         return jsonify({"prediction": prediction})
#     except Exception as e:
#         return jsonify({"error": str(e)})

# # Crop page
# @app.route("/crop")
# @login_required
# def crop():
#     return render_template("crop.html")

# # Soil recommendation page
# @app.route("/soil", methods=["GET", "POST"])
# @login_required
# def soil():
#     if request.method == "POST":
#         # Implement soil image processing here
#         # For now, just return a dummy recommendation
#         return jsonify({"recommendation": "Recommended crops for your soil: Wheat, Rice"})
#     return render_template("soil.html")

# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# import sqlite3
# import os
# import pickle
# import numpy as np
# import cv2
# import tensorflow as tf
# from werkzeug.utils import secure_filename
# from weather.weather import get_weather_data  # Ensure your weather helper function is implemented

# app = Flask(__name__)
# app.secret_key = "supersecretkey"  # Consider using an environment variable in production

# # Setup Flask-Login
# login_manager = LoginManager(app)
# login_manager.login_view = "index"

# # Load the trained crop prediction model (for tabular data)
# crop_model = pickle.load(open("model/model.pkl", "rb"))

# # Load the Soil Classifier Model (CNN for soil image classification)
# soil_model = tf.keras.models.load_model("soil_classifier/soil_classifier.h5")
# soil_classes = ["sandy", "loamy", "clayey", "silty"]  # Adjust according to your training

# # ---------------------------
# # User Authentication Classes & Functions
# # ---------------------------
# class User(UserMixin):
#     pass

# @login_manager.user_loader
# def load_user(user_id):
#     conn = sqlite3.connect("database/users.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
#     user_data = cursor.fetchone()
#     conn.close()
#     if user_data:
#         user = User()
#         user.id = user_data[0]
#         user.username = user_data[1]
#         return user
#     return None

# # ---------------------------
# # Routes
# # ---------------------------

# # Landing page (Login/Signup)
# @app.route("/")
# def index():
#     return render_template("index.html")

# # Login Route (GET and POST)
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
#         user_data = cursor.fetchone()
#         conn.close()
#         if user_data:
#             user = User()
#             user.id = user_data[0]
#             login_user(user)
#             return redirect(url_for("home"))
#         return "Invalid credentials"
#     return render_template("login.html")

# # Signup Route (GET and POST)
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         try:
#             cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#             conn.commit()
#         except sqlite3.IntegrityError:
#             conn.close()
#             return "Username already exists."
#         conn.close()
#         return redirect(url_for("index"))
#     return render_template("signup.html")

# # Logout Route
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("index"))

# # Dashboard (Home) after login
# @app.route("/home")
# @login_required
# def home():
#     return render_template("home.html")

# # Weather Forecast Page
# @app.route("/weather", methods=["GET", "POST"])
# @login_required
# def weather():
#     if request.method == "POST":
#         city = request.form["city"]
#         weather_data = get_weather_data(city)  # Ensure your get_weather_data returns a dictionary
#         return jsonify(weather_data)
#     return render_template("weather.html")

# # Crop Prediction Page (Tabular Data Prediction)
# @app.route("/predict", methods=["POST"])
# @login_required
# def predict():
#     try:
#         # Expected 7 fields: Nitrogen, Phosphorus, Potassium, Temperature, Humidity, ph, Rainfall
#         data = [float(request.form[key]) for key in ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "ph", "Rainfall"]]
#         prediction = crop_model.predict([np.array(data)])[0]
#         return jsonify({"prediction": prediction})
#     except Exception as e:
#         return jsonify({"error": str(e)})

# # Crop Recommendation Page (to render crop.html)
# @app.route("/crop")
# @login_required
# def crop():
#     return render_template("crop.html")

# # # Soil Recommendation Page (Image Upload & Processing)
# # @app.route("/soil", methods=["GET", "POST"])
# # @login_required
# # def soil():
# #     if request.method == "POST":
# #         if "soilImage" not in request.files:
# #             return jsonify({"error": "No file uploaded"}), 400
        
# #         file = request.files["soilImage"]
        
# #         if file.filename == "":
# #             return jsonify({"error": "No selected file"}), 400
        
# #         filename = secure_filename(file.filename)
# #         upload_path = os.path.join("static", "uploads", filename)
# #         os.makedirs(os.path.dirname(upload_path), exist_ok=True)
# #         file.save(upload_path)

# #         print(f"File uploaded: {upload_path}")  # Debugging statement

# #         # Load and preprocess the image
# #         try:
# #             img = cv2.imread(upload_path)
# #             if img is None:
# #                 return jsonify({"error": "Error reading image file"}), 400

# #             img = cv2.resize(img, (150, 150))  # Ensure correct input size for the model
# #             img = img / 255.0  # Normalize
# #             img = np.expand_dims(img, axis=0)

# #             print(f"Image Shape: {img.shape}")  # Should be (1, 150, 150, 3)

# #             # Predict soil type
# #             prediction = soil_model.predict(img)
# #             print(f"Prediction array: {prediction}")  # Verify prediction shape and values

# #             class_index = np.argmax(prediction)
# #             soil_type = soil_classes[class_index]

# #             print(f"Predicted Soil Type: {soil_type}")  # Debugging statement
# #             print(f"Predicted Class Index: {class_index}")  # Debugging index

# #             # Crop recommendations
# #             crop_recommendations = {
# #                 "sandy": "Carrots, Peanuts, Watermelon",
# #                 "loamy": "Wheat, Maize, Sugarcane",
# #                 "clayey": "Rice, Jute, Soybeans",
# #                 "silty": "Vegetables, Fruits, Rice"
# #             }
# #             recommended_crops = crop_recommendations.get(soil_type, "No recommendation")
            
# #             return jsonify({
# #                 "soil_type": soil_type,
# #                 "recommended_crops": recommended_crops
# #             })
# #         except Exception as e:
# #             print(f"Error processing image: {e}")  # Debugging
# #             return jsonify({"error": "Error processing image"}), 500

# #     return render_template("soil.html")





# @app.route("/soil", methods=["GET", "POST"])
# @login_required
# def soil():
#     if request.method == "POST":
#         if "soilImage" not in request.files:
#             return jsonify({"error": "No file uploaded"}), 400
        
#         file = request.files["soilImage"]
        
#         if file.filename == "":
#             return jsonify({"error": "No selected file"}), 400
        
#         filename = secure_filename(file.filename)
#         upload_path = os.path.join("static", "uploads", filename)
#         os.makedirs(os.path.dirname(upload_path), exist_ok=True)
#         file.save(upload_path)

#         print(f"File uploaded: {upload_path}")  # Debugging statement

#         # Load and preprocess the image
#         try:
#             img = cv2.imread(upload_path)
#             if img is None:
#                 return jsonify({"error": "Error reading image file"}), 400

#             img = cv2.resize(img, (150, 150))  # Ensure correct input size for the model
#             img = img / 255.0  # Normalize
#             img = np.expand_dims(img, axis=0)

#             print(f"Image Shape: {img.shape}")  # Should be (1, 150, 150, 3)

#             # Predict soil type
#             prediction = soil_model.predict(img)
#             print(f"Prediction array: {prediction}")  # Verify prediction shape and values

#             class_index = np.argmax(prediction)
#             soil_type = soil_classes[class_index]

#             print(f"Predicted Soil Type: {soil_type}")  # Debugging statement
#             print(f"Predicted Class Index: {class_index}")  # Debugging index

#             # Crop recommendations
#             crop_recommendations = {
#                 "sandy": "Carrots, Peanuts, Watermelon",
#                 "loamy": "Wheat, Maize, Sugarcane",
#                 "clayey": "Rice, Jute, Soybeans",
#                 "silty": "Vegetables, Fruits, Rice"
#             }
#             recommended_crops = crop_recommendations.get(soil_type, "No recommendation")
            
#             return jsonify({
#                 "soil_type": soil_type,
#                 "recommended_crops": recommended_crops
#             })
#         except Exception as e:
#             print(f"Error processing image: {e}")  # Debugging
#             return jsonify({"error": "Error processing image"}), 500

#     return render_template("soil.html")

# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# import sqlite3
# import requests
# import os
# import pickle
# import numpy as np
# import cv2
# import tensorflow as tf
# from werkzeug.utils import secure_filename

# app = Flask(__name__)
# app.secret_key = "supersecretkey"

# # Setup Flask-Login
# login_manager = LoginManager(app)
# login_manager.login_view = "index"

# # Load trained crop prediction model
# crop_model = pickle.load(open("model/model.pkl", "rb"))

# # Load trained soil classifier model
# try:
#     soil_model = tf.keras.models.load_model("soil_classifier/soil_classifier.h5")
#     soil_classes = ["alluvial", "black", "clay", "red"]
# except Exception as e:
#     print("Error loading soil classifier model:", e)
#     soil_model = None
#     soil_classes = []

# # User Authentication
# class User(UserMixin):
#     pass

# @login_manager.user_loader
# def load_user(user_id):
#     conn = sqlite3.connect("database/users.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
#     user_data = cursor.fetchone()
#     conn.close()
#     if user_data:
#         user = User()
#         user.id = user_data[0]
#         return user
#     return None

# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#         conn.commit()
#         conn.close()

#         return redirect(url_for("login"))  # Redirect to login page after signup

#     return render_template("signup.html")

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
#         user_data = cursor.fetchone()
#         conn.close()
#         if user_data:
#             user = User()
#             user.id = user_data[0]
#             login_user(user)
#             return redirect(url_for("home"))
#         return "Invalid credentials"
#     return render_template("login.html")

# @app.route("/home")
# @login_required
# def home():
#     return render_template("home.html")

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()  # Log out the current user
#     return redirect(url_for("index"))  # Redirect to home or login page after logout

# @app.route("/crop")
# @login_required
# def crop():
#     return render_template("crop.html")

# @app.route("/soil", methods=["POST"])
# @login_required
# def soil():
#     if "soilImage" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
    
#     file = request.files["soilImage"]
#     filename = secure_filename(file.filename)
#     upload_path = os.path.join("static", "uploads", filename)
#     os.makedirs(os.path.dirname(upload_path), exist_ok=True)
#     file.save(upload_path)

#     try:
#         img = cv2.imread(upload_path)
#         img = cv2.resize(img, (150, 150))
#         img = img / 255.0
#         img = np.expand_dims(img, axis=0)

#         prediction = soil_model.predict(img)
#         class_index = np.argmax(prediction)
#         soil_type = soil_classes[class_index]

#         crop_recommendations = {
#             "alluvial": "Wheat, Rice, Jute, Sugarcane",
#             "black": "Cotton, Pulses, Soyabean",
#             "clay": "Rice, Wheat, Sorghum",
#             "red": "Cotton, Millets, Tobacco"
#         }
#         recommended_crops = crop_recommendations.get(soil_type, "No recommendation")

#         return jsonify({"soil_type": soil_type, "recommended_crops": recommended_crops})
#     except Exception as e:
#         return jsonify({"error": "Error processing image"}), 500

# # @app.route("/weather", methods=["GET", "POST"])
# # @login_required
# # def weather():
# #     # Example: Fetch weather data from OpenWeatherMap API
# #     api_key = "8db2f2c7b281d045956c170dc3e2bc9d"  # Replace with your valid API key
    
# #     # Use the city provided in the form, default to Dhaka
# #     city = request.form.get("city", "Dhaka") if request.method == "POST" else "Dhaka"
    
# #     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

# #     try:
# #         response = requests.get(url)
# #         data = response.json()

# #         if data["cod"] == 200:
# #             weather_data = {
# #                 "city": data["name"],
# #                 "temperature": data["main"]["temp"],
# #                 "humidity": data["main"]["humidity"],
# #                 "description": data["weather"][0]["description"],
# #                 "wind_speed": data["wind"]["speed"],
# #                 "pressure": data["main"]["pressure"]
# #             }

# #             if request.method == "POST":
# #                 return jsonify(weather_data)  # Return weather data as JSON response
# #             else:
# #                 return render_template("weather.html", weather=weather_data)  # Render the weather page for GET request

# #         else:
# #             error_message = f"Error fetching weather data: {data.get('message', 'Unknown error')}"
# #             return render_template("error.html", error_message=error_message)

# #     except requests.exceptions.RequestException as e:
# #         error_message = f"Request error occurred: {str(e)}"
# #         return render_template("error.html", error_message=error_message)

# #     except Exception as e:
# #         error_message = f"An unexpected error occurred: {str(e)}"
# #         return render_template("error.html", error_message=error_message)


# # Weather Forecast Page
# @app.route("/weather", methods=["GET", "POST"])
# @login_required
# def weather():
#     if request.method == "POST":
#         city = request.form["city"]
#         weather_data = get_weather_data(city)  # Ensure your get_weather_data returns a dictionary
#         return jsonify(weather_data)
#     return render_template("weather.html")

# @app.route("/predict", methods=["POST"])
# @login_required
# def predict():
#     try:
#         data = [float(request.form[key]) for key in 
#                 ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "ph", "Rainfall"]]
#         prediction = crop_model.predict([np.array(data)])[0]
#         return jsonify({"prediction": prediction})
#     except Exception as e:
#         return jsonify({"error": str(e)})

# if __name__ == "__main__":
#     app.run(debug=True)





# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# import sqlite3
# import requests
# import os
# import pickle
# import numpy as np
# import cv2
# import tensorflow as tf
# from werkzeug.utils import secure_filename

# app = Flask(__name__)
# app.secret_key = "supersecretkey"

# # Setup Flask-Login
# login_manager = LoginManager(app)
# login_manager.login_view = "index"

# # Load trained crop prediction model
# crop_model = pickle.load(open("model/model.pkl", "rb"))

# # Load trained soil classifier model
# try:
#     soil_model = tf.keras.models.load_model("soil_classifier/soil_classifier.h5")
#     soil_classes = ["alluvial", "black", "clay", "red"]
# except Exception as e:
#     print("Error loading soil classifier model:", e)
#     soil_model = None
#     soil_classes = []

# # User Authentication
# class User(UserMixin):
#     pass

# @login_manager.user_loader
# def load_user(user_id):
#     conn = sqlite3.connect("database/users.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
#     user_data = cursor.fetchone()
#     conn.close()
#     if user_data:
#         user = User()
#         user.id = user_data[0]
#         return user
#     return None

# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#         conn.commit()
#         conn.close()

#         return redirect(url_for("login"))  # Redirect to login page after signup

#     return render_template("signup.html")

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
#         user_data = cursor.fetchone()
#         conn.close()
#         if user_data:
#             user = User()
#             user.id = user_data[0]
#             login_user(user)
#             return redirect(url_for("home"))
#         return "Invalid credentials"
#     return render_template("login.html")

# @app.route("/home")
# @login_required
# def home():
#     return render_template("home.html")

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()  # Log out the current user
#     return redirect(url_for("index"))  # Redirect to home or login page after logout

# @app.route("/crop")
# @login_required
# def crop():
#     return render_template("crop.html")

# @app.route("/soil", methods=["POST"])
# @login_required
# def soil():
#     if "soilImage" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
    
#     file = request.files["soilImage"]
#     filename = secure_filename(file.filename)
#     upload_path = os.path.join("static", "uploads", filename)
#     os.makedirs(os.path.dirname(upload_path), exist_ok=True)
#     file.save(upload_path)

#     try:
#         img = cv2.imread(upload_path)
#         img = cv2.resize(img, (150, 150))
#         img = img / 255.0
#         img = np.expand_dims(img, axis=0)

#         prediction = soil_model.predict(img)
#         class_index = np.argmax(prediction)
#         soil_type = soil_classes[class_index]

#         crop_recommendations = {
#             "alluvial": "Wheat, Rice, Jute, Sugarcane",
#             "black": "Cotton, Pulses, Soyabean",
#             "clay": "Rice, Wheat, Sorghum",
#             "red": "Cotton, Millets, Tobacco"
#         }
#         recommended_crops = crop_recommendations.get(soil_type, "No recommendation")

#         return jsonify({"soil_type": soil_type, "recommended_crops": recommended_crops})
#     except Exception as e:
#         print(f"Error processing soil image: {e}")
#         return jsonify({"error": "Error processing image"}), 500

# @app.route("/weather")
# @login_required
# def weather():
#     print("Weather route accessed")  # Debugging line to check if route is hit.
    
#     api_key = "your_openweathermap_api_key"  # Replace with your valid API key
#     city = "Dhaka"  # You can dynamically change this based on user input or location
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

#     try:
#         response = requests.get(url)
#         print(f"Status Code: {response.status_code}")  # Log status code for debugging
        
#         data = response.json()
#         print(f"Response Data: {data}")  # Print the API response for debugging
        
#         if data["cod"] == 200:
#             weather_data = {
#                 "city": data["name"],
#                 "temperature": data["main"]["temp"],
#                 "humidity": data["main"]["humidity"],
#                 "description": data["weather"][0]["description"]
#             }
#             return render_template("weather.html", weather=weather_data)
#         else:
#             error_message = f"Error fetching weather data: {data.get('message', 'Unknown error')}"
#             print(error_message)
#             return render_template("error.html", error_message=error_message)

#     except requests.exceptions.RequestException as e:
#         error_message = f"Request error occurred: {str(e)}"
#         print(error_message)
#         return render_template("error.html", error_message=error_message)

#     except Exception as e:
#         error_message = f"An unexpected error occurred: {str(e)}"
#         print(error_message)
#         return render_template("error.html", error_message=error_message)

# @app.route("/predict", methods=["POST"])
# @login_required
# def predict():
#     try:
#         data = [float(request.form[key]) for key in 
#                 ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "ph", "Rainfall"]]
#         prediction = crop_model.predict([np.array(data)])[0]
#         return jsonify({"prediction": prediction})
#     except Exception as e:
#         print(f"Error in prediction: {e}")
#         return jsonify({"error": str(e)})

# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# import sqlite3
# import os
# import pickle
# import numpy as np
# import cv2
# import tensorflow as tf
# from werkzeug.utils import secure_filename
# from weather.weather import get_weather_data

# app = Flask(__name__)
# app.secret_key = "supersecretkey"

# # Setup Flask-Login
# login_manager = LoginManager(app)
# login_manager.login_view = "index"

# # Load trained crop prediction model with error handling
# try:
#     crop_model = pickle.load(open("model/model.pkl", "rb"))
#     print("✅ Crop model loaded successfully!")
# except Exception as e:
#     print("❌ Error loading crop model:", e)
#     crop_model = None

# # Load trained soil classifier model
# try:
#     soil_model = tf.keras.models.load_model("soil_classifier/soil_classifier.h5")
#     soil_classes = ["alluvial", "black", "clay", "red"]
# except Exception as e:
#     print("❌ Error loading soil classifier model:", e)
#     soil_model = None
#     soil_classes = []

# # User Authentication
# class User(UserMixin):
#     pass

# @login_manager.user_loader
# def load_user(user_id):
#     conn = sqlite3.connect("database/users.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
#     user_data = cursor.fetchone()
#     conn.close()
#     if user_data:
#         user = User()
#         user.id = user_data[0]
#         return user
#     return None

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#         conn.commit()
#         conn.close()

#         return redirect(url_for("login"))  

#     return render_template("signup.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
#         user_data = cursor.fetchone()
#         conn.close()
#         if user_data:
#             user = User()
#             user.id = user_data[0]
#             login_user(user)
#             return redirect(url_for("home"))
#         return "Invalid credentials"
#     return render_template("login.html")

# @app.route("/home")
# @login_required
# def home():
#     return render_template("home.html")

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()  
#     return redirect(url_for("index"))

# @app.route("/crop")
# @login_required
# def crop():
#     return render_template("crop.html")

# @app.route("/predict", methods=["POST"])
# @login_required
# def predict():
#     try:
#         data = [float(request.form[key]) for key in 
#                 ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "ph", "Rainfall"]]

#         print("🔹 Received Input:", data)  

#         if crop_model is None:
#             print("❌ Model not loaded!")
#             return jsonify({"error": "Model not loaded!"})

#         prediction = crop_model.predict([np.array(data)])[0]
#         print("✅ Prediction Output:", prediction)
        
#         return jsonify({"prediction": prediction})
#     except Exception as e:
#         print("❌ Error:", str(e))  
#         return jsonify({"error": str(e)})

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# import sqlite3
# import os
# import pickle
# import numpy as np
# import cv2
# import tensorflow as tf
# from werkzeug.utils import secure_filename
# from weather.weather import get_weather_data  # Assuming you have a function to fetch weather data

# app = Flask(__name__)
# app.secret_key = "supersecretkey"

# # Setup Flask-Login
# login_manager = LoginManager(app)
# login_manager.login_view = "index"

# # Load trained crop prediction model with error handling
# try:
#     crop_model = pickle.load(open("model/model.pkl", "rb"))
#     print("✅ Crop model loaded successfully!")
# except Exception as e:
#     print("❌ Error loading crop model:", e)
#     crop_model = None

# # Load trained soil classifier model
# try:
#     soil_model = tf.keras.models.load_model("soil_classifier/soil_classifier.h5")
#     soil_classes = ["alluvial", "black", "clay", "red"]
# except Exception as e:
#     print("❌ Error loading soil classifier model:", e)
#     soil_model = None
#     soil_classes = []

# # User Authentication
# class User(UserMixin):
#     pass

# @login_manager.user_loader
# def load_user(user_id):
#     conn = sqlite3.connect("database/users.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
#     user_data = cursor.fetchone()
#     conn.close()
#     if user_data:
#         user = User()
#         user.id = user_data[0]
#         return user
#     return None

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#         conn.commit()
#         conn.close()

#         return redirect(url_for("login"))  

#     return render_template("signup.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
#         user_data = cursor.fetchone()
#         conn.close()
#         if user_data:
#             user = User()
#             user.id = user_data[0]
#             login_user(user)
#             return redirect(url_for("home"))
#         return "Invalid credentials"
#     return render_template("login.html")

# @app.route("/home")
# @login_required
# def home():
#     return render_template("home.html")

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()  
#     return redirect(url_for("index"))

# @app.route("/crop")
# @login_required
# def crop():
#     return render_template("crop.html")

# @app.route("/predict", methods=["POST"])
# @login_required
# def predict():
#     try:
#         data = [float(request.form[key]) for key in 
#                 ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "ph", "Rainfall"]]

#         print("🔹 Received Input:", data)  

#         if crop_model is None:
#             print("❌ Model not loaded!")
#             return jsonify({"error": "Model not loaded!"})

#         prediction = crop_model.predict([np.array(data)])[0]
#         print("✅ Prediction Output:", prediction)
        
#         return jsonify({"prediction": prediction})
#     except Exception as e:
#         print("❌ Error:", str(e))  
#         return jsonify({"error": str(e)})

# @app.route("/soil", methods=["GET", "POST"])
# @login_required
# def soil():
#     if request.method == "POST":
#         # Check if the user has uploaded a file
#         if 'soilImage' not in request.files:
#             return jsonify({"error": "No file part"})
        
#         file = request.files['soilImage']
        
#         if file.filename == '':
#             return jsonify({"error": "No selected file"})
        
#         # Save the uploaded file temporarily
#         filename = secure_filename(file.filename)
#         file_path = os.path.join("uploads", filename)
#         file.save(file_path)
        
#         # Preprocess the image for classification
#         image = cv2.imread(file_path)
#         image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))  # Resize the image to the input size
#         image = np.expand_dims(image, axis=0)  # Add batch dimension
#         image = image / 255.0  # Normalize the image

#         # Predict soil type
#         predictions = soil_model.predict(image)
#         predicted_class = np.argmax(predictions, axis=1)[0]  # Get the predicted class index
#         soil_type = soil_classes[predicted_class]  # Get the corresponding soil type

#         # Recommend crops based on soil type
#         recommended_crops = recommend_crops(soil_type)  # Assuming this function will give crop suggestions

#         # Return the result as JSON
#         return jsonify({
#             "soil_type": soil_type,
#             "recommended_crops": recommended_crops
#         })
    
#     return render_template("soil.html")

# @app.route("/weather", methods=["GET", "POST"])
# @login_required
# def weather():
#     weather_data = None  # Store weather data to pass to the template

#     if request.method == "POST":
#         try:
#             city = request.form.get("city")
#             if not city:
#                 return render_template("weather.html", error="City name is required")
            
#             # Assuming you have a function to get weather data
#             weather_data = get_weather_data(city)
            
#             if weather_data.get("error"):
#                 return render_template("weather.html", error=weather_data["error"])
            
#         except Exception as e:
#             print("❌ Error fetching weather data:", e)
#             return render_template("weather.html", error="Failed to fetch weather data")

#     # Return the weather data (if available) or an empty page
#     return render_template("weather.html", weather_data=weather_data)



# if __name__ == "__main__":
#     app.run(debug=True)




# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# import sqlite3
# import os
# import pickle
# import numpy as np
# import cv2
# import tensorflow as tf
# from werkzeug.utils import secure_filename
# from weather.weather import get_weather_data  # Assuming you have a function to fetch weather data

# app = Flask(__name__)
# app.secret_key = "supersecretkey"

# # Setup Flask-Login
# login_manager = LoginManager(app)
# login_manager.login_view = "index"

# # Image size for soil model
# IMG_SIZE = 150  # Ensure this matches the one used during model training

# # Load trained crop prediction model
# try:
#     crop_model = pickle.load(open("model/model.pkl", "rb"))
#     print("✅ Crop model loaded successfully!")
# except Exception as e:
#     print("❌ Error loading crop model:", e)
#     crop_model = None

# # Load trained soil classifier model
# try:
#     soil_model = tf.keras.models.load_model("soil_classifier/soil_classifier.h5")
#     soil_classes = ["alluvial", "black", "clay", "red"]
# except Exception as e:
#     print("❌ Error loading soil classifier model:", e)
#     soil_model = None
#     soil_classes = []

# # Recommend crops based on soil type
# def recommend_crops(soil_type):
#     crops_dict = {
#         "alluvial": ["Rice", "Sugarcane", "Wheat"],
#         "black": ["Cotton", "Groundnut", "Sunflower"],
#         "clay": ["Soybean", "Rice", "Maize"],
#         "red": ["Pulses", "Groundnut", "Millets"]
#     }

#     return ", ".join(crops_dict.get(soil_type, []))

# # User Authentication
# class User(UserMixin):
#     pass

# @login_manager.user_loader
# def load_user(user_id):
#     conn = sqlite3.connect("database/users.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
#     user_data = cursor.fetchone()
#     conn.close()
#     if user_data:
#         user = User()
#         user.id = user_data[0]
#         return user
#     return None

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#         conn.commit()
#         conn.close()

#         return redirect(url_for("login"))

#     return render_template("signup.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
#         user_data = cursor.fetchone()
#         conn.close()
#         if user_data:
#             user = User()
#             user.id = user_data[0]
#             login_user(user)
#             return redirect(url_for("home"))
#         return "Invalid credentials"
#     return render_template("login.html")

# @app.route("/home")
# @login_required
# def home():
#     return render_template("home.html")

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()  
#     return redirect(url_for("index"))

# @app.route("/crop")
# @login_required
# def crop():
#     return render_template("crop.html")

# @app.route("/predict", methods=["POST"])
# @login_required
# def predict():
#     try:
#         data = [float(request.form[key]) for key in 
#                 ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "ph", "Rainfall"]]

#         print("🔹 Received Input:", data)  

#         if crop_model is None:
#             print("❌ Model not loaded!")
#             return jsonify({"error": "Model not loaded!"})

#         prediction = crop_model.predict([np.array(data)])[0]
#         print("✅ Prediction Output:", prediction)
        
#         return jsonify({"prediction": prediction})
#     except Exception as e:
#         print("❌ Error:", str(e))  
#         return jsonify({"error": str(e)})

# @app.route("/soil", methods=["GET", "POST"])
# @login_required
# def soil():
#     if request.method == "POST":
#         # Check if the user has uploaded a file
#         if 'soilImage' not in request.files:
#             return jsonify({"error": "No file part"})
        
#         file = request.files['soilImage']
        
#         if file.filename == '':
#             return jsonify({"error": "No selected file"})
        
#         # Ensure the 'uploads' directory exists before saving the file
#         upload_folder = "uploads"
#         if not os.path.exists(upload_folder):
#             os.makedirs(upload_folder)
        
#         # Save the uploaded file temporarily
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(upload_folder, filename)
#         file.save(file_path)
        
#         # Preprocess the image for classification
#         image = cv2.imread(file_path)
#         image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))  # Resize the image to the input size
#         image = np.expand_dims(image, axis=0)  # Add batch dimension
#         image = image / 255.0  # Normalize the image

#         # Predict soil type
#         predictions = soil_model.predict(image)
#         predicted_class = np.argmax(predictions, axis=1)[0]  # Get the predicted class index
#         soil_type = soil_classes[predicted_class]  # Get the corresponding soil type

#         # Recommend crops based on soil type
#         recommended_crops = recommend_crops(soil_type)  # Using the recommend_crops function

#         # Return the result as JSON
#         return jsonify({
#             "soil_type": soil_type,
#             "recommended_crops": recommended_crops
#         })
    
#     return render_template("soil.html")

# @app.route("/weather", methods=["GET", "POST"])
# @login_required
# def weather():
#     weather_data = None  # Store weather data to pass to the template

#     if request.method == "POST":
#         try:
#             city = request.form.get("city")
#             if not city:
#                 return render_template("weather.html", error="City name is required")
            
#             # Assuming you have a function to get weather data
#             weather_data = get_weather_data(city)
            
#             if weather_data.get("error"):
#                 return render_template("weather.html", error=weather_data["error"])
            
#         except Exception as e:
#             print("❌ Error fetching weather data:", e)
#             return render_template("weather.html", error="Failed to fetch weather data")

#     return render_template("weather.html", weather_data=weather_data)

# if __name__ == "__main__":
#     app.run(debug=True)




# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# import sqlite3
# import os
# import pickle
# import numpy as np
# import cv2
# import tensorflow as tf
# from werkzeug.utils import secure_filename
# from weather.weather import get_weather_data  # Assuming you have a function to fetch weather data

# app = Flask(__name__)
# app.secret_key = "supersecretkey"

# # Setup Flask-Login
# login_manager = LoginManager(app)
# login_manager.login_view = "index"

# # Image size for soil model
# IMG_SIZE = 150  # Ensure this matches the one used during model training

# # Load trained crop prediction model
# try:
#     crop_model = pickle.load(open("model/model.pkl", "rb"))
#     print("✅ Crop model loaded successfully!")
# except Exception as e:
#     print("❌ Error loading crop model:", e)
#     crop_model = None

# # Load trained soil classifier model
# try:
#     soil_model = tf.keras.models.load_model("soil_classifier/soil_classifier.h5")
#     soil_classes = ["alluvial", "black", "clay", "red"]
# except Exception as e:
#     print("❌ Error loading soil classifier model:", e)
#     soil_model = None
#     soil_classes = []

# # Recommend crops based on soil type
# def recommend_crops(soil_type):
#     crops_dict = {
#         "alluvial": ["Rice", "Sugarcane", "Wheat"],
#         "black": ["Cotton", "Groundnut", "Sunflower"],
#         "clay": ["Soybean", "Rice", "Maize"],
#         "red": ["Pulses", "Groundnut", "Millets"]
#     }
#     return ", ".join(crops_dict.get(soil_type, []))

# # User Authentication
# class User(UserMixin):
#     pass

# @login_manager.user_loader
# def load_user(user_id):
#     conn = sqlite3.connect("database/users.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
#     user_data = cursor.fetchone()
#     conn.close()
#     if user_data:
#         user = User()
#         user.id = user_data[0]
#         return user
#     return None

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#         conn.commit()
#         conn.close()

#         return redirect(url_for("login"))

#     return render_template("signup.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     error_message = None  # Initialize error_message variable
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         conn = sqlite3.connect("database/users.db")
#         cursor = conn.cursor()
#         cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
#         user_data = cursor.fetchone()
#         conn.close()

#         if user_data:
#             user = User()
#             user.id = user_data[0]
#             login_user(user)
#             return redirect(url_for("home"))
#         else:
#             error_message = "Invalid username or password"  # Set error message for invalid credentials

#     return render_template("login.html", error_message=error_message)

# @app.route("/home")
# @login_required
# def home():
#     return render_template("home.html")

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("index"))

# @app.route("/crop")
# @login_required
# def crop():
#     return render_template("crop.html")

# @app.route("/predict", methods=["POST"])
# @login_required
# def predict():
#     try:
#         data = [float(request.form[key]) for key in 
#                 ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "ph", "Rainfall"]]

#         print("🔹 Received Input:", data)

#         if crop_model is None:
#             print("❌ Model not loaded!")
#             return jsonify({"error": "Model not loaded!"})

#         prediction = crop_model.predict([np.array(data)])[0]
#         print("✅ Prediction Output:", prediction)
        
#         return jsonify({"prediction": prediction})
#     except Exception as e:
#         print("❌ Error:", str(e))
#         return jsonify({"error": str(e)})

# @app.route("/soil", methods=["GET", "POST"])
# @login_required
# def soil():
#     if request.method == "POST":
#         # Check if the user has uploaded a file
#         if 'soilImage' not in request.files:
#             return jsonify({"error": "No file part"})
        
#         file = request.files['soilImage']
        
#         if file.filename == '':
#             return jsonify({"error": "No selected file"})
        
#         # Ensure the 'uploads' directory exists before saving the file
#         upload_folder = "uploads"
#         if not os.path.exists(upload_folder):
#             os.makedirs(upload_folder)
        
#         # Save the uploaded file temporarily
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(upload_folder, filename)
#         file.save(file_path)
        
#         # Preprocess the image for classification
#         image = cv2.imread(file_path)
#         image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))  # Resize the image to the input size
#         image = np.expand_dims(image, axis=0)  # Add batch dimension
#         image = image / 255.0  # Normalize the image

#         # Predict soil type
#         predictions = soil_model.predict(image)
#         predicted_class = np.argmax(predictions, axis=1)[0]  # Get the predicted class index
#         soil_type = soil_classes[predicted_class]  # Get the corresponding soil type

#         # Recommend crops based on soil type
#         recommended_crops = recommend_crops(soil_type)  # Using the recommend_crops function

#         # Return the result as JSON
#         return jsonify({
#             "soil_type": soil_type,
#             "recommended_crops": recommended_crops
#         })
    
#     return render_template("soil.html")

# @app.route("/weather", methods=["GET", "POST"])
# @login_required
# def weather():
#     weather_data = None  # Store weather data to pass to the template

#     if request.method == "POST":
#         try:
#             city = request.form.get("city")
#             if not city:
#                 return render_template("weather.html", error="City name is required")
            
#             # Assuming you have a function to get weather data
#             weather_data = get_weather_data(city)
            
#             if weather_data.get("error"):
#                 return render_template("weather.html", error=weather_data["error"])
            
#         except Exception as e:
#             print("❌ Error fetching weather data:", e)
#             return render_template("weather.html", error="Failed to fetch weather data")

#     return render_template("weather.html", weather_data=weather_data)

# if __name__ == "__main__":
#     app.run(debug=True)




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
from weather.weather import get_weather_data  # Assuming you have a function to fetch weather data

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "index"

# Image size for soil model
IMG_SIZE = 150  # Ensure this matches the one used during model training

# Load trained crop prediction model
try:
    crop_model = pickle.load(open("model/model.pkl", "rb"))
    print("✅ Crop model loaded successfully!")
except Exception as e:
    print("❌ Error loading crop model:", e)
    crop_model = None

# Load trained soil classifier model
try:
    soil_model = tf.keras.models.load_model("soil_classifier/soil_classifier.h5")
    soil_classes = ["alluvial", "black", "clay", "red"]
except Exception as e:
    print("❌ Error loading soil classifier model:", e)
    soil_model = None
    soil_classes = []

# Recommend crops based on soil type
def recommend_crops(soil_type):
    crops_dict = {
        "alluvial": ["Rice", "Sugarcane", "Wheat"],
        "black": ["Cotton", "Groundnut", "Sunflower"],
        "clay": ["Soybean", "Rice", "Maize"],
        "red": ["Pulses", "Groundnut", "Millets"]
    }
    return ", ".join(crops_dict.get(soil_type, []))

# User Authentication
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
    error_message = None  # Initialize error_message variable
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
            error_message = "Invalid username or password"  # Set error message for invalid credentials

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
            print("❌ Model not loaded!")
            return jsonify({"error": "Model not loaded!"})

        prediction = crop_model.predict([np.array(data)])[0]
        print("✅ Prediction Output:", prediction)
        
        return jsonify({"prediction": prediction})
    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)})

@app.route("/soil", methods=["GET", "POST"])
@login_required
def soil():
    if request.method == "POST":
        # Check if the user has uploaded a file
        if 'soilImage' not in request.files:
            return jsonify({"error": "No file part"})
        
        file = request.files['soilImage']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"})
        
        # Ensure the 'uploads' directory exists before saving the file
        upload_folder = "uploads"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # Save the uploaded file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Preprocess the image for classification
        image = cv2.imread(file_path)
        image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))  # Resize the image to the input size
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        image = image / 255.0  # Normalize the image

        # Predict soil type
        predictions = soil_model.predict(image)
        
        # Print raw predictions for analysis
        print("🔹 Raw predictions:", predictions)

        # Confidence threshold to decide on uncertain predictions
        confidence_threshold = 0.6
        if max(predictions[0]) < confidence_threshold:
            soil_type = "Uncertain"
        else:
            predicted_class = np.argmax(predictions, axis=1)[0]  # Get the predicted class index
            soil_type = soil_classes[predicted_class]  # Get the corresponding soil type

        print("🔹 Predicted class:", predicted_class, "Predicted soil type:", soil_type)

        # Recommend crops based on soil type
        recommended_crops = recommend_crops(soil_type)  # Using the recommend_crops function

        # Return the result as JSON
        return jsonify({
            "soil_type": soil_type,
            "recommended_crops": recommended_crops
        })
    
    return render_template("soil.html")

@app.route("/weather", methods=["GET", "POST"])
@login_required
def weather():
    weather_data = None  # Store weather data to pass to the template

    if request.method == "POST":
        try:
            city = request.form.get("city")
            if not city:
                return render_template("weather.html", error="City name is required")
            
            # Assuming you have a function to get weather data
            weather_data = get_weather_data(city)
            
            if weather_data.get("error"):
                return render_template("weather.html", error=weather_data["error"])
            
        except Exception as e:
            print("❌ Error fetching weather data:", e)
            return render_template("weather.html", error="Failed to fetch weather data")

    return render_template("weather.html", weather_data=weather_data)

if __name__ == "__main__":
    app.run(debug=True)



