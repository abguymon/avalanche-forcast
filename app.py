from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import json
import os
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import LabelBinarizer, StandardScaler
from sklearn.model_selection import train_test_split
import plotly.graph_objs as go
import plotly.utils
import folium
from datetime import datetime

app = Flask(__name__)

class AvalanchePredictor:
    def __init__(self):
        self.data = None
        self.models = {}
        self.scaler = StandardScaler()
        self.label_binarizer = LabelBinarizer()
        self.feature_columns = ['maxtempC', 'mintempC', 'totalSnow_cm', 'tempC', 
                               'windspeedKmph', 'winddirDegree', 'precipMM', 'humidity']
        
    def load_data(self, file_path='allData.csv'):
        """Load and preprocess the avalanche data"""
        try:
            self.data = pd.read_csv(file_path)
            print(f"Loaded data shape: {self.data.shape}")
            
            # Clean the data - remove rows with NaN in feature columns
            feature_cols = self.feature_columns + ['Dangerous']
            self.data = self.data.dropna(subset=feature_cols)
            print(f"After cleaning shape: {self.data.shape}")
            
            # Convert Dangerous column to boolean if it's not already
            if self.data['Dangerous'].dtype == 'object':
                self.data['Dangerous'] = self.data['Dangerous'].map({'TRUE': True, 'FALSE': False})
            else:
                # Already boolean, just ensure it's proper boolean type
                self.data['Dangerous'] = self.data['Dangerous'].astype(bool)
            
            # Ensure all feature columns are numeric
            for col in self.feature_columns:
                if col in self.data.columns:
                    self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
            
            # Fix Depth column - convert to numeric and handle corrupted values
            if 'Depth' in self.data.columns:
                self.data['Depth'] = pd.to_numeric(self.data['Depth'], errors='coerce')
                self.data['Depth'] = self.data['Depth'].fillna(0)
            
            # Fix Width column - convert to numeric and handle corrupted values  
            if 'Width' in self.data.columns:
                self.data['Width'] = pd.to_numeric(self.data['Width'], errors='coerce')
                self.data['Width'] = self.data['Width'].fillna(0)
            
            # Remove any remaining NaN values
            self.data = self.data.dropna(subset=self.feature_columns + ['Dangerous'])
            print(f"Final data shape: {self.data.shape}")
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def train_models(self):
        """Train all ML models"""
        if self.data is None:
            return False
            
        # Prepare features and labels
        X = self.data[self.feature_columns].values
        y = self.data['Dangerous'].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=42)
        
        # Train MLP Classifier
        self.models['mlp'] = MLPClassifier(
            hidden_layer_sizes=(64, 32), 
            max_iter=1000, 
            random_state=42
        )
        self.models['mlp'].fit(X_train, y_train)
        
        # Train Logistic Regression
        self.models['logistic'] = LogisticRegression(random_state=42, max_iter=1000)
        self.models['logistic'].fit(X_train, y_train)
        
        # Train HAC (for clustering)
        self.models['hac'] = AgglomerativeClustering(n_clusters=2)
        self.models['hac'].fit(X_scaled)
        
        return True
    
    def predict(self, weather_data, model_type='mlp'):
        """Make prediction using specified model"""
        if model_type not in self.models:
            return None
            
        # Scale the input data
        weather_array = np.array([weather_data]).reshape(1, -1)
        weather_scaled = self.scaler.transform(weather_array)
        
        if model_type == 'hac':
            prediction = self.models[model_type].predict(weather_scaled)[0]
            return bool(prediction)
        else:
            prediction = self.models[model_type].predict(weather_scaled)[0]
            probability = self.models[model_type].predict_proba(weather_scaled)[0]
            return {
                'prediction': bool(prediction),
                'probability': float(max(probability))
            }

# Initialize the predictor
predictor = AvalanchePredictor()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/test')
def test():
    """Test page for debugging"""
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>API Test</title></head>
    <body>
        <h1>API Test</h1>
        <div id="results"></div>
        <script>
            async function testAPI() {
                const resultsDiv = document.getElementById('results');
                try {
                    const response = await fetch('/api/data');
                    const data = await response.json();
                    resultsDiv.innerHTML = `
                        <h2>Data API Results:</h2>
                        <p>Total Records: ${data.total_records}</p>
                        <p>Dangerous Count: ${data.dangerous_count}</p>
                        <p>Locations: ${data.locations}</p>
                    `;
                } catch (error) {
                    resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
                }
            }
            document.addEventListener('DOMContentLoaded', testAPI);
        </script>
    </body>
    </html>
    '''

@app.route('/api/data')
def get_data():
    """API endpoint to get data summary"""
    if predictor.data is None:
        if not predictor.load_data():
            return jsonify({'error': 'Failed to load data'}), 500
    
    # Get basic statistics
    stats = {
        'total_records': int(len(predictor.data)),
        'dangerous_count': int(predictor.data['Dangerous'].sum()),
        'safe_count': int((~predictor.data['Dangerous']).sum()),
        'locations': int(predictor.data['Location'].nunique()),
        'date_range': {
            'start': str(predictor.data['Date'].min()),
            'end': str(predictor.data['Date'].max())
        }
    }
    
    return jsonify(stats)

@app.route('/api/locations')
def get_locations():
    """Get location data for mapping"""
    if predictor.data is None:
        if not predictor.load_data():
            return jsonify({'error': 'Failed to load data'}), 500
    
    locations = predictor.data.groupby(['Area', 'latitude', 'longitude']).agg({
        'Dangerous': ['count', 'sum'],
        'Depth': 'mean'
    }).reset_index()
    
    locations.columns = ['Location', 'latitude', 'longitude', 'total_events', 'dangerous_events', 'avg_depth']
    locations['danger_rate'] = locations['dangerous_events'] / locations['total_events']
    
    # Convert to native Python types for JSON serialization
    locations_dict = locations.to_dict('records')
    for location in locations_dict:
        for key, value in location.items():
            if hasattr(value, 'item'):  # numpy scalar
                location[key] = value.item()
            elif hasattr(value, 'tolist'):  # numpy array
                location[key] = value.tolist()
    
    return jsonify(locations_dict)

@app.route('/api/weather_stats')
def get_weather_stats():
    """Get weather statistics for visualization"""
    if predictor.data is None:
        if not predictor.load_data():
            return jsonify({'error': 'Failed to load data'}), 500
    
    weather_stats = {}
    for col in predictor.feature_columns:
        if col in predictor.data.columns:
            weather_stats[col] = {
                'mean': float(predictor.data[col].mean()),
                'std': float(predictor.data[col].std()),
                'min': float(predictor.data[col].min()),
                'max': float(predictor.data[col].max())
            }
    
    return jsonify(weather_stats)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make avalanche prediction"""
    if predictor.data is None:
        if not predictor.load_data():
            return jsonify({'error': 'Failed to load data'}), 500
    
    if not predictor.models:
        if not predictor.train_models():
            return jsonify({'error': 'Failed to train models'}), 500
    
    data = request.get_json()
    model_type = data.get('model', 'mlp')
    
    # Extract weather parameters
    weather_data = []
    for col in predictor.feature_columns:
        weather_data.append(float(data.get(col, 0)))
    
    try:
        result = predictor.predict(weather_data, model_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/correlation')
def get_correlation():
    """Get correlation matrix for weather features"""
    if predictor.data is None:
        if not predictor.load_data():
            return jsonify({'error': 'Failed to load data'}), 500
    
    # Calculate correlation matrix
    corr_data = predictor.data[predictor.feature_columns + ['Dangerous']].corr()
    
    return jsonify(corr_data.to_dict())

def main():
    """Main entry point for the application"""
    # Load data and train models on startup
    if predictor.load_data():
        predictor.train_models()
        print("Models trained successfully!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
