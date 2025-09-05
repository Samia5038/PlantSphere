

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load the crop recommendation dataset
df = pd.read_csv("Crop_recommendation.csv")
print("Columns in dataset:", df.columns.tolist())

# Use the 'label' column as the target variable
X = df.drop(columns=["label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# Save the model
pickle.dump(model, open("model/model.pkl", "wb"))
print("Crop prediction model trained and saved successfully!")

