# Gas Station Recommendation Web Agent

[![Build Status](https://github.com/geoz-lab/gas-station-recommendation/workflows/Deploy%20Gas%20Station%20Recommendation%20App/badge.svg)](https://github.com/geoz-lab/gas-station-recommendation/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Status: Active](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/geoz-lab/gas-station-recommendation)

An AI-powered gas station recommendation web app that helps you find the best gas stations based on cost, distance, travel time, and user review. Get intelligent recommendations from AI agent to save money on gas!

![How to Use](./how_to_use.gif)

## 📋 Table of Contents
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#️-installation--setup)
- [How to Use](#-how-to-use-the-app)
- [Understanding Results](#-understanding-your-results)
- [Pro Tips](#-pro-tips)
- [Troubleshooting](#-troubleshooting)
- [Security & Privacy](#-security--privacy)
- [Mobile Usage](#-mobile-usage)
- [Getting Help](#-getting-help)
- [Project Structure](#️-project-structure)
- [License](#-license)
- [Contributing](#-contributing)

## 🚀 Features

- 🗺️ **Interactive Map**: View gas stations on Google Maps with (real-time) prices
- 🤖 **AI Analysis**: Get intelligent recommendations from AI agent (Claude and ChatGPT)
- 💰 **Cost Analysis**: Calculate total costs including travel expenses
- 📍 **Location Services**: Use current location or enter any address
- 🔒 **Secure**: API keys (input in the .env)
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile with a web broswer
- ⚡ **Real-time Data**: Get current gas prices from Google Maps (if the price accurate)

## 📋 Prerequisites

Before you start, you'll need:
- Python 3.8 or higher
- Google Maps API Key
- Claude.ai (OpenAI) API Key (recommended for AI features)

## 🛠️ Installation & Setup

### Step 1: Clone and Install
```bash
# Clone the repository
git clone https://github.com/geoz-lab/gas-station-recommendation.git
cd gas_station-recommendation

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get API Keys

**For current test version the API key is not provided**

#### Google Maps API Key (Required)

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project or select existing one
3. Enable these APIs:
   - **Places API** (for gas station search)
   - **Maps JavaScript API** (for interactive map)
   - **Geocoding API** (for address conversion)
4. Create credentials → API Key
5. **Important**: Restrict the key to only these APIs for security

#### Claude AI API Key (Recommended)
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Create a new API key
4. Copy the key (starts with `sk-ant-`)

### Step 3: Configure API Keys
```bash
python setup.py
```
This will securely encrypt and store your API keys.

### Step 4: Run the App
```bash
python web_app.py
```
The app will be available at: **http://localhost:8080**

## 🎯 How to Use the App

### 1. **Car Setup** (First Time)
When you first open the app, you'll see the Car Setup section:

- **MPG (Miles per Gallon)**: Enter your car's fuel efficiency
  - Typical values: 20-35 MPG
  - Find this in your car's manual or online
- **Fuel Tank Size**: Enter your tank capacity in gallons
  - Typical values: 11-20 gallons
- **Fuel Grade**: Select your preferred fuel type
  - Regular (87): Most common, cheapest
  - Mid-Grade (89): Better performance
  - Premium (91): Best performance, most expensive

### 2. **Fuel Needs**
Choose how much fuel you want to buy:

- **Specific Gallons**: Enter exact amount (e.g., 10 gallons)
- **Percentage of Tank**: Enter percentage (e.g., 50% = half tank)

### 3. **Location**
Select your starting point:

- **Use Current Location**: Automatically detects your location
- **Enter Address**: Type any address (e.g., "123 Main St, San Francisco, CA")

### 4. **Search Settings**
- **Search Radius**: How far to look for gas stations (1-20 miles)
  - Start with 5-10 miles for best results

### 5. **Find Gas Stations**
Click **"Find Gas Stations"** and wait for results!

## 📊 Understanding Your Results

### **Gas Station List**
Each station shows:
- **Station Name & Brand** (Shell, Chevron, etc.)
- **Distance** from your location
- **Travel Time** to get there
- **Price per Gallon** for your selected fuel grade
- **Total Cost** including:
  - Fuel cost
  - Travel cost (gas used to get there and back)
  - **Effective cost per gallon** (total cost ÷ fuel needed)

### **AI Recommendations**
The AI analyzes each station and provides:
- **Top 5 Recommended Stations** with badges
- **Detailed Analysis** explaining why each station is recommended
- **Cost vs. Convenience** trade-offs
- **Brand reliability** considerations

### **Interactive Map**
- **Blue Marker**: Your location
- **Green Markers**: Gas stations with prices
- **Red Markers**: AI-recommended stations
- **Click any marker** for detailed information

## 💡 Pro Tips

### **Save Money**
- Look for stations with **lower effective cost per gallon**
- Consider **travel distance** - a cheaper station far away might cost more overall
- Check **AI recommendations** for the best value

### **Best Times to Use**
- **Before long trips**: Plan your fuel stops
- **When gas prices are high**: Find the best deals
- **In unfamiliar areas**: Discover nearby stations

### **Understanding Costs**
- **Fuel Cost**: Just the gas you buy
- **Travel Cost**: Gas used driving to/from the station
- **Total Cost**: What you actually pay
- **Effective Cost/Gallon**: True cost including travel

## 🔧 Troubleshooting

### **Common Issues**

#### "API key not configured"
- Run `python setup.py` to configure your keys
- Make sure you have valid API keys from Google, Claude, and/or OpenAI

#### "No gas stations found"
- **Increase search radius** (try 10-15 miles)
- **Check your location** - make sure it's correct
- **Try a different address** if using current location

#### "Map not loading"
- **Check Google Maps API key** is valid and has correct permissions
- **Enable billing** in Google Cloud Console
- **Check internet connection**

#### "AI analysis not working"
- **Check API key** is valid
- **Verify internet connection**
- **Try refreshing the page**

#### "Prices seem wrong"
- **Gas prices are from Google Maps** (may be 24+ hours old)
- **Prices vary by location** and time
- **Check the price source** in the station details

### **Performance Tips**
- **Use current location** for faster results
- **Start with smaller search radius** (5-10 miles)
- **Close other browser tabs** for better performance

## 🔒 Security & Privacy

- **API keys are encrypted**
- **No personal data** is stored or transmitted
- **Location data** is only used for gas station search
- **All API calls** are made directly from browser

## 📱 Mobile Usage

The app will work great on mobile devices:
- **Responsive design** adapts to screen size
- **Touch-friendly** interface
- **GPS location** works on mobile browsers
- **Fast loading** on mobile networks

## 🆘 Getting Help

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Verify your API keys** are correct
3. **Try refreshing the page**
4. **Check your internet connection**
5. **Restart the app** if needed

## 🏗️ Project Structure

```
gas_station_recommendation/
├── web_app.py              # Main Flask application
├── setup.py                # Secure API key setup
├── secure_config.py        # Encrypted API key management
├── config.py               # Application configuration
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── services/               # Core services
│   ├── gas_price_service.py    # Google Maps price extraction
│   ├── location_service.py     # Geocoding and location
│   ├── map_service.py          # Google Maps integration
│   ├── gas_filter.py           # Station filtering logic
│   └── llm_service.py          # Claude AI integration
├── models/                 # Data models
├── static/                 # CSS, JS, images
├── templates/              # HTML templates
└── utils/                  # Utility functions
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note**: While this project is open source, please respect the terms of service for the external APIs used (Google Maps, Claude AI, OpenAI).

## 🤝 Contributing and Future Work

We welcome contributions! Here's how you can help:

### 🐛 **Reporting Bugs**
- Use the [Issues](https://github.com/geoz-lab/gas-station-recommendation/issues) page
- Include steps to reproduce the bug
- Describe your environment (OS, Python version, etc.)

### 💡 **Feature Requests**
- Submit feature requests via Issues
- Explain the use case and benefits
- Consider if it fits the project's scope

### 🔧 **Code Contributions**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-features`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing features'`)
6. Push to the branch (`git push origin feature/amazing-features`)
7. Open a Pull Request

### 📝 **Code Style**
- Follow PEP 8 for Python code
- Add comments for complex logic
- Update documentation as needed
- Test your changes before submitting

## 🤔 **Future Directions**

- Integrate live gas prices (GasBuddy, AAA, Google Maps, etc.)
* Add route-based gas station search (gas along a trip and avoid tolls)
* Improve travel time estimates using real-time traffic
* Cache API results to reduce costs and improve speed
* Maybe voice input for hands-free use
* Add backup/fallback APIs for price and location data
* A better UI interface (I am not familiar with frontend)

**Thank you for contributing!** 🚀

---

**Happy gas hunting! ⛽💰** 