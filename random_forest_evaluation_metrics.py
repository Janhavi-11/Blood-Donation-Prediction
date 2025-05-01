import pickle
from sklearn.ensemble import RandomForestClassifier  
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix
import pandas as pd

# Load your data
data = pd.read_csv('blood_donation_dataset.csv')

# Define features and target variable
X = data[['Age', 'Gender', 'Weight', 'Height', 'Hemoglobin', 'Blood Type','Last Donation (months)', 'Total Number of Donations']].copy()  # Make a copy to avoid SettingWithCopyWarning
y = data['Donation Status']

# Encode 'Blood Type' if it's a categorical feature using .loc
X.loc[:, 'Blood Type'] = X['Blood Type'].astype('category').cat.codes

# Encode 'Gender' if it's a categorical feature using .loc
X.loc[:, 'Gender'] = data['Gender'].astype('category').cat.codes  # Assuming your dataset has a 'Gender' column

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a model (Random Forest example)
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Save the trained model and scaler
pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(scaler, open('scaler.pkl', 'wb'))

# Check the accuracy and precision
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label=1)  # Change pos_label if necessary
conf_matrix = confusion_matrix(y_test, y_pred)

# Print the results
print(f"\nModel accuracy:- {accuracy * 100:.2f}%")
print(f"\nModel precision:- {precision:.2f}")
print("\nConfusion Matrix:-")
print(conf_matrix)
