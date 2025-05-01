from flask import Flask, request, render_template
import numpy as np
import pickle

# Create a Flask application
app = Flask(__name__)

# Load the trained model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve form data
        age = int(request.form['age'])
        gender = request.form['gender']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        hemoglobin = float(request.form['hemoglobin'])
        blood_group = request.form['blood_group']
        last_donation = int(request.form['last_donation'])  # Corrected field name
        total_donations = int(request.form['total_donations'])  # Corrected field name

        # Strict eligibility conditions
        if age < 18:
            result = "Not eligible to donate blood. Age must be 18 or older."
        elif weight < 50:
            result = "Not eligible to donate blood. Weight must be at least 50 kg."
        elif hemoglobin < 12.5:
            result = "Not eligible to donate blood. Hemoglobin must be at least 12.5 g/dL."
        elif last_donation < 2:
            result = "Not eligible to donate blood. Must wait at least 2 months since the last donation."
        else:
            # Encode gender and blood group using dictionaries
            gender_mapping = {'Male': 0, 'Female': 1, 'Other': 2}
            blood_group_mapping = {
                'A+': 0, 'A-': 1, 'B+': 2, 'B-': 3, 'AB+': 4, 'AB-': 5, 'O+': 6, 'O-': 7
            }
            gender_encoded = gender_mapping[gender]
            blood_group_encoded = blood_group_mapping[blood_group]

            # Create a feature array for prediction
            features = np.array([[age, gender_encoded, weight, height, hemoglobin, blood_group_encoded, last_donation, total_donations]])

            # Make a prediction using the loaded model
            prediction = model.predict(features)

            # Interpret the prediction
            if prediction[0] == 1:
                result = "The donor is likely to donate blood."
            else:
                result = "The donor is unlikely to donate blood."

        # Create a prediction message without new lines
        prediction_text = f"{result}"

        # Display the prediction result along with all input values
        return render_template('index.html', prediction_text=prediction_text)
    except Exception as e:
        return render_template('index.html', prediction_text=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
