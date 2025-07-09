# 🚗 Gas Station Recommendation App

An intelligent web application that helps users find the best gas stations based on location, fuel prices, and AI-powered recommendations.

## 🌟 Features

- **📍 Smart Location Detection**: Use GPS or enter any address
- **💰 Real-time Price Comparison**: Compare prices for 87, 89, and 91 fuel grades
- **🤖 AI-Powered Recommendations**: Claude AI analyzes and ranks stations
- **🚗 Cost Analysis**: Includes travel expenses and fuel efficiency
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🌐 Real-time Data**: Live gas station data from Google Maps API

## 🚀 Live Demo

- **Web App**: [Coming Soon - Deploy to get URL]
- **GitHub Pages**: [Coming Soon]

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **APIs**: Google Maps, Claude AI
- **Deployment**: Railway, Render, Docker, GitHub Pages

## 📦 Quick Start

### Prerequisites

- Python 3.9+
- Conda (recommended)
- Google Maps API Key
- Claude API Key

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/gas-station-recommendation.git
   cd gas-station-recommendation
   ```

2. **Set up conda environment**:
   ```bash
   conda create -n gas-reco python=3.11
   conda activate gas-reco
   ```

3. **Install dependencies**:
   ```bash
   cd gas_recommendation_app
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Create .env file
   echo "GOOGLE_MAPS_API_KEY=your_google_maps_api_key" > .env
   echo "CLAUDE_API_KEY=your_claude_api_key" >> .env
   ```

5. **Run the app**:
   ```bash
   python web_app.py
   ```

6. **Open in browser**: http://localhost:8080

## 🚀 Deployment Options

### Option 1: Railway (Recommended)

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**:
   ```bash
   cd deploy
   ./railway_deploy.sh
   ```

### Option 2: Render

1. **Go to Render**: https://render.com
2. **Connect your GitHub repository**
3. **Configure as Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn web_app:app`
4. **Add environment variables** (see below)

### Option 3: Docker

```bash
cd deploy
./docker_deploy.sh
```

### Option 4: GitHub Pages (Static Landing)

```bash
cd deploy
./github_pages_deploy.sh
```

## 🔑 Environment Variables

Set these in your deployment platform:

```bash
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
CLAUDE_API_KEY=your_claude_api_key
FLASK_ENV=production
PORT=8080
```

## 📁 Project Structure

```
gas_station_recommendation/
├── gas_recommendation_app/          # Main application
│   ├── services/                    # Business logic services
│   │   ├── fuel_calculator.py      # Fuel cost calculations
│   │   ├── gas_filter.py           # Station filtering
│   │   ├── gas_price_service.py    # Price data service
│   │   ├── llm_service.py          # Claude AI integration
│   │   ├── location_service.py     # Geocoding service
│   │   └── map_service.py          # Google Maps integration
│   ├── models/                      # Data models
│   ├── utils/                       # Utility functions
│   ├── static/                      # CSS, JS, images
│   ├── templates/                   # HTML templates
│   ├── web_app.py                   # Flask application
│   └── requirements.txt             # Python dependencies
├── deploy/                          # Deployment configurations
├── dist/                           # Packaged application
└── README.md                       # This file
```

## 🧪 Testing

```bash
cd gas_recommendation_app
python test_app.py
```

## 🔧 Configuration

### API Keys Setup

1. **Google Maps API**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Maps JavaScript API, Places API, and Geocoding API
   - Create API key

2. **Claude API**:
   - Go to [Anthropic Console](https://console.anthropic.com/)
   - Create API key

## 📊 API Endpoints

- `GET /` - Main web interface
- `GET /api/config` - Configuration info
- `POST /api/search-stations` - Search for gas stations
- `GET /api/current-location` - Get current location
- `GET /health` - Health check

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Maps API for location and gas station data
- Claude AI for intelligent recommendations
- Bootstrap for responsive UI components
- Flask for the web framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/gas-station-recommendation/issues)
- **Email**: ge.zhang.phys@gmail.com
- **Documentation**: [Wiki](https://github.com/yourusername/gas-station-recommendation/wiki)

## 🚀 Roadmap

- [ ] Mobile app (React Native)
- [ ] Price alerts
- [ ] Route optimization
- [ ] User accounts and favorites
- [ ] Historical price tracking
- [ ] Integration with more fuel providers

---

⭐ **Star this repository if you find it helpful!** 