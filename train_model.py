import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the preprocessed data
X_train = pd.read_csv('X_train_scaled.csv')
X_test = pd.read_csv('X_test_scaled.csv')
y_train = pd.read_csv('y_train.csv')
y_test = pd.read_csv('y_test.csv')

# Debug prints to check the contents of the files
print("X_train head:")
print(X_train.head())
print("y_train head:")
print(y_train.head())

print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train.values.ravel())  # Use .values.ravel() to convert y_train to the correct shape

# Evaluate the model
y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy Score:", accuracy_score(y_test, y_pred))

# Save the trained model
joblib.dump(model, 'random_forest_model.joblib')
print("Model training completed and saved.")
