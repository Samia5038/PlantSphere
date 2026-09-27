# PlantSphere – AI-Based Smart Agriculture Assistant

## Overview

PlantSphere is a Flask-based machine learning application designed to support agricultural decision-making through **crop prediction, soil image classification, crop recommendation, and weather information**.

The system combines structured agricultural data and soil images to provide AI-assisted insights for crop selection and soil analysis.

## Technologies

* **Python** for application development.
* **Flask** for the web application and backend.
* **Scikit-learn** for crop prediction.
* **Random Forest** for agricultural data classification.
* **TensorFlow / Keras** for soil image classification.
* **OpenCV** for image processing.
* **Pandas & NumPy** for data processing.
* **SQLite** for database management.
* **HTML, CSS & JavaScript** for the frontend.

## Features

#### Crop Prediction

* Predicts suitable crops using N, P, K, temperature, humidity, pH, and rainfall.
* Uses a Random Forest classification model.

#### Soil Classification

* Accepts uploaded soil images.
* Classifies soil into predefined categories using a CNN-based model.
* Provides crop recommendations based on the predicted soil type.

#### Weather Information

* Retrieves weather information for a selected location.
* Provides additional environmental context for agricultural decisions.

## Machine Learning Workflow

```text
Agricultural Parameters
          |
          v
   Random Forest Model
          |
          v
    Crop Prediction


    Soil Image
          |
          v
      CNN Model
          |
          v
   Soil Classification
          |
          v
 Crop Recommendation
```

## Code Management

* Machine learning models and training scripts are separated from the application logic.
* Data processing and prediction functions are organized into reusable components.
* Flask routes and application logic are structured separately.
* Image preprocessing is handled before CNN-based classification.
* Clear naming conventions are followed for variables, functions, and files.
* Error handling is implemented for invalid inputs and application-level exceptions.
* The project structure is organized to support future model and feature extensions.

## Installation

```bash
git clone https://github.com/Samia5038/PlantSphere.git
cd PlantSphere
pip install -r requirements.txt
python app.py
```

Run the application at:

```text
http://127.0.0.1:5000
```

## Future Improvements

* Expand agricultural and soil-image datasets.
* Improve soil classification performance.
* Integrate real-time soil sensor data.
* Incorporate explainable AI techniques.
* Develop weather-aware crop recommendations.
* Evaluate the system using larger and geographically diverse datasets.

## Academic Context

PlantSphere is developed as an academic project demonstrating the integration of **Machine Learning, Computer Vision, and Web Technologies** for agricultural decision support.

## Author

**Samia Mahbub**
Department of Computer Science and Engineering
University of Chittagong

[GitHub Repository](https://github.com/Samia5038/PlantSphere)

