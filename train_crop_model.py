import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load the crop recommendation dataset
df = pd.read_csv("Crop_recommendation.csv")

# Use the 'label' column as the target variable
X = df.drop(columns=["label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
os.makedirs("model", exist_ok=True)
pickle.dump(model, open("model/model.pkl", "wb"))

print("Crop prediction model trained and saved successfully!")
