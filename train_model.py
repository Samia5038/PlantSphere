# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# import pickle

# # Load dataset
# df = pd.read_csv("Crop_recommendation.csv")

# # Feature selection
# X = df.drop(columns=["crop"])
# y = df["crop"]

# # Split dataset
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train model
# model = DecisionTreeClassifier()
# model.fit(X_train, y_train)

# # Save model
# pickle.dump(model, open("model/model.pkl", "wb"))

# print("Model trained and saved successfully!")







# import pandas as pd
# import pickle
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier

# # Load dataset
# df = pd.read_csv("Crop_recommendation.csv")
# print("Columns in dataset:", df.columns.tolist())

# # Use 'label' column as the target variable
# X = df.drop(columns=["label"])
# y = df["label"]

# # Split dataset into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model using RandomForestClassifier
# model = RandomForestClassifier()
# model.fit(X_train, y_train)

# # Optionally, evaluate the model accuracy
# accuracy = model.score(X_test, y_test)
# print("Model Accuracy:", accuracy)

# # Save the trained model to a file
# pickle.dump(model, open("model/model.pkl", "wb"))

# print("Model trained and saved successfully!")





# import pandas as pd
# import pickle
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier

# # Load dataset
# df = pd.read_csv("Crop_recommendation.csv")
# print("Columns in dataset:", df.columns.tolist())

# # Use 'label' column as target
# X = df.drop(columns=["label"])
# y = df["label"]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model = RandomForestClassifier()
# model.fit(X_train, y_train)

# # Optionally, evaluate model accuracy
# accuracy = model.score(X_test, y_test)
# print("Model Accuracy:", accuracy)

# # Save the model
# pickle.dump(model, open("model/model.pkl", "wb"))
# print("Model trained and saved successfully!")





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
