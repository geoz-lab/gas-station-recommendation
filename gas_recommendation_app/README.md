# Gas Station Recommendation App

An AI-powered gas station recommendation app that helps you find the best gas stations based on cost, distance, and travel time.

## Features

- 🗺️ **Interactive Map**: View gas stations on Google Maps
- 🤖 **AI Analysis**: Get intelligent recommendations from Claude AI
- 💰 **Cost Analysis**: Calculate total costs including travel expenses
- 📍 **Location Services**: Use current location or enter any address
- 🔒 **Secure**: API keys are encrypted and stored safely

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup API Keys
```bash
python setup.py
```

This will securely configure your API keys:
- **Google Maps API Key**: For gas station locations and mapping
- **Claude AI API Key**: For intelligent recommendations

### 3. Run the App
```bash
python web_app.py
```

The app will be available at: http://localhost:8080

## API Keys Required

### Google Maps API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Places API
   - Maps JavaScript API
   - Geocoding API
4. Create credentials (API Key)
5. Restrict the key to the APIs you enabled

### Claude AI API Key
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Create a new API key
4. Copy the key (starts with `sk-ant-`)

## Security

- API keys are encrypted using Fernet encryption
- Keys are stored in `.secure_config` (encrypted) and `.key` files
- Files have restrictive permissions (600)
- Never commit these files to version control

## Project Structure

```
gas_recommendation_app/
├── web_app.py              # Main Flask application
├── setup.py                # API key setup script
├── secure_config.py        # Secure API key management
├── config.py               # Application configuration
├── requirements.txt        # Python dependencies
├── services/               # Core services
│   ├── gas_price_service.py
│   ├── location_service.py
│   ├── map_service.py
│   ├── gas_filter.py
│   └── llm_service.py
├── models/                 # Data models
├── static/                 # CSS, JS, images
└── templates/              # HTML templates
```

## Usage

1. Enter your car details (MPG, tank size)
2. Specify how much fuel you need
3. Choose your location (current or address)
4. Select search radius
5. Get AI-powered recommendations!

The app will show you:
- List of nearby gas stations with prices
- Interactive map with station locations
- AI analysis of the best options
- Cost breakdown including travel expenses

## Troubleshooting

- **"API key not configured"**: Run `python setup.py` to configure your keys
- **"No gas stations found"**: Try increasing the search radius
- **Map not loading**: Check your Google Maps API key and billing setup

## License

This project is for educational and personal use. 