# Avalanche Forecast Dashboard

A modern web application for avalanche risk prediction using machine learning models. This project analyzes weather data to predict avalanche danger levels using multiple ML algorithms.

## 🏔️ Features

- **Interactive Dashboard**: Modern, responsive web interface built with Flask and Bootstrap
- **Multiple ML Models**: 
  - Neural Network (MLP Classifier)
  - Logistic Regression
  - Hierarchical Agglomerative Clustering (HAC)
- **Data Visualization**: 
  - Interactive charts using Plotly
  - Geographic mapping with Leaflet
  - Weather statistics and correlation matrices
- **Real-time Prediction**: Input weather conditions and get instant avalanche risk predictions
- **Data Exploration**: Comprehensive analysis of historical avalanche and weather data

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Or on Windows:
   ```powershell
   pip install uv
   ```

2. **Clone or navigate to the project directory**:
   ```bash
   cd avalanche-forcast
   ```

3. **Install dependencies and run the application**:
   ```bash
   uv sync
   uv run python app.py
   ```

   Or use the convenient startup script:
   ```bash
   ./start.sh  # Linux/Mac
   start.bat    # Windows
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 🌐 Free Cloud Deployment

### 🚀 Railway (Recommended - Free Tier)
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app)
3. Connect your GitHub repo
4. Railway auto-deploys your Docker app!
5. Get a live URL like: `https://avalanche-forcast-production.up.railway.app`

### 🐳 Render (Free Tier)
1. Push your code to GitHub  
2. Go to [render.com](https://render.com)
3. Connect your GitHub repo
4. Select "Docker" environment
5. Deploy with one click!

### 🐳 Local Docker Deployment
```bash
# Quick deployment
./deploy.sh

# Manual Docker deployment
docker-compose up --build -d
```

### 🐍 Traditional Python Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Start with Gunicorn (production WSGI server)
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```

## 📊 Data Structure

The application uses the following weather features for prediction:

- `maxtempC`: Maximum temperature in Celsius
- `mintempC`: Minimum temperature in Celsius  
- `totalSnow_cm`: Total snowfall in centimeters
- `tempC`: Current temperature in Celsius
- `windspeedKmph`: Wind speed in km/h
- `winddirDegree`: Wind direction in degrees
- `precipMM`: Precipitation in millimeters
- `humidity`: Humidity percentage

## 🤖 Machine Learning Models

### 1. Neural Network (MLP)
- Multi-layer perceptron classifier
- Hidden layers: 64, 32 neurons
- Uses early stopping and validation
- Provides probability scores

### 2. Logistic Regression
- Linear classification model
- Fast training and prediction
- Good baseline model
- Provides probability scores

### 3. Hierarchical Agglomerative Clustering
- Unsupervised clustering approach
- Groups similar weather patterns
- Binary classification (safe/dangerous)

## 🎯 How to Use

### Making Predictions

1. **Navigate to the dashboard** at `http://localhost:5000`
2. **Enter weather conditions** in the prediction form:
   - Temperature ranges (min/max/current)
   - Snow accumulation
   - Wind conditions
   - Precipitation and humidity
3. **Select a model** from the dropdown
4. **Click "Predict Risk"** to get results
5. **View the prediction** with confidence scores

### Exploring Data

- **Statistics Overview**: View total records, dangerous events, and locations
- **Weather Charts**: Analyze weather feature distributions
- **Correlation Matrix**: Understand feature relationships
- **Interactive Map**: Explore avalanche locations geographically

## 📁 Project Structure

```
avalanche-forcast/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main dashboard template
├── data/                 # Data files and model outputs
├── process/              # Original ML model scripts
├── preprocess/           # Data preprocessing scripts
├── scraper/              # Data collection scripts
└── README.md            # This file
```

## 🔧 API Endpoints

- `GET /api/data` - Get dataset statistics
- `GET /api/locations` - Get location data for mapping
- `GET /api/weather_stats` - Get weather feature statistics
- `GET /api/correlation` - Get feature correlation matrix
- `POST /api/predict` - Make avalanche risk prediction

## 📈 Model Performance

The models are trained on historical avalanche data with the following features:
- Weather conditions (temperature, wind, precipitation)
- Snow accumulation data
- Geographic location information
- Historical avalanche occurrence records

## 🛠️ Development

### uv Commands

- `uv sync` - Install dependencies from pyproject.toml
- `uv run python app.py` - Run the application
- `uv add <package>` - Add a new dependency
- `uv remove <package>` - Remove a dependency
- `uv lock` - Generate/update the lock file

### Adding New Features

1. **New ML Models**: Add to the `AvalanchePredictor` class in `app.py`
2. **Visualizations**: Extend the JavaScript functions in `index.html`
3. **API Endpoints**: Add new routes to the Flask app

### Data Updates

#### Updating Avalanche Data
To update the dataset with new avalanche records:
1. Run the improved scraper to get latest avalanche data:
   ```bash
   cd scraper
   uv run python scraper_improved.py
   ```

2. Merge new avalanche data with existing coordinates:
   ```bash
   uv run python merge_new_data.py avalanches_scraped_YYYYMMDD_HHMMSS.csv ../avalanches_lat_long.csv avalanches_enhanced.csv
   ```

#### Updating Weather Data
To fetch historical weather data for new avalanche records:

1. **Set up OpenWeatherMap API key**:
   ```bash
   cd scraper
   uv run python setup_api.py
   ```
   Or manually set the environment variable:
   ```bash
   export OPENWEATHER_API_KEY='your_api_key_here'
   ```

2. **Fetch weather data**:
   ```bash
   uv run python update_weather_data.py
   ```

3. **Restart the application** to use the updated dataset:
   ```bash
   uv run python app.py
   ```

#### Manual Data Updates
To manually update the dataset:
1. Replace `allData.csv` with new data
2. Ensure the same column structure
3. Restart the application to retrain models

## 📝 Original Project

This webapp is built on top of the original avalanche forecasting project that included:
- Weather data scraping and preprocessing
- Multiple ML model implementations
- Feature selection and optimization
- Model performance analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Always consult with professional avalanche forecasters and local authorities before making safety decisions in avalanche terrain.

---

**Built with ❤️ using Flask, scikit-learn, and modern web technologies**
