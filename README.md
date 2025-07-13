# Gas Station Recommendation App

An AI-powered gas station recommendation app that helps you find the best gas stations based on cost, distance, and travel time. Get intelligent recommendations from Claude AI to save money on gas!

## 🚀 Features

- 🗺️ **Interactive Map**: View gas stations on Google Maps with real-time prices
- 🤖 **AI Analysis**: Get intelligent recommendations from Claude AI
- 💰 **Cost Analysis**: Calculate total costs including travel expenses
- 📍 **Location Services**: Use current location or enter any address
- 🔒 **Secure**: API keys are encrypted and stored safely
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- ⚡ **Real-time Data**: Get current gas prices from Google Maps

## 📋 Prerequisites

Before you start, you'll need:
- Python 3.8 or higher
- Google Maps API Key
- Claude AI API Key (optional but recommended for AI features)

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
  - Typical values: 12-20 gallons
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
- **Search Radius**: How far to look for gas stations (1-50 miles)
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
- Make sure you have valid API keys from Google and Claude

#### "No gas stations found"
- **Increase search radius** (try 10-15 miles)
- **Check your location** - make sure it's correct
- **Try a different address** if using current location

#### "Map not loading"
- **Check Google Maps API key** is valid and has correct permissions
- **Enable billing** in Google Cloud Console
- **Check internet connection**

#### "AI analysis not working"
- **Check Claude API key** is valid
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

- **API keys are encrypted** using Fernet encryption
- **No personal data** is stored or transmitted
- **Location data** is only used for gas station search
- **All API calls** are made directly from your browser

## 📱 Mobile Usage

The app works great on mobile devices:
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

This project is for educational and personal use. Please respect the terms of service for Google Maps and Claude AI APIs.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Happy gas hunting! ⛽💰** 