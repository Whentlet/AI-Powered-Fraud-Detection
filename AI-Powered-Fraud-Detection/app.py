from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Define model and scaler paths
MODEL_PATH = 'models/isolation_forest_model.pkl'
SCALER_PATH = 'models/standard_scaler.pkl'

# Load pre-trained model and scaler (or train if not found)
def load_or_train_model():
    global model, scaler
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        logging.info('Loading pre-trained model and scaler.')
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
    else:
        logging.warning('Model or scaler not found. Training a new model.')
        # Generate dummy data for training
        np.random.seed(42)
        num_samples = 10000
        data = np.random.randn(num_samples, 5) * 10 # 5 features
        # Introduce some anomalies
        data[np.random.choice(num_samples, 100), :] += np.random.randn(100, 5) * 50
        
        df_train = pd.DataFrame(data, columns=[f'feature_{i}' for i in range(5)])
        
        # Train scaler
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df_train)
        joblib.dump(scaler, SCALER_PATH)
        
        # Train Isolation Forest model
        model = IsolationForest(random_state=42, contamination=0.01) # Assuming 1% anomalies
        model.fit(scaled_data)
        joblib.dump(model, MODEL_PATH)
        logging.info('New model and scaler trained and saved.')

load_or_train_model()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        df = pd.DataFrame(data, index=[0])
        
        # Ensure input features match training features
        if list(df.columns) != [f'feature_{i}' for i in range(5)]:
            return jsonify({'error': 'Invalid input features. Expected 5 features named feature_0 to feature_4.'}), 400

        # Preprocess data (e.g., scaling)
        processed_data = scaler.transform(df)
        
        # Make prediction (-1 for anomaly, 1 for normal)
        prediction = model.predict(processed_data)
        
        # Convert prediction to boolean for fraud detection
        fraud_detected = bool(prediction[0] == -1)
        
        logging.info(f'Prediction made: Fraud Detected = {fraud_detected}')
        return jsonify({'fraud_detected': fraud_detected})

    except Exception as e:
        logging.error(f'Error during prediction: {e}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
