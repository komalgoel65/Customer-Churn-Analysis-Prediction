from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# --- Load trained model and its columns ---
model = pickle.load(open('model.pkl', 'rb'))
model_columns = pickle.load(open('model_columns.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        form = request.form

        # Safe type conversion helpers
        def safe_float(value):
            try:
                return float(value)
            except:
                return 0.0

        def safe_int(value):
            try:
                return int(value)
            except:
                return 0

        # --- Collect user inputs ---
        data = {
            'gender': form.get('gender', 'Male'),
            'SeniorCitizen': safe_int(form.get('SeniorCitizen', 0)),
            'Partner': form.get('Partner', 'No'),
            'Dependents': form.get('Dependents', 'No'),
            'tenure': safe_float(form.get('tenure', 0)),
            'PhoneService': form.get('PhoneService', 'Yes'),
            'MultipleLines': form.get('MultipleLines', 'No'),
            'InternetService': form.get('InternetService', 'DSL'),
            'OnlineSecurity': form.get('OnlineSecurity', 'No'),
            'OnlineBackup': form.get('OnlineBackup', 'No'),
            'DeviceProtection': form.get('DeviceProtection', 'No'),
            'TechSupport': form.get('TechSupport', 'No'),
            'StreamingTV': form.get('StreamingTV', 'No'),
            'StreamingMovies': form.get('StreamingMovies', 'No'),
            'Contract': form.get('Contract', 'Month-to-month'),
            'PaperlessBilling': form.get('PaperlessBilling', 'Yes'),
            'PaymentMethod': form.get('PaymentMethod', 'Electronic check'),
            'MonthlyCharges': safe_float(form.get('MonthlyCharges', 0)),
            'TotalCharges': safe_float(form.get('TotalCharges', 0))
        }

        # --- Prepare DataFrame for prediction ---
        df = pd.DataFrame([data])
        df = pd.get_dummies(df)

        # Align columns with training data
        df = df.reindex(columns=model_columns, fill_value=0)

        # --- Make Prediction ---
        prediction = model.predict(df)[0]

        if prediction == 1:
            result = "❌ Customer is likely to leave."
        else:
            result = "✅ Customer is likely to stay."

        return render_template('index.html', prediction=result)

    except Exception as e:
        return render_template('index.html', prediction=f"⚠️ Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
