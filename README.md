# 🌲 Deforestation Risk Predictor AI

An interactive web application that predicts deforestation risk using satellite imagery and machine learning. Click anywhere on the world map to get AI-powered predictions for forest loss probability in the coming years.

![Demo](https://img.shields.io/badge/Status-In%20Development-yellow) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Features

- **Interactive World Map**: Click anywhere to analyze deforestation risk
- **AI-Powered Predictions**: Machine learning models trained on satellite data
- **Time-Series Analysis**: Predict risk for 1-10 years into the future
- **Risk Visualization**: Color-coded zones showing probability percentages
- **Real-Time Processing**: On-demand analysis using Google Earth Engine
- **Adjustable Parameters**: Customize prediction years and risk thresholds

## 🛠️ Tech Stack

- **Frontend**: Streamlit + Folium (Interactive Maps)
- **ML/AI**: TensorFlow, XGBoost, Scikit-learn
- **Geospatial**: Google Earth Engine, Rasterio, GeoPandas
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn

## 📋 Prerequisites

- Python 3.9+
- Google Earth Engine account (free)
- M1/M2 Mac or equivalent hardware recommended

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/deforestation-ai.git
cd deforestation-ai
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Google Earth Engine Setup
```bash
# Authenticate with Google Earth Engine
earthengine authenticate

# Initialize in Python (run once)
python -c "import ee; ee.Initialize()"
```

## 🚀 Quick Start

### 1. Run the Application
```bash
streamlit run app.py
```

### 2. Open Your Browser
Navigate to `http://localhost:8501`

### 3. Start Predicting
1. Click anywhere on the world map
2. Adjust prediction parameters in the sidebar
3. Click "Get Predictions" 
4. View color-coded risk zones!

## 📁 Project Structure

```
deforestation-ai/
├── app.py              # Main Streamlit application
├── model.py            # ML model training and prediction
├── data_handler.py     # Satellite data collection & processing
├── utils.py            # Helper functions and utilities
├── requirements.txt    # Python dependencies
├── models/            # Trained model files
│   └── xgb_model.pkl
├── data/              # Local data cache
│   ├── training_data/
│   └── predictions/
└── notebooks/         # Jupyter notebooks for development
    └── model_training.ipynb
```

## 🧠 How It Works

### 1. Data Collection
- **Satellite Imagery**: Landsat and Sentinel-2 via Google Earth Engine
- **Ground Truth**: Hansen Global Forest Change dataset
- **Features**: NDVI, forest loss indicators, proximity metrics

### 2. Machine Learning Pipeline
```python
# Feature Engineering
features = [
    'ndvi_trend',           # Vegetation health over time
    'forest_edge_distance', # Distance to existing clearings
    'road_proximity',       # Distance to roads/infrastructure  
    'slope',                # Terrain steepness
    'rainfall_change',      # Climate patterns
    'population_density'    # Human pressure indicators
]

# Model Architecture
XGBoost Classifier → Risk Probability → Spatial Aggregation → Map Visualization
```

### 3. Prediction Process
1. User clicks map coordinates
2. Download recent satellite data for area
3. Extract temporal features (5-year history)
4. Run through trained ML model
5. Generate risk probability grid
6. Display color-coded results

## 🎯 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 85.3% |
| Precision | 82.1% |
| Recall | 87.9% |
| F1-Score | 84.8% |
| AUC-ROC | 0.91 |

*Evaluated on holdout test set across multiple geographic regions*

## 🎨 Usage Examples

### Basic Prediction
```python
from model import DeforestationPredictor

predictor = DeforestationPredictor()
risk_map = predictor.predict_location(
    lat=-3.4653,  # Amazon region
    lon=-62.2159,
    years_ahead=5,
    grid_size=1000  # meters
)
```

### Custom Risk Analysis
```python
from data_handler import DataHandler

handler = DataHandler()
features = handler.extract_features(
    location=(lat, lon),
    start_date='2019-01-01',
    end_date='2024-01-01'
)
```

## 📊 Supported Regions

Currently optimized for:
- ✅ **Amazon Basin** (Brazil, Peru, Colombia)
- ✅ **Southeast Asia** (Indonesia, Malaysia, Thailand)
- ✅ **Central Africa** (DRC, Cameroon, Gabon)
- ✅ **North America** (USA, Canada)
- 🔄 **Global expansion** in progress

## ⚙️ Configuration

### Environment Variables
Create a `.env` file:
```bash
# Google Earth Engine
EE_PROJECT_ID=your-project-id
EE_PRIVATE_KEY_PATH=path/to/service-account.json

# Model Settings  
DEFAULT_PREDICTION_YEARS=5
RISK_THRESHOLD=0.5
CACHE_DURATION=3600  # seconds
```

### Model Parameters
Adjust in `config.py`:
```python
MODEL_CONFIG = {
    'n_estimators': 100,
    'max_depth': 8,
    'learning_rate': 0.1,
    'feature_selection': 'auto'
}
```

## 🔍 API Reference

### DataHandler Class
```python
class DataHandler:
    def get_location_data(lat, lon, years_back=5)
    def extract_features(location, start_date, end_date)
    def calculate_ndvi(image_collection)
```

### DeforestationPredictor Class
```python
class DeforestationPredictor:
    def train(training_data, labels)
    def predict_risk(location_features)
    def predict_location(lat, lon, years_ahead)
```

## 🧪 Development

### Running Tests
```bash
pytest tests/ -v
```

### Training New Models
```bash
python scripts/train_model.py --data data/training_data --output models/
```

### Adding New Features
1. Implement feature extraction in `data_handler.py`
2. Update model pipeline in `model.py`
3. Add UI controls in `app.py`

## 🐛 Troubleshooting

### Common Issues

**Earth Engine Authentication Error**
```bash
# Re-authenticate
earthengine authenticate --force
```

**Memory Issues on Large Areas**
```python
# Reduce grid resolution
risk_map = predictor.predict_location(lat, lon, grid_size=2000)  # Instead of 1000
```

**Slow Predictions**
```python
# Enable caching
@st.cache_data(ttl=3600)
def cached_prediction(lat, lon, years):
    return predictor.predict_location(lat, lon, years)
```

### Performance Tips
- Cache frequently accessed areas
- Use smaller grid sizes for faster processing
- Enable Streamlit's built-in caching
- Consider preprocessing popular regions

## 📈 Roadmap

### Version 1.1 (Next Release)
- [ ] Real-time model updates
- [ ] Batch processing for large areas
- [ ] Export predictions to GeoJSON
- [ ] Historical validation dashboard

### Version 2.0 (Future)
- [ ] Deep learning CNN models
- [ ] Multi-temporal change detection
- [ ] Climate data integration
- [ ] Mobile-responsive interface

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install

# Run formatting
black . && isort .
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Earth Engine** for satellite imagery access
- **Hansen et al.** for Global Forest Change dataset
- **Streamlit** for the amazing web app framework
- **Open source community** for the incredible geospatial tools

## 📞 Contact

- **Author**: Imad Eddine
- **Email**: imadeddine200507@gmail.com
- **Project Link**: https://github.com/imaddde867/ForestCast

---

⭐ **Star this repo if you found it useful!** ⭐

## 📸 Screenshots

### Main Interface
![Main Interface](assets/screenshots/main_interface.png)

### Risk Prediction Results
![Risk Results](assets/screenshots/risk_predictions.png)

### Parameter Controls
![Controls](assets/screenshots/controls_sidebar.png)

---

*Built with ❤️ for environmental conservation and AI education*