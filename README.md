# AI-Powered Fraud Detection

This project implements an AI-powered system for real-time fraud detection. It utilizes various machine learning techniques to identify anomalous transactions and prevent financial fraud.

## Features
- **Anomaly Detection**: Unsupervised learning models to identify unusual patterns.
- **Supervised Learning**: Classification models (e.g., Random Forest, XGBoost) trained on labeled data.
- **Real-time Processing**: Integration with streaming data platforms for immediate analysis.
- **Data Visualization**: Interactive dashboards to monitor fraud trends and model performance.

## Technologies
- Python
- Scikit-learn
- Pandas, NumPy
- Apache Kafka (for streaming)
- Flask (for API)

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Whentlet/AI-Powered-Fraud-Detection.git
   cd AI-Powered-Fraud-Detection
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the fraud detection service:
   ```bash
   python app.py
   ```

## Usage
Integrate with your transaction processing system to send transaction data to the API endpoint for real-time fraud scoring.

## License
This project is licensed under the MIT License.
