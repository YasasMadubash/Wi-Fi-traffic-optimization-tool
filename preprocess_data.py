import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib  # Import joblib

# Load the captured traffic data
df = pd.read_csv('captured_traffic.csv')

# Print initial data for debugging
print("Initial DataFrame:")
print(df.head())

# Preprocess the 'protocol' column to convert it to integer
df['protocol'] = df['protocol'].apply(lambda x: int(x.strip('()').split(',')[0]))

# Select features and target (for demonstration, I'm assuming 'length' is the target)
# You should adjust this based on your actual target column
features = ['length', 'src_port', 'dst_port', 'protocol']
target = 'length'

X = df[features]
y = df[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert scaled arrays back to DataFrames
X_train_scaled = pd.DataFrame(X_train_scaled, columns=features)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=features)

# Save the processed data
X_train_scaled.to_csv('X_train_scaled.csv', index=False)
X_test_scaled.to_csv('X_test_scaled.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)
joblib.dump(scaler, 'scaler.joblib')  # Save the scaler

print("Data preprocessing completed and files saved.")
